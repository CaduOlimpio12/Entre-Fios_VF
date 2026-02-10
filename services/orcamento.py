import math
from core.fornecedores import FORNECEDORES, get_preco_usmark
from core.produtos import PRODUTOS
from core.pagamentos import TAXAS_PAGAMENTO
from core.estampas import ESTAMPAS
from core.logistica import PESOS_PRODUTOS, CAPACIDADE_PACOTE, PACOTE_PADRAO
from core.frete import calcular_frete_consolidado

def calcular_logistica_orcamento(itens):
    peso_total_produtos = 0
    volumes_totais = 0
    quantidades_por_grupo = {}
    for item in itens:
        produto_nome = item["produto"]
        quantidade = item["quantidade"]
        grupo = PRODUTOS.get(produto_nome, {}).get("grupo", "MEDIA")
        peso_unitario = PESOS_PRODUTOS.get(grupo, 0.18)
        peso_total_produtos += (peso_unitario * quantidade)
        quantidades_por_grupo[grupo] = quantidades_por_grupo.get(grupo, 0) + quantidade
    for grupo, qtd in quantidades_por_grupo.items():
        cap = CAPACIDADE_PACOTE.get(grupo, 15)
        volumes_totais += math.ceil(qtd / cap)
    peso_final = round(peso_total_produtos + (volumes_totais * PACOTE_PADRAO["peso_embalagem"]), 2)
    return peso_final, volumes_totais

def gerar_orcamento_consolidado(itens, regiao, forma_pagamento, parcelas=1):
    subtotal_venda_produtos = 0
    custo_total_produtos = 0
    detalhes_itens = []
    for item in itens:
        fornecedor = item["fornecedor"]
        produto = item["produto"]
        quantidade = item["quantidade"]
        estampa_frente = item.get("estampa_frente", "Nenhuma")
        estampa_costas = item.get("estampa_costas", "Nenhuma")
        if fornecedor not in FORNECEDORES or produto not in FORNECEDORES[fornecedor]:
            continue
        if fornecedor == "USMARK":
            preco_venda_unit_base, custo_unit_base, curva = get_preco_usmark(produto, quantidade)
        else:
            dados_p = FORNECEDORES[fornecedor][produto]
            preco_venda_unit_base = dados_p["valor"]
            custo_unit_base = dados_p["base"]
            curva = dados_p["curva"]
        valor_frente = ESTAMPAS.get(estampa_frente, 0.0)
        valor_costas = ESTAMPAS.get(estampa_costas, 0.0)
        total_estampas = valor_frente + valor_costas
        custo_unit = custo_unit_base + curva + total_estampas
        preco_venda_unit = preco_venda_unit_base + curva + total_estampas
        subtotal_item = preco_venda_unit * quantidade
        custo_item = custo_unit * quantidade
        subtotal_venda_produtos += subtotal_item
        custo_total_produtos += custo_item
        detalhes_itens.append({
            "produto": produto,
            "descricao": PRODUTOS.get(produto, {}).get("descricao", "-"),
            "tamanho": item.get("tamanho", "-"),
            "fornecedor": fornecedor,
            "quantidade": quantidade,
            "preco_unitario": preco_venda_unit,
            "subtotal": subtotal_item,
            "custo_unitario": custo_unit,
        })
    peso_total, volumes = calcular_logistica_orcamento(itens)
    opcoes_frete = calcular_frete_consolidado(peso_total, volumes, regiao)
    taxa = TAXAS_PAGAMENTO.get(forma_pagamento, {}).get(parcelas, 0.0)
    resultados_finais = []
    for trans, valor_frete in opcoes_frete.items():
        custo_final = custo_total_produtos + valor_frete
        subtotal_com_frete = subtotal_venda_produtos + valor_frete
        venda_final = round(subtotal_com_frete * (1 + (taxa / 100)), 2)
        valor_taxa = round(venda_final - subtotal_com_frete, 2)
        lucro = round(venda_final - custo_final, 2)
        margem = round((lucro / venda_final) * 100, 2) if venda_final > 0 else 0
        resultados_finais.append({
            "transportadora": trans, "valor_frete": valor_frete, "subtotal_produtos": round(subtotal_venda_produtos, 2),
            "valor_taxa": valor_taxa, "venda_total": venda_final, "custo_total": round(custo_final, 2),
            "lucro_total": lucro, "margem": margem
        })
    return {
        "itens": detalhes_itens, "peso_total": peso_total, "volumes": volumes,
        "regiao": regiao, "pagamento": f"{forma_pagamento} ({parcelas}x)",
        "taxa_percentual": taxa, "opcoes": resultados_finais
    }
