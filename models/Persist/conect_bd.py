import psycopg2
from typing import Any, Tuple, List, Dict
class ConexaoBD:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection =psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            print("Conexão com o banco de dados estabelecida com sucesso!")
            self.cursor = self.connection.cursor()
            # Executa uma query simples para verificar a versão do Postgres
            self.cursor.execute("SELECT version();")
            db_version = self.cursor.fetchone()
            print("Conexão com o banco de dados estabelecida com sucesso!")
            print(f"Versão do banco: {db_version}")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao conectar ao banco de dados:", error)

    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados fechada.")




    def execute_command(self, sql: str, valores: List[Tuple[Any]]):
        """Executa comando com múltiplos valores usando executemany."""
        if not self.cursor or not self.connection:
            raise RuntimeError("Conexão não foi estabelecida. Chame conectar() primeiro.")
        try:
            self.cursor.executemany(sql, valores)
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            raise error
            

# Exemplo de uso (descomente para testar):
conectar = ConexaoBD(user='postgres', password='123456', host='127.0.0.1', port='5432', database='db_projaposta')
# conectar.conectar()
# # ... use os métodos aqui ...
# conectar.fechar_conexao()