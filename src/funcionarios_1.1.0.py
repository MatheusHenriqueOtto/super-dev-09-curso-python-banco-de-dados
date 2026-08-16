"""
Sistema de Funcionários
Versão: 1.1.0

Melhorias implementadas:
- Validação de entradas numéricas
- Validação de datas
- Compatível com Windows e Linux
- Tratamento de exceções do MySQL
- Fechamento seguro de conexões
- Formatação de salários
- Melhor organização do código
"""

from typing import cast
from mysql import connector
from mysql.connector import Error
from datetime import date, datetime
import os

# ============================================================
# CONFIGURAÇÕES
# ============================================================

HOST = "127.0.0.1"
PORTA = 3306
USUARIO = "root"
SENHA = "admin"
BANCO = "restau_calabresa"

# ============================================================
# BANCO DE DADOS
# ============================================================


def conectar():
    """Abre conexão com o banco de dados"""
    conexao = connector.connect(
        host=HOST,
        port=PORTA,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
    )
    return conexao 


# ============================================================
# UTILITÁRIOS
# ============================================================


def limpar_tela():
    """Limpa a tela em Windows ou Linux"""
    os.system("cls" if os.name == "nt" else "clear")


def formatar_data(data: date | None) -> str:
    if data is None:
        return "-"
    return data.strftime("%d/%m/%Y")


def formatar_salario(valor: float | None) -> str:
    if valor is None:
        return "-"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um valor numérico válido.")


def ler_int(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_data(mensagem: str) -> str:
    while True:
        try:
            data = datetime.strptime(input(mensagem), "%d/%m/%Y")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            print("Data inválida. Utilize o formato dd/mm/aaaa.")


# ============================================================
# CRUD
# ============================================================


def cadastrar():
    print("\n===== CADASTRAR FUNCIONÁRIO =====")

    nome = input("Nome: ").strip()
    cargo = input("Cargo: ").strip()
    salario = ler_float("Salário: ")
    data_nascimento = ler_data("Data de nascimento (dd/mm/aaaa): ")

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO funcionarios
        (nome, cargo, salario, data_nascimento)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                nome,
                cargo,
                salario,
                data_nascimento,
            ),
        )

        conexao.commit()

        print(f"\n[OK] Funcionário cadastrado com ID {cursor.lastrowid}")

    except Error as erro:
        print(f"\n[ERRO] {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def listar_funcionarios():

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nome,
                cargo,
                salario,
                data_nascimento
            FROM funcionarios
            ORDER BY nome ASC
            """
        )

        funcionarios = cast(
            list[
                tuple[
                    int,
                    str,
                    str | None,
                    float | None,
                    date | None,
                ]
            ],
            cursor.fetchall(),
        )

        if not funcionarios:
            print("\nNenhum funcionário cadastrado.")
            return

        print("-" * 100)
        print(
            f"{'ID':<5}"
            f"{'NOME':<30}"
            f"{'CARGO':<25}"
            f"{'NASCIMENTO':<15}"
            f"{'SALÁRIO':>20}"
        )
        print("-" * 100)

        for funcionario in funcionarios:

            id_func = funcionario[0]
            nome = funcionario[1]
            cargo = funcionario[2] or "-"
            salario = formatar_salario(funcionario[3])
            nascimento = formatar_data(funcionario[4])

            print(
                f"{id_func:<5}"
                f"{nome:<30}"
                f"{cargo:<25}"
                f"{nascimento:<15}"
                f"{salario:>20}"
            )

        print("-" * 100)

    except Error as erro:
        print(f"\n[ERRO] {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def excluir_funcionario():

    listar_funcionarios()

    id_deletar = ler_int(
        "\nDigite o ID do funcionário a ser removido: "
    )

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM funcionarios WHERE id = %s",
            (id_deletar,),
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("\nFuncionário não encontrado.")
        else:
            print("\nFuncionário removido com sucesso.")

    except Error as erro:
        print(f"\n[ERRO] {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def alterar_funcionario():

    listar_funcionarios()

    print("\n===== ALTERAR FUNCIONÁRIO =====")

    id_alterar = ler_int(
        "Digite o ID do funcionário: "
    )

    nome = input("Nome: ").strip()
    cargo = input("Cargo: ").strip()
    salario = ler_float("Salário: ")
    data_nascimento = ler_data(
        "Data de nascimento (dd/mm/aaaa): "
    )

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
        UPDATE funcionarios
        SET
            nome = %s,
            cargo = %s,
            salario = %s,
            data_nascimento = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (
                nome,
                cargo,
                salario,
                data_nascimento,
                id_alterar,
            ),
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("\nFuncionário não encontrado.")
        else:
            print("\nFuncionário alterado com sucesso.")

    except Error as erro:
        print(f"\n[ERRO] {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


# ============================================================
# MENU
# ============================================================


def menu_funcionario():

    while True:

        print(
            """
==============================
 SISTEMA DE FUNCIONÁRIOS
==============================

1 - Listar Funcionários
2 - Cadastrar Funcionário
3 - Alterar Funcionário
4 - Excluir Funcionário
5 - Limpar Tela
0 - Sair

"""
        )

        opcao = ler_int("Escolha uma opção: ")

        match opcao:
            case 1:
                listar_funcionarios()

            case 2:
                cadastrar()

            case 3:
                alterar_funcionario()

            case 4:
                excluir_funcionario()

            case 5:
                limpar_tela()

            case 0:
                print("\nEncerrando sistema...")
                break

            case _:
                print("\nOpção inválida.")

        input("\nPressione ENTER para continuar...")
        limpar_tela()

