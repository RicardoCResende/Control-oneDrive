from Conectar import conexao
import PySimpleGUI as sg

con, cursor = conexao()


def despesa():
    cursor.execute('select * from despesas')
    despesas = cursor.fetchall()
    layout = [[sg.T('Despesas Fixas', font=('times', 16))]]
    fr = []
    cursor.execute('select sum(valor) from despesas')
    soma = cursor.fetchone()
    soma = soma[0]
    try:
        for c in despesas:
            fr.append([sg.T(f"{c[1]}: R${c[2]:.2f}", font=('times', 15))])
        layout.append([sg.Frame('', fr, border_width=2)])
        layout.append([sg.T(f'Total de Despesas: R$ {soma:.2f}', font=('times', 17))])
        layout.append([sg.B('Editar', border_width=5), sg.T(size=20), sg.B('Voltar', border_width=5)])

    except:
        layout.append([sg.Frame('', [[sg.T('Não Há Despesas Cadastradas!', font=('times', 15))]])])
        layout.append([sg.B('Editar', border_width=5), sg.T(size=20), sg.B('Voltar', border_width=5)])

    finally:
        janela = sg.Window('', layout, no_titlebar=True, grab_anywhere=True)
        button, values = janela.Read()
        janela.close()

    if button == 'Editar':
        layout = [
            [sg.Image('Images/despesa.png')],
            [sg.B('Editar Item', image_filename='Images/editar_despesa.png',
                  button_color=sg.theme_background_color(), use_ttk_buttons=True), sg.T(size=15),
             sg.B('Add Item', image_filename='Images/add_despesas.png', button_color=sg.theme_background_color(),
                  use_ttk_buttons=True), sg.T(size=15),
             sg.B('Excluir Item', image_filename='Images/excluir_despesa.png', button_color=sg.theme_background_color(),
                  use_ttk_buttons=True), sg.T(size=15),
             sg.B('Voltar', image_filename='Images/sair_button.png', button_color=sg.theme_background_color(),
                  use_ttk_buttons=True)],
            [sg.T('        Editar', size=32), sg.T('Adicionar', size=32), sg.T('Excluir', size=30), sg.T('Voltar')]
        ]
        janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
        button, values = janela.Read()
        janela.close()

        if button == 'Add Item':
            layout = [
                [sg.Image('Images/conta.png')],
                [sg.Text('Nome da Despesa:'), sg.Input('', key='nome')],
                [sg.T('Valor da Despesa: R$'), sg.Input('', key='valor')],
                [sg.B('Confirmar', border_width=5), sg.B('Cancelar', border_width=5)]
            ]

            janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
            button, values = janela.Read()
            janela.close()

            if button == 'Confirmar':
                cursor.execute(f'insert into despesas(item, valor) values("{values["nome"]}", "{values["valor"]}")')
                con.commit()

        elif button == 'Excluir Item':
            cursor.execute('select item from despesas')
            despesas = cursor.fetchall()
            layout = [
                [sg.Text('Selecione a Despesa a Ser Excluida:'),
                 sg.Combo(despesas, font=('times', 13), tooltip='Selecione a despesa', key='despesa')],
                [sg.Checkbox('Excluir Todas', key='todas', font=('times', 13))],
                [sg.B('Confirmar', border_width=5, size=(23, 2)), sg.B('Cancelar', border_width=5, size=(23, 2))]
            ]

            janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
            button, values = janela.Read()
            janela.close()

            if button == 'Confirmar':
                if values['todas']:
                    layout = [[sg.T('Deseja Realmente Apagar Todas as Despesas?', font=('tomes', 15))],
                              [sg.B('Sim', size=(25, 2), border_width=5), sg.B("Não", size=(25, 2), border_width=5)]]
                    janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
                    button, values = janela.Read()
                    janela.close()
                    if button == 'Sim':
                        cursor.execute('delete from despesas')
                        print(button)
                        # con.commit()
                else:
                    cursor.execute(f'delete from despesas where item = "{values["despesa"][0]}"')
                    # con.commit()

        elif button == "Editar Item":
            cursor.execute('select item from despesas')
            despesas = cursor.fetchall()
            layout = [
                [sg.T('Selecione o Item Que Deseja Alterar', font=('times', 14))],
                [sg.LBox(despesas, size=(25, 10), font=('times', 17))],
                [sg.B('Confirmar', size=(25, 2), border_width=5), sg.B('Cancelar', size=(25, 2), border_width=5)]
            ]

            janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
            button, vallues = janela.Read()
            janela.close()
