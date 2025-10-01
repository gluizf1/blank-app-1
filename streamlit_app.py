import streamlit as st
import pandas as pd
from datetime import datetime

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

# Atualiza session_state com os dados editados
st.session_state.produtos = produtos_editados

# ----------------------------
# Botões de adicionar/remover abaixo do último produto
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
# Data da proposta ao final em português (manual)
# ----------------------------
meses_pt = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

dia = data_proposta.day
mes = meses_pt[data_proposta.month - 1]
ano = data_proposta.year

st.markdown(f"**Rio de Janeiro, {dia} de {mes} de {ano}.**")

# ----------------------------
# Espaço para assinatura
# ----------------------------
st.markdown("\n\n\n")  # Espaço em branco
st.markdown("**Gustavo Luiz Freitas de Sousa**")  # Nome
st.markdown("CPF: 148.288.697-94")  # CPF
