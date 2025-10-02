import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from babel.numbers import format_currency

# ==============================
# Função para gerar Excel modelo
# ==============================
def gerar_excel_modelo():
    data = {
        "Produto": ["Produto A", "Produto B", "Produto C"],
        "Quant.": [10, 5, 2],
        "Preço Unit.": [25.50, 100.00, 350.75],
        "Observações": ["", "", ""]
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

# ==============================
# Função para gerar o PDF
# ==============================
def gerar_pdf(cliente, produtos_df):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    style_section = ParagraphStyle(name="SectionTitle", fontSize=12, leading=14, spaceAfter=8, alignment=TA_LEFT, bold=True)
    style_normal = styles["Normal"]

    elementos = []

    # Logo no cabeçalho
    elementos.append(Image("logo.jpg", width=120, height=50))
    elementos.append(Spacer(1, 12))

    # Dados fixos da empresa
    elementos.append(Paragraph("<b>Empresa XYZ</b>", style_normal))
    elementos.append(Paragraph("CNPJ: 00.000.000/0001-00", style_normal))
    elementos.append(Paragraph("Endereço: Rua Exemplo, 123 - Cidade/UF", style_normal))
    elementos.append(Paragraph("Telefone: (00) 0000-0000", style_normal))
    elementos.append(Spacer(1, 20))

    # Dados do cliente
    elementos.append(Paragraph(f"<b>Cliente:</b> {cliente}", style_normal))
    elementos.append(Spacer(1, 12))

    # Seção Produtos
    elementos.append(Paragraph("<b>Produtos</b>", style_section))

    # Criar tabela de produtos
    data = [["Produto", "Quant.", "Preço Unit. (R$)", "Total (R$)", "Observações"]]
    total_geral = 0

    for _, row in produtos_df.iterrows():
        total = row["Quant."] * row["Preço Unit."]
        total_geral += total
        data.append([
            row["Produto"],
            str(row["Quant."]),
            f"{row['Preço Unit.']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            row.get("Observações", "")
        ])

    # Linha de total
    data.append(["", "", "Total Geral", f"{total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ""])

    tabela = Table(data, hAlign="LEFT")
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (1, 1), (-2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elementos.append(tabela)

    elementos.append(Spacer(1, 20))

    # Assinatura e data
    elementos.append(Paragraph(f"{datetime.now().strftime('%d/%m/%Y')}", style_normal))
    elementos.append(Image("assinatura.png", width=120, height=50))
    elementos.append(Paragraph("Gustavo Luiz Freitas de Sousa", style_normal))

    doc.build(elementos)
    buffer.seek(0)
    return buffer

# ==============================
# Interface Streamlit
# ==============================
st.title("Gerador de Proposta Comercial")

# Barra lateral com upload e modelo
with st.sidebar:
    st.subheader("Importar Produtos")
    uploaded_file = st.file_uploader("Carregar Excel", type=["xlsx"])
    st.download_button(
        label="Baixar Modelo Excel",
        data=gerar_excel_modelo(),
        file_name="produtos_modelo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Nome do cliente
cliente = st.text_input("Nome do Cliente", "")

# Produtos
if uploaded_file:
    produtos_df = pd.read_excel(uploaded_file)
else:
    st.info("Carregue um arquivo Excel para preencher os produtos.")
    produtos_df = pd.DataFrame(columns=["Produto", "Quant.", "Preço Unit.", "Observações"])

# Mostrar tabela no app
if not produtos_df.empty:
    st.subheader("Produtos Carregados")
    st.dataframe(produtos_df)

# Botão para gerar PDF
if st.button("Baixar Proposta em PDF"):
    if not cliente:
        st.error("Digite o nome do cliente antes de gerar o PDF.")
    elif produtos_df.empty:
        st.error("Carregue os produtos antes de gerar o PDF.")
    else:
        pdf_buffer = gerar_pdf(cliente, produtos_df)
        st.download_button(
            label="Baixar Proposta em PDF",
            data=pdf_buffer,
            file_name=f"proposta_{cliente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
