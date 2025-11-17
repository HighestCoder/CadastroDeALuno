import sqlite3

def conectar():
    return sqlite3.connect("sistema.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # tabela de alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aluno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL,
            dataNasc TEXT NOT NULL,
            nota REAL
        )
    """)

    # tabela de disciplinas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT NOT NULL,
            sala TEXT NOT NULL,
            professor TEXT NOT NULL
        )
    """)

    # tabela de notas (relacionamento)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (aluno_id) REFERENCES aluno (id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplina (id)
        )
    """)

    conn.commit()
    conn.close()
