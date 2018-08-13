# 1 - saldo, 2 - saque, 10 - inserir cédulas
import getpass

from autenticacao import AutenticarContaBanco
from caixa_eletronico import CaixaEletronicoSacar, CaixaEletronicoDepositar


class AutenticarContaConsole:

    @staticmethod
    def esta_autenticado():
        numero_conta_digitada = input('Digite sua conta: ')
        senha_digitada = getpass.getpass('Digite sua senha: ')

        return AutenticarContaBanco.autenticacao(numero_conta_digitada, senha_digitada)


class CaixaEletronicoConsole:

    @staticmethod
    def chamar_operacao():
        option_typed = CaixaEletronicoConsole.__obter_operacoes_menu()
        CaixaEletronicoOperacao.fazer_operacao(option_typed)

    @staticmethod
    def __obter_operacoes_menu():
        print("%s - Saldo" % CaixaEletronicoOperacao.OPERACAO_MOSTRAR_SALDO)
        print("%s - Saque" % CaixaEletronicoOperacao.OPERACAO_SACAR)
        bank_account = AutenticarContaBanco.conta_banco_autenticada
        if bank_account.admin:
            print('%s - Inserir cédulas' % CaixaEletronicoOperacao.OPERACAO_INSERIR_DINHEIRO)
        return input('Escolha uma das opções acima: ')


class CaixaEletronicoOperacao:
    OPERACAO_MOSTRAR_SALDO = '1'
    OPERACAO_SACAR = '2'
    OPERACAO_INSERIR_DINHEIRO = '10'

    @staticmethod
    def fazer_operacao(opcao):
        bank_account = AutenticarContaBanco.conta_banco_autenticada
        if opcao == CaixaEletronicoOperacao.OPERACAO_MOSTRAR_SALDO:
            MostrarSaldoOperacao.fazer_operacao()
        elif opcao == CaixaEletronicoOperacao.OPERACAO_SACAR:
            SaqueOperacao.fazer_operacao()
        elif opcao == CaixaEletronicoOperacao.OPERACAO_INSERIR_DINHEIRO and bank_account.admin:
            InserirDinheiroOperacao.fazer_operacao()


class MostrarSaldoOperacao:

    @staticmethod
    def fazer_operacao():
        conta = AutenticarContaBanco.conta_banco_autenticada
        print('Seu saldo é %s' % conta.valor)


class SaqueOperacao:

    @staticmethod
    def fazer_operacao():
        valor_digitado = input('Digite o valor a ser sacado: ')
        valor_int = int(valor_digitado)
        conta = AutenticarContaBanco.conta_banco_autenticada
        caixa_eletronico = CaixaEletronicoSacar.sacar(conta, valor_int)
        if caixa_eletronico.valor_restante != 0:
            print('O caixa não tem cédulas disponíveis para este valor')
        else:
            print('Pegue as notas:')
            print(caixa_eletronico.valor_retirado_usuario)
            print(vars(conta))


class InserirDinheiroOperacao:

    @staticmethod
    def fazer_operacao():
        quantidade_digitado = input('Digite a quantidade de cédulas: ')
        dinheiro_digitado = input('Digite a cédula a ser incluída: ')

        caixa_eletronica = CaixaEletronicoDepositar.inserir_dinheiro_conta(dinheiro_digitado, int(quantidade_digitado))
        print(caixa_eletronica.valor_retirado)