import Cadastro as cd
import Menus as mn
import Receitas as rc
import Relatorios as rl
import Login

acesso = Login.logar()

while True:
    botao = mn.menu(acesso)
    if botao == 'relatorio':
        rl.Relatorio()
    elif botao == 'new_user':
        Login.add()
    elif botao == 'cadastro':
        try:
            botao_cad = mn.menucad(acesso)
        except:
            continue
        if botao_cad == 'Cad Cliente':
            try:
                cd.cadastro_cliente()
            except:
                continue
        elif botao_cad == 'serviço':
            try:
                cd.cadastro_servico()
            except:
                continue
        elif botao_cad == 'baixa':
            try:
                rc.baixa()
            except:
                continue
        elif botao_cad == 'Lista de Clientes':
            try:
                cd.ver_lista(acesso)
            except:
                continue
        elif botao_cad == 'Editar um Cliente':
            try:
                cd.editar_cliente()
            except:
                continue
        elif botao_cad == 'Excluir':
            try:
                cd.excluir_cliente()
            except:
                continue
        elif botao_cad == 'Ver Dados de Clientes':
            try:
                cd.ver_dados()
            except:
                continue
    elif botao == 'sair':

        break
