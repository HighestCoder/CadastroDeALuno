#cd "C:\Users\YagoCF\Desktop\sistema_cadastro" 
import banco
import sqlite3
import json
import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

# CRIA AS TABELAS NO BANCO
banco.criar_tabelas()

# FUNÇÃO PARA SALVAR EM JSON
def salvar_em_json(dados, nome_arquivo): 
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo: 
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

# ==========================
# CONFIGURAÇÃO DA JANELA PRINCIPAL
# ==========================
root = tk.Tk()
root.title("Sistema de Cadastro de Alunos")
root.geometry("650x600")
root.configure(bg="#F5F5F5")

header = tk.Frame(root, bg="#0288D1", height=80)
header.pack(fill="x")

conteudo = tk.Frame(root, bg="#F5F5F5")
conteudo.pack(fill="both", expand=True)

logo = tk.PhotoImage(file="es.png")

bottom_frame = tk.Frame(root, bg="#F5F5F5")
bottom_frame.pack(side="bottom", fill="x", pady=10)

tk.Label(bottom_frame, image=logo, bg="#F5F5F5").pack(side="left", padx=20)

# ==========================
# ESTILOS
# ==========================
style = ttk.Style()
style.theme_use("clam")

style.configure("Modern.TButton",
                font=("Segoe UI", 12, "bold"),
                padding=8,
                background="#4CAF50",
                foreground="white",
                borderwidth=0)

style.map("Modern.TButton",
          background=[("active", "#45A049")],
          foreground=[("active", "white")])

# ==========================
# FUNÇÕES AUXILIARES
# ==========================
def limpar_tela():
    for widget in conteudo.winfo_children():
        widget.destroy()


# ==========================
# CADASTRO DE ALUNO
# ==========================
def mostrar_cadastro():
    limpar_tela()

    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text="Cadastro de Aluno", font=("Segoe UI", 18, "bold"),
             bg="#F5F5F5", fg="#333").pack(pady=20)

    # Campos de entrada
    tk.Label(frame, text="Nome:", bg="#F5F5F5").pack()
    entry_nome = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_nome.pack(pady=3)

    tk.Label(frame, text="Matrícula:", bg="#F5F5F5").pack()
    entry_matricula = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_matricula.pack(pady=3)

    tk.Label(frame, text="Data de Nascimento:", bg="#F5F5F5").pack()
    data_var = tk.StringVar()
    entry_data = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_data.pack(pady=3)

    tk.Label(frame, text="Nota:", bg="#F5F5F5").pack()
    entry_nota = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_nota.pack(pady=3)

    def salvar():
        nome = entry_nome.get().strip()
        matricula = entry_matricula.get().strip()
        dataNasc = entry_data.get().strip()
        nota = entry_nota.get().strip()

        if not nome or not matricula or not dataNasc or not nota:
            messagebox.showwarning("Aviso", "Preencha todos os campos antes de salvar.")
            return

        try:
            nota_float = float(nota)
        except ValueError:
            messagebox.showerror("Erro", "A nota deve ser um número (ex: 7.5)")
            return

        conexao = banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO aluno (nome, matricula, dataNasc, nota)
            VALUES (?, ?, ?, ?)
        """, (nome, matricula, dataNasc, nota_float))
        conexao.commit()
        conexao.close()

        aluno = {"nome": nome, "matricula": matricula,
                 "dataNasc": dataNasc, "nota": nota_float}

        try:
            with open("alunos.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            dados = []

        dados.append(aluno)
        salvar_em_json(dados, "alunos.json")

        messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso!")
        mostrar_menu()

    ttk.Button(frame, text="Salvar", width=25,
               style="Modern.TButton", command=salvar).pack(pady=10)
    ttk.Button(frame, text="Voltar", width=25,
               style="Modern.TButton", command=mostrar_menu).pack(pady=5)


# ==========================
# LISTAGEM DE ALUNOS
# ==========================
def listar():
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text="Listagem de Alunos", font=("Segoe UI", 18, "bold"),
             bg="#F5F5F5", fg="#333").pack(pady=20)

    conexao = banco.conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, matricula, dataNasc, nota FROM aluno")
    alunos = cursor.fetchall()
    conexao.close()

    if len(alunos) == 0:
        tk.Label(frame, text="Nenhum aluno cadastrado ainda.",
                 bg="#F5F5F5", fg="#555").pack(pady=10)
    else:
        colunas = ("ID", "Nome", "Matrícula", "Data de Nascimento", "Nota")
        tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=10)

        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=120, anchor="center")

        for aluno in alunos:
            tabela.insert("", "end", values=aluno)

        tabela.pack(pady=10)

        def excluir_aluno():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um aluno para excluir.")
                return
            id_aluno = tabela.item(selecionado)["values"][0]
            confirmar = messagebox.askyesno("Confirmação", f"Excluir o aluno ID {id_aluno}?")
            if not confirmar:
                return
            conexao_local = banco.conectar()
            cursor_local = conexao_local.cursor()
            cursor_local.execute("DELETE FROM aluno WHERE id = ?", (id_aluno,))
            conexao_local.commit()
            conexao_local.close()
            tabela.delete(selecionado)
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")

        def editar_aluno():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um aluno para editar.")
                return
            valores = tabela.item(selecionado)["values"]
            id_aluno, nome_atual, matricula_atual, dataNasc_atual, nota_atual = valores
            mostrar_edicao(id_aluno, nome_atual, matricula_atual, dataNasc_atual, nota_atual)

        ttk.Button(frame, text="Editar", width=25,
                   style="Modern.TButton", command=editar_aluno).pack(pady=5)
        ttk.Button(frame, text="Excluir", width=25,
                   style="Modern.TButton", command=excluir_aluno).pack(pady=5)

    ttk.Button(frame, text="Voltar", width=25,
               style="Modern.TButton", command=mostrar_menu).pack(pady=20)

# ==========================
# EDIÇÃO DE ALUNO
# ==========================
def mostrar_edicao(id_aluno, nome_atual, matricula_atual, dataNasc_atual, nota_atual):
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text=f"Editar Aluno (ID: {id_aluno})",
             font=("Segoe UI", 18, "bold"), bg="#F5F5F5", fg="#333").pack(pady=20)

    tk.Label(frame, text="Nome:", bg="#F5F5F5").pack()
    entry_nome = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_nome.insert(0, nome_atual)
    entry_nome.pack(pady=3)

    tk.Label(frame, text="Matrícula:", bg="#F5F5F5").pack()
    entry_matricula = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_matricula.insert(0, matricula_atual)
    entry_matricula.pack(pady=3)

    tk.Label(frame, text="Data de Nascimento:", bg="#F5F5F5").pack()
    entry_data = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_data.insert(0, dataNasc_atual)
    entry_data.pack(pady=3)

    tk.Label(frame, text="Nota:", bg="#F5F5F5").pack()
    entry_nota = tk.Entry(frame, font=("Segoe UI", 11), width=35)
    entry_nota.insert(0, nota_atual)
    entry_nota.pack(pady=3)

    def salvar_alteracoes():
        novo_nome = entry_nome.get()
        nova_matricula = entry_matricula.get()
        nova_data = entry_data.get()
        nova_nota = entry_nota.get()

        try:
            nova_nota_float = float(nova_nota)
        except ValueError:
            messagebox.showerror("Erro", "A nota deve ser numérica (ex: 8.5)")
            return

        conexao_local = banco.conectar()
        cursor_local = conexao_local.cursor()
        cursor_local.execute("""
            UPDATE aluno
            SET nome = ?, matricula = ?, dataNasc = ?, nota = ?
            WHERE id = ?
        """, (novo_nome, nova_matricula, nova_data, nova_nota_float, id_aluno))
        conexao_local.commit()
        conexao_local.close()

        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        listar()

    ttk.Button(frame, text="Salvar", width=25,
               style="Modern.TButton", command=salvar_alteracoes).pack(pady=10)
    ttk.Button(frame, text="Cancelar", width=25,
               style="Modern.TButton", command=listar).pack(pady=5)


# ==========================
# CADASTRO DE DISCIPLINAS
# ==========================
def mostrar_cadastro_disciplina():
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text="Cadastro de Disciplina",
             font=("Segoe UI", 18, "bold"), bg="#F5F5F5", fg="#333").pack(pady=20)

    entry_nome = tk.Entry(frame, width=35)
    tk.Label(frame, text="Nome da Disciplina", bg="#F5F5F5").pack()
    entry_nome.pack(pady=3)

    entry_turno = tk.Entry(frame, width=35)
    tk.Label(frame, text="Turno", bg="#F5F5F5").pack()
    entry_turno.pack(pady=3)

    entry_sala = tk.Entry(frame, width=35)
    tk.Label(frame, text="Sala", bg="#F5F5F5").pack()
    entry_sala.pack(pady=3)

    entry_professor = tk.Entry(frame, width=35)
    tk.Label(frame, text="Professor", bg="#F5F5F5").pack()
    entry_professor.pack(pady=3)

    def salvar():
        nome = entry_nome.get()
        turno = entry_turno.get()
        sala = entry_sala.get()
        professor = entry_professor.get()

        if not nome or not turno or not sala or not professor:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        conexao = banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO disciplina (nome, turno, sala, professor)
            VALUES (?, ?, ?, ?)
        """, (nome, turno, sala, professor))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f"Disciplina {nome} cadastrada com sucesso!")
        mostrar_menu()

    ttk.Button(frame, text="Salvar", width=25,
               style="Modern.TButton", command=salvar).pack(pady=10)
    ttk.Button(frame, text="Voltar", width=25,
               style="Modern.TButton", command=mostrar_menu).pack(pady=5)


# ==========================
# CADASTRO DE DISCIPLINAS
# ==========================
def mostrar_cadastro_disciplina():
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text="Cadastro de Disciplina",
             font=("Segoe UI", 18, "bold"), bg="#F5F5F5", fg="#333").pack(pady=20)

    tk.Label(frame, text="Nome:", bg="#F5F5F5").pack()
    entry_nome = tk.Entry(frame, width=35)
    entry_nome.pack(pady=3)

    tk.Label(frame, text="Turno:", bg="#F5F5F5").pack()
    entry_turno = tk.Entry(frame, width=35)
    entry_turno.pack(pady=3)

    tk.Label(frame, text="Sala:", bg="#F5F5F5").pack()
    entry_sala = tk.Entry(frame, width=35)
    entry_sala.pack(pady=3)

    tk.Label(frame, text="Professor:", bg="#F5F5F5").pack()
    entry_professor = tk.Entry(frame, width=35)
    entry_professor.pack(pady=3)

    def salvar():
        nome = entry_nome.get().strip()
        turno = entry_turno.get().strip()
        sala = entry_sala.get().strip()
        professor = entry_professor.get().strip()

        if not nome or not turno or not sala or not professor:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        conexao = banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO disciplina (nome, turno, sala, professor)
            VALUES (?, ?, ?, ?)
        """, (nome, turno, sala, professor))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f"Disciplina {nome} cadastrada com sucesso!")
        listar_disciplinas()

    ttk.Button(frame, text="Salvar", width=25,
               style="Modern.TButton", command=salvar).pack(pady=10)
    ttk.Button(frame, text="Voltar", width=25,
               style="Modern.TButton", command=mostrar_menu).pack(pady=5)


# ==========================
# LISTAGEM DE DISCIPLINAS
# ==========================
def listar_disciplinas():
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text="Listagem de Disciplinas", font=("Segoe UI", 18, "bold"),
             bg="#F5F5F5", fg="#333").pack(pady=20)

    conexao = banco.conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, turno, sala, professor FROM disciplina")
    disciplinas = cursor.fetchall()
    conexao.close()

    if not disciplinas:
        tk.Label(frame, text="Nenhuma disciplina cadastrada ainda.",
                 bg="#F5F5F5", fg="#555").pack(pady=10)
    else:
        colunas = ("ID", "Nome", "Turno", "Sala", "Professor")
        tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=10)

        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=110, anchor="center")

        for disc in disciplinas:
            tabela.insert("", "end", values=disc)

        tabela.pack(pady=10)

        # Botões Editar / Excluir
        def excluir_disciplina():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma disciplina para excluir.")
                return

            id_disciplina = tabela.item(selecionado)["values"][0]
            confirmar = messagebox.askyesno("Confirmação", f"Excluir a disciplina ID {id_disciplina}?")
            if not confirmar:
                return

            conexao_local = banco.conectar()
            cursor_local = conexao_local.cursor()
            cursor_local.execute("DELETE FROM disciplina WHERE id = ?", (id_disciplina,))
            conexao_local.commit()
            conexao_local.close()

            tabela.delete(selecionado)
            messagebox.showinfo("Sucesso", "Disciplina excluída com sucesso!")

        def editar_disciplina():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma disciplina para editar.")
                return
            valores = tabela.item(selecionado)["values"]
            id_disc, nome_atual, turno_atual, sala_atual, professor_atual = valores
            mostrar_edicao_disciplina(id_disc, nome_atual, turno_atual, sala_atual, professor_atual)

        ttk.Button(frame, text="Editar", width=25, style="Modern.TButton",
                   command=editar_disciplina).pack(pady=5)
        ttk.Button(frame, text="Excluir", width=25, style="Modern.TButton",
                   command=excluir_disciplina).pack(pady=5)

    ttk.Button(frame, text="Voltar", width=25,
               style="Modern.TButton", command=mostrar_menu).pack(pady=20)


# ==========================
# EDIÇÃO DE DISCIPLINA
# ==========================
def mostrar_edicao_disciplina(id_disc, nome_atual, turno_atual, sala_atual, professor_atual):
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text=f"Editar Disciplina (ID: {id_disc})",
             font=("Segoe UI", 18, "bold"), bg="#F5F5F5", fg="#333").pack(pady=20)

    tk.Label(frame, text="Nome:", bg="#F5F5F5").pack()
    entry_nome = tk.Entry(frame, width=35)
    entry_nome.insert(0, nome_atual)
    entry_nome.pack(pady=3)

    tk.Label(frame, text="Turno:", bg="#F5F5F5").pack()
    entry_turno = tk.Entry(frame, width=35)
    entry_turno.insert(0, turno_atual)
    entry_turno.pack(pady=3)

    tk.Label(frame, text="Sala:", bg="#F5F5F5").pack()
    entry_sala = tk.Entry(frame, width=35)
    entry_sala.insert(0, sala_atual)
    entry_sala.pack(pady=3)

    tk.Label(frame, text="Professor:", bg="#F5F5F5").pack()
    entry_professor = tk.Entry(frame, width=35)
    entry_professor.insert(0, professor_atual)
    entry_professor.pack(pady=3)

    def salvar_alteracoes():
        novo_nome = entry_nome.get().strip()
        novo_turno = entry_turno.get().strip()
        nova_sala = entry_sala.get().strip()
        novo_professor = entry_professor.get().strip()

        if not novo_nome or not novo_turno or not nova_sala or not novo_professor:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        conexao = banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE disciplina
            SET nome = ?, turno = ?, sala = ?, professor = ?
            WHERE id = ?
        """, (novo_nome, novo_turno, nova_sala, novo_professor, id_disc))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Disciplina atualizada com sucesso!")
        listar_disciplinas()

    ttk.Button(frame, text="Salvar", width=25, style="Modern.TButton",
               command=salvar_alteracoes).pack(pady=10)
    ttk.Button(frame, text="Cancelar", width=25, style="Modern.TButton",
               command=listar_disciplinas).pack(pady=5)

# ==========================
# MENU PRINCIPAL
# ==========================
def mostrar_menu():
    limpar_tela()
    frame = tk.Frame(conteudo, bg="#F5F5F5")
    frame.pack(expand=True)

    tk.Label(frame, text="📘 Sistema de Cadastro", font=("Segoe UI", 18, "bold"),
             bg="#F5F5F5", fg="#333").pack(pady=20)

    ttk.Button(frame, text="Cadastrar Aluno", width=25,
               style="Modern.TButton", command=mostrar_cadastro).pack(pady=5)
    ttk.Button(frame, text="Listar Alunos", width=25,
               style="Modern.TButton", command=listar).pack(pady=5)
    ttk.Button(frame, text="Cadastrar Disciplina", width=25,
               style="Modern.TButton", command=mostrar_cadastro_disciplina).pack(pady=5)
    ttk.Button(frame, text="Listar Disciplinas", width=25,
               style="Modern.TButton", command=listar_disciplinas).pack(pady=5)
    ttk.Button(frame, text="Sair", width=25,
               style="Modern.TButton", command=root.destroy).pack(pady=20)

# ==========================
# INICIAR SISTEMA
# ==========================
mostrar_menu()
root.mainloop()