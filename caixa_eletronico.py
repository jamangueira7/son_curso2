# dependência circular
# from file import MoneySlipsFileReader, MoneySlipsFileWriter
from arquivo import EscreverArquivoBanco


class ContaBanco:
    def __init__(self, numero_conta, nome, senha, valor, admin):
        self.numero_conta = numero_conta
        self.nome = nome
        self.senha = senha
        self.valor = valor
        self.admin = admin

    def checar_numero_conta(self, numero_conta):
        return numero_conta == self.numero_conta

    def chegar_senha(self, senha):
        return senha == self.senha

    def debitar_saldo(self, valor):
        self.valor -= valor


class CaixaEletronicoDepositar:

    @staticmethod
    def inserir_dinheiro_conta(valor_dinherio, valor):
        caixa_eletronico = CaixaEletronicoGetter().get()
        caixa_eletronico.valor_retirado[valor_dinherio] += valor
        from arquivo import EscreverDinheiroNoArquivo
        EscreverDinheiroNoArquivo().escrever_dinheiro_combinado(caixa_eletronico.valor_retirado)
        return caixa_eletronico


class CaixaEletronicoSacar:

    @staticmethod
    def sacar(conta_banco, valor):
        caixa_eletronico = CaixaEletronicoGetter().get()
        dinheiro_usuario = caixa_eletronico.sacar(valor)
        if dinheiro_usuario:
            CaixaEletronicoSacar.__debitar_saldo(conta_banco, valor)
            from arquivo import EscreverDinheiroNoArquivo
            EscreverDinheiroNoArquivo().escrever_dinheiro_combinado(caixa_eletronico.valor_retirado)
        return caixa_eletronico

    @staticmethod
    def __debitar_saldo(conta_banco, valor):
        conta_banco.debitar_saldo(valor)
        EscreverArquivoBanco().escrever_conta_banco(conta_banco)


class CaixaEletronicoGetter:  # design pattern - factory

    def get(self):
        from arquivo import LerArquivoCombinarDinheiro
        valor_retirado = LerArquivoCombinarDinheiro().obter_dinheiro_combinado()
        return CaixaEletronico(valor_retirado)


class CaixaEletronico:

    def __init__(self, valor_retirado):
        self.valor_retirado = valor_retirado
        self.valor_retirado_usuario = {}
        self.valor_restante = 0

    def sacar(self, valor):
        self.valor_restante = valor

        self.__calculate_valor_retirado_usuario('100')
        self.__calculate_valor_retirado_usuario('50')
        self.__calculate_valor_retirado_usuario('20')

        if self.valor_restante == 0:
            self.__decrease_valor_retirado()

        return False if self.valor_restante != 0 else self.valor_retirado

    def __calculate_valor_retirado_usuario(self, dinheiro_conta):
        dinheiro_conta_int = int(dinheiro_conta)
        if 0 < self.valor_restante // dinheiro_conta_int <= self.valor_retirado[dinheiro_conta]:
            self.valor_retirado_usuario[dinheiro_conta] = self.valor_restante // dinheiro_conta_int
            self.valor_restante = self.valor_restante - self.valor_restante // dinheiro_conta_int * dinheiro_conta_int

    def __decrease_valor_retirado(self):
        for dinheiro_conta in self.valor_retirado_usuario:
            self.valor_retirado[dinheiro_conta] -= self.valor_retirado_usuario[dinheiro_conta]


lista_contas = [
    ContaBanco('0001-02', 'Fulano da Silva', '123456', 100, False),
    ContaBanco('0002-02', 'Cicrano da Silva', '123456', 50, False),
    ContaBanco('1111-11', 'Admin da Silva', '123456', 1000, True),
]