import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def gerar_pdf(caminho_logo="/mnt/data/LogoSample_ByTailorBrands.jpg"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=30
    )

    elementos = []
    estilos = getSampleStyleSheet()

    # Estilos
    estilos.add(ParagraphStyle(name="Titulo", fontSize=16, alignment=1, spaceAfter=20, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="SectionTitle", fontSize=12, alignment=0, spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold", italic=True))
    estilos.add(ParagraphStyle(name="NormalText", fontSize=10, alignment=0, spaceAfter=6))

    # Logo
    if caminho_logo:
        logo = Image(caminho_logo, width=100, height=100)
        logo.hAlign = "CENTER"
        elementos.append(logo)
        elementos.append(Spacer(1, 12))

    # Título
    elementos.append(Paragraph("Proposta Comercial", estilos["Titulo"]))
    elementos.append(Spacer(1, 20))

    # Dados do cliente
    elementos.append(Paragraph("A/C", estilos["SectionTitle"]))
    elementos.append(Paragraph("Nome do Cliente", estilos["NormalText"]))
    elementos.append(Paragraph("Empresa Exemplo LTDA", estilos["NormalText"]))
    elementos.append(Paragraph("email@cliente.com", estilos["NormalText"]))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Dados do Cliente", estilos["SectionTitle"]))
    elementos.append(Paragraph("CNPJ: 12.345.678/0001-90", estilos["NormalText"]))
    elementos.append(Paragraph("Endereço: Rua Exemplo, 123 - São Paulo/SP", estilos["NormalText"]))
    elementos.append(Spacer(1, 12))

    # Dados bancários
    elementos.append(Paragraph("Dados Bancários", estilos["SectionTitle"]))
    elementos.append(Paragraph("Banco: Nubank", estilos["NormalText"]))
    elementos.append(Paragraph("Agência: 0001", estilos["NormalText"]))
    elementos.append(Paragraph("Conta: 123456-7", estilos["NormalText"]))
    elementos.append(Paragraph("PIX: exemplo@pix.com", estilos["NormalText"]))
    elementos.append(Spacer(1, 12))

    # Itens da proposta
    elementos.append(Paragraph("Itens da Proposta", estilos["SectionTitle"]))
    data = [
        ["Produto", "Quantidade", "Valor Unitário (R$)", "Total (R$)"],
        ["Produto A", "10", "50,00", "500,00"],
        ["Produto B", "5", "100,00", "500,00"],
        ["Produto C", "2", "250,00", "500,00"],
    ]

    tabela = Table(data, colWidths=[200, 80, 100, 100])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ROUNDEDCORNERS", [10]),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 20))

    # Totais
    elementos.append(Paragraph("Subtotal: R$ 1.500,00", estilos["NormalText"]))
    elementos.append(Paragraph("Impostos: R$ 150,00", estilos["NormalText"]))
    elementos.append(Paragraph("Total: R$ 1.650,00", estilos["NormalText"]))
    elementos.append(Spacer(1, 20))

    # Condições comerciais
    elementos.append(Paragraph("Condições Comerciais", estilos["SectionTitle"]))
    elementos.append(Paragraph("Prazo de entrega: 15 dias úteis", estilos["NormalText"]))
    elementos.append(Paragraph("Validade da proposta: 30 dias", estilos["NormalText"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


# --- STREAMLIT ---
st.title("Gerador de Proposta Comercial")

if st.button("Exportar para PDF"):
    pdf_buffer = gerar_pdf()
    st.download_button(
        label="Baixar Proposta em PDF",
        data=pdf_buffer,
        file_name="proposta_comercial.pdf",
        mime="application/pdf"
    )
