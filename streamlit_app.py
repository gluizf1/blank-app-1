import streamlit as st
import pandas as pd

st.title("📄 Proposta Comercial Interativa")

# Dados do cliente
st.sidebar.header("Informações da Proposta")
cliente = st.sidebar.text_input("Nome do Cliente", "Cliente Exemplo")
data_proposta = st.sidebar.date_input("Data da Proposta")
validade_proposta = st.sidebar.text_input("Validade da Proposta", "30 dias")

# Lista de produtos inicial
produtos = [
    {"Produto": "Produto A", "Quantidade": 1, "Preço Unitário (R$)": 100.0, "Observações": ""},
    {"Produto": "Produto B", "Quantidade": 2, "Preço Unitário (R$)": 150.0, "Observações": ""}
]

st.header("Itens da Proposta")
# Criar lista para armazenar produtos editados
produtos_editados = []

for i, item in enumerate(produtos):
    st.subheader(f"Produto {i+1}")
    nome = st.text_input(f"Nome do Produto {i+1}", item["Produto"], key=f"nome_{i}")
    qtd = st.number_input(f"Quantidade {i+1}", min_value=0, value=item["Quantidade"], key=f"qtd_{i}")
    preco = st.number_input(f"Preço Unitário {i+1}", min_value=0.0, value=item['Preço Unitário (R$)'], key=f"preco_{i}")
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

# Mostrar tabela final
df_final = pd.DataFrame(produtos_editados)
st.subheader("Resumo da Proposta")
st.dataframe(df_final)

# Total geral
total_geral = df_final["Total (R$)"].sum()
st.markdown(f"**Total Geral: R$ {total_geral:.2f}**")

# Detalhes do cliente
st.markdown("---")
st.subheader("Detalhes do Cliente")
st.markdown(f"- **Cliente:** {cliente}")
st.markdown(f"- **Data da Proposta:** {data_proposta}")
st.markdown(f"- **Validade:** {validade_proposta}")
