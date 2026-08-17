from funcionarios_1_1_0 import menu_funcionario
from clientes import menu_cliente
from pratos_feitos import menu_prato_feito
from mesas import menu_mesa
from bebidas import menu_bebida
import os


def __main():
    os.system("cls" if os.name == "nt" else "clear")
    mensagem = """
=================================
MENU:
=================================

1 - Funcionarios
2 - Pratos feitos
3 - Clientes
4 - Bebidas
5 - Mesas
0 - Sair

Digite a opção desejada: """

    opcao = int(input(mensagem))

    while opcao != 0:
        os.system("cls")
        if opcao == 1:
            menu_funcionario()
        elif opcao == 2:
            menu_prato_feito()
        elif opcao == 3:
            menu_cliente()
        elif opcao == 4:
            menu_bebida()
        elif opcao == 5:
            menu_mesa()
        elif opcao != 10:
            print("Opção invalida")
        print("\n")

        opcao = int(input(mensagem))

    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    __main()