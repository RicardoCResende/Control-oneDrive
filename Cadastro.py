import PySimpleGUI as sg
from Conectar import conexao
import Receitas as rc
from dateutil.relativedelta import relativedelta
import datetime as dt

con, cursor = conexao()


def cadastro_cliente():
    cursor.execute('select nome from estados;')
    linha = cursor.fetchall()
    layout = [
        [sg.Image('Images/cad.png')],
        [sg.Text('Nome'), sg.Input('', key='nome')],
        [sg.Text('RG'), sg.Input('', key='rg')],
        [sg.Text('CPF'), sg.Input('', key='cpf')],
        [sg.Text('Email'), sg.Input('', key='email')],
        [sg.Text('Estado'), sg.Combo(linha, key='estado'), sg.Button('confirmar', border_width=5)],
        [sg.Text('Cidade'), sg.Listbox((), key='cidade', size=(30, 4))],
        [sg.Text('Rua:'), sg.Input('', key='rua')],
        [sg.Text('Numero'), sg.Input('', key='numero')],
        [sg.Text('Complemento'), sg.Input('', key='complemento')],
        [sg.Text('Bairro'), sg.Input('', key='bairro')],
        [sg.Text('cep'), sg.Input('', key='cep')],
        [sg.Button('Enviar', size=15, border_width=5), sg.T(size=33), sg.B('Cancelar', size=15, border_width=5)]
    ]
    janela = sg.Window('Cadastro Cliente', layout, no_titlebar=True, grab_anywhere=True)
    while True:
        button, values3 = janela.Read()
        if button == 'Cancelar':
            janela.close()
            break
        cursor.execute(f'select id from estados where nome = "{values3["estado"][0]}"')
        id_estado = cursor.fetchall()
        id_estado = id_estado[0][0]
        cursor.execute(f'select nome from cidades where id_estado = {id_estado}')
        cidades = cursor.fetchall()
        janela['cidade'].update(cidades)
        if button == 'Enviar':
            cursor.execute(f"insert into clientes(nome, rg, cpf, email)"
                           f"values('{values3['nome']}', '{values3['rg']}', '{values3['cpf']}', '{values3['email']}')"
                           )
            con.commit()
            cursor.execute(f'select id from clientes where nome = "{values3["nome"]}"')
            id_c = cursor.fetchone()
            cursor.execute(f"insert into endereco(rua, numero, complemento, bairro, cidade, estado, cep, cliente) "
                           f"values('{values3['rua']}', '{values3['numero']}', '{values3['complemento']}', "
                           f"'{values3['bairro']}', "
                           f"'{values3['cidade'][0][0]}', '{values3['estado'][0]}', '{values3['cep']}', {id_c[0]})")
            con.commit()
            janela.close()
            break


def cadastro_servico():
    cursor.execute('select nome from clientes;')
    clientes = cursor.fetchall()
    sg.theme('DarkBlue')
    layout = [
        [sg.Image('Images/receitaanual.png')],
        [sg.Text('Serviço:', font=('times', 14)), sg.Input('', key='tipo')],
        [sg.Text('Valor Total R$', font=('times', 14)), sg.Input('', key='valor')],
        [sg.Text('Valor Entrada R$', font=('times', 14)), sg.Input('', key='entrada')],
        [sg.Text('N° de Parcelas:', font=('times', 14)), sg.Input('', key='parcelas')],
        [sg.Text('Dia de Vencimento da Parcela', font=('times', 14)), sg.Input('', key='vencimento', size=15)],
        [sg.Text('Data:', font=('times', 14)), sg.Input(key='data', size=(15, 1)),
         sg.CalendarButton('Selecione', close_when_date_chosen=True, target='data',
                           no_titlebar=False, format='%Y-%m-%d', border_width=5)],
        [sg.Text('Selecione o Cliente na Lista:', font=('times', 14))],
        [sg.Combo(clientes, key='cliente', size=(37, 4), font=('times', 12))],
        [sg.Button('Confirmar', size=20, border_width=5), sg.T(size=22), sg.B('Cancelar', size=20, border_width=5)]
    ]
    janela = sg.Window('Cadastro de Serviço', layout, no_titlebar=True, grab_anywhere=True)
    button, values = janela.Read()
    if button == 'Cancelar' or button == sg.WIN_CLOSED:
        janela.close()
    elif button == 'Confirmar':
        cursor.execute(f'select id from clientes where nome = "{values["cliente"][0]}"')
        id_c = cursor.fetchone()
        id_c = id_c[0]
        cursor.execute(
            f'insert into servico(tipo, valor_total, valor_entrada, num_parcelas, valor_restante, '
            f'data, id_cliente, vencimento)'
            f'values("{values["tipo"]}", "{values["valor"]}", "{values["entrada"]}", '
            f'"{values["parcelas"]}", "{float(values["valor"]) - float(values["entrada"])}", "{values["data"]}", '
            f'"{id_c}", "{values["vencimento"]}")'
        )
        con.commit()
        cursor.execute('select max(id) from servico')
        id_s = cursor.fetchone()
        data = dt.date.today()
        parcela = int(values['parcelas'])
        data = dt.date(year=int(values['data'][:4]), month=int(values['data'][5:7]), day=int(values['vencimento']))
        for c in range(0, int(values['parcelas'])):
            data += relativedelta(months=1)
            cursor.execute(f"insert into fatura(id_cliente, id_servico, vencimento, parcela)"
                           f"values('{id_c}', '{id_s[0]}', '{data}', '{parcela}')")
            parcela -= 1
            con.commit()
        cursor.execute(f'INSERT INTO `controldb`.`pagamentos` (`valor`, `cliente_id`, `servico_id`, `data`, '
                       f'parcela) '
                       f'VALUES ("{values["entrada"]}", "{id_c}", "{id_s[0]}", "{values["data"]}",'
                       f'"0")')
        con.commit()
        janela.close()


def carregar_cliente():
    """
    Carrega um cliente expecifico
    :return: um dicionario com os dados do cliente, outro com os dados dos serviços a ele atribuidos e
    um terceiro com o endereço
    """
    cursor.execute('select nome from clientes')
    lista = cursor.fetchall()
    layout = [
        [sg.Image('Images/lupa2.png')],
        [sg.Text('Selecione o Cliente na Lista', font=('times', 15))],
        [sg.Listbox(lista, size=(50, 5), key='cliente')],
        [sg.Button('Confirmar', border_width=5, size=20), sg.T(size=29), sg.B('Cancelar', border_width=5, size=20)]
    ]
    janela = sg.Window('Seleção de Cliente', layout, no_titlebar=True, grab_anywhere=True)
    button, values = janela.Read()
    if button == 'Cancelar':
        janela.close()
    elif button == 'Confirmar':
        cursor.execute(f'select * from clientes where nome = "{values["cliente"][0][0]}"')
        cliente = cursor.fetchall()
        cursor.execute(f'select * from servico where id_cliente = {cliente[0][0]} and num_parcelas > 0')
        servico = cursor.fetchall()
        cursor.execute(f"select * from endereco where cliente = {cliente[0][0]}")
        endereco = cursor.fetchall()
        janela.close()
        return cliente[0], servico, endereco


def editar_cliente():
    """
    Editar dados de clientes
    :return:
    """
    lay1 = []
    lay2 = []
    contador = 0
    serv = []
    cliente, servico, endereco = carregar_cliente()
    for c in servico:
        serv.append([c[0], c[1]])
    coluna1 = [
        [sg.Checkbox('Nome   ', key='nome'), sg.Checkbox('RG', key='rg')],
        [sg.Checkbox('CPF     ', key='cpf'), sg.Checkbox('Tel', key='tel')],
        [sg.Checkbox('E-Mail  ', key='email'), sg.Checkbox('Endereço', key='endereco')]
    ]
    coluna2 = [
        [sg.Checkbox('Tipo de Serviço  ', key='tipo'), sg.Checkbox('Valor Total', key='valor_total')],
        [sg.Checkbox('Valor da Entrada', key='valor_entrada'), sg.Checkbox('N° de Parcelas', key='num_parcelas')],
        [sg.Checkbox('Vencimento       ', key='vencimento'), sg.Checkbox('Data', key='data')]
    ]
    layout = [
        [sg.Image('Images/teste1.png')],
        [sg.Text('Selecione o item que deseja alterar', font=('times', 16))],
        [sg.T('')],
        [sg.T(size=1), sg.Frame('Dados Pessoais', coluna1, border_width=5), sg.T(size=9), sg.Frame('Dados de Serviços', coluna2, border_width=5)],
        [sg.T('')],
        [sg.B('Confirmar', border_width=5, size=20), sg.T(size=26), sg.B('Cancelar', border_width=5, size=20)]
    ]
    janela = sg.Window('', layout, no_titlebar=True, grab_anywhere=True)
    button, values = janela.Read()
    janela.close()
    layout1 = [
        [sg.T('Digite os Novos valores', font=('times', 16))],
        [sg.T('')]
    ]
    for c in values:
        if values[c]:
            if c == 'endereco':
                cursor.execute('select nome from estados;')
                linha = cursor.fetchall()
                fr = [
                    [sg.Text('Estado'), sg.Combo(linha, key='estado'), sg.Button('confirmar')],
                    [sg.Text('Cidade'), sg.Listbox((), key='cidade', size=(30, 4))],
                    [sg.Text('Rua:'), sg.Input('', key='rua')],
                    [sg.Text('Numero'), sg.Input('', key='numero')],
                    [sg.Text('Complemento'), sg.Input('', key='complemento')],
                    [sg.Text('Bairro'), sg.Input('', key='bairro')],
                    [sg.Text('cep'), sg.Input('', key='cep')]
                ]
                layout1.append([sg.Frame('Endereço', fr)])
            elif c == 'tipo' or c == 'valor_total' or c == 'valor_entrada' or c == 'num_parcelas' \
                    or c == 'data' or c == 'vencimento':
                if contador == 0:
                    contador += 1
                    cursor.execute(f"select tipo from servico where id_cliente = {cliente[0]}")
                    servico = cursor.fetchall()
                    lay2.append([sg.T('Selecione o Serviço:'), sg.Combo(servico, size=(37, 4), key='servico',
                                                                        font=('times', 12))])
                if c == 'data':
                    lay2.append([sg.T('Data do Serviço'), sg.Input(key='data'),
                                 sg.CalendarButton('Selecione', target='data',
                                                   close_when_date_chosen=True, format='20%y-%m-%d')])
                else:
                    lay2.append([sg.T(f'{c}:'), sg.Input('', key=c)])
            else:
                lay1.append([sg.T(f'{c}:'), sg.Input('', key=c)])
    layout1.append([sg.Frame('Pessoal', lay1)])
    layout1.append([sg.Frame('Serviço', lay2)])
    layout1.append([sg.T('')])
    layout1.append(
        [sg.B('Confirmar', size=20, border_width=5), sg.T(size=10), sg.B('Cancelar', size=20, border_width=5)])
    janela = sg.Window('', layout1, grab_anywhere=True, no_titlebar=True)
    while True:
        button, values3 = janela.Read()
        if button == 'Cancelar':
            janela.close()
            break
        if button == 'Confirmar':
            janela.close()
            for c in values3:
                if c == 'nome' or c == 'rg' or c == 'cpf' or c == 'tel' or c == 'email':
                    cursor.execute(f"update clientes set {c} = '{values3[c]}' where id = {cliente[0]}")
                    con.commit()
                if c == 'estado' or c == 'cidade' or c == 'rua' or c == 'numero' or c == 'complemento' \
                        or c == 'bairro' or c == 'cep':
                    if c == 'estado' or c == 'cidade':
                        cursor.execute(f"update endereco set {c} = '{values3[c][0]}' where cliente = {cliente[0]}")
                    else:
                        cursor.execute(f"update endereco set {c} = '{values3[c]}' where cliente = {cliente[0]}")
                    con.commit()
                if c == 'tipo' or c == 'valor_total' or c == 'valor_entrada' or c == 'num_parcelas' \
                        or c == 'data' or c == 'vencimento':
                    for a in serv:
                        for b in a:
                            if b == values3['servico'][0]:
                                id_serv = a[0]
                    cursor.execute(f"update servico set {c} = '{values3[c]}' where id = {id_serv}")
                    con.commit()
        cursor.execute(f'select id from estados where nome = "{values3["estado"][0]}"')
        id_estado = cursor.fetchall()
        id_estado = id_estado[0][0]
        cursor.execute(f'select nome from cidades where id_estado = {id_estado}')
        cidades = cursor.fetchall()
        janela['cidade'].update(cidades)


def excluir_cliente():
    """
    Exclui um cliente
    :return:
    """
    cliente, servico, endereco = carregar_cliente()
    layout = [
        [sg.Image('Images/del.png')],
        [sg.Text(f'Deseja Realmente Excluir {cliente[1]}?', font=('times', 18))],
        [sg.Button('Sim', size=(25, 2), border_width=5), sg.Text('', size=30),
         sg.Button('Não', size=(25, 2), border_width=5)]
    ]
    janela = sg.Window('Excluir', layout, no_titlebar=True, grab_anywhere=True)
    button, values = janela.Read()
    if button == 'Sim':
        try:
            cursor.execute(f"delete from servico where id_cliente = {cliente[0]}")
            cursor.execute(f"delete from endereco where cliente = {cliente[0]}")
            cursor.execute(f"delete from clientes where id = {cliente[0]}")
        except:
            sg.popup('É Impossivel Excluir Um Cliente Que Tem Faturas Em Aberto!', font=('times', 16))
        janela.close()
        con.commit()
    elif button == 'Não':
        janela.close()


def ver_dados():
    """
    Exibe todos os dados relacionados a um cliente
    :return:
    """
    cliente, servico, endereco = carregar_cliente()
    pagamento = rc.carregar_pagamentos(cliente[0])
    layout = [
        [sg.Text(f'Nome: {cliente[1]}', font=('times', 16))],
        [sg.Text(f'RG: {cliente[2]}', font=('times', 16))],
        [sg.Text(f'CPF: {cliente[3]}', font=('times', 16))],
        [sg.Text(f'Telefone: {cliente[4]}', font=('times', 16))],
        [sg.Text(f'E-Mail: {cliente[5]}', font=('times', 16))],
        [sg.Text(f'Endereço: {endereco[0][0]} {endereco[0][1]} {endereco[0][2]} {endereco[0][3]} {endereco[0][4]}',
                 font=('times', 16))]
    ]
    contra = []
    for i, c in enumerate(servico):
        contra.append(f'       - Tipo de Serviço: {servico[i][1]}')
        contra.append(f'       - Valor Total: R$ {servico[i][2]:.2f}')
        contra.append(f'       - Valor da Entrada: R$ {servico[i][3]:.2f}')
        contra.append(f'       - Valor Restante: R$ {servico[i][5]:.2f}')
        contra.append(f'       - Numero de Parcelas: {servico[i][4]}')
        contra.append(f'       - Valor das Parcelas: {(float(servico[i][5]) / int(servico[i][4])):.2f}')
        contra.append(f'       - Vencimento da Parcela: dia {servico[i][8]}')
        contra.append(f'       - Data do Serviço: {servico[i][6]}')
        contra.append('------------------------------------------------------------------')
    collumn1 = []
    for i, c in enumerate(pagamento):
        if c[3] == 0:
            continue
        cursor.execute(f"select tipo from servico where id = {c[2]}")
        tipo = cursor.fetchone()
        collumn1.append(f'       - Serviço: {tipo[0]}')
        collumn1.append(f'       - Valor do Pagamento: R$ {float(c[0]):.2f}')
        collumn1.append(f'       - Data do Pagamento: {c[1]}')
        collumn1.append(f'       - Número da Parcela: {c[3]}')
        collumn1.append('------------------------------------------------------------------')
    layout.append([sg.Frame('Serviços e Pagamentos', [[sg.Output(key='saida', size=(50, 30))]], border_width=5),
                   sg.B('Ver Serviços', key='serv', border_width=6),
                   sg.B('Ver Pagamentos', key='pag', border_width=6)])
    layout.append([sg.Button('Sair', size=15, border_width=5)])
    janela = sg.Window('dados do cliente', layout, no_titlebar=True, grab_anywhere=True)
    while True:
        button, values = janela.Read()
        if button == 'serv':
            janela['saida'].update('')
            for c in contra:
                print(c)
        elif button == 'pag':
            janela['saida'].update('')
            for c in collumn1:
                print(c)
        elif button == 'Sair':
            break
    janela.close()


def ver_lista(acesso):
    """
    Exibe uma lista com todos os clientes cadastrados
    :return:
    """
    cursor.execute('select id, nome from clientes')
    clientes = cursor.fetchall()
    layout = [[sg.Text('Clientes Cadastrados no Banco de Dados:', font=('times', 16))]]
    lista = []
    menu = ['', ['Editar', 'Detalhes']]
    for c in clientes:
        # a Key do buttonmenu recebe o id do cliente
        lista.append([sg.T(f'{c[1]}', font=('times', 14))])
    if acesso:
        layout.append([sg.Frame('', lista),
                       sg.ButtonMenu('...', menu, font=('times', 14), key='...', border_width=2, text_color='white')])
        layout.append([sg.B('Sair', border_width=5)])
        janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
        button, values = janela.Read()
        janela.close()
    else:
        layout.append([sg.Frame('', lista),
                       sg.ButtonMenu('...', menu, font=('times', 14), key='...', border_width=2,
                                     text_color='white', disabled=True)])
        layout.append([sg.B('Sair', border_width=5)])
        janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
        button, values = janela.Read()
        janela.close()
    if values['...'] == 'Editar':
        editar_cliente()
    elif values['...'] == 'Detalhes':
        ver_dados()
