from mysql import connector

BANCO = "restau_calabresa"
USUARIO = "root"
SENHA = "admin"
PORTA = 3306
HOST = "127.0.0.1"


def conectar():
    conexao = connector.connect(
        database=BANCO,
        user=USUARIO,
        password=SENHA,
        port=PORTA,
        host=HOST
    )
    return conexao
