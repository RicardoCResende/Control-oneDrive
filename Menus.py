import PySimpleGUI as sg


def menu(acesso):
    """
    Cria a janela inicial do sistema
    :return: o botão que foi pressionado.
    """
    sg.theme('DarkBlue')
    layout = [
        [sg.Image('Images/logo2.png', background_color='darkblue')]]
    if acesso:
        layout.append([sg.Button(key='relatorio', image_filename='Images/relatorio_button.png', border_width=0,
                                 button_color=sg.theme_background_color(), use_ttk_buttons=True),
                       sg.Text('', size=22),
                       sg.Button('', image_filename='Images/cadastro_button.png', border_width=0,
                                 button_color=(sg.theme_background_color()), key='cadastro', use_ttk_buttons=True,
                                 tooltip='Menu Clientes'),
                       sg.Text('', size=23),
                       sg.B(key='new_user', image_filename='Images/new_user.png', border_width=0,
                            button_color=sg.theme_background_color(), use_ttk_buttons=True),
                       sg.Text('', size=23),
                       sg.Button('', image_filename='Images/sair_button.png', border_width=0,
                                 button_color=sg.theme_background_color(), key='sair', use_ttk_buttons=True)])
        layout.append([sg.T(' Menu Relatórios', text_color='white'), sg.T(size=24),
                       sg.T('Menu Cliente', text_color='white'), sg.T(size=28),
                       sg.T('Add Usuário', text_color='white'),
                       sg.T(size=30), sg.T('Sair', text_color='white')])
    else:
        layout.append([sg.Button(key='relatorio', image_filename='Images/relatorio_button.png', border_width=0,
                                 button_color=sg.theme_background_color(), use_ttk_buttons=True, disabled=True),
                       sg.Text('', size=42),
                       sg.Button('', image_filename='Images/cadastro_button.png', border_width=0,
                                 button_color=(sg.theme_background_color()), key='cadastro', use_ttk_buttons=True,
                                 tooltip='Menu Clientes'),
                       sg.Text('', size=42),
                       sg.Button('', image_filename='Images/sair_button.png', border_width=0,
                                 button_color=sg.theme_background_color(), key='sair', use_ttk_buttons=True)])

        layout.append([sg.T(' Menu Relatórios', text_color='white'), sg.T(size=44),
                       sg.T('Menu Clientes', text_color='white'),
                       sg.T(size=49), sg.T('Sair', text_color='white')])
    janela = sg.Window('Inicio', layout, no_titlebar=True, grab_anywhere=True)
    button, values = janela.Read()
    janela.close()
    return button


def menucad(acesso):
    """
    Gera a janela com opções de cadastro
    :return: o botão escolhido
    """
    if acesso:
        layout = [
            [sg.Image('Images/clientes.png')],
            [sg.Button('', key='serviço', border_width=0,
                       image_filename='Images/servico.png', button_color=sg.theme_background_color(), use_ttk_buttons=True),
             sg.T(''), sg.Button('', key='Cad Cliente', border_width=0, image_filename='Images/cadastro.png',
                                 button_color=sg.theme_background_color(), use_ttk_buttons=True),
             sg.Button(key='Ver Dados de Clientes', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/dados_cliente.png', use_ttk_buttons=True),
             sg.T(''),
             sg.Button(key='Editar um Cliente', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/editar_dados.png', use_ttk_buttons=True),
             sg.T(''),
             sg.Button(key='baixa', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/baixa_button.png', use_ttk_buttons=True),
             sg.Button(key='Excluir', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/excluir_cliente.png', use_ttk_buttons=True),
             sg.Button(key='Lista de Clientes', border_width=0, image_filename='Images/clientes_button.png',
                       button_color=sg.theme_background_color(), use_ttk_buttons=True),
             sg.Button(key='Voltar', button_color=sg.theme_background_color(),
                       image_filename='Images/sair_button.png', border_width=0, use_ttk_buttons=True)],
            [sg.T('Cadastrar Serviço', text_color='white'), sg.T(''), sg.T('Cadastrar Cliente', text_color='white'),
             sg.T(''), sg.T('Detalhar Cliente', text_color='white'), sg.T(size=2),
             sg.T('Editar Cliente', text_color='white'), sg.T(size=5),
             sg.T('Pagamento', text_color='white'), sg.T(size=1), sg.T('Excluir Cliente', text_color='white'),
             sg.T(size=1), sg.T('Listar Clientes', text_color='white'), sg.T(size=4), sg.T('Voltar', text_color='white')]
        ]
    else:
        layout = [
            [sg.Image('Images/clientes.png')],
            [sg.Button('', key='serviço', border_width=0,
                       image_filename='Images/servico.png', button_color=sg.theme_background_color(),
                       use_ttk_buttons=True),
             sg.T(''), sg.Button('', key='Cad Cliente', border_width=0, image_filename='Images/cadastro.png',
                                 button_color=sg.theme_background_color(), use_ttk_buttons=True),
             sg.Button(key='Ver Dados de Clientes', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/dados_cliente.png', use_ttk_buttons=True, disabled=True),
             sg.T(''),
             sg.Button(key='Editar um Cliente', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/editar_dados.png', use_ttk_buttons=True),
             sg.T(''),
             sg.Button(key='baixa', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/baixa_button.png', use_ttk_buttons=True, disabled=True),
             sg.Button(key='Excluir', border_width=0, button_color=sg.theme_background_color(),
                       image_filename='Images/excluir_cliente.png', use_ttk_buttons=True),
             sg.Button(key='Lista de Clientes', border_width=0, image_filename='Images/clientes_button.png',
                       button_color=sg.theme_background_color(), use_ttk_buttons=True),
             sg.Button(key='Voltar', button_color=sg.theme_background_color(),
                       image_filename='Images/sair_button.png', border_width=0, use_ttk_buttons=True)],
            [sg.T('Cadastrar Serviço', text_color='white'), sg.T(''), sg.T('Cadastrar Cliente', text_color='white'),
             sg.T(''), sg.T('Detalhar Cliente', text_color='white'), sg.T(size=2),
             sg.T('Editar Cliente', text_color='white'), sg.T(size=5),
             sg.T('Pagamento', text_color='white'), sg.T(size=1), sg.T('Excluir Cliente', text_color='white'),
             sg.T(size=1), sg.T('Listar Clientes', text_color='white'), sg.T(size=4),
             sg.T('Voltar', text_color='white')]
        ]
    janela = sg.Window('Menu Cadastro', layout, no_titlebar=True, grab_anywhere=True)
    button, values = janela.Read()
    janela.close()
    return button
