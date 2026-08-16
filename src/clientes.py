from binascii import Error
import os

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
    documento = validar_tamanho_str(18, "CPF: ")
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




