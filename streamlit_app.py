import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

st.title("Gerador de Proposta Comercial")

# ----------------------------
# Dados básicos da proposta
# ----------------------------
st.sidebar.header("Detalhes da Proposta")
cliente = st.sidebar.text_input("Nome do Cliente", "Cliente Exemplo")
data_proposta = st.sidebar.date_input("Data da Proposta", datetime.today())
prazo_pagamento = st.sidebar.text_input("Prazo de Pagamento", "30 dias")
prazo_entrega = st.sidebar.text_input("Prazo de Entrega", "15 dias")
validade_proposta = st.sidebar.text_input("Validade da Proposta", "30 dias")

# ----------------------------
# Apenas 1 produto
# ----------------------------
st.header("Produto da Proposta")

nome_produto = st.text_input("Nome do Produto", "Produto A")
qtd = st.number_input("Quantidade", min_value=1, value=1)
preco = st.number_input("Preço Unitário (R$)", min_value=0.0, value=100.0)
obs = st.text_area("Observações", "")

total = qtd * preco

df_final = pd.DataFrame([{
    "Produto": nome_produto,
    "Quantidade": qtd,
    "Preço Unitário (R$)": preco,
    "Observações": obs,
    "Total (R$)": total
}])

st.subheader("Resumo da Proposta")
st.dataframe(df_final)
st.markdown(f"**Total Geral: R$ {total:.2f}**")

# ----------------------------
# Data em PT-BR
# ----------------------------
meses_pt = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}
dia = data_proposta.day
mes = meses_pt[data_proposta.month]
ano = data_proposta.year
data_formatada = f"{dia} de {mes} de {ano}"

# ----------------------------
# Função para gerar PDF
# ----------------------------
def gerar_pdf(caminho_logo="logo.png"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=22, leading=26, spaceAfter=20, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="SectionTitle", alignment=TA_CENTER, fontSize=14, leading=18, spaceAfter=10, fontName="Helvetica-BoldOblique"))
    estilos.add(ParagraphStyle(name="ACStyle", fontSize=14, leading=20, spaceAfter=15, fontName="Helvetica"))
    estilos.add(ParagraphStyle(name="CellStyle", fontSize=10, leading=12))

    # Logo
    try:
        logo = Image(caminho_logo)
        logo.drawHeight = 71
        logo.drawWidth = 174
        logo.hAlign = 'CENTER'
        elementos.append(logo)
        elementos.append(Spacer(1, 15))
    except:
        elementos.append(Spacer(1, 75))

    # Título
    elementos.append(Paragraph("Proposta Comercial", estilos["CenterTitle"]))
    elementos.append(Spacer(1, 10))

    # A/C
    elementos.append(Paragraph(f"A/C {cliente}", estilos["ACStyle"]))
    elementos.append(Spacer(1, 10))

    # Dados fixos
    elementos.append(Paragraph("Dados da Empresa", estilos["SectionTitle"]))
    dados_empresa = [
        "Nome da Empresa: GUSTAVO LUIZ FREITAS DE SOUSA",
        "CNPJ: 41.640.044/0001-63",
        "IE: 33.822.412.281",
        "IM: 1.304.930-0",
        "Endereço: Rua Henrique Fleiuss, 444 - Tijuca",
        "Cidade/UF: Rio de Janeiro / RJ",
        "CEP: 20521-260"
    ]
    for linha in dados_empresa:
        elementos.append(Paragraph(linha, estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("Dados para Contato", estilos["SectionTitle"]))
    contato = ["E-mail: gustavo_lfs@hotmail.com", "Telefone: (21) 996913090"]
    for linha in contato:
        elementos.append(Paragraph(linha, estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("Dados Bancários", estilos["SectionTitle"]))
    bancarios = ["Banco: Inter", "Agência: 0001", "Conta: 12174848-0", "PIX: 41.640.044/0001-63"]
    for linha in bancarios:
        elementos.append(Paragraph(linha, estilos["Normal"]))
    elementos.append(Spacer(1, 15))

    # Itens
    elementos.append(Paragraph("Itens da Proposta", estilos["SectionTitle"]))
    elementos.append(Spacer(1, 10))

    if not df_final.empty:
        dados_tabela = [list(df_final.columns)]
        for row in df_final.values.tolist():
            nova_linha = [Paragraph(str(item), estilos["CellStyle"]) for item in row]
            dados_tabela.append(nova_linha)

        col_widths = [150, 70, 100, 150, 80]
        tabela = Table(dados_tabela, colWidths=col_widths, repeatRows=1)
        estilo = TableStyle([
            ("BOX", (0,0), (-1,-1), 1, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.5, colors.black),
            ("ALIGN", (1,1), (-1,-1), "CENTER"),
            ("ALIGN", (-2,1), (-1,-1), "RIGHT"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ])
        tabela.setStyle(estilo)
        elementos.append(tabela)
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"Total Geral: R$ {total:.2f}", estilos["Normal"]))
        elementos.append(Spacer(1, 20))

    # Condições
    elementos.append(Paragraph("Condições Comerciais", estilos["SectionTitle"]))
    elementos.append(Paragraph(f"Validade da Proposta: {validade_proposta}", estilos["Normal"]))
    elementos.append(Paragraph(f"Prazo de Pagamento: {prazo_pagamento}", estilos["Normal"]))
    elementos.append(Paragraph(f"Prazo de Entrega: {prazo_entrega}", estilos["Normal"]))
    elementos.append(Paragraph("Impostos: Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.", estilos["Normal"]))
    elementos.append(Spacer(1, 40))

    # Data + assinatura
    elementos.append(Paragraph(f"Rio de Janeiro, {data_formatada}.", estilos["Normal"]))
    elementos.append(Spacer(1, 50))
    elementos.append(Paragraph("Gustavo Luiz Freitas de Sousa", estilos["Normal"]))
    elementos.append(Paragraph("CPF: 148.288.697-94", estilos["Normal"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer

# ----------------------------
# Botão para download do PDF
# ----------------------------
pdf_buffer = gerar_pdf("logo.png")
st.download_button(
    label="📥 Baixar Proposta em PDF",
    data=pdf_buffer,
    file_name=f"proposta_{cliente}.pdf",
    mime="application/pdf"
)
