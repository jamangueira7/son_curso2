import os


def limpar():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def cabecalho():
    print("****************************************")
    print("*** School of Net - Caixa Eletrônico ***")
    print("****************************************")