from typing import cast
from mysql import connector
from datetime import date
import os
# pip install mysql-connector-python
# py -m pip install mysql-connector-python

HOST = "127.0.0.1"
PORTA = 3306
USUARIO = "root"
SENHA = "admin"
BANCO = "restau_calabresa"


def conectar():
    """Abre a conecão com o banco de dados"""
    conexao = connector.connect(
        host=HOST,
        port=PORTA,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
    )
    return conexao


def cadastrar():
    print("\n----- CADASTRAR FUNCIONARIO -----")
    nome = input("Nome: ")
    cargo = input("Cargo: ")
    salario = float(input("Sálario: ").replace(",", "."))
    data_nascimento = input("Data de nascimento: (dd/mm/YYYY)")

    data_nasciento_partes = data_nascimento.split("/")
    data_nascimento = f"{data_nasciento_partes[2]}-{data_nasciento_partes[1]}-{data_nasciento_partes[0]}"

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO funcionarios (nome, cargo, salario, data_nascimento) VALUES (%s, %s, %s, %s)",
        (nome, cargo, salario, data_nascimento),
    )


    conexao.commit()
    print(f"\n[OK] funcionario cadastrado com id: {cursor.lastrowid}")

    conexao.close()
    cursor.close()


def formatar_data(data: date | None):
    if data is None:
        return "-"
    return data.strftime("%d/%m/%Y")

def listar_funcionarios():
    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """SELECT id, nome, cargo, salario, data_nascimento FROM funcionarios ORDER BY nome ASC"""
    )

    #fetchall() retorna todas as linhas encontradas naquela consulta
    #cada linha contem uma tupla onde cada posição e a coluna do select

    funcionarios = cast(
    list[tuple[int, str, str | None, float | None, date | None]],
    cursor.fetchall()
    )

    if len(funcionarios) == 0:
        print("Nenhum funcionario cadastrado")
        return

    print("-"*100, end="")
    print(f"\n{'ID':<4} {'NOME':<25} {'CARGO':<20} {'NASCIMENTO':<30} {'SALARIO':>10}")
    print("-"*100)

    for colaborador in funcionarios:
        
        id = colaborador[0]
        nome = colaborador[1]
        cargo = colaborador[2] if colaborador[2] else "-"
        salario = colaborador[3] if colaborador[3] else "-"
        data_nascimento = formatar_data(colaborador[4]) if formatar_data(colaborador[4]) else "-"

        print(
            f"{id:<4} {nome:<25} {cargo:<20} {data_nascimento:<30} {salario:>10}"
        )
    print("-"*100)


def excluir_funcionario():
    listar_funcionarios()

    id_deletar = int(input("Digite o Id do usuario a ser deletado: "))

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM funcionarios WHERE id = %s", (id_deletar,))
    conexao.commit()

    cursor.close()
    conexao.close()

    if cursor.rowcount == 0:
        print("Funcionario com esse id não foi encontrado")
    else:
        print("Registro apagado com sucesso")


def alterar_funcionario():
    listar_funcionarios()

    print("\n----- ALTERAR FUNCIONARIO -----")
    id_alterar = int(input("Digite o Id do usuario a ser alterado: "))
    nome = input("Nome: ")
    cargo = input("Cargo: ")
    salario = float(input("Sálario: ").replace(",", "."))
    data_nascimento = input("Data de nascimento: (dd/mm/YYYY)")

    data_nasciento_partes = data_nascimento.split("/")
    data_nascimento = f"{data_nasciento_partes[2]}-{data_nasciento_partes[1]}-{data_nasciento_partes[0]}"

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE funcionarios SET nome = %s, cargo = %s, salario = %s, data_nascimento = %s WHERE id = %s",
        (nome, cargo, salario, data_nascimento, id_alterar)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    if cursor.rowcount == 0:
        print("Funcionario com esse Id não foi encontrado")
        print(cursor.rowcount)
    else:
        print(cursor.rowcount)
        print("Funcionario alterado com sucesso")


def menu_funcionario():
    mensagem = """MENU:
1 - Listar
2 - Cadastrar
3 - Editar
4 - Apagar
5 - Sair

Digite a opção desejada: """

    opcao = int(input(mensagem))

    while opcao != 5:
        os.system("cls")
        if opcao == 1:
            listar_funcionarios()
        elif opcao == 2:
            cadastrar()
        elif opcao == 3:
            alterar_funcionario()
        elif opcao == 4:
            excluir_funcionario()
        elif opcao != 5:
            print("Opção invalida")
        print("\n")
    

        opcao = int(input(mensagem))
    os.system("cls")