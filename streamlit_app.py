import streamlit as st
import pandas as pd
from datetime import datetime
import locale

# Tentar importar o reportlab
try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    reportlab_disponivel = True
except ImportError:
    reportlab_disponivel = False

# Definir locale para português
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
except:
    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

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
# A/C e dados fixos da empresa
# ----------------------------
st.markdown(f"**A/C: {cliente}**")
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
# Inicializa lista de produtos no session_state
# ----------------------------
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"Produto": "Produto A", "Quantidade": 1, "Preço Unitário (R$)": 100.0, "Observações": ""},
        {"Produto": "Produto B", "Quantidade": 2, "Preço Unitário (R$)": 150.0, "Observações": ""}
    ]

# ----------------------------
# Funções para adicionar/remover produtos
# ----------------------------
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

# Atualiza session_state
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
# Mostrar tabela final
# ----------------------------
df_final = pd.DataFrame(produtos_editados)
st.subheader("Resumo da Proposta")
st.dataframe(df_final)

# Total geral
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
# Data + assinatura
# ----------------------------
data_formatada = data_proposta.strftime("%d de %B de %Y")
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"**Rio de Janeiro, {data_formatada}.**")
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("**Gustavo Luiz Freitas de Sousa**")
st.markdown("CPF: 148.288.697-94")

# ----------------------------
# Exportar PDF
# ----------------------------
if reportlab_disponivel:
    if st.button("📥 Exportar para PDF"):
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate("proposta.pdf", pagesize=A4)
        elements = []

        elements.append(Paragraph(f"A/C: {cliente}", styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Tabela de produtos
        tabela_data = [["Produto", "Qtd", "Preço Unitário", "Observações", "Total"]]
        for p in produtos_editados:
            tabela_data.append([p["Produto"], p["Quantidade"], f"R$ {p['Preço Unitário (R$)']:.2f}", p["Observações"], f"R$ {p['Total (R$)']:.2f}"])
        tabela = Table(tabela_data)
        tabela.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 1, colors.black)]))
        elements.append(tabela)
        elements.append(Spacer(1, 24))

        elements.append(Paragraph(f"Total Geral: R$ {total_geral:.2f}", styles["Heading3"]))
        elements.append(Spacer(1, 24))

        elements.append(Paragraph("Condições Comerciais", styles["Heading2"]))
        elements.append(Paragraph(f"Validade da Proposta: {validade_proposta}", styles["Normal"]))
        elements.append(Paragraph(f"Prazo de Pagamento: {prazo_pagamento}", styles["Normal"]))
        elements.append(Paragraph(f"Prazo de Entrega: {prazo_entrega}", styles["Normal"]))
        elements.append(Paragraph("Impostos: Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.", styles["Normal"]))
        elements.append(Spacer(1, 48))

        elements.append(Paragraph(f"Rio de Janeiro, {data_formatada}.", styles["Normal"]))
        elements.append(Spacer(1, 48))
        elements.append(Paragraph("Gustavo Luiz Freitas de Sousa", styles["Normal"]))
        elements.append(Paragraph("CPF: 148.288.697-94", styles["Normal"]))

        doc.build(elements)

        with open("proposta.pdf", "rb") as f:
            st.download_button("⬇️ Baixar PDF", f, file_name="proposta.pdf")
else:
    st.warning("⚠️ O módulo `reportlab` não está instalado. Adicione `reportlab` ao arquivo requirements.txt ou instale localmente com `pip install reportlab`.")
