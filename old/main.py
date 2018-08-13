from console import CaixaEletronicoConsole, AutenticarContaConsole
from utilitarios import clear, header


def main():
    clear()
    header()

    if AutenticarContaConsole.esta_autenticado():
        clear()
        header()

        CaixaEletronicoConsole.chamar_operacao()
    else:
        print('Conta inválida')


if __name__ == '__main__':
    while True:
        main()

        input('Pressione <ENTER> para continuar...')