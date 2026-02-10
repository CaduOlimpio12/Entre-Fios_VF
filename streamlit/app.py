import sys
import os
import uuid
import streamlit as st
import requests

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.fornecedores import FORNECEDORES
from core.produtos import PRODUTOS
from core.pagamentos import TAXAS_PAGAMENTO
from core.estampas import ESTAMPAS
from pdf_utils import gerar_pdf_orcamento

st.set_page_config(page_title="Entre-Fios: Orçamentos", layout="wide")

logo_path = os.path.join(root_path, "Logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=220)

if "lista_itens" not in st.session_state:
    st.session_state.lista_itens = []
if "resultado_consolidado" not in st.session_state:
    st.session_state.resultado_consolidado = None


def _normalizar_item(item):
    """Garante um identificador estável para cada item da lista."""
    if "id" not in item:
        item["id"] = str(uuid.uuid4())
    return item

st.title("📦 Entre-Fios: Sistema de Orçamentos")

with st.expander("➕ Adicionar Produto ao Orçamento", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        f_sel = st.selectbox("Fornecedor", list(FORNECEDORES.keys()))
        p_sel = st.selectbox("Produto", list(FORNECEDORES[f_sel].keys()))
        q_sel = st.number_input("Quantidade", min_value=1, value=1, step=1)
    with col2:
        ef_sel = st.selectbox("Estampa Frente", list(ESTAMPAS.keys()))
        ec_sel = st.selectbox("Estampa Costas", list(ESTAMPAS.keys()))
        dados_p = PRODUTOS.get(p_sel, {})
        tam_sel = st.selectbox("Tamanho", dados_p.get("tamanhos", ["P"]))
    with col3:
        st.info(f"📝 **Descrição:** {dados_p.get('descricao', 'Sem descrição.')}")
        if st.button("➕ Adicionar à Lista", type="primary"):
            st.session_state.lista_itens.append(_normalizar_item({
                "fornecedor": f_sel, "produto": p_sel, "quantidade": q_sel,
                "tamanho": tam_sel, "estampa_frente": ef_sel, "estampa_costas": ec_sel
            }))
            st.rerun()

if st.session_state.lista_itens:
    st.session_state.lista_itens = [_normalizar_item(item) for item in st.session_state.lista_itens]
    st.subheader("📂 Itens do Orçamento")
    for item in st.session_state.lista_itens:
        with st.container(border=True):
            c1, c2, c3 = st.columns([6, 3, 1])
            c1.write(f"**{item['produto']}** ({item['fornecedor']}) - Qtd: {item['quantidade']}")
            c2.write(f"Tam: {item['tamanho']} | Estampas: {item['estampa_frente']}/{item['estampa_costas']}")
            if c3.button("🗑️", key=f"del_{item['id']}"):
                st.session_state.lista_itens = [i for i in st.session_state.lista_itens if i["id"] != item["id"]]
                st.rerun()

    st.divider()
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        reg_sel = st.selectbox("Região", ["São Paulo (Capital/Interior)", "Sudeste (RJ/MG/ES)", "Sul / Centro-Oeste", "Norte / Nordeste"])
    with col_cfg2:
        pag_sel = st.selectbox("Pagamento", list(TAXAS_PAGAMENTO.keys()))
        parc_sel = st.select_slider("Parcelas", options=list(TAXAS_PAGAMENTO[pag_sel].keys())) if pag_sel == "Crédito Parcelado" else 1

    if st.button("🧮 Calcular Orçamento Completo", type="primary"):
        itens_payload = [{k: v for k, v in item.items() if k != "id"} for item in st.session_state.lista_itens]
        payload = {"itens": itens_payload, "regiao": reg_sel, "forma_pagamento": pag_sel, "parcelas": parc_sel}
        resp = requests.post("http://127.0.0.1:8000/orcamento", json=payload )
        if resp.status_code == 200:
            st.session_state.resultado_consolidado = resp.json()
            st.success("Calculado!")

if st.session_state.resultado_consolidado:
    res = st.session_state.resultado_consolidado
    tab_cli, tab_adm = st.tabs(["📄 Cliente", "🔐 Administrativo"])
    with tab_cli:
        cols = st.columns(len(res["opcoes"]))
        for idx, opt in enumerate(res["opcoes"]):
            with cols[idx]:
                with st.container(border=True):
                    st.metric(opt["transportadora"], f"R$ {opt['venda_total']:,.2f}".replace('.', ','))
                    pdf = gerar_pdf_orcamento(res, "cliente", idx)
                    st.download_button(f"📥 PDF {opt['transportadora']}", pdf, f"orcamento_{opt['transportadora']}.pdf", mime="application/pdf")
    with tab_adm:
        st.write(f"**Volumes:** {res['volumes']} pacotes (32x40)")
        st.table(res["opcoes"])
        pdf_adm = gerar_pdf_orcamento(res, "interno", 0)
        st.download_button("📥 Baixar Relatório Administrativo", pdf_adm, "relatorio_adm.pdf", mime="application/pdf")