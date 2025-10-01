import streamlit as st
import pandas as pd

# Título do app
st.title("Proposta Comercial")

# Dados iniciais da proposta
st.sidebar.header("Informações da Proposta")
cliente = st.sidebar.text_input("Nome do Cliente", "Cliente Exemplo")
data_proposta = st.sidebar.date_input("Data da Proposta")
validade_proposta = st.sidebar.text_input("Validade da Proposta", "30 dias")

# Tabela de produtos (editável)
st.header("Itens")
default_data = {
    "Produto": ["Produto A", "Produto B"],
    "Quantidade": [1, 2],
    "Preço Unitário (R$)": [100.0, 150.0],
    "Observações": ["", ""]
}

# Cria dataframe
df = pd.DataFrame(default_data)

# Permitir edição da tabela
edited_df = st.experimental_data_editor(df, num_rows="dynamic")

# Calcula total por item
edited_df["Total (R$)"] = edited_df["Quantidade"] * edited_df["Preço Unitário (R$)"]

# Mostra tabela final
st.subheader("Resumo da Proposta")
st.dataframe(edited_df)

# Total geral
total_geral = edited_df["Total (R$)"].sum()
st.markdown(f"**Total Geral: R$ {total_geral:.2f}**")

# Exibir informações do cliente
st.markdown("---")
st.subheader("Detalhes do Cliente")
st.markdown(f"- **Cliente:** {cliente}")
st.markdown(f"- **Data da Proposta:** {data_proposta}")
st.markdown(f"- **Validade:** {validade_proposta}")
