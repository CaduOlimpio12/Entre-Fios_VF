import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _moeda(valor):
    return f"R$ {valor:.2f}"


def _configurar_fundo(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#ECECEC"))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.restoreState()


def gerar_pdf_orcamento(dados_orc, tipo="cliente", opcao_idx=0):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.9 * cm,
        leftMargin=1.9 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        "Titulo",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        alignment=1,
        textColor=colors.black,
        spaceAfter=0.9 * cm,
    )
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        alignment=1,
        textColor=colors.HexColor("#4F4F4F"),
        leading=11,
    )

    opt = dados_orc["opcoes"][opcao_idx]
    itens = dados_orc.get("itens", [])
    item_ref = itens[0] if itens else {}

    produto = item_ref.get("produto", "-")
    descricao = item_ref.get("descricao", "-")
    tamanho = item_ref.get("tamanho", "-")
    quantidade = sum(item.get("quantidade", 0) for item in itens) if itens else 0

    if len({item.get("tamanho") for item in itens if item.get("tamanho")}) > 1:
        tamanho = "Múltiplos"

    elementos = []

    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Logo.png"))
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.0 * cm, height=2.0 * cm)
        logo.hAlign = "CENTER"
        elementos.append(logo)
        elementos.append(Spacer(1, 0.45 * cm))

    titulo_tipo = "CLIENTE" if tipo == "cliente" else "ADMINISTRATIVO"
    elementos.append(Paragraph(f"ORÇAMENTO ENTRE-FIOS ({titulo_tipo})", titulo_style))

    dados_tabela = [
        ["PRODUTO", produto],
        ["DESCRIÇÃO", descricao],
        ["TAMANHO", tamanho],
        ["QUANTIDADE", f"{quantidade} unidades"],
        ["VALOR UNITÁRIO CAMISA", _moeda(item_ref.get("preco_unitario", 0.0))],
        ["SUBTOTAL CAMISAS", _moeda(opt.get("subtotal_produtos", 0.0))],
        ["FORMA DE PAGAMENTO", dados_orc.get("pagamento", "-")],
        ["TAXA DE PAGAMENTO", f"{dados_orc.get('taxa_percentual', 0.0)}%"],
        ["TRANSPORTADORA", opt.get("transportadora", "-")],
        ["VALOR DO FRETE", _moeda(opt.get("valor_frete", 0.0))],
        ["VALOR TOTAL FINAL", _moeda(opt.get("venda_total", 0.0))],
    ]

    if tipo == "interno":
        dados_tabela.extend(
            [
                ["LUCRO", _moeda(opt.get("lucro_total", 0.0))],
                ["MARGEM DE LUCRO", f"{opt.get('margem', 0.0)}%"],
            ]
        )

    tabela = Table(dados_tabela, colWidths=[6.0 * cm, 9.0 * cm])
    estilos_tabela = [
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E3E3E3")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#8F8F8F")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]

    total_linha_idx = 10
    estilos_tabela.extend(
        [
            ("BACKGROUND", (0, total_linha_idx), (-1, total_linha_idx), colors.HexColor("#D0D0D0")),
            ("FONTNAME", (0, total_linha_idx), (-1, total_linha_idx), "Helvetica-Bold"),
        ]
    )

    tabela.setStyle(TableStyle(estilos_tabela))
    elementos.append(tabela)
    elementos.append(Spacer(1, 1.0 * cm))

    elementos.append(Paragraph("Entre-Fios Estamparia - Qualidade em cada detalhe.", footer_style))
    elementos.append(
        Paragraph(
            "■ WhatsApp: (11) 91592-2431 | ■ CNPJ: 53.497.169/0001-65",
            footer_style,
        )
    )

    doc.build(elementos, onFirstPage=_configurar_fundo, onLaterPages=_configurar_fundo)
    return buffer.getvalue()
