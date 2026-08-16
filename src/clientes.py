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

