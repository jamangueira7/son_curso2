import os
import ast


# dependência circular
# from cash_machine import BankAccount


class ArquivoBanco:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self._arquivo = None

    def _abrir_arquivo_banco(self, tipo):  # convenção - protegido
        return open(ArquivoBanco.BASE_PATH + '/_arquivo_banco.dat', tipo)

    def _ler_linhas(self):
        self._arquivo = self._abrir_arquivo_banco('r')
        linhas = self._arquivo.readlines()
        self._arquivo.close()
        return linhas

    def _escrever_linhas(self, linhas):
        self._arquivo = self._abrir_arquivo_banco('w')
        self._arquivo.writelines(linhas)
        self._arquivo.close()


class LerArquivoBanco(ArquivoBanco):

    def obter_indice_linha_conta_bancaria(self, numero_conta):
        linhas = self._ler_linhas()
        linhas = self.__pular_primeira_linha(linhas)
        linha_index = -1
        for index, linha in enumerate(linhas):
            conta_criada = self.__criar_conta_para_linha_arquivo(linha)
            if conta_criada.checar_numero_conta(numero_conta):
                line_index = index
                break
        return linha_index + 1

    def obter_conta(self, numero_conta):
        linhas = self._ler_linhas()
        linhas = self.__pular_primeira_linha(linhas)
        conta = None
        for linha in linhas:
            conta_criada = self.__criar_conta_para_linha_arquivo(linha)
            if conta_criada.checar_numero_conta(numero_conta):
                conta = conta_criada
                break
        return conta

    def __criar_conta_para_linha_arquivo(self, linha):
        conta_arquivo = linha.split(';')
        from caixa_eletronico import ContaBanco
        return ContaBanco(
            conta_arquivo[0],
            conta_arquivo[1],
            conta_arquivo[2],
            float(conta_arquivo[3]),
            ast.literal_eval(conta_arquivo[4])
        )

    def __pular_primeira_linha(self, linhas):
        return linhas[1:len(linhas)]


class EscreverArquivoBanco(ArquivoBanco):

    def escrever_conta_banco(self, conta):
        linha_para_alterar = LerArquivoBanco().obter_indice_linha_conta_bancaria(conta.numero_conta)
        linhas = self._ler_linhas()
        linhas[linha_para_alterar] = self.__formatar_linha_para_escever(conta)
        self._escrever_linhas(linhas)

    def __formatar_linha_para_escever(self, conta):
        linha = "%s;%s;%s;%s;%s;" % (
            conta.numero_conta,
            conta.nome,
            conta.senha,
            str(conta.valor),
            str(conta.admin)
        )
        return linha + '\n'


class ArquivoCombinarDinheiro(ArquivoBanco):
    DINHEIRO_LINHA = 0


class LerArquivoCombinarDinheiro(ArquivoCombinarDinheiro):

    def __init__(self):
        super().__init__()
        self.__dinheiro = {}

    def obter_dinheiro_combinado(self):
        self._arquivo = self._abrir_arquivo_banco('r')
        linha_para_ler = ArquivoCombinarDinheiro.DINHEIRO_LINHA
        linha = self._arquivo.readlines(linha_para_ler)[0]
        while self.__tem_ponto_e_virgula(linha):
            ponto_virgula_pos = linha.find(';')
            valor_dinheiro = linha[0:ponto_virgula_pos]
            self.__add_dinheiro_combinado_para_linha_arquivo(valor_dinheiro)
            # 20=5000;50=5000
            if self.__tem_dinheiro_para_ler(ponto_virgula_pos, linha):
                break
            else:
                linha = linha[ponto_virgula_pos + 1:len(linha)]
        return self.__dinheiro

    def __tem_dinheiro_para_ler(self, ponto_virgula_pos, linha):
        return ponto_virgula_pos + 1 == len(linha)

    def __tem_ponto_e_virgula(self, linha):
        return linha.find(';') != -1

    def __add_dinheiro_combinado_para_linha_arquivo(self, valor_dinheiro):
        igual_pos = valor_dinheiro.find('=')  # 20=5000
        dinheiro = valor_dinheiro[0:igual_pos]
        count_valor_dinheiro = len(valor_dinheiro)
        valor = valor_dinheiro[igual_pos + 1:count_valor_dinheiro]
        self.__dinheiro[dinheiro] = int(valor)


class EscreverDinheiroNoArquivo(ArquivoCombinarDinheiro):

    def escrever_dinheiro_combinado(self, dinheiros):
        linhas = self._ler_linhas()
        linha_para_escrever = ArquivoCombinarDinheiro.DINHEIRO_LINHA
        linhas[linha_para_escrever] = self.__formatar_linha_para_escrever(dinheiros)
        self._escrever_linhas(linhas)

    def __formatar_linha_para_escrever(self, dinheiros):
        linha = ""
        for dinheiro, valor in dinheiros.items():
            linha += dinheiro + '=' + str(valor) + ';'
        return linha + '\n'