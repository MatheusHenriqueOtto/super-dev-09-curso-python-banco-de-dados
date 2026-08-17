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
    print("\n---- CADASTRAR BEBIDA ----")
    nome = input("Nome: ")
    valor = float(input("Valor: ").replace(",", "."))
    tipo = input("Tipo: ")
 
    conexao = conectar()
    cursor = conexao.cursor()
 
    cursor.execute(
        "INSERT INTO bebidas (nome, valor, tipo) VALUES (%s, %s, %s)",
        (nome, valor, tipo)
    )
 
    conexao.commit()
    print(f"\n[OK] Bebida cadastrada com ID: {cursor.lastrowid}")
 
    cursor.close()
    conexao.close()
 
def listar_bebidas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT
    id, nome, valor, tipo
    FROM bebidas
    ORDER BY nome ASC
    """)
    bebidas = cursor.fetchall()
 
    cursor.close()
    conexao.close()
 
    if len(bebidas) == 0:
        print("Nenhuma bebida encontrada")
        return
 
    print("-"*76)
    print(f"\n{'ID':<4} {'NOME':<25} {'VALOR':<20} {'TIPO':<20}")
    print("-"*76)
    for bebida in bebidas:
        id = bebida[0]
        nome = bebida[1]
        valor = bebida[2]
        tipo = bebida[3]
 
        print(f"{id:<4} {nome:<25} {valor:<20} {tipo:<20}")
    print("-"*76)
 
def excluir_bebida():
    listar_bebidas()
 
    id_bebida = int(input("ID da bebida que você quer excluir: "))
 
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM bebidas WHERE id = %s", (id_bebida,))
    conexao.commit()
 
    rowcount = cursor.rowcount
 
    cursor.close()
    conexao.close()
 
    if rowcount == 0:
        print("Bebida não encontrada com este id")
    else:
        print("Registro apagado com sucesso")
 
def alterar_bebida():
    listar_bebidas()
 
    id_bebida = int(input("Id da bebida que você quer alterar: "))
    nome = input("Nome: ")
    valor = float(input("Valor: ").replace(",", "."))
    tipo = input("Tipo: ")
 
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE bebidas SET nome = %s, valor = %s, tipo = %s WHERE id = %s",
        (nome, valor, tipo, id_bebida),
    )
    conexao.commit()
 
    rowcount = cursor.rowcount
 
    cursor.close()
    conexao.close()
 
    if rowcount == 0:
        print("Bebida não encontrada com este id")
    else:
        print("Bebida alterada com sucesso")
 
def menu_bebida():
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
            listar_bebidas()
        elif opcao == 2:
            cadastrar()
        elif opcao == 3:
            alterar_bebida()
        elif opcao == 4:
            excluir_bebida()
        elif opcao != 5:
            print("Opção inválida")
        print("\n")
 
        opcao = int(input(mensagem))
 
