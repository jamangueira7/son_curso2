# 1 - saldo, 2 - saque, 10 - inserir cédulas
import getpass

from autenticacao import AutenticarContaBanco
from caixa_eletronico import CaixaEletronicoSacar, CaixaEletronicoDepositar


class AuthBankAccountConsole:

    @staticmethod
    def is_auth():
        account_number_typed = input('Digite sua conta: ')
        password_typed = getpass.getpass('Digite sua senha: ')

        return AutenticarContaBanco.autenticacao(account_number_typed, password_typed)


class CashMachineConsole:

    @staticmethod
    def call_operation():
        option_typed = CashMachineConsole.__get_menu_options_typed()
        CashMachineOperation.do_operation(option_typed)

    @staticmethod
    def __get_menu_options_typed():
        print("%s - Saldo" % CashMachineOperation.OPERATION_SHOW_BALANCE)
        print("%s - Saque" % CashMachineOperation.OPERATION_WITHDRAW)
        bank_account = AutenticarContaBanco.conta_banco_autenticada
        if bank_account.admin:
            print('%s - Inserir cédulas' % CashMachineOperation.OPERATION_INSERT_MONEY_BILL)
        return input('Escolha uma das opções acima: ')


class CashMachineOperation:
    OPERATION_SHOW_BALANCE = '1'
    OPERATION_WITHDRAW = '2'
    OPERATION_INSERT_MONEY_BILL = '10'

    @staticmethod
    def do_operation(option):
        bank_account = AutenticarContaBanco.conta_banco_autenticada
        if option == CashMachineOperation.OPERATION_SHOW_BALANCE:
            ShowBalanceOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_WITHDRAW:
            WithDrawOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_INSERT_MONEY_BILL and bank_account.admin:
            InsertMoneyBillOperation.do_operation()


class ShowBalanceOperation:

    @staticmethod
    def do_operation():
        bank_account = AutenticarContaBanco.conta_banco_autenticada
        print('Seu saldo é %s' % bank_account.value)


class WithDrawOperation:

    @staticmethod
    def do_operation():
        value_typed = input('Digite o valor a ser sacado: ')
        value_int = int(value_typed)
        bank_account = AutenticarContaBanco.conta_banco_autenticada
        cash_machine = CaixaEletronicoSacar.sacar(bank_account, value_int)
        if cash_machine.value_remaining != 0:
            print('O caixa não tem cédulas disponíveis para este valor')
        else:
            print('Pegue as notas:')
            print(cash_machine.money_slips_user)
            print(vars(bank_account))


class InsertMoneyBillOperation:

    @staticmethod
    def do_operation():
        amount_typed = input('Digite a quantidade de cédulas: ')
        money_bill_typed = input('Digite a cédula a ser incluída: ')

        cash_machine = CaixaEletronicoDepositar.insert_money_bill(money_bill_typed, int(amount_typed))
        print(cash_machine.money_slips)