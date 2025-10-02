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
import os

# ---------- Helper: formata número no padrão brasileiro (1.234,56) ----------
def formato_brl_num(valor):
    try:
        return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(valor)

# ---------- App ----------
st.set_page_config(page_title="Gerador de Proposta", layout="wide")
st.title("Gerador de Proposta Comercial")

# ----------------------------
# Sidebar: detalhes da proposta + upload
# ----------------------------
st.sidebar.header("Detalhes da Proposta")
cliente = st.sidebar.text_input("Nome do Cliente", "Cliente Exemplo")
data_proposta = st.sidebar.date_input("Data da Proposta", datetime.today())
prazo_pagamento = st.sidebar.text_input("Prazo de Pagamento", "30 dias")
prazo_entrega = st.sidebar.text_input("Prazo de Entrega", "15 dias")
validade_proposta = st.sidebar.text_input("Validade da Proposta", "30 dias")

st.sidebar.markdown("---")
st.sidebar.header("Upload de Produtos")
uploaded_file = st.sidebar.file_uploader(
    "Enviar planilha (.xlsx) com colunas: Produto, Quant., Preço Unit., Observações", 
    type=["xlsx"]
)

# Função para gerar o Excel em memória
def gerar_excel_modelo():
    data = {
        "Produto": ["Produto A", "Produto B", "Produto C"],
        "Quant.": [10, 5, 2],
        "Preço Unit.": [25.50, 100.00, 350.75],
        "Observações": ["", "", ""]
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

# Colocar botão na barra lateral
with st.sidebar:
    st.download_button(
        label="Baixar Modelo Excel",
        data=gerar_excel_modelo(),
        file_name="produtos_modelo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ----------------------------
# Processa upload de Excel
# ----------------------------
if uploaded_file is not None:
    last = st.session_state.get("_last_uploaded_name")
    if last != getattr(uploaded_file, "name", None):
        try:
            df_excel = pd.read_excel(uploaded_file)
            expected = {"Produto", "Quant.", "Preço Unit."}
            if not expected.issubset(set(df_excel.columns)):
                st.sidebar.error(f"Planilha inválida. Precisa conter as colunas: {sorted(list(expected))}")
            else:
                novos = []
                for _, r in df_excel.iterrows():
                    quant = pd.to_numeric(r.get("Quant.", 0), errors="coerce")
                    preco = pd.to_numeric(r.get("Preço Unit.", 0), errors="coerce")
                    novos.append({
                        "id": str(uuid.uuid4()),
                        "Produto": str(r.get("Produto", "")) if pd.notna(r.get("Produto", "")) else "",
                        "Quant.": float(quant) if pd.notna(quant) else 0.0,
                        "Preço Unit.": float(preco) if pd.notna(preco) else 0.0,
                        "Observações": str(r.get("Observações", "")) if "Observações" in df_excel.columns and pd.notna(r.get("Observações", "")) else ""
                    })
                st.session_state.produtos = novos
                st.session_state._last_uploaded_name = getattr(uploaded_file, "name", None)
                st.sidebar.success("Produtos carregados com sucesso.")
        except Exception as e:
            st.sidebar.error(f"Erro ao ler o Excel: {e}")

# ----------------------------
# Inicializa produtos se não houver
# ----------------------------
if "produtos" not in st.session_state or not st.session_state.produtos:
    st.session_state.produtos = [
        {"id": str(uuid.uuid4()), "Produto": "Produto Exemplo", "Quant.": 1, "Preço Unit.": 100.0, "Observações": ""}
    ]

# ----------------------------
# Dados fixos da empresa (visíveis no app)
# ----------------------------
st.markdown(f"**A/C {cliente}**")
st.markdown("### Dados da Empresa")
st.markdown("""**Nome da Empresa:** GUSTAVO LUIZ FREITAS DE SOUSA  
**CNPJ:** 41.640.044/0001-63  
**IE:** 33.822.412.281  
**IM:** 1.304.930-0  
**Endereço:** Rua Henrique Fleiuss, 444 - Tijuca  
**Cidade/UF:** Rio de Janeiro / RJ  
**CEP:** 20521-260""")

st.markdown("### Dados para Contato")
st.markdown("""**E-mail:** gustavo_lfs@hotmail.com  
**Telefone:** (21) 996913090""")

st.markdown("### Dados Bancários")
st.markdown("""**Banco:** Inter  
**Agência:** 0001  
**Conta:** 12174848-0  
**PIX:** 41.640.044/0001-63""")

# ----------------------------
# Funções para manipular produtos
# ----------------------------
def adicionar_produto():
    st.session_state.produtos.append({"id": str(uuid.uuid4()), "Produto": "", "Quant.": 1, "Preço Unit.": 0.0, "Observações": ""})
    st.experimental_rerun()

def remover_produto():
    if len(st.session_state.produtos) > 1:
        st.session_state.produtos.pop()
    st.experimental_rerun()

def limpar_produtos():
    st.session_state.produtos = [{"id": str(uuid.uuid4()), "Produto": "", "Quant.": 1, "Preço Unit.": 0.0, "Observações": ""}]
    st.experimental_rerun()

# ----------------------------
# Edição dinâmica dos produtos
# ----------------------------
st.header("Itens da Proposta")
produtos_editados = []
for i, item in enumerate(st.session_state.produtos):
    with st.expander(f"Produto {i+1}", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            nome = st.text_input("Nome do Produto", item.get("Produto", ""), key=f"nome_{item['id']}")
            obs = st.text_input("Observações", item.get("Observações", ""), key=f"obs_{item['id']}")
        with col2:
            qtd = st.number_input("Quant.", min_value=0.0, value=float(item.get("Quant.", 0)), key=f"qtd_{item['id']}")
            preco = st.number_input("Preço Unit. (R$)", min_value=0.0, value=float(item.get("Preço Unit.", 0.0)), key=f"preco_{item['id']}")
        total = qtd * preco
        st.markdown(f"**Total do Item: R$ {formato_brl_num(total)}**")
        produtos_editados.append({
            "id": item['id'],
            "Produto": nome,
            "Quant.": qtd,
            "Preço Unit.": preco,
            "Observações": obs,
            "Total (R$)": total
        })

# Atualiza session_state de forma consistente
st.session_state.produtos = produtos_editados

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
# Resumo e total
# ----------------------------
df_final = pd.DataFrame(produtos_editados)
st.subheader("Resumo da Proposta")
st.dataframe(df_final, use_container_width=True)
total_geral = df_final["Total (R$)"].sum() if not df_final.empty else 0.0
st.markdown(f"**Total Geral: R$ {formato_brl_num(total_geral)}**")

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
# Data formatada PT-BR
# ----------------------------
meses_pt = {1:"janeiro",2:"fevereiro",3:"março",4:"abril",5:"maio",6:"junho",7:"julho",8:"agosto",9:"setembro",10:"outubro",11:"novembro",12:"dezembro"}
data_formatada = f"{data_proposta.day} de {meses_pt[data_proposta.month]} de {data_proposta.year}"
st.markdown(f"\n\n\n**Rio de Janeiro, {data_formatada}.**")
st.markdown("**Gustavo Luiz Freitas de Sousa**")

# ----------------------------
# Função gerar PDF (robusta)
# ----------------------------
def gerar_pdf_bytes(cliente, data_formatada, df_final, total_geral, prazo_pagamento, prazo_entrega, validade_proposta):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elementos = []
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=22, leading=26, spaceAfter=12, fontName="Helvetica-Bold"))
    estilos.add(ParagraphStyle(name="SectionTitle", alignment=TA_LEFT, fontSize=12, leading=14, spaceAfter=6, fontName="Helvetica-BoldOblique"))
    estilos.add(ParagraphStyle(name="NormalLeft", alignment=TA_LEFT, fontSize=10, leading=12))

    # Logo
    logo_path = "logo.jpg"
    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 50
        logo.drawWidth = 120
        logo.hAlign = 'CENTER'
        elementos.append(logo)
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("Proposta Comercial", estilos["CenterTitle"]))
    elementos.append(Spacer(1, 6))
    elementos.append(Paragraph(f"A/C {cliente}", estilos["NormalLeft"]))
    elementos.append(Spacer(1, 8))

    # Dados fixos
    elementos.append(Paragraph("Dados da Empresa", estilos["SectionTitle"]))
    for linha in [
        "Nome da Empresa: GUSTAVO LUIZ FREITAS DE SOUSA",
        "CNPJ: 41.640.044/0001-63",
        "IE: 33.822.412.281",
        "IM: 1.304.930-0",
        "Endereço: Rua Henrique Fleiuss, 444 - Tijuca",
        "Cidade/UF: Rio de Janeiro / RJ",
        "CEP: 20521-260"
    ]:
        elementos.append(Paragraph(linha, estilos["NormalLeft"]))
    elementos.append(Spacer(1, 6))

    # Contato
    elementos.append(Paragraph("Dados para Contato", estilos["SectionTitle"]))
    for linha in ["E-mail: gustavo_lfs@hotmail.com", "Telefone: (21) 996913090"]:
        elementos.append(Paragraph(linha, estilos["NormalLeft"]))
    elementos.append(Spacer(1, 6))

    # Bancários
    elementos.append(Paragraph("Dados Bancários", estilos["SectionTitle"]))
    for linha in ["Banco: Inter", "Agência: 0001", "Conta: 12174848-0", "PIX: 41.640.044/0001-63"]:
        elementos.append(Paragraph(linha, estilos["NormalLeft"]))
    elementos.append(Spacer(1, 10))

    # Itens
    elementos.append(Paragraph("Itens da Proposta", estilos["SectionTitle"]))
    if not df_final.empty:
        df_tabela = df_final.copy()
        if "Preço Unit." in df_tabela.columns:
            df_tabela = df_tabela.rename(columns={"Preço Unit.": "Preço Unit. (R$)"})
        for col in ["Preço Unit. (R$)", "Total (R$)"]:
            if col in df_tabela.columns:
                df_tabela[col] = df_tabela[col].apply(formato_brl_num)
        header = list(df_tabela.columns)
        dados_tabela = [header] + [[Paragraph(str(c), estilos["NormalLeft"]) for c in row] for row in df_tabela.itertuples(index=False, name=None)]
        largura_total = A4[0] - doc.leftMargin - doc.rightMargin
        col_widths = [largura_total * 0.35 if "Produto" in c else
                      largura_total * 0.25 if "Observações" in c else
                      largura_total * 0.10 if "Quant." in c else
                      largura_total * 0.15 for c in header]
        tabela = Table(dados_tabela, colWidths=col_widths, repeatRows=1)
        estilo_table = TableStyle([
            ("BOX", (0,0), (-1,-1), 1, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.4, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ])
        for ci, col in enumerate(header):
            align = "LEFT" if "Produto" in col or "Observações" in col else "CENTER"
            estilo_table.add("ALIGN", (ci,1), (ci,-1), align)
        tabela.setStyle(estilo_table)
        elementos.append(tabela)
        elementos.append(Spacer(1, 8))
        elementos.append(Paragraph(f"Total Geral: R$ {formato_brl_num(total_geral)}", estilos["NormalLeft"]))
        elementos.append(Spacer(1, 10))
    else:
        elementos.append(Paragraph("Nenhum item adicionado.", estilos["NormalLeft"]))
        elementos.append(Spacer(1, 10))

    # Condições comerciais
    elementos.append(Paragraph("Condições Comerciais", estilos["SectionTitle"]))
    for linha in [
        f"Validade da Proposta: {validade_proposta}",
        f"Prazo de Pagamento: {prazo_pagamento}",
        f"Prazo de Entrega: {prazo_entrega}",
        "Impostos: Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto."
    ]:
        elementos.append(Paragraph(linha, estilos["NormalLeft"]))
    elementos.append(Spacer(1, 8))

    # Data + assinatura
    elementos.append(Paragraph(f"Rio de Janeiro, {data_formatada}.", estilos["NormalLeft"]))
    assinatura_path = "assinatura.png"
    if os.path.exists(assinatura_path):
        assinatura = Image(assinatura_path)
        assinatura.drawHeight = 50
        assinatura.drawWidth = 120
        assinatura.hAlign = 'LEFT'
        elementos.append(assinatura)
    elementos.append(Paragraph("Gustavo Luiz Freitas de Sousa", estilos["NormalLeft"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()

# ----------------------------
# Botão de download PDF
pdf_bytes = gerar_pdf_bytes(cliente, data_formatada, df_final, total_geral, prazo_pagamento, prazo_entrega, validade_proposta)
st.download_button(
    label="Baixar Proposta em PDF",
    data=pdf_bytes,
    file_name=f"proposta_{cliente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
    mime="application/pdf"
)
