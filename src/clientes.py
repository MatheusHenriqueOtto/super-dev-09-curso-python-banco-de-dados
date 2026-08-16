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


def validar_tamanho_str(tamanho: int, mensagem: str) -> str:
    resposta = input(mensagem).strip()
    while len(resposta) > tamanho or len(resposta) < 3:
        print(f"A resposta tem que ter no maximo {tamanho} caracteres e no minimo 3")
        resposta = input(mensagem).strip()

    return resposta



