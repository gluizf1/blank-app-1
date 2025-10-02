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
# Informações do cliente
# ----------------------------
st.sidebar.header("Detalhes da Proposta")
cliente = st.sidebar.text_input("Nome do Cliente", "Cliente Exemplo")
data_proposta = st.sidebar.date_input("Data da Proposta", datetime.today())
prazo_pagamento = st.sidebar.text_input("Prazo de Pagamento", "30 dias")
prazo_entrega = st.sidebar.text_input("Prazo de Entrega", "15 dias")
validade_proposta = st.sidebar.text_input("Validade da Proposta", "30 dias")

# ----------------------------
# A/C e dados fixos da empresa
# ----------------------------
st.markdown(f"**A/C {cliente}**")
st.markdown("### Dados da Empresa")
st.markdown("""
**Nome da Empresa:** GUSTAVO LUIZ FREITAS DE SOUSA  
**CNPJ:** 41.640.044/0001-63  
**IE:** 33.822.412.281  
**IM:** 1.304.930-0  
**Endereço:** Rua Henrique Fleiuss, 444 - Tijuca  
**Cidade/UF:** Rio de Janeiro / RJ  
**CEP:** 20521-260
""")

st.markdown("### Dados para Contato")
st.markdown("""
**E-mail:** gustavo_lfs@hotmail.com  
**Telefone:** (21) 996913090
""")

st.markdown("### Dados Bancários")
st.markdown("""
**Banco:** Inter  
**Agência:** 0001  
**Conta:** 12174848-0  
**PIX:** 41.640.044/0001-63
""")

# ----------------------------
# Inicializa lista de produtos
# ----------------------------
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"Produto": "Produto A", "Quantidade": 1, "Preço Unitário (R$)": 100.0, "Observações": ""}
    ]

def adicionar_produto():
    st.session_state.produtos.append({"Produto": "", "Quantidade": 1, "Preço Unitário (R$)": 0.0, "Observações": ""})

def remover_produto():
    if st.session_state.produtos:
        st.session_state.produtos.pop()

# ----------------------------
# Editar produtos
# ----------------------------
st.header("Itens da Proposta")
produtos_editados = []

for i, item in enumerate(st.session_state.produtos):
    st.subheader(f"Produto {i+1}")
    nome = st.text_input(f"Nome do Produto {i+1}", item["Produto"], key=f"nome_{i}")
    qtd = st.number_input(f"Quantidade {i+1}", min_value=0, value=item["Quantidade"], key=f"qtd_{i}")
    preco = st.number_input(f"Preço Unitário {i+1}", min_value=0.0, value=item["Preço Unitário (R$)"], key=f"preco_{i}")
    obs = st.text_input(f"Observações {i+1}", item["Observações"], key=f"obs_{i}")

    total = qtd * preco
    st.markdown(f"**Total do Item: R$ {total:.2f}**")

    produtos_editados.append({
        "Produto": nome,
        "Quantidade": qtd,
        "Preço Unitário (R$)": preco,
        "Observações": obs,
        "Total (R$)": total
    })

st.session_state.produtos = produtos_editados

# ----------------------------
# Botões de adicionar/remover
# ----------------------------
col1, col2 = st.columns(2)
with col1:
    st.button("➕ Adicionar Produto", on_click=adicionar_produto)
with col2:
    st.button("➖ Remover Produto", on_click=remover_produto)

# ----------------------------
# Resumo da proposta
# ----------------------------
df_final = pd.DataFrame(produtos_editados)
st.subheader("Resumo da Proposta")
st.dataframe(df_final)

total_geral = df_final["Total (R$)"].sum()
st.markdown(f"**Total Geral: R$ {total_geral:.2f}**")

# ----------------------------
# Condições Comerciais
# ----------------------------
st.markdown("---")
st.subheader("Condições Comerciais")
st.markdown(f"- **Validade da Proposta:** {validade_proposta}")
st.markdown(f"- **Prazo de Pagamento:** {prazo_pagamento}")
st.markdown(f"- **Prazo de Entrega:** {prazo_entrega}")
st.markdown("- **Impostos:** Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.")

# ----------------------------
# Data em PT-BR (manual)
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

st.markdown("\n\n\n")
st.markdown(f"**Rio de Janeiro, {data_formatada}.**")
st.markdown("\n\n\n")
st.markdown("**Gustavo Luiz Freitas de Sousa**")
st.markdown("CPF: 148.288.697-94")

# ----------------------------
# Função para gerar PDF com logo centralizado
# ----------------------------
def gerar_pdf_com_logo_central(caminho_logo="logo.jpg"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=22, leading=26, spaceAfter=20, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="SectionTitle", alignment=TA_CENTER, fontSize=14, leading=18, spaceAfter=10, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="ACStyle", fontSize=14, leading=20, spaceAfter=15, fontName="Helvetica"))
    estilos.add(ParagraphStyle(name="CellStyle", fontSize=10, leading=12))

    # Logo centralizado
    try:
        logo = Image(caminho_logo)
        logo.drawHeight = 42 
        logo.drawWidth = 104 
        logo.hAlign = 'CENTER'
        elementos.append(logo)
        elementos.append(Spacer(1, 15))
    except:
        elementos.append(Spacer(1, 75))

    # Título principal centralizado
    elementos.append(Paragraph("Proposta Comercial", estilos["CenterTitle"]))
    elementos.append(Spacer(1, 10))

    # A/C normal
    elementos.append(Paragraph(f"A/C {cliente}", estilos["ACStyle"]))
    elementos.append(Spacer(1, 10))

    # Dados da empresa
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

    # Dados de contato
    elementos.append(Paragraph("Dados para Contato", estilos["SectionTitle"]))
    contato = ["E-mail: gustavo_lfs@hotmail.com", "Telefone: (21) 996913090"]
    for linha in contato:
        elementos.append(Paragraph(linha, estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    # Dados bancários
    elementos.append(Paragraph("Dados Bancários", estilos["SectionTitle"]))
    bancarios = ["Banco: Inter", "Agência: 0001", "Conta: 12174848-0", "PIX: 41.640.044/0001-63"]
    for linha in bancarios:
        elementos.append(Paragraph(linha, estilos["Normal"]))
    elementos.append(Spacer(1, 15))

    # Itens da Proposta
    elementos.append(Paragraph("Itens da Proposta", estilos["SectionTitle"]))
    elementos.append(Spacer(1, 10))

    # Tabela de produtos
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
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ])
        tabela.setStyle(estilo)
        elementos.append(tabela)
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"Total Geral: R$ {total_geral:.2f}", estilos["Normal"]))
        elementos.append(Spacer(1, 20))

    # Condições comerciais
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
pdf_buffer = gerar_pdf_com_logo_central(caminho_logo="logo.jpg")
st.download_button(
    label="Baixar Proposta em PDF",
    data=pdf_buffer,
    file_name=f"proposta_{cliente}.pdf",
    mime="application/pdf"
)
