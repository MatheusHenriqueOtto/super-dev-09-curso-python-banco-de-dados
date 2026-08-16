from funcionario import menu_funcionario
import os


def __main():
    os.system("cls")
    mensagem = """MENU:
1 - Funcionarios
2 - Pratos feitos
3 - Clientes
4 - Bebidas
5 - Mesas
10 - Sair

Digite a opção desejada: """

    opcao = int(input(mensagem))

    while opcao != 10:
        os.system("cls")
        if opcao == 1:
            menu_funcionario()
        elif opcao != 10:
            print("Opção invalida")
        print("\n")

        opcao = int(input(mensagem))

    os.system("cls")

if __name__ == "__main__":
    __main()