#Criando as varias de cada planilha
planilha = cliente.open(SPREADSHEET_NAME)
aba_leads = planilha.worksheet("LEADS")
aba_vendas = planilha.worksheet("VENDA")
aba_proposta_yamaha = planilha.worksheet("PROPOSTA-YAMAHA")
aba_proposta_ancora = planilha.worksheet("PROPOSTA-ANCORA")
aba_proposta_gazin = planilha.worksheet("PROPOSTA-GAZIN")

#Conexão com a planilha e mensagem de erro caso de algum problema
try:
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_SHEETS_CREDENTIALS, SCOPE)
    client = gspread.authorize(credentials)
    spreadsheet = client.open("Projeto")
except Exception as e:
    messagebox.showerror("Erro", f"Erro ao conectar com Google Sheets: {e}")
    exit()

#Essa função esconde todas as paginas e mostra apenas a pagina selecionada
def mostrar_pagina(pagina):
    for frame in [pagina1, pagina2, pagina3, pagina4, pagina5]:
        frame.pack_forget()
    pagina.pack(expand=True)

def enviar_proposta_para_sheets():
    try:
        #Coleta todos os dados do formulario para inserção na planilha
        #Se tiver um campo de data, acessa o entry dentro do widget, senão acessa o valor direto
        dados_proposta = [widget.entry.get() if valor == 'DATA' else widget.get() for valor, widget in campos_proposta]

        #Extrai o CPF e a administradora e guarda em variveis, para fazer a validação
        cpf = next((widget.get() for valor, widget in campos_proposta if valor == 'CPF'), None)
        administradora = next((widget.get() for valor, widget in campos_proposta if valor == 'ADMINISTRADORA'), None)
        
        #Mapea as administradoras existentes
        planilhas = {
            'YAMAHA': aba_proposta_yamaha,
            'GAZIN': aba_proposta_gazin,
            'ANCORA': aba_proposta_ancora
        }
        #Valida se a administradora existe
        if administradora not in planilhas:
            status_proposta.config(text="❌ Administradora inválida!", bootstyle="danger")
            return #Sai da função caso a administradora não exista no mapeamento
        
        #Define a aba correta para enviar os dados vindos do formulario
        aba_destino = planilhas[administradora]

        #Busca por todas as linhas da planilha
        todas_linhas = aba_destino.get_all_values()  
        
        #Verifica se existe uma proposta em aberto sem status
        for linha in todas_linhas:
            if len(linha) >= 11: #garante que a linha tenha pelo menos 11 colunas
                cpf_existente = linha[3]  #coluna D - CPF (índice 3)
                status = linha[10]        #coluna K - STATUS (índice 10)

                #Se encontrar uma proposta em aberta com o mesmo CPF, bloqueia o envio de novas propostas
                if cpf_existente == cpf and status.strip() == "":
                    status_proposta.config(
                        text="❌ Já existe uma proposta ativa (sem status) para esse CPF!",
                        bootstyle="danger"
                    )
                    return  #Bloqueia o envio de novas propostas para esse CPF, enquanto não atualiza o status

        #Envia os dados caso passe na validação de prosposta        
        aba_destino.append_row(dados_proposta)

        #Mensagem de sucesso
        status_lead.config(text="✅ Proposta enviado com sucesso!")

        #Limpa a mensagem de sucesso apos 3 segundos
        root.after(3000, lambda: status_proposta.config(text=""))
        
        #Limpa os campos, para nova inserção de dados no formulario
        for _, widget in campos_proposta:
            if isinstance(widget, ttk.Entry): #se o campo for de entrada de texto
                widget.delete(0, 'end') #limpa o campo
            elif isinstance(widget, ttk.Combobox): #se for um campo de seleção
                widget.set('')#reseta o valor selecionado
    except Exception as e:
        #captura qualquer erro e exibe na tela
        status_proposta.config(text=f"❌ Erro: {e}", bootstyle="danger")

#Função para buscar as propostas
def buscar_proposta_google_sheets():

    #Extrai o CPF e valida
    cpf_digitado = campos_buscar_proposta[0][1].get().strip() 

    #verifica se o CPF foi preenchido 
    if not cpf_digitado:
        status_busca.config(text="Digite um CPF válido!", bootstyle="danger")
        return #cancela caso esteja vazio
    
    #Extrai a Administradora e valida
    administradora_selecionada = campos_buscar_proposta[1][1].get().strip()

    #verifica se a administradora é valida
    if administradora_selecionada not in ['YAMAHA', 'GAZIN', 'ANCORA']:
        status_busca.config(text="Selecione uma administradora válida!", bootstyle="danger")
        return #cancela caso não seja valido
    
    try:
        #Mapea as administradoras existentes
        abas = {
            'YAMAHA': aba_proposta_yamaha,
            'GAZIN': aba_proposta_gazin,
            'ANCORA': aba_proposta_ancora
        }

        #seleciona a aba correta
        aba = abas[administradora_selecionada]

        #pega todas as linhas da planilha como dicionario (header: valor)
        dados = aba.get_all_records()

        #Lista para armazenar as propostas encontradas para o CPF digitado
        propostas_cpf = []  

        #percorre todas as linhas buscando CPF
        for linha in dados:
            if str(linha.get("CPF", "")).strip() == cpf_digitado:
                propostas_cpf.append(linha)
            
        #caso não encontre, mostra erro
        if not propostas_cpf:
            status_busca.config(text="CPF não encontrado nesta administradora.", bootstyle="danger")
            return
        
        #função auxiliar para converter a string em data em objeto datetime, para depois puxar a mais recente
        def parse_data(data_str):
            try:
                return datetime.strptime(data_str, "%d/%m/%Y") #Converte a data para o formato brasileiro dia/mes/ano
            except Exception:
                return datetime.min  #caso data inválida, joga para o fim da ordenação

        #ordena as propostas pela data da mais recente
        propostas_cpf.sort(key=lambda x: parse_data(x.get("DATA", "")), reverse=True)

        #pega a proposta mais recente
        proposta_recente = propostas_cpf[0]

        #montagem do texto para exibição na tela
        proposta_texto = (
            f"Vendedor: {linha['VENDEDOR']}\n"
            f"Nome: {linha['NOME']}\n"
            f"Telefone: {linha['TELEFONE']}\n"
            f"Tipo de Carta: {linha['TIPO DE CARTA']}\n"
            f"Valor da Carta: {linha['VALOR DA CARTA']}\n"
            f"Administradora: {linha['ADMINISTRADORA']}\n"
            f"Taxa: {linha['TAXA']}%\n"
            f"Valor da Parcela: {linha['VALOR DA PARCELA']}\n"
            f"Status: {linha['STATUS']}\n"
            f"Data: {linha['DATA']}\n"
            "------------------------"
        )

        #exibe as informações na tela
        status_busca.config(text=proposta_texto, bootstyle="success")

        #Salva o numero da linha para utilização futura
        linha_proposta_recente = dados.index(proposta_recente) + 2  #+2 porque o cabeçalho ocupa a 1ª linha

        #guarda a linha para edição futura
        linha_encontrada.set(linha_proposta_recente)

        #guarda a aba onde a proposta foi encontrada
        aba_encontrada.set(administradora_selecionada)  

    except Exception as e:
        #em caso de erro, exibe a mensagem
        status_busca.config(text=f"Erro ao buscar: {str(e)}", bootstyle="danger")


def atualizar_status_proposta():
    #declara que as variaveis globais serão utilizadas nessa função
    global linha_encontrada, aba_encontrada

    #Verifica se houve busca anterior
    if linha_encontrada.get() == "" or aba_encontrada.get() == "":
        #Se não teve busca, exibe um aviso de erro
        status_busca.config(text="⚠️ Nenhuma proposta foi buscada ainda.", bootstyle="warning")
        return

    #Obtém novo status da interface
    novo_status = campos_buscar_proposta[2][1].get().strip().upper()

    #verifica se o novo status é permitido
    if novo_status not in ["", "APROVADO", "NÃO APROVADO"]:
        #Se não for, exibe a mensagem de erro e encerra a função
        status_busca.config(text="⚠️ Status inválido! Use '', 'APROVADO' ou 'NÃO APROVADO'.", bootstyle="danger")
        return

    try:
        #Mapeia as administradoras existentes
        aba = {
            'YAMAHA': aba_proposta_yamaha,
            'GAZIN': aba_proposta_gazin,
            'ANCORA': aba_proposta_ancora
        }.get(aba_encontrada.get()) #Seleciona a aba correta com base na administradora

        #se a aba não for encontrada, exibe o erro e cancela a função
        if not aba:
            status_busca.config(text="Erro: Aba da administradora não encontrada.", bootstyle="danger")
            return

        # Atualiza a célula da coluna K (coluna 11) com o novo status
        linha = int(linha_encontrada.get()) #converte a linha de string para inteiro
        aba.update_cell(int(linha_encontrada.get()), 11, novo_status) #atualiza a celula com o novo status

        #exibe mensagem de sucesso
        status_busca.config(text="✅ Status atualizado com sucesso!", bootstyle="success")

        #limpa as variaveis globais para evitar atualizações futuras sem nova busca
        linha_encontrada.set("")
        aba_encontrada.set("")

    except Exception as e:
        #se ocorrer qualquer erro, exibe a mensagem de erro na interface
        status_busca.config(text=f"Erro ao atualizar: {str(e)}", bootstyle="danger")
    

def enviar_lead_para_sheets():
    try:
        #Coleta todos os dados do formulario para inserção na planilha
        #Se tiver um campo de data, acessa o entry dentro do widget, senão acessa o valor direto
        dados_lead = [widget.entry.get() if valor == 'DATA' else widget.get() for valor, widget in campos_lead]

        #Adiciona a nova linha com os dados do lead na aba correta
        aba_leads.append_row(dados_lead)
        
        #Atualiza o Label de status
        status_lead.config(text="✅ Lead enviado com sucesso!")

        #Limpa apos 3 segundos a mensagem de sucesso
        root.after(3000, lambda: status_lead.config(text=""))  
        
        #Limpa os campos após o envio, para cadastro de novos
        for _, widget in campos_lead:
            if isinstance(widget, ttk.Entry): #se for texto limpa o conteudo
                widget.delete(0, 'end')
            elif isinstance(widget, ttk.Combobox): #se for combobox, reseta o valor
                widget.set('')

    except Exception as e:
        #em caso de erro, exibe na tela
        status_lead.config(text=f"❌ Erro: {e}", bootstyle="danger")

def enviar_venda_para_sheets():
    try:
        #Coleta todos os dados do formulario para inserção na planilha
        #Se tiver um campo de data, acessa o entry dentro do widget, senão acessa o valor direto
        dados_venda = [widget.entry.get() if valor == 'DATA' else widget.get() for valor, widget in campos_venda]

        #Adiciona a nova linha com os dados da venda na aba correta
        aba_vendas.append_row(dados_venda)
        
        #atualiza o Label de status
        status_venda.config(text="✅ Venda enviada com sucesso!")

        #Limpa apos 3 segundos a mensagem de sucesso
        root.after(3000, lambda: status_venda.config(text=""))  
        
        #Limpa os campos
        for _, widget in campos_venda:
            if isinstance(widget, ttk.Entry): #se for texto limpa o conteudo
                widget.delete(0, 'end')
            elif isinstance(widget, ttk.Combobox): #se for combobox, reseta o valor
                widget.set('')

    except Exception as e:
        #em caso de erro, exibe na tela
        status_venda.config(text=f"❌ Erro: {e}", bootstyle="danger")
