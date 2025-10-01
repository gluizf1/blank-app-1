import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

st.title("📄 Proposta Comercial Interativa")

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
# Inicializa lista de produtos no session_state
# ----------------------------
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"Produto": "Produto A", "Quantidade": 1, "Preço Unitário (R$)": 100.0, "Observações": ""},
        {"Produto": "Produto B", "Quantidade": 2, "Preço Unitário (R$)": 150.0, "Observações": ""}
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

col1, col2 = st.columns(2)
with col1:
    st.button("➕ Adicionar Produto", on_click=adicionar_produto)
with col2:
    st.button("➖ Remover Produto", on_click=remover_produto)

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
# Exportar para PDF
# ----------------------------
def gerar_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    # Cabeçalho
    elements.append(Paragraph(f"A/C: {cliente}", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Dados da Empresa</b>", styles["Heading3"]))
    elements.append(Paragraph("Nome da Empresa: GUSTAVO LUIZ FREITAS DE SOUSA", normal))
    elements.append(Paragraph("CNPJ: 41.640.044/0001-63", normal))
    elements.append(Paragraph("IE: 33.822.412.281", normal))
    elements.append(Paragraph("IM: 1.304.930-0", normal))
    elements.append(Paragraph("Endereço: Rua Henrique Fleiuss, 444 - Tijuca", normal))
    elements.append(Paragraph("Cidade/UF: Rio de Janeiro / RJ", normal))
    elements.append(Paragraph("CEP: 20521-260", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Dados para Contato</b>", styles["Heading3"]))
    elements.append(Paragraph("E-mail: gustavo_lfs@hotmail.com", normal))
    elements.append(Paragraph("Telefone: (21) 996913090", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Dados Bancários</b>", styles["Heading3"]))
    elements.append(Paragraph("Banco: Inter", normal))
    elements.append(Paragraph("Agência: 0001", normal))
    elements.append(Paragraph("Conta: 12174848-0", normal))
    elements.append(Paragraph("PIX: 41.640.044/0001-63", normal))
    elements.append(Spacer(1, 24))

    # Itens da proposta
    elements.append(Paragraph("<b>Itens da Proposta</b>", styles["Heading2"]))
    tabela_dados = [["Produto", "Qtd", "Preço Unit.", "Observações", "Total (R$)"]]
    for item in produtos_editados:
        tabela_dados.append([
            item["Produto"], item["Quantidade"],
            f"R$ {item['Preço Unitário (R$)']:.2f}",
            item["Observações"],
            f"R$ {item['Total (R$)']:.2f}"
        ])
    tabela = Table(tabela_dados, hAlign="LEFT")
    tabela.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
    ]))
    elements.append(tabela)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Total Geral:</b> R$ {total_geral:.2f}", normal))
    elements.append(Spacer(1, 24))

    # Condições comerciais
    elements.append(Paragraph("<b>Condições Comerciais</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Validade da Proposta: {validade_proposta}", normal))
    elements.append(Paragraph(f"Prazo de Pagamento: {prazo_pagamento}", normal))
    elements.append(Paragraph(f"Prazo de Entrega: {prazo_entrega}", normal))
    elements.append(Paragraph("Impostos: Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.", normal))
    elements.append(Spacer(1, 36))

    # Data em português
    meses_pt = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    dia = data_proposta.day
    mes = meses_pt[data_proposta.month - 1]
    ano = data_proposta.year
    elements.append(Paragraph(f"Rio de Janeiro, {dia} de {mes} de {ano}.", normal))
    elements.append(Spacer(1, 48))

    # Assinatura
    elements.append(Paragraph(" ", normal))  # espaço em branco
    elements.append(Paragraph("Gustavo Luiz Freitas de Sousa", normal))
    elements.append(Paragraph("CPF: 148.288.697-94", normal))

    # Gera o PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

if st.button("📥 Exportar para PDF"):
    pdf_buffer = gerar_pdf()
    st.download_button(
        label="⬇️ Baixar Proposta em PDF",
        data=pdf_buffer,
        file_name=f"Proposta_{cliente}.pdf",
        mime="application/pdf"
    )
