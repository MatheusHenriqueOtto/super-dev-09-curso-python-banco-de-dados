from mysql import connector
 
HOST = "127.0.0.1"
PORTA = 3306
USUARIO = "root"
SENHA = "admin"
BANCO = "restau_calabresa"
 
def conectar():
    conexao = connector.connect(
        host=HOST,
        port=PORTA,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
    )
    return conexao
 
def cadastrar():
    print("\n---- CADASTRAR MESA ----")
    numero = input("Número (ex: 001): ").zfill(3)
    lugares = int(input("Lugares: "))
 
    conexao = conectar()
    cursor = conexao.cursor()
 
    cursor.execute(
        "INSERT INTO mesas (numero, lugares) VALUES (%s, %s)",
        (numero, lugares)
    )
 
    conexao.commit()
    print(f"\n[OK] Mesa cadastrada com ID: {cursor.lastrowid}")
 
    cursor.close()
    conexao.close()
 
def listar_mesas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT
    id, numero, lugares
    FROM mesas
    ORDER BY numero ASC
    """)
    mesas = cursor.fetchall()
 
    cursor.close()
    conexao.close()
 
    if len(mesas) == 0:
        print("Nenhuma mesa encontrada")
        return
 
    print("-"*56)
    print(f"\n{'ID':<4} {'NÚMERO':<15} {'LUGARES':<20}")
    print("-"*56)
    for mesa in mesas:
        id = mesa[0]
        numero = mesa[1]
        lugares = mesa[2]
 
        print(f"{id:<4} {numero:<15} {lugares:<20}")
    print("-"*56)
 
def excluir_mesa():
    listar_mesas()
 
    id_mesa = int(input("ID da mesa que você quer excluir: "))
 
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM mesas WHERE id = %s", (id_mesa,))
    conexao.commit()
 
    rowcount = cursor.rowcount
 
    cursor.close()
    conexao.close()
 
    if rowcount == 0:
        print("Mesa não encontrada com este id")
    else:
        print("Registro apagado com sucesso")
 
def alterar_mesa():
    listar_mesas()
 
    id_mesa = int(input("Id da mesa que você quer alterar: "))
    numero = input("Número (ex: 001): ").zfill(3)
    lugares = int(input("Lugares: "))
 
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE mesas SET numero = %s, lugares = %s WHERE id = %s",
        (numero, lugares, id_mesa),
    )
    conexao.commit()
 
    rowcount = cursor.rowcount
 
    cursor.close()
    conexao.close()
 
    if rowcount == 0:
        print("Mesa não encontrada com este id")
    else:
        print("Mesa alterada com sucesso")
 
def menu_mesa():
    mensagem = """MENU:
    1 - Listar
    2 - Cadastrar
    3 - Editar
    4 - Apagar
    5 - Voltar
    Digite a opção desejada: """
 
    opcao = int(input(mensagem))
 
    while opcao != 5:
        if opcao == 1:
            listar_mesas()
        elif opcao == 2:
            cadastrar()
        elif opcao == 3:
            alterar_mesa()
        elif opcao == 4:
            excluir_mesa()
        elif opcao != 5:
            print("Opção inválida")
        print("\n")
 
        opcao = int(input(mensagem))
 
menu_mesa()