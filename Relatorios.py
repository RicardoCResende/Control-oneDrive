import datetime
from Conectar import conexao
import PySimpleGUI as sg
import Despesas
from Mes import troca_mes
from Contratos import contract

con, cursor = conexao()


def devedores():
    cursor.execute(f'select c.nome, s.tipo, f.vencimento, s.valor_restante / s.num_parcelas from fatura f '
                   f'join clientes c '
                   f'join servico s where c.id = f.id_cliente and s.num_parcelas > 1 '
                   f'and s.id = f.id_servico and f.vencimento < "{datetime.date.today()}"')
    dev = cursor.fetchall()
    return dev


def relatorio_simples():
    cursor.execute('select sum(valor_restante), count(valor_restante) from servico')
    dados1 = cursor.fetchall()
    dados1 = dados1[0]

    cursor.execute('select vencimento, num_parcelas, valor_restante, id from servico')
    ven = cursor.fetchall()

    cursor.execute('select servico_id, data from pagamentos')
    pago = cursor.fetchall()

    dev = devedores()
    cursor.execute('select * from despesas')
    despesas = cursor.fetchall()
    desp = []

    cursor.execute('select sum(valor) from despesas')
    soma = cursor.fetchone()
    soma = soma[0]

    for c in despesas:
        desp.append((c[1], c[2]))
    despesas = []

    for c in desp:
        despesas.append([sg.T(f'{c[0]}: R$ {float(c[1]):.2f}', font=('times', 15))])
    mensal = []
    soma_mensal = 0
    nomes = []
    for i, c in enumerate(dev):
        mensal.append([])
        if c[0] not in nomes:
            nomes.append(c[0])
            mensal[i].append([sg.Frame(f'{c[0]}',
                                       [[sg.T(f"Serviço: {c[1]}\nVencimento: {c[2]}\nValor: "
                                              f"R${c[3]:.2f}", font=('times', 15))]])])
        else:
            mensal[i - 1].append([sg.Frame(f'{c[0]}',
                                           [[sg.T(f"Serviço: {c[1]}\nVencimento: {c[2]}\nValor: "
                                                  f"R${c[3]:.2f}", font=('times', 15))]])])
        soma_mensal += float(c[3])
    try:
        cursor.execute(f'select sum(valor) from pagamentos where month(data) = "{datetime.date.today().month}"')
        soma_pagamentos = cursor.fetchone()
        soma_mensal1 = soma_mensal
        soma_mensal1 += soma_pagamentos[0]
        saldo = [
            [sg.T(f'Receita Mensal ..... R$ {soma_mensal1:.2f}', font=('times', 15))],
            [sg.T(f'Despesa Mensal ..... R$ {soma:.2f}', font=('times', 15))],
            [sg.T(f'Saldo Líquido  ..... R$ {(soma_mensal1 - soma):.2f}', font=('times', 15))]
        ]
    except:
        saldo = [[sg.T('Não Há Receita ou Despesa Cadastrada Para uma Correta Exibição!', font=('times', 15))]]
    mensal_simples = [[sg.T(f'Parcelas em Atraso: {len(dev)}', font=('times', 15))],
                      [sg.T(f'Montante Devedor R${soma_mensal:.2f}', font=('times', 15))]]
    total = [[sg.T('Total a Receber de Todos Serviços:', font=('times', 15))],
             [sg.T(f'R${dados1[0]} de {dados1[1]} serviços.',
                   font=('times', 14))]]
    layout = [[sg.Image('Images/receita1.png')],
              [sg.T('Relátorio Simplificado de Receitas e Despesas', font=('times', 15))],
              [sg.Frame('Receita Total', total, border_width=5), sg.T(size=5),
               sg.Frame('Receita Mensal', mensal_simples, border_width=5)],
              [sg.Frame('Despesa Total', despesas, border_width=5), sg.T(size=5),
               sg.Frame('Saldo Líquido', saldo, border_width=5)],
              [sg.B('Sair', border_width=5),
               sg.B('Pagamentos Atrasados', tooltip='detalhes de atrasados', border_width=5)]
              ]

    janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
    button, values = janela.Read()
    janela.close()

    if button == 'Pagamentos Atrasados':
        i = 0
        tabela = []
        for c in mensal:
            if c:
                i += 1
                tabela.append(sg.Tab(f'Cliente {i}', c))

        layout = [
            [sg.Image('Images/receita.png')],
            [sg.TabGroup([tabela])],
            [sg.B('Voltar', border_width=5)]
        ]
        janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
        button, values = janela.Read()
    janela.close()


def relatorio_detalhado():
    # buscar as parcelas do mes atual
    cursor.execute(
        f'select c.nome, s.tipo, s.valor_restante / s.num_parcelas, f.vencimento from fatura f '
        f'join clientes c join servico s where c.id = f.id_cliente and s.id = f.id_servico '
        f'and year(f.vencimento) = "{datetime.date.today().year}" '
        f'and (month(f.vencimento) = "{datetime.date.today().month}" or f.vencimento < "{datetime.date.today()}")'
    )
    faturas = cursor.fetchall()
    # Pegando a soma de todas as faturas
    cursor.execute(
        f'select sum(s.valor_restante / s.num_parcelas) from fatura f '
        f'join clientes c join servico s where c.id = f.id_cliente and s.id = f.id_servico '
        f'and year(f.vencimento) = "{datetime.date.today().year}" '
        f'and (month(f.vencimento) = "{datetime.date.today().month}" or f.vencimento < "{datetime.date.today()}")'
    )
    soma_mes = cursor.fetchone()
    mes = datetime.date.today().month
    mes = troca_mes(mes)
    cursor.execute('select * from despesas')
    despesas = cursor.fetchall()
    tx2 = []
    cursor.execute('select sum(valor) from despesas')
    soma = cursor.fetchone()
    soma = soma[0]
    try:
        for c in despesas:
            tx2.append([sg.T(f"{c[1]}: R${c[2]:.2f}")])
        tx2.append([sg.T(f'Total de Despesas: R$ {soma:.2f}', font=('times', 15))])

    except:
        tx2.append([sg.Frame('', [[sg.T('Não Há Despesas Cadastradas!', font=('times', 15))]])])

    tx = []
    tx1 = []
    for c in faturas:
        tx.append(
            [sg.T(f'Cliente: {c[0]}\n'
                  f'Serviço: {c[1]}\n'
                  f'Valor: R$ {float(c[2]):.2f}\n'
                  f'Vencimento: {format(c[3], "%d/%m/%Y")}\n')]
        )
    dev = devedores()

    for c in dev:
        tx1.append(
            [sg.T(f'Cliente: {c[0]}\n'
                  f'Serviço: {c[1]}\n'
                  f'Valor: R$ {float(c[3]):.2f}\n'
                  f'Vencimento: {format(c[2], "%d/%m/%Y")}\n')]
        )
    try:
        tx.append([sg.T(f'Total a Receber: R$ {float(soma_mes[0]):.2f}', font=('times', 14))])
    except:
        tx.append([sg.Frame('', [[sg.T('Não Há Receitas Cadastradas!', font=('times', 15))]])])

    # Contratos
    cursor.execute('select s.tipo, s.valor_total, s.valor_restante, s.data, c.nome from servico s '
                   'join clientes c on s.id_cliente = c.id')
    servicos = cursor.fetchall()
    coluna1 = []
    coluna2 = []
    coluna3 = []
    coluna4 = []
    total_contratos = 0
    cont = 0
    servicos1 = []
    for c in servicos:
        if float(c[2]) > 0:
            servicos1.append(c)
    for c in servicos1:
        contrato = [sg.T(f'Cliente: {c[4]}\n'
                         f'Serviço: {c[0]}\n'
                         f'Valor do Contrato: R$ {float(c[1]):.2f}\n'
                         f'Valor Restante: R$ {float(c[2]):.2f}\n'
                         f'Data do Contrato: {format(c[3], "%d/%m/%Y")}\n')]
        total_contratos += float(c[2])
        if cont < 4:
            coluna1.append(contrato)
        elif 4 <= cont < 8:
            coluna2.append(contrato)
        elif 8 <= cont < 12:
            coluna3.append(contrato)
        elif cont >= 12:
            coluna4.append(contrato)
        cont += 1
    tx3 = [[sg.Column(coluna1), sg.Column(coluna2), sg.Column(coluna3), sg.Column(coluna4)],
           [sg.T(f'Valor Total Restante a Receber: R$ {total_contratos:.2f}', font=('times', 14))]]

    # Grafico
    cursor.execute('select sum(valor), month(data) from pagamentos group by month(data)')
    montantes = cursor.fetchall()
    coluna1 = []
    coluna2 = []
    cont = 0
    for c in montantes:
        if cont < 6:
            coluna1.append([sg.T(f'{troca_mes(c[1])}', size=10),
                            sg.I(size=int(c[0] / 300), background_color='blue', border_width=-5),
                            sg.T(f'R${float(c[0]):.2f}', font=('times', 7))])
        else:
            coluna2.append([sg.T(f'{troca_mes(c[1])}', size=10),
                            sg.I(size=int(c[0] / 300), background_color='blue', border_width=-5),
                            sg.T(f'R${float(c[0]):.2f}', font=('times', 7))])
        cont += 1
    grafico = [[sg.Column(coluna1), sg.Column(coluna2)]]

    layout = [
        [sg.Frame(f'Parcelas a Receber em {mes}', tx, border_width=8),
         sg.T(size=5), sg.VSeparator(), sg.T(size=5),
         sg.Frame(f'Pagamentos em Atraso', tx1, title_color='red', border_width=8),
         sg.T(size=5), sg.VSeparator(), sg.T(size=5),
         sg.Frame('Contratos Ativos', tx3, border_width=8)],
        [sg.Frame('Despesas Fixas', tx2, border_width=8), sg.T(size=10),
         sg.Fr('Receita Anual', grafico, border_width=8)],
        [sg.Button('Sair', size=(20, 2), border_width=5)]
    ]

    janela = sg.Window('', layout, grab_anywhere=True, no_titlebar=True)
    button, values = janela.Read()
    janela.close()


class Relatorio:
    def __init__(self):
        layout = [
            [sg.Image('Images/relatorio.png')],
            [sg.Button(key='Relatório Simplificado', border_width=0, image_filename='Images/relatorio_sim_botao.png',
                       button_color=sg.theme_background_color(), use_ttk_buttons=True), sg.T(size=4),
             sg.Button(key='Relatório Detalhado', border_width=0, image_filename='Images/relatorio_deta_botao.png',
                       button_color=sg.theme_background_color(), use_ttk_buttons=True), sg.T(size=4),
             sg.B(key='contratos', border_width=0, button_color=sg.theme_background_color(), use_ttk_buttons=True,
                  image_filename='Images/contrato.png'), sg.T(size=4),
             sg.B(key='Relatório Despesas', border_width=0, use_ttk_buttons=True,
                  button_color=sg.theme_background_color(), image_filename='Images/despesa_botao.png'), sg.T(size=4),
             sg.Button(key='Voltar', border_width=0, image_filename='Images/sair_button.png',
                       button_color=sg.theme_background_color(), use_ttk_buttons=True)],
            [sg.T('Relatório Simples', text_color='white'), sg.T(size=4), sg.T('Relatório Detalhado',
                                                                               text_color='white'), sg.T(size=5),
             sg.T('Contratos', text_color='white'), sg.T(size=11), sg.T('Despesas', text_color='white'), sg.T(size=12),
             sg.T('Voltar', text_color='white')]
        ]
        janela = sg.Window('Relátorios', layout, grab_anywhere=True, no_titlebar=True)
        button, values = janela.Read()
        janela.close()
        if button == 'Relatório Detalhado':
            relatorio_detalhado()
        elif button == 'Relatório Simplificado':
            relatorio_simples()
        elif button == 'Relatório Despesas':
            Despesas.despesa()
        elif button == 'contratos':
            contract()
