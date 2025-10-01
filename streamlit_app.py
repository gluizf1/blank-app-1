import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ---------------------------
# Função para gerar o PDF
# ---------------------------
def gerar_pdf(dados_cliente, produtos, dados_bancarios, pix, caminho_logo="/mnt/data/LogoSample_ByTailorBrands.jpg"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)

    elementos = []
    estilos = getSampleStyleSheet()

    # Estilos
    estilos.add(ParagraphStyle(name="Titulo", fontSize=16, alignment=1, spaceAfter=20, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="SectionTitle", fontSize=12, alignment=0, spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold", italic=True))
    estilos.add(ParagraphStyle(name="Normal", fontSize=10, alignment=0))

    # Logo
    if caminho_logo:
        logo = Image(caminho_logo, width=120, height=120)
        logo.hAlign = "CENTER"
        elementos.append(logo)
        elementos.append(Spacer(1, 20))

    # Título principal
    elementos.append(Paragraph("Proposta Comercial", estilos["Titulo"]))
    elementos.append(Spacer(1, 20))

    # Dados do Cliente
    elementos.append(Paragraph("A/C", estilos["SectionTitle"]))
    elementos.append(Paragraph(dados_cliente, estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    # Dados de Contato
    elementos.append(Paragraph("Dados de Contato", estilos["SectionTitle"]))
    elementos.append(Paragraph("Telefone: (11) 99999-9999<br/>Email: contato@empresa.com", estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    # Dados Bancários
    elementos.append(Paragraph("Dados Bancários", estilos["SectionTitle"]))
    elementos.append(Paragraph(dados_bancarios, estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    # PIX
    elementos.append(Paragraph("Chave PIX", estilos["SectionTitle"]))
    elementos.append(Paragraph(pix, estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    # Itens da Proposta
    elementos.append(Paragraph("Itens da Proposta", estilos["SectionTitle"]))
    elementos.append(Spacer(1, 12))

    # Montar tabela de produtos
    data = [["Descrição", "Qtd.", "Valor Unit.", "Total"]]
    for p in produtos:
        data.append([
            p["descricao"],
            str(p["quantidade"]),
            f"R$ {p['valor_unit']:.2f}",
            f"R$ {p['quantidade'] * p['valor_unit']:.2f}"
        ])

    # Criar tabela
    tabela = Table(data, colWidths=[220, 60, 100, 100])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # fundo cinza só no cabeçalho
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.black),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabela)

    # Total geral
    total = sum([p["quantidade"] * p["valor_unit"] for p in produtos])
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"<b>Total: R$ {total:.2f}</b>", estilos["Normal"]))

    # Observações
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("Observações", estilos["SectionTitle"]))
    elementos.append(Paragraph("Validade da proposta: 7 dias.", estilos["Normal"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


# ---------------------------
# App Streamlit
# ---------------------------
st.title("Gerador de Propostas Comerciais")

# Dados do cliente
dados_cliente = st.text_area("Dados do Cliente", "Empresa XYZ\nCNPJ: 00.000.000/0000-00")

# Produtos
st.subheader("Produtos")
produtos = []
num_produtos = st.number_input("Quantidade de itens", 1, 20, 3)

for i in range(num_produtos):
    with st.expander(f"Item {i+1}"):
        descricao = st.text_input(f"Descrição {i+1}", f"Produto {i+1}")
        quantidade = st.number_input(f"Quantidade {i+1}", 1, 100, 1)
        valor_unit = st.number_input(f"Valor Unitário {i+1}", 0.0, 10000.0, 100.0)
        produtos.append({"descricao": descricao, "quantidade": quantidade, "valor_unit": valor_unit})

# Dados bancários
dados_bancarios = st.text_area("Dados Bancários", "Banco XYZ\nAgência: 0001\nConta: 12345-6")

# PIX
pix = st.text_input("Chave PIX", "contato@empresa.com")

# Botão para gerar PDF
if st.button("Gerar PDF"):
    pdf_buffer = gerar_pdf(dados_cliente, produtos, dados_bancarios, pix)
    st.download_button("📥 Baixar Proposta em PDF", data=pdf_buffer, file_name="proposta.pdf", mime="application/pdf")
