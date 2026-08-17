from mysql.connector import Error
import os
from typing import cast
from mysql import connector

BANCO = "restau_calabresa"
USUARIO = "root"
SENHA = "admin"
PORTA = 3306
HOST = "127.0.0.1"


def conectar_banco():
    conexao = connector.connect(
        database=BANCO,
        user=USUARIO,
        password=SENHA,
        port=PORTA,
        host=HOST
    )
    return conexao


def limpar_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def verificar_int(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um numero inteiro valido!")


def validar_tamanho_str(
    tamanho_maximo: int,
    mensagem: str,
    tamanho_minimo: int = 3
) -> str:
    resposta = input(mensagem).strip()

    while (
        len(resposta) > tamanho_maximo
        or len(resposta) < tamanho_minimo
    ):
        print(
            f"A resposta tem que ter no maximo {tamanho_maximo} caracteres "
            f"e no minimo {tamanho_minimo}"
        )
        resposta = input(mensagem).strip()

    return resposta


def verificar_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um valor numérico válido.")


def formatar_custo(valor: float | None) -> str:
    if valor is None:
        return "-"
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def cadastrar():
    print("\n====== CADASTRAR PRATO FEITO ======")

    nome = validar_tamanho_str(255, "Nome: ")
    custo = verificar_float(
        "Digite o valor do prato: "
    )

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO pratos_feitos
        (nome, custo)
        VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (
                nome,
                custo,
            ),
        )

        conexao.commit()

        print(
            f"\n[OK]Deu boa, o prato feito foi criado com o ID: "
            f"{cursor.lastrowid}"
        )

    except Error as erro:
        print(
            f"\n[ERRO]Não deu boa, ao tentar cadastrar o prato feito "
            f"ocorreu {erro}"
        )

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def listar_pratos_feitos():
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nome,
                custo
            FROM pratos_feitos
            ORDER BY nome ASC
            """
        )

        pratos_feitos = cast(
            list[
                tuple[
                    int,
                    str,
                    float
                ]
            ],
            cursor.fetchall(),
        )

        if not pratos_feitos:
            print("\nNenhum prato feito cadastrado.")
            return

        print("-" * 100)
        print(
            f"{'ID':<5}"
            f"{'NOME':<50}"
            f"{'CUSTO':<10}"
        )
        print("-" * 100)

        for prato_feito in pratos_feitos:
            id_prato_feito = prato_feito[0]
            nome = prato_feito[1]
            custo = formatar_custo(prato_feito[2])

            print(
                f"{id_prato_feito:<5}"
                f"{nome:<50}"
                f"{custo:<10}"
            )

        print("-" * 100)

    except Error as erro:
        print(
            f"\n[ERRO]Não deu boa ao listar os pratos feitos, "
            f"ocorreu esse erro: {erro}"
        )

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def excluir_prato_feito():
    listar_pratos_feitos()

    id_deletar = verificar_int(
        "\nDigite o ID do prato feito a ser removido: "
    )

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM pratos_feitos WHERE id = %s",
            (id_deletar,),
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("\nPrato feito não encontrado.")
        else:
            print("\nPrato feito removido com sucesso")

    except Error as erro:
        print(
            f"\n[Erro]Não deu boa ao tentar deletar um prato feito, "
            f"ocorreu o erro: {erro}"
        )

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def alterar_prato_feito():
    listar_pratos_feitos()

    print("\n===== ALTERAR PRATO FEITO =====")

    id_alterar = verificar_int(
        "Digite o ID do prato feito: "
    )

    nome = validar_tamanho_str(255, "Nome: ")

    custo = verificar_float(
        "Digite o preço do prato feito: "
    )

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
        UPDATE pratos_feitos
        SET
            nome = %s,
            custo = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (
                nome,
                custo,
                id_alterar,
            ),
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("\nPrato feito não encontrado.")
        else:
            print("\nPrato alterado com sucesso")

    except Error as erro:
        print(
            f"\n[Erro]Não deu boa ao tentar alterar um prato feito, "
            f"ocorreu o erro: {erro}"
        )

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()



def menu_prato_feito():

    while True:

        print(
            """
==============================
 SISTEMA DE PRATOS FEITOS
==============================

1 - Listar Pratos feitos
2 - Cadastrar Prato feito
3 - Alterar Prato feito
4 - Excluir Prato feito
5 - Limpar Tela
0 - Sair

"""
        )

        opcao = verificar_int("Escolha uma opção: ")

        match opcao:
            case 1:
                listar_pratos_feitos()

            case 2:
                cadastrar()

            case 3:
                alterar_prato_feito()

            case 4:
                excluir_prato_feito()

            case 5:
                limpar_terminal()

            case 0:
                print("\nEncerrando sistema...")
                break

            case _:
                print("\nOpção inválida.")

        input("\nPressione ENTER para continuar...")
        limpar_terminal()

