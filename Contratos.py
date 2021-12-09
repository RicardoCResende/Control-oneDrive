import PySimpleGUI as sg
from Conectar import conexao

con, cursor = conexao()


def contract():
    cursor.execute('select nome from clientes')
    clientes = cursor.fetchall()

    layout = [
        [sg.T('Selecione o Cliente que deseja visualizar os Contratos')],
        [sg.Combo(clientes, key='cliente'), sg.B('Confirmar', border_width=5)],
        [sg.Listbox((), size=(100, 10), font=('times', 15), key='lista'),
         sg.B('Confirmar', border_width=5, key='contrato')],
        [sg.Output(key='saida', size=(70, 20), font=('times', 18))],
        [sg.B('Sair', border_width=5, size=(15, 2))]
    ]

    janela = sg.Window('', layout, no_titlebar=True, grab_anywhere=True)
    while True:
        button, vallues = janela.Read()
        if button == 'Sair':
            janela.close()
            break
        try:
            cursor.execute(f'select s.tipo, c.nome, s.data, s.id from servico s join clientes c '
                           f'where s.id_cliente = c.id and c.nome = "{vallues["cliente"][0]}" order by s.data')
            contr = cursor.fetchall()
            contratos = []
        except:
            sg.popup("Selecione o Cliente!", font=('times', 15))
            continue
        for c in contr:
            contratos.append(f'{c[3]} - Serviço - {c[0]}, Cliente - {c[1]}, Data - {format(c[2], "%d/%m/%Y")}')
        if button == 'Confirmar':
            janela['lista'].update(contratos)
        if button == 'contrato':
            try:
                cursor.execute(f'select s.tipo, c.nome, s.data, s.valor_total, s.valor_entrada, s.valor_restante '
                               f'from servico s join clientes c where s.id = {vallues["lista"][0][:2]} and s.id_cliente = c.id')
                contrato = cursor.fetchall()
                janela['saida'].update('')
                cursor.execute(f'select valor, data, parcela from pagamentos where '
                               f'servico_id = {vallues["lista"][0][:2]} order by data')
                pag = cursor.fetchall()
                pagamentos = []
                if pag:
                    for c in pag:
                        pagamentos.append(f'Valor da Parcela >> R${c[0]} |  Data >> {format(c[1], "%d/%m/%Y")} |  '
                                          f'Parcela >> {c[2]}')
                teste = (f'Serviço >>>  {contrato[0][0]}\n'
                         f'Cliente >>>  {contrato[0][1]}\n'
                         f'Data do Contrato >>>  {format(contrato[0][2], "%d/%m/%Y")}\n'
                         f'Valor do Contrato >>>  R${float(contrato[0][3]):.2f}\n'
                         f'Valor da Entrada >>>  R${float(contrato[0][4]):.2f}\n'
                         f'Saldo Restante >>>  R${float(contrato[0][5]):.2f}\n'
                         f'Pagamentos:\n')
                print(teste)
                for c in pagamentos:
                    print(c)
            except:
                sg.popup('Selecione o Serviço!', font=('times', 15))
