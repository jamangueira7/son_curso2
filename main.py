from console import CaixaEletronicoConsole, AutenticarContaConsole
from utilitarios import limpar, cabecalho


def main():
    limpar()
    cabecalho()

    if AutenticarContaConsole.esta_autenticado():
        limpar()
        cabecalho()

        CaixaEletronicoConsole.chamar_operacao()
    else:
        print('Conta inválida')


if __name__ == '__main__':
    while True:
        main()

        input('Pressione <ENTER> para continuar...')