import mysql.connector as my
import PySimpleGUI as sg


def conexao():
    """
    Cria uma conexão com o banco
    :return: retorna 'con' como conexão e 'cursor' como o ponteiro
    """
    con = my.connect(
            host='localhost',
            database='controldb',
            user='root',
            passwd='010203'
        )

    if con.is_connected():
        cursor = con.cursor()
        return con, cursor

    else:
        sg.theme('DarkBlue')
        layout = [
           [sg.Image()],
           [sg.T('Conexão com o Servidor Interrompida!', font=('times', 16))],
           [sg.B('Sair', size=15, border_width=5)]
        ]
        janela = sg.Window('', no_titlebar=True, grab_anywhere=True)
        button, values = janela.Read()
        janela.close()
