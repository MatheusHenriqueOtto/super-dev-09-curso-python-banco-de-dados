from binascii import Error
import os
from typing import cast

from mysql import connector

BANCO = "restau_cabresa"
SENHA = "admin"
PORTA = 3306
USUARIO = "root"
HOST = "127.0.0.1"

def conectar_banco():
    conexao = connector.connect(
        host=HOST,
        port=PORTA,
        password=SENHA,
        user=USUARIO,
        database=BANCO
    )
    return conexao

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def verificar_int(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def validar_tamanho_str(tamanho_maximo: int, mensagem: str, tamanho_minimo: int = 3) -> str:
    resposta = input(mensagem).strip()
    while len(resposta) > tamanho_maximo or len(resposta) < tamanho_minimo:
        print(f"A resposta tem que ter no maximo {tamanho_maximo} caracteres e no minimo {tamanho_minimo}")
        resposta = input(mensagem).strip()

    return resposta


def cadastrar():
    print("\n====== CADASTRAR CLIENTE ======")

    nome = validar_tamanho_str(255, "Nome: ")
    documento = validar_tamanho_str(18, "CPF: "tamanho_minimo=12)
    telefone = validar_tamanho_str(15, "Telefone: ", tamanho_minimo=11)

    conexao = None
    cursor = None

    try: 
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO clientes
        (nome, documento, telefone)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                nome,
                documento,
                telefone,
            ),
        )

        conexao.commit()

        print(f"\n[OK]Deu boa, o cliente foi criado com o ID: {cursor.lastrowid}")

    except Error as erro:
        print(f"\n[ERRO]Não deu boa, ao tentar cadastrar o cliente ocorreu {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def listar_clientes():
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
                documento,
                telefone
            FROM clientes
            ORDER BY nome ASC
            """
        )

        clientes = cast(
            list[
                tuple[
                    int,
                    str,
                    str,
                    str
                ]
            ],
            cursor.fetchall(),
        )

        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        print("-" * 100)
        print(
            f"{'ID':5}"
            f"{'NOME':<30}"
            f"{'DOCUMENTO':<20}"
            f"{'TELEFONE':<20}"
        )
        print("-" * 100)

        for cliente in clientes:

            id_cli = cliente[0]
            nome = cliente[1]
            documento = cliente[2]
            telefone = cliente[3]

            print(
                f"{id_cli:<5}"
                f"{nome:<30}"
                f"{documento:<20}"
                f"{telefone:<20}"
            )

        print("-" * 100)

    except Error as erro:
        print(f"\n[ERRO]Não de boa ao listar os clientes, ocorreu esse erro: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def execluir_cliente():
    listar_clientes()

    id_deletar = verificar_int(
        "\nDigite o ID do cliente a ser removido: "
    )

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM clientes WHERE id = %s",
            (id_deletar,),
        )
        if cursor.rowcount == 0:
            print("\nCliente não encontrado.")
        else:
            print("\nCliente removido com sucesso")

    except Error as erro:
        print("\n[Erro]Não deu boa ao tentar deletar um cliente, ocorreu o erro: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def alterar_cliente():
    listar_clientes()

    print("\n===== ALTERAR CLIENTE =====")

    id_alterar = verificar_int(
        "Digite o ID do funcionario: "
    )

    nome = validar_tamanho_str(255, "Nome: ")
    documento = validar_tamanho_str(18, "CPF: ", tamanho_minimo=12)
    telefone = validar_tamanho_str(15, "Telefone: ", tamanho_minimo=10)

    conexao = None
    cursor = None

    try: 
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
        UPDATE clientes
        SET
            nome = %s,
            documento = %s,
            telefone = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (
                nome,
                documento,
                telefone
            ),
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("\nCliente não encontrado.")
        else:
            print("\nCliente alterado com sucesso")

    except Error as erro:
        print("\n[Erro]Não deu boa ao tentar alterar um cliente, ocorreu o erro: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


    