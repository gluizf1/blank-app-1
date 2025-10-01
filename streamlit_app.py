def gerar_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []
    estilos = getSampleStyleSheet()

    # Cabeçalho
    elementos.append(Paragraph(f"Proposta Comercial", estilos["Title"]))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph(f"A/C: {cliente}", estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    # Dados fixos da empresa
    elementos.append(Paragraph("<b>Dados da Empresa</b>", estilos["Heading3"]))
    elementos.append(Paragraph("Nome da Empresa: GUSTAVO LUIZ FREITAS DE SOUSA", estilos["Normal"]))
    elementos.append(Paragraph("CNPJ: 41.640.044/0001-63", estilos["Normal"]))
    elementos.append(Paragraph("IE: 33.822.412.281", estilos["Normal"]))
    elementos.append(Paragraph("IM: 1.304.930-0", estilos["Normal"]))
    elementos.append(Paragraph("Endereço: Rua Henrique Fleiuss, 444 - Tijuca", estilos["Normal"]))
    elementos.append(Paragraph("Cidade/UF: Rio de Janeiro / RJ", estilos["Normal"]))
    elementos.append(Paragraph("CEP: 20521-260", estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    # Dados para contato
    elementos.append(Paragraph("<b>Dados para Contato</b>", estilos["Heading3"]))
    elementos.append(Paragraph("E-mail: gustavo_lfs@hotmail.com", estilos["Normal"]))
    elementos.append(Paragraph("Telefone: (21) 996913090", estilos["Normal"]))
    elementos.append(Spacer(1, 10))

    # Dados bancários
    elementos.append(Paragraph("<b>Dados Bancários</b>", estilos["Heading3"]))
    elementos.append(Paragraph("Banco: Inter", estilos["Normal"]))
    elementos.append(Paragraph("Agência: 0001", estilos["Normal"]))
    elementos.append(Paragraph("Conta: 12174848-0", estilos["Normal"]))
    elementos.append(Paragraph("PIX: 41.640.044/0001-63", estilos["Normal"]))
    elementos.append(Spacer(1, 20))

    # Tabela de produtos
    if not df_final.empty:
        tabela = Table(
            [list(df_final.columns)] + df_final.values.tolist(),
            colWidths=[100, 70, 100, 100, 80]
        )
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ]))
        elementos.append(tabela)
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"Total Geral: R$ {total_geral:.2f}", estilos["Normal"]))
        elementos.append(Spacer(1, 20))

    # Condições comerciais
    elementos.append(Paragraph("<b>Condições Comerciais</b>", estilos["Heading3"]))
    elementos.append(Paragraph(f"Validade da Proposta: {validade_proposta}", estilos["Normal"]))
    elementos.append(Paragraph(f"Prazo de Pagamento: {prazo_pagamento}", estilos["Normal"]))
    elementos.append(Paragraph(f"Prazo de Entrega: {prazo_entrega}", estilos["Normal"]))
    elementos.append(Paragraph("Impostos: Nos preços estão incluídos todos os custos indispensáveis à perfeita execução do objeto.", estilos["Normal"]))
    elementos.append(Spacer(1, 40))

    # Data + assinatura
    elementos.append(Paragraph(f"Rio de Janeiro, {data_formatada}.", estilos["Normal"]))
    elementos.append(Spacer(1, 40))
    elementos.append(Paragraph("Gustavo Luiz Freitas de Sousa", estilos["Normal"]))
    elementos.append(Paragraph("CPF: 148.288.697-94", estilos["Normal"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer
