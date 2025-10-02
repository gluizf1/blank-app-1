import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from babel.numbers import format_currency

# ------------------ Configuração do estilo ------------------
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="SectionTitle", fontSize=12, leading=14, spaceAfter=6, alignment=TA_LEFT, bold=True))
styles.add(ParagraphStyle(name="NormalLeft", fontSize=10, leading=12, alignment=TA_LEFT))

# ------------------ Função para gerar PDF ------------------
def gerar_proposta_pdf(dados, produtos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    # Logo
    try:
        logo = Image("logo.jpg", width=100, height=50)
        story.append(logo)
    except:
        pass
    story.append(Spacer(1, 12))

    # Dados fixos da empresa
    story.append(Paragraph("<b>Empresa Exemplo LTDA</b>", styles["NormalLeft"]))
    story.append(Paragraph("CNPJ: 12.345.678/0001-99", styles["NormalLeft"]))
    story.append(Paragraph("Endereço: Rua Exemplo, 123 - São Paulo/SP", styles["NormalLeft"]))
    story.append(Paragraph("Telefone: (11) 99999-9999 | Email: contato@empresa.com", styles["NormalLeft"]))
    story.append(Spacer(1, 12))

    # Dados da proposta
    story.append(Paragraph("Dados da Proposta", styles["SectionTitle"]))
    for chave, valor in dados.items():
        story.append(Paragraph(f"<b>{chave}:</b> {valor}", styles["NormalLeft"]))
    story.append(Spacer(1, 12))

    # Tabela de produtos
    story.append(Paragraph("Itens da Proposta", styles["SectionTitle"]))

    data = [["Produto", "Quant.", "Preço Unit. (R$)", "Total (R$)"]]
    for item in produtos:
        total = item["Quant."] * item["Preço Unit."]
        data.append([
            item["Produto"],
            str(item["Quant."]),
            f"{item['Preço Unit.']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        ])

    tabela = Table(data, hAlign="LEFT")
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 12))

    # Impostos
    story.append(Paragraph("Impostos", styles["SectionTitle"]))
    story.append(Paragraph("ICMS: 18%", styles["NormalLeft"]))
    story.append(Paragraph("ISS: 5%", styles["NormalLeft"]))
    story.append(Spacer(1, 6))  # menor espaço que as seções

    # Data, assinatura e nome
    data_atual = datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(f"{data_atual}", styles["NormalLeft"]))
    try:
        assinatura = Image("assinatura.png", width=120, height=50)
        story.append(assinatura)
    except:
        pass
    story.append(Paragraph("Gustavo Luiz Freitas de Sousa", styles["NormalLeft"]))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# ------------------ App Streamlit ------------------
st.title("Gerador de Proposta Comercial")

# Upload do Excel na barra lateral
st.sidebar.header("Carregar Produtos")
uploaded_file = st.sidebar.file_uploader("Faça upload do arquivo Excel", type=["xlsx"])

# Dados fixos
dados = {
    "Cliente": "Fulano de Tal",
    "Validade": "30 dias",
    "Condição de Pagamento": "À vista"
}

# Produtos
produtos = []
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        for _, row in df.iterrows():
            produtos.append({
                "Produto": row["Produto"],
                "Quant.": int(row["Quant."]),
                "Preço Unit.": float(row["Preço Unit."])
            })
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")

# Exibição dos dados fixos na tela
st.subheader("Dados da Proposta")
for chave, valor in dados.items():
    st.write(f"**{chave}:** {valor}")

# Exibição dos produtos carregados
if produtos:
    st.subheader("Itens da Proposta")
    df_display = pd.DataFrame(produtos)
    df_display["Total (R$)"] = df_display["Quant."].astype(float) * df_display["Preço Unit."].astype(float)
    st.dataframe(df_display)

# Botão de download
if st.button("📄 Baixar Proposta em PDF"):
    if produtos:
        pdf = gerar_proposta_pdf(dados, produtos)
        st.download_button(
            label="Clique para baixar",
            data=pdf,
            file_name="proposta.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Adicione produtos antes de gerar a proposta.")
