import streamlit as st
import pandas as pd

# ----------------------------
# Informações do cliente e data
# ----------------------------
st.sidebar.header("Detalhes da Proposta")
cliente = st.sidebar.text_input("Nome do Cliente", "Cliente Exemplo")
data_proposta = st.sidebar.date_input("Data da Proposta", pd.to_datetime("2025-10-01"))
prazo_pagamento = st.sidebar.text_input("Prazo de Pagamento", "30 dias")
prazo_entrega = st.sidebar.text_input("Prazo de Entrega", "15 dias")

# Colunas para colocar a data no canto superior direito
col1, col2 = st.columns([3, 1])
with col2:
    st.markdown(f"**Data da Proposta: {data_proposta}**")

# Título principal
st.title("📄 Proposta Comercial Interativa")

# Mostrar cliente logo abaixo do título
st.markdown(f"**A/C: {cliente}**")

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
st.markdown(f"- **Validade da Proposta:** {st.sidebar.text_input('Validade da Proposta', '30 dias')}")
st.markdown(f"- **Prazo de Pagamento:** {prazo_pagamento}")
st.markdown(f"- **Prazo de Entrega:** {prazo_entrega}")
st.markdown("- **Impostos:** Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.")
