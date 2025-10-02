import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import uuid

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
# Upload Excel de produtos
# ----------------------------
uploaded_file = st.sidebar.file_uploader("Upload Excel de Produtos", type="xlsx")
df_excel = None
if uploaded_file:
    try:
        df_excel = pd.read_excel(uploaded_file)
        st.sidebar.success("Arquivo carregado com sucesso!")
    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo Excel: {e}")

# ----------------------------
# Inicializa lista de produtos
# ----------------------------
if "produtos" not in st.session_state:
    if df_excel is not None:
        # Preencher produtos a partir do Excel
        produtos_iniciais = []
        for _, row in df_excel.iterrows():
            produtos_iniciais.append({
                "id": str(uuid.uuid4()),
                "Produto": row.get("Produto", ""),
                "Quant.": row.get("Quant.", 1),
                "Preço Unit.": row.get("Preço Unit.", 0.0),
                "Observações": row.get("Observações", "")
            })
        st.session_state.produtos = produtos_iniciais
    else:
        st.session_state.produtos = [
            {"id": str(uuid.uuid4()), "Produto": "Produto A", "Quant.": 1, "Preço Unit.": 100.0, "Observações": ""}
        ]

def adicionar_produto():
    st.session_state.produtos.append({"id": str(uuid.uuid4()), "Produto": "", "Quant.": 1, "Preço Unit.": 0.0, "Observações": ""})
    st.rerun()

def remover_produto():
    if len(st.session_state.produtos) > 1:
        st.session_state.produtos.pop()
    st.rerun()

def limpar_produtos():
    st.session_state.produtos = [{"id": str(uuid.uuid4()), "Produto": "", "Quant.": 1, "Preço Unit.": 0.0, "Observações": ""}]
    st.rerun()

# ----------------------------
# Editar produtos
# ----------------------------
st.header("Itens da Proposta")
produtos_editados = []

for i, item in enumerate(st.session_state.produtos):
    with st.expander(f"Produto {i+1}", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            nome = st.text_input(f"Nome do Produto", item["Produto"], key=f"nome_{item['id']}")
            obs = st.text_input(f"Observações", item["Observações"], key=f"obs_{item['id']}")
        with col2:
            qtd = st.number_input("Quant.", min_value=0.0, value=float(item["Quant."]), key=f"qtd_{item['id']}")
            preco = st.number_input("Preço Unit. (R$)", min_value=0.0, value=float(item["Preço Unit."]), key=f"preco_{item['id']}")

        total = qtd * preco
        st.markdown(f"**Total do Item: R$ {total:,.2f}**")

        produtos_editados.append({
            "Produto": nome,
            "Quant.": qtd,
            "Preço Unit.": preco,
            "Observações": obs,
            "Total (R$)": total
        })

st.session_state.produtos = [
    {**old, "Produto": new["Produto"], "Quant.": new["Quant."], "Preço Unit.": new["Preço Unit."], "Observações": new["Observações"]}
    for old, new in zip(st.session_state.produtos, produtos_editados)
]

# ----------------------------
# Botões de adicionar/remover/limpar
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.button("➕ Adicionar Produto", on_click=adicionar_produto)
with col2:
    st.button("➖ Remover Último", on_click=remover_produto, disabled=len(st.session_state.produtos) <= 1)
with col3:
    st.button("🗑️ Limpar Todos", on_click=limpar_produtos)

# ----------------------------
# Resumo da proposta
# ----------------------------
df_final = pd.DataFrame(produtos_editados)
st.subheader("Resumo da Proposta")
st.dataframe(df_final)

total_geral = df_final["Total (R$)"].sum() if not df_final.empty else 0.0
st.markdown(f"**Total Geral: R$ {total_geral:,.2f}**")

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

st.markdown(f"\n\n\n**Rio de Janeiro, {data_formatada}.**")
st.markdown("**Gustavo Luiz Freitas de Sousa**")

# ----------------------------
# Função para gerar PDF
# ----------------------------
@st.cache_data
def gerar_pdf(cliente, data_formatada, df_final, total_geral, prazo_pagamento, prazo_entrega, validade_proposta):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=22, leading=26, spaceAfter=20, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="SectionTitle", alignment=TA_LEFT, fontSize=14, leading=18, spaceAfter=5, fontName="Helvetica-BoldOblique"))
    estilos.add(ParagraphStyle(name="ACStyle", fontSize=14, leading=20, spaceAfter=15, fontName="Helvetica"))
    estilos.add(ParagraphStyle(name="CellStyle", fontSize=9, leading=11))

    # Logo fixa
    try:
        logo = Image("logo.jpg")
        logo.drawHeight = 50
        logo.drawWidth = 120
        logo.hAlign = 'CENTER'
        elementos.append(logo)
        elementos.append(Spacer(1, 10))
    except Exception as e:
        st.error(f"Erro ao carregar a logo: {e}")
        elementos.append(Spacer(1, 75))

    elementos.append(Paragraph("Proposta Comercial", estilos["CenterTitle"]))
    elementos.append(Spacer(1, 10))
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
    elementos.append(Spacer(1, 10))

    # Itens da proposta
    elementos.append(Paragraph("Itens da Proposta", estilos["SectionTitle"]))
    elementos.append(Spacer(1, 5))

    if not df_final.empty:
        df_tabela = df_final.copy()
        df_tabela.rename(columns={"Preço Unit.": "Preço Unit. (R$)"}, inplace=True)

        def formato_brl(valor):
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        df_tabela["Preço Unit. (R$)"] = df_tabela["Preço Unit. (R$)"].apply(formato_brl)
        df_tabela["Total (R$)"] = df_tabela["Total (R$)"].apply(formato_brl)

        dados_tabela = [list(df_tabela.columns)]
        for row in df_tabela.values.tolist():
            nova_linha = [Paragraph(str(item).replace('\n', ' '), estilos["CellStyle"]) for item in row]
            dados_tabela.append(nova_linha)

        # Largura proporcional
        colunas = list(df_tabela.columns)
        largura_total = A4[0] - 80
        larguras = []
        for col in colunas:
            if col in ["Produto", "Observações"]:
                larguras.append(largura_total * 0.3)
            elif col == "Preço Unit. (R$)":
                larguras.append(largura_total * 0.15)
            elif col == "Quant.":
                larguras.append(largura_total * 0.1)
            else:
                larguras.append(largura_total * 0.15)

        tabela = Table(dados_tabela, colWidths=larguras, repeatRows=1)
        estilo = TableStyle([
            ("BOX", (0,0), (-1,-1), 1, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.5, colors.black),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,0), 9),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ])
        tabela.setStyle(estilo)
        elementos.append(tabela)
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"Total Geral: {formato_brl(total_geral)}", estilos["Normal"]))
        elementos.append(Spacer(1, 20))
    else:
        elementos.append(Paragraph("Nenhum item adicionado.", estilos["Normal"]))
        elementos.append(Spacer(1, 20))

    # Condições comerciais
    elementos.append(Paragraph("Condições Comerciais", estilos["SectionTitle"]))
    elementos.append(Paragraph(f"Validade da Proposta: {validade_proposta}", estilos["Normal"]))
    elementos.append(Paragraph(f"Prazo de Pagamento: {prazo_pagamento}", estilos["Normal"]))
    elementos.append(Paragraph(f"Prazo de Entrega: {prazo_entrega}", estilos["Normal"]))
    elementos.append(Paragraph("Impostos: Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.", estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    # Data + assinatura
    elementos.append(Paragraph(f"Rio de Janeiro, {data_formatada}.", estilos["Normal"]))
    try:
        assinatura = Image("assinatura.png")
        assinatura.drawHeight = 50
        assinatura.drawWidth = 120
        assinatura.hAlign = 'LEFT'
        elementos.append(assinatura)
    except Exception as e:
        st.error(f"Erro ao carregar a assinatura: {e}")

    elementos.append(Paragraph("Gustavo Luiz Freitas de Sousa", estilos["Normal"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer

# ----------------------------
# Download automático do PDF
# ----------------------------
pdf_buffer = gerar_pdf(cliente, data_formatada, df_final, total_geral, prazo_pagamento, prazo_entrega, validade_proposta)
st.download_button(
    label="Baixar Proposta em PDF", 
    data=pdf_buffer,
    file_name=f"proposta_{cliente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
    mime="application/pdf"
)
