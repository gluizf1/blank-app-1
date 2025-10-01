import streamlit as st
import pandas as pd
from datetime import datetime
from babel.dates import format_date  # ✅ Usar Babel para data em português

# ----------------------------
# Função para formatar data em pt-BR
# ----------------------------
def formatar_data(data):
    return format_date(data, format="d 'de' MMMM 'de' yyyy", locale="pt_BR")

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
# Exibir data formatada
# ----------------------------
data_formatada = formatar_data(data_proposta)

st.markdown("---")
st.subheader("Condições Comerciais")
st.markdown(f"- **Validade da Proposta:** {validade_proposta}")
st.markdown(f"- **Prazo de Pagamento:** {prazo_pagamento}")
st.markdown(f"- **Prazo de Entrega:** {prazo_entrega}")
st.markdown("- **Impostos:** Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.")

# ----------------------------
# Data + Assinatura
# ----------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"**Rio de Janeiro, {data_formatada}.**")
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("**Gustavo Luiz Freitas de Sousa**")
st.markdown("CPF: 148.288.697-94")
