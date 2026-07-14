from sqlalchemy import create_engine, text, engine
from sqlalchemy.orm import sessionmaker, declarative_base 
import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError

"""Conexão modo SQLalchemy, Usando o Url do banco de dados"""
URL_BANCO = ("postgresql://postgres:123456@127.0.0.1:5432/db_projaposta")
engine = create_engine(URL_BANCO)

"""Conectando a sessao local"""
sessaolocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
"""Crando a calsse que crias as tabelas"""
Base = declarative_base()


def testa_conxao():
    try:
        """Traz a versão do Banco de dados""" 
        with engine.connect() as eng:
            db_version = eng.execute(text("SELECT version();")).fetchone()
        
        """Retorna print para saber se a conexão foi bem sucedida """
        print(f'Conectado ao banco de dados \nVersão do banco de dados: {db_version}')
        print(f'Versão do Alchemy Usado: {sqlalchemy.__version__}')
        
        """Retorna o erro do próprio alchemy caso a conexão tenha falhado"""                              
    except SQLAlchemyError as error:
        print(f"não foi possível estabeler conexão com banco: {error}")


def get_db():
    bd  = sessaolocal()
    try:
        yield bd
    finally:
        bd.close()
        
        
if __name__ == "__main__":
    testa_conxao()
