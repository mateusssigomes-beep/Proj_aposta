from typing import Any, List, Tuple, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base 
import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError


class ConexaoBD:

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = None # motor que conecta com o banco de dados, ele sabe o que tem que fazer 
        self.base = None # Base é uma classe que transforma outras classes python em tabelas usando comandos como __tablename__ = 'nome'
        self.session = None# Sessão são os commandos Dao, usado para fazer ediçã, adição, exclusão e procura, abrir usar e fechar

    def conectar(self):
        try:
            """Conexão com o banco de dados Utilziando o Url do banco de dadosm por meio de SLQAlchemy"""
            url = (
                f"postgresql+psycopg2://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.database}"
            )
            #Engine se conectando ao banco de dados
            self.engine = create_engine(url) 
         
            with self.engine.connect() as conn: # gerenciador de contexto utilizado para finalzar autolaticamente o comando logo deposi de usado, 
                db_version = conn.execute(text("SELECT version();")).fetchone() # Text Traduz para o alchemy que algo esta em SQL puro, "SELECT version();"

            print("Conexao com o banco de dados estabelecida")
            print(f"Versao do banco: {db_version}")

        except SQLAlchemyError as erro:
            print(f"Erro ao conectar com o banco de dados: {erro}")

   
    def fechar_conexao(self):
        try:
            if self.engine:
                self.engine.dispose()
                print("Conexao com o banco de dados fechada.")
        except:
            print('Conexão não estabelecida')


    """outro caso que não sera necessário ter no comando"""

    def executar_comando(self, sql: str, valores: List[Tuple[Any]] | None = None):
    #     """Executa um comando SQL dentro de uma transacao."""
        if not self.engine:
            raise RuntimeError("Conexao nao foi estabelecida. Chame conectar() primeiro.")

        try:
            with self.engine.begin() as conn: # with faz a finzalização do comando automaticamente, no caso ele fecha a conexão 
                if valores:
                    conn.exec_driver_sql(sql, valores)
        except SQLAlchemyError as error:
            raise error



    """
        Comando a baixo foram retirados por conta do Alchemy ter uma função que cria as tabelas por meio de classes python
        Base: crias as tabelas e depoia pode ser ignorado, apenas faz a criação  delas
        Session vai fazer a parte das Daos, Adicionar, Editar, Excluir, Atualizar   
        Base.metadata.create_all(bind=engine)   # substitui criar_tabelas()
        Base.metadata.drop_all(bind=engine)     # substitui destruir_tabelas()
    """

    def criar_tabelas(self):
        if not self.engine:
            raise RuntimeError("Conexao nao foi estabelecida. Chame conectar() primeiro.")

        comandos = [
            """
            CREATE TABLE IF NOT EXISTS Team (
                id INT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                grupo VARCHAR(20) NOT NULL,
                vitorias INT NOT NULL,
                empates INT NOT NULL,
                derrotas INT NOT NULL
            );
        
            CREATE TABLE IF NOT EXISTS Bet (
                id INT PRIMARY KEY,
                idGame INT,
                idUser INT,
                multiplier FLOAT NOT NULL,
                pontos_ganhos INT NOT NULL,
                pontos_apostados INT NOT NULL,
                chute_gol_casa INT NOT NULL,
                chute_gol_visitante INT NOT NULL,
                status VARCHAR NOT NULL
            );
         
            CREATE TABLE IF NOT EXISTS Game (
                id INT PRIMARY KEY,
                pontos INT NOT NULL,
                status VARCHAR(10) NOT NULL,
                time_vencedor VARCHAR(20) NOT NULL,
                data TIMESTAMP NOT NULL,
                gol_visistante INT NOT NULL,
                gol_casa INT NOT NULL
            );
           
            CREATE TABLE IF NOT EXISTS "User" (
                id INT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                data_nascimento TIMESTAMP NOT NULL,
                cpf VARCHAR(22) NOT NULL,
                senha_hash VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                login VARCHAR(100) NOT NULL,
                pontos INT NOT NULL,
                status VARCHAR(10) NOT NULL,
                admin BOOLEAN NOT NULL
            );
            """,
        ]

        try:
            with self.engine.begin() as conn:
                for comando in comandos:
                    conn.execute(text(comando))
            print("Tabelas criadas")
        except SQLAlchemyError as error:
            print(f"Tabela nao pode ser criada: {error}")

    def destruir_tabelas(self):
        if not self.engine:
            raise RuntimeError("Conexao nao foi estabelecida. Chame conectar() primeiro.")

        comandos = [
            'DROP TABLE IF EXISTS "User";',
            "DROP TABLE IF EXISTS Bet;",
            "DROP TABLE IF EXISTS Game;",
            "DROP TABLE IF EXISTS Team;",
        ]

        try:
            with self.engine.begin() as conn:
                for comando in comandos:
                    conn.execute(text(comando))
            print("Tabelas excluidas")
        except SQLAlchemyError as error:
            print(f"Tabelas inexistentes: {error}")


# conector = ConexaoBD(
#     user="postgres",
#     password="123456",
#     host="127.0.0.1",
#     port="5432",
#     database="db_projaposta",
# )
# # conector.conectar()
# conector.fechar_conexao()



