#configurações da janela com o tema, tamanho, nome e guardando duas variaveis para utilização em uma das funções
root = ttk.Window(themename='cyborg')
root.geometry("600x700")
root.title('Grupo Fideliza')
root.resizable(False, False)
linha_encontrada = ttk.StringVar()
aba_encontrada = ttk.StringVar()