# Criação das paginas
pagina1 = ttk.Frame(root, padding=20) #Menu principal
pagina2 = ttk.Frame(root, padding=20) #venda
pagina3 = ttk.Frame(root, padding=20) #lead
pagina4 = ttk.Frame(root, padding=20) #proposta
pagina5 = ttk.Frame(root, padding=20) #busca

# Configurações padrões de botões
botão_largura = 15 
botão_espaçamento = (10, 10)

# --- Tela 1: Menu Principal ---
#Texto principal
ttk.Label(pagina1, text="SELECIONE UMA OPÇÃO", font=("Arial", 16, "bold"), bootstyle="primary").pack(pady=20)
#botao para cadastro de lead
botao_lead = ttk.Button(pagina1, text='📋 LEAD', bootstyle="purple", width=botão_largura, padding=botão_espaçamento, command=lambda: mostrar_pagina(pagina3))
botao_lead.pack(pady=20)
#botao para cadastro de venda
botao_venda = ttk.Button(pagina1, text='💰 VENDA', bootstyle="success", width=botão_largura, padding=botão_espaçamento, command=lambda: mostrar_pagina(pagina2))
botao_venda.pack(pady=20)
#botao para cadastro de proposta
botao_proposta = ttk.Button(pagina1, text='💲 PROPOSTA', bootstyle="info", width=botão_largura, padding=botão_espaçamento, command=lambda: mostrar_pagina(pagina4))
botao_proposta.pack(pady=20)
#botao para busca de proposta
botao_busca = ttk.Button(pagina1, text='🔍 BUSCAR\nPROPOSTA', bootstyle="light", width=botão_largura, padding=botão_espaçamento, command=lambda: mostrar_pagina(pagina5))
botao_busca.pack(pady=20)


# --- Tela 2: Cadastro de Venda ---

#Lista de tuplas, (rotulo/descritivo) = vendedor, combobox com lista de vendedores
campos_venda = [
    #criação dos campos de texto (ttk.entry), seleção(ttk.combobox) + opções de seleção, data(ttk.DateEntry)
    ("VENDEDOR", ttk.Combobox(pagina2, values=['JEOVANE', 'RAISSA', 'CAMILA', 'ELAINE', 'PEDRO', 'MARILIA', 'JERFESON', 'MICHELE', 'CARLA', 'EMILY', 'SABRINA', 'FLÁVIA', 'GREICI'], state='readonly')),
    ("NOME DO CLIENTE", ttk.Entry(pagina2)),
    ("TELEFONE", ttk.Entry(pagina2)),
    ("IDADE", ttk.Entry(pagina2)),
    ("GÊNERO", ttk.Combobox(pagina2, values=['M', 'F'], state='readonly')),
    ("ESTADO", ttk.Combobox(pagina2, values=['Acre', 'Alagoas', 'Amazonas', 'Bahia', 'Ceará', 'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'], state='readonly')),
    ("TIPO DE CARTA", ttk.Combobox(pagina2, values=['IMÓVEL', 'AUTOMÓVEL', 'SERVIÇO', 'MÁQUINAS E EQUIPAMENTOS'], state='readonly')),
    ("VALOR DA CARTA", ttk.Entry(pagina2)),
    ("DATA", ttk.DateEntry(pagina2)),
]

#percorre toda a lista onde cada item é uma tupla, i representa o indice, label text é o texto do rotulo, widget é o campo de entrada
for i, (label_text, widget) in enumerate(campos_venda):
    #cria o label com o texto "label_text", configura posicionamento, fonte, tamanho, espaçamento e alinhamento
    ttk.Label(pagina2, text=label_text, font=("Arial", 10, "bold"), bootstyle="primary").grid(row=i, column=0, sticky=W, pady=5)
    widget.grid(row=i, column=1, padx=10, pady=5, sticky=EW)

#cria um botao "enviar" estilizado de sucesso, apos ser clicado chama a função para enviar para planilha
botao_enviar_venda = ttk.Button(pagina2, text='✅ ENVIAR', bootstyle="success", command=enviar_venda_para_sheets)
#posiciona o botao apos os campos, ocupando duas colunas com espaçamento vertical
botao_enviar_venda.grid(row=len(campos_venda), column=0, columnspan=2, pady=20)

#cria um botão "voltar" estilizado com o tema "danger", e chama a função mostrar pagina, indicando pagina 1
botao_voltar1 = ttk.Button(pagina2, text='⬅ Voltar', bootstyle="danger", command=lambda: mostrar_pagina(pagina1))
#posiciona o botao apos o enviar, ocupando duas colunas com espaçamento vertical
botao_voltar1.grid(row=len(campos_venda) + 1, column=0, columnspan=2, pady=20)

#cria um label para exibir a mensagem de status, inicialmente está vazio
status_venda = ttk.Label(pagina2, text="", bootstyle="success")
#posiciona o label abaixo dos botões, ocupando duas colunas com espaçamento vertical
status_venda.grid(row=len(campos_venda) + 2, column=0, columnspan=2, pady=20)

# --- Tela 3: Cadastro de Lead ---

#Lista de tuplas, (rotulo/descritivo) = vendedor, combobox com lista de vendedores
campos_lead = [
    #criação dos campos de texto (ttk.entry), seleção(ttk.combobox) + opções de seleção, data(ttk.DateEntry)
    ("VENDEDOR", ttk.Combobox(pagina3, values=['JEOVANE', 'RAISSA', 'CAMILA', 'ELAINE', 'PEDRO', 'MARILIA', 'JERFESON', 'MICHELE', 'CARLA', 'EMILY', 'SABRINA', 'FLÁVIA', 'GREICI'], state='readonly')),
    ("NOME", ttk.Entry(pagina3)),
    ("TELEFONE", ttk.Entry(pagina3)),
    ("IDADE", ttk.Entry(pagina3)),
    ("ESTADO", ttk.Combobox(pagina3, values=['Acre', 'Alagoas', 'Amazonas', 'Bahia', 'Ceará', 'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'], state='readonly')),
    ("TIPO DE CARTA", ttk.Combobox(pagina3, values=['IMÓVEL', 'AUTOMÓVEL', 'SERVIÇO', 'MÁQUINAS E EQUIPAMENTOS'], state='readonly')),
    ("VALOR DA CARTA", ttk.Entry(pagina3)),
    ("DATA", ttk.DateEntry(pagina3)),
]

#percorre toda a lista onde cada item é uma tupla, i representa o indice, label text é o texto do rotulo, widget é o campo de entrada
for i, (label_text, widget) in enumerate(campos_lead):
    #cria o label com o texto "label_text", configura posicionamento, fonte, tamanho, espaçamento e alinhamento
    ttk.Label(pagina3, text=label_text, font=("Arial", 10, "bold"), bootstyle="primary").grid(row=i, column=0, sticky=W, pady=5)
    widget.grid(row=i, column=1, padx=10, pady=5, sticky=EW)

#cria um botao "enviar" estilizado de sucesso, apos ser clicado chama a função para enviar para planilha
botao_enviar_lead = ttk.Button(pagina3, text='✅ ENVIAR', bootstyle="success", command=enviar_lead_para_sheets)
#posiciona o botao apos os campos, ocupando duas colunas com espaçamento vertical
botao_enviar_lead.grid(row=len(campos_lead), column=0, columnspan=2, pady=20)

#cria um botão "voltar" estilizado com o tema "danger", e chama a função mostrar pagina, indicando pagina 1
botao_voltar1 = ttk.Button(pagina3, text='⬅ Voltar', bootstyle="danger", command=lambda: mostrar_pagina(pagina1))
#posiciona o botao apos o enviar, ocupando duas colunas com espaçamento vertical
botao_voltar1.grid(row=len(campos_lead) + 1, column=0, columnspan=2, pady=20)

#cria um label para exibir a mensagem de status, inicialmente está vazio
status_lead = ttk.Label(pagina3, text="", bootstyle="success")
#posiciona o label abaixo dos botões, ocupando duas colunas com espaçamento vertical
status_lead.grid(row=len(campos_lead) + 2, column=0, columnspan=2, pady=20)

# --- Tela 4: Cadastro de Proposta ---

#Lista de tuplas, (rotulo/descritivo) = vendedor, combobox com lista de vendedores
campos_proposta = [
    #criação dos campos de texto (ttk.entry), seleção(ttk.combobox) + opções de seleção, data(ttk.DateEntry)
    ("VENDEDOR", ttk.Combobox(pagina4, values=['JEOVANE', 'RAISSA', 'CAMILA', 'ELAINE', 'PEDRO', 'MARILIA', 'JERFESON', 'MICHELE', 'CARLA', 'EMILY', 'SABRINA', 'FLÁVIA', 'GREICI'], state='readonly')),
    ("NOME", ttk.Entry(pagina4)),
    ("TELEFONE", ttk.Entry(pagina4)),
    ("CPF", ttk.Entry(pagina4)),
    ("TIPO DE CARTA", ttk.Combobox(pagina4, values=['IMÓVEL', 'AUTOMÓVEL', 'SERVIÇO', 'MÁQUINAS E EQUIPAMENTOS'], state='readonly')),
    ("VALOR DA CARTA", ttk.Entry(pagina4)),
    ("TAXA", ttk.Entry(pagina4)),
    ("VALOR DA PARCELA", ttk.Entry(pagina4)),
    ("DATA", ttk.DateEntry(pagina4)),
    ("ADMINISTRADORA", ttk.Combobox(pagina4, values=['ANCORA', 'GAZIN', 'YAMAHA'], state='readonly')),
]

#percorre toda a lista onde cada item é uma tupla, i representa o indice, label text é o texto do rotulo, widget é o campo de entrada
for i, (label_text, widget) in enumerate(campos_proposta):
    #cria o label com o texto "label_text", configura posicionamento, fonte, tamanho, espaçamento e alinhamento
    ttk.Label(pagina4, text=label_text, font=("Arial", 10, "bold"), bootstyle="primary").grid(row=i, column=0, sticky=W, pady=5)
    widget.grid(row=i, column=1, padx=10, pady=5, sticky=EW)

#cria um botao "enviar" estilizado de sucesso, apos ser clicado chama a função para enviar para planilha
botao_enviar_proposta = ttk.Button(pagina4, text='✅ ENVIAR', bootstyle="success", command=enviar_proposta_para_sheets)
#posiciona o botao apos os campos, ocupando duas colunas com espaçamento vertical
botao_enviar_proposta.grid(row=len(campos_proposta), column=0, columnspan=2, pady=20)

#cria um botão "voltar" estilizado com o tema "danger", e chama a função mostrar pagina, indicando pagina 1
botao_voltar1 = ttk.Button(pagina4, text='⬅ Voltar', bootstyle="danger", command=lambda: mostrar_pagina(pagina1))
#posiciona o botao apos o enviar, ocupando duas colunas com espaçamento vertical
botao_voltar1.grid(row=len(campos_proposta) + 1, column=0, columnspan=2, pady=20)

#cria um label para exibir a mensagem de status, inicialmente está vazio
status_proposta = ttk.Label(pagina4, text="", bootstyle="success")
#posiciona o label abaixo dos botões, ocupando duas colunas com espaçamento vertical
status_proposta.grid(row=len(campos_proposta) + 2, column=0, columnspan=2, pady=20)

# --- Tela 5: Busca da proposta ---

#Lista de tuplas, (rotulo/descritivo) = vendedor, combobox com lista de vendedores
campos_buscar_proposta = [
    #criação dos campos de texto (ttk.entry), seleção(ttk.combobox) + opções de seleção
    ("CPF", ttk.Entry(pagina5)),
    ("ADMINISTRADORA", ttk.Combobox(pagina5, values=['ANCORA', 'GAZIN', 'YAMAHA'], state='readonly')),
    ("STATUS", ttk.Combobox(pagina5, values=['', 'APROVADO', 'NÃO APROVADO'], state='readonly')),
]

#percorre toda a lista onde cada item é uma tupla, i representa o indice, label text é o texto do rotulo, widget é o campo de entrada
for i, (label_text, widget) in enumerate(campos_buscar_proposta):
    #cria o label com o texto "label_text", configura posicionamento, fonte, tamanho, espaçamento e alinhamento
    ttk.Label(pagina5, text=label_text, font=("Arial", 10, "bold"), bootstyle="primary").grid(row=i, column=0, sticky=W, pady=5)
    widget.grid(row=i, column=1, padx=10, pady=5, sticky=EW)

#cria um botao "enviar" estilizado de "warning", apos ser clicado chama a função para enviar para planilha
botao_atualizar_status = ttk.Button(pagina5, text="🔄 Atualizar Status", bootstyle="warning", command=atualizar_status_proposta)
#posiciona o botao apos os campos, ocupando duas colunas com espaçamento vertical
botao_atualizar_status.grid(row=len(campos_buscar_proposta), column=0, columnspan=2, pady=20)

#cria um botao "enviar" estilizado de sucesso, apos ser clicado chama a função para enviar para planilha
botao_enviar_buscar_proposta = ttk.Button(pagina5, text='✅ PESQUISAR', bootstyle="success", command=buscar_proposta_google_sheets)
#posiciona o botao apos o botão atualizar, ocupando duas colunas com espaçamento vertical
botao_enviar_buscar_proposta.grid(row=len(campos_buscar_proposta) + 1, column=0, columnspan=2, pady=20)

#cria um botão "voltar" estilizado com o tema "danger", e chama a função mostrar pagina, indicando pagina 1
botao_voltar1 = ttk.Button(pagina5, text='⬅ Voltar', bootstyle="danger", command=lambda: mostrar_pagina(pagina1))
#posiciona o botao apos o enviar, ocupando duas colunas com espaçamento vertical
botao_voltar1.grid(row=len(campos_buscar_proposta) + 2, column=0, columnspan=2, pady=20)

#cria um label para exibir a mensagem de status, inicialmente está vazio
status_busca = ttk.Label(pagina5, text="", bootstyle="success")
#posiciona o label abaixo dos botões, ocupando duas colunas com espaçamento vertical
status_busca.grid(row=len(campos_buscar_proposta) + 3, column=0, columnspan=2, pady=10)

#chama a função de mostrar a pagina, passando o argumento "pagina1" que é a janela principal
mostrar_pagina(pagina1)

#faz com que a janela se mantenha aberta
root.mainloop()