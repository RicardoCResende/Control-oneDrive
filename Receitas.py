import PySimpleGUI as sg
import Cadastro as cd
from Conectar import conexao


con, cursor = conexao()


def baixa():
    #Da baixa em um pagamento, é possivel escolher o serviço
    cliente, servico, endereco = cd.carregar_cliente()
    servicos = []
    for c in servico:
        if float(c[5]) > 0:
            servicos.append(c[1])
    cursor.execute(f'select sum(valor_restante) from servico where id_cliente = {cliente[0]}')
    soma = cursor.fetchone()
    soma = soma[0]
    layout = [
        [sg.Image(fr'Images\dinheiro.png')],
        [sg.Text(f'Confirme o valor da baixa no pagamento de {cliente[1]}', font=('times', 15))],
        [sg.Text(f'O valor Total devido é de R${soma:.2f}')],
        [sg.Text('Selecione o Serviço'), sg.Combo(servicos, key='servico'), sg.Ok()],
        [sg.Text('Valor da parcela deste serviço:'), sg.Text(key='v_serv')],
        [sg.Text('R$', font=('times', 14)), sg.Input('', key='baixa')],
        [sg.Text('Data:', font=('times', 14)), sg.Input(key='data', size=(15, 1)),
         sg.CalendarButton('Selecione', close_when_date_chosen=True, target='data',
                           no_titlebar=False, format='%Y-%m-%d')],
        [sg.Button('Confirmar', size=30, border_width=5), sg.Text('', size=18),
         sg.Button('Cancelar', size=30, border_width=5)]]
    janela = sg.Window('Baixa de Pagamento', layout, grab_anywhere=True, no_titlebar=True)
    while True:
        button, values = janela.Read()
        cursor.execute(f'select valor_restante, num_parcelas, id from servico where tipo ='
                       f' "{values["servico"]}" and id_cliente = {cliente[0]}')
        info = cursor.fetchall()
        soma1 = info[0][0] / info[0][1]
        janela['v_serv'].update(f'R${soma1:.2f}')
        if button == 'Confirmar':
            cursor.execute(f'INSERT INTO `controldb`.`pagamentos` (`valor`, `cliente_id`, `servico_id`, `data`, '
                           f'parcela) '
                           f'VALUES ("{values["baixa"]}", "{cliente[0]}", "{info[0][2]}", "{values["data"]}",'
                           f'"{info[0][1]}")')
            con.commit()
            cursor.execute(f'update servico set valor_restante = "{float(info[0][0]) - float(values["baixa"])}",'
                           f' num_parcelas = "{int(info[0][1]) - 1}" '
                           f'where id = {info[0][2]}')
            con.commit()
            if float(values["baixa"]) == soma:
                cursor.execute(f'delete from fatura where id_cliente = "{cliente[0]}" and id_servico = "{info[0][2]}"')
                con.commit()
            else:
                cursor.execute(f'delete from fatura where id_cliente = "{cliente[0]}" and id_servico = "{info[0][2]}" '
                               f'and parcela = "{info[0][1]}"')
                con.commit()
            janela.close()
            break
        if button == 'Cancelar' or button == sg.WIN_CLOSED:
            janela.close()
            break
    cursor.close()
    con.close()


def carregar_pagamentos(id_cliente):
    """
    Recebe o parametro do id do cliente para retornar os dados de pagamentos
    :return: retorna uma lista com todos os dados do pagamento
    """
    cursor.execute(f"select valor, data, servico_id, parcela from pagamentos where cliente_id = {id_cliente}")
    pagamentos = cursor.fetchall()
    return pagamentos

