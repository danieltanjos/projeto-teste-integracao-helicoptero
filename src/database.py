"""Modulo de banco de dados (SQLite) da operacao AeroLog Helicopteros."""
import sqlite3


class Database:
    """Gerencia a conexao e as operacoes no banco SQLite."""

    def __init__(self, caminho=":memory:"):
        self.conn = sqlite3.connect(caminho)
        self.conn.row_factory = sqlite3.Row
        self.criar_tabelas()

    def criar_tabelas(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS aeronaves (
                id INTEGER PRIMARY KEY,
                prefixo TEXT NOT NULL UNIQUE,
                status_manutencao TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS pilotos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aeronave_id INTEGER NOT NULL,
                piloto_id INTEGER NOT NULL,
                inicio TEXT NOT NULL,
                fim TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (aeronave_id) REFERENCES aeronaves (id)
            );
            """
        )
        self.conn.commit()

    def inserir_aeronave(self, id, prefixo, status_manutencao):
        self.conn.execute(
            "INSERT INTO aeronaves (id, prefixo, status_manutencao) VALUES (?, ?, ?)",
            (id, prefixo, status_manutencao),
        )
        self.conn.commit()

    def inserir_piloto(self, id, nome):
        self.conn.execute("INSERT INTO pilotos (id, nome) VALUES (?, ?)", (id, nome))
        self.conn.commit()

    def buscar_aeronave(self, aeronave_id):
        cur = self.conn.execute("SELECT * FROM aeronaves WHERE id = ?", (aeronave_id,))
        return cur.fetchone()

    def buscar_conflitos(self, aeronave_id, inicio, fim):
        """Retorna agendamentos da aeronave que se sobrepoem ao intervalo."""
        cur = self.conn.execute(
            """
            SELECT * FROM agendamentos
            WHERE aeronave_id = ? AND status = 'AGENDADO'
              AND inicio < ? AND fim > ?
            """,
            (aeronave_id, fim, inicio),
        )
        return cur.fetchall()

    def inserir_agendamento(self, aeronave_id, piloto_id, inicio, fim):
        cur = self.conn.execute(
            """
            INSERT INTO agendamentos (aeronave_id, piloto_id, inicio, fim, status)
            VALUES (?, ?, ?, ?, 'AGENDADO')
            """,
            (aeronave_id, piloto_id, inicio, fim),
        )
        self.conn.commit()
        return cur.lastrowid

    def buscar_agendamento(self, agendamento_id):
        cur = self.conn.execute(
            "SELECT * FROM agendamentos WHERE id = ?", (agendamento_id,)
        )
        return cur.fetchone()

    def listar_agendamentos(self):
        return self.conn.execute("SELECT * FROM agendamentos").fetchall()

    def fechar(self):
        self.conn.close()
