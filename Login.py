import PySimpleGUI as sg
from Conectar import conexao

con, cursor = conexao()

def logar():
    sg.theme('DarkBlue')
    acesso = False

    cursor.execute('select nome from login')
    login = cursor.fetchall()
    nomes = []
    cont = 0
    for c in login:
        nomes.append(c[0])
    layout = [
        [sg.Image('Images/login.png')],
        [sg.T('Usuário:'), sg.I('', key='login')],
        [sg.T('Senha:'), sg.I('', key='senha', password_char='*')],
        [sg.B('Entrar', size=(15, 2), border_width=5), sg.T('', size=27),
         sg.B('Cancelar', size=(15, 2), border_width=5)]
    ]

    janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
    while True:
        button, vallues = janela.Read()
        if button == 'Entrar':
            if cont > 2:
                break
            if vallues['login'] in nomes:
                cursor.execute(f'select senha from login where nome = "{vallues["login"]}"')
                senha = cursor.fetchone()
                try:
                    vallues['senha'] = int(vallues['senha'])
                except:
                    sg.popup('Somente Números', font=('times', 15))
                    continue
                if senha[0] == int(vallues['senha']):
                    acesso = True
                    break
                else:
                    sg.popup('Senha Inválida', font=('times', 15))
                    cont += 1
            else:
                sg.popup('Usuário não Cadastrado', font=('times', 15))
        elif button == 'Cancelar':
            break
    janela.close()
    return acesso


def add():
    layout = [
        [sg.T('Usuário:'), sg.I('', key='user')],
        [sg.T('Senha:'), sg.I('', key='senha1')],
        [sg.T('Confirme a Senha:'), sg.I('', key='senha2')],
        [sg.B('Confirmar', size=(15, 2), border_width=5), sg.T(size=20), sg.B('Cancelar', size=(15, 2), border_width=5)]
    ]
    janela = sg.Window('', layout, no_titlebar=True, grab_anywhere=True)
    while True:
        button, vallues = janela.Read()
        if button == 'Cancelar':
            break
        elif button == 'Confirmar':
            try:
                vallues['senha1'] = int(vallues['senha1'])
                vallues['senha2'] = int(vallues['senha2'])
                if vallues['senha1'] == vallues['senha2']:
                    cursor.execute(f'insert into login values("{vallues["user"]}", {vallues["senha1"]})')
                    con.commit()
                    break
                else:
                    sg.popup('A Confirmação de Senha está Diferente da Original', font=('times', 15))
            except:
                sg.popup('A Senha Deve Conter Apenas Números', font=('times', 15))

    janela.close()
