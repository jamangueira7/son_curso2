from caixa_eletronico import lista_contas
from arquivo import LerArquivoBanco


class AutenticarContaBanco:
    conta_banco_autenticada = None

    @staticmethod
    def autenticacao(numero_conta, senha):
        conta_lida = LerArquivoBanco()
        conta_banco = conta_lida.obter_conta(numero_conta)
        if conta_banco and AutenticarContaBanco.__tem_conta_bancaria_valida(conta_banco, numero_conta, senha):
            AutenticarContaBanco.conta_banco_autenticada = conta_banco
            return conta_banco
        return False

    @staticmethod
    def __tem_conta_bancaria_valida(conta_banco, numero_conta, senha):
        return conta_banco.checar_numero_conta(numero_conta) and \
               conta_banco.chegar_senha(senha)