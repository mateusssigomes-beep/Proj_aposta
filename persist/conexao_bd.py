from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError



"""
Conexão modo SQLalchemy, Usando o Url do banco de dados  e Drive
Nesta conexão será usado como Drive o Psycopg2
"""
URL_BANCO = ("postgresql+psycopg2://postgres:123456@127.0.0.1:5432/db_projaposta")

try:
    """
    Engine sera o core da conexão com  o banco, ele tende a conter as pools para cada chamada de sistema. 
    Também faz a tradução da lingaguem python para SQL, como um tradutor, Ele contem varias funcionalidades dentro de si.
    Elém de ser Lazy(Preguisoço), ele só entra em Ação quando chamado, masmo após criar ele não tem atuação dentro do banco de dados
    """
    engine = create_engine(URL_BANCO)#, echo=True)  # create_engine recebe os parametros de Url do banco para conexão e echo=True, que tem como função mostrar todas as geraçõe SQL
    with engine.connect() as conn:
        versao = conn.execute(text("SELECT version();")).fetchone()
        print('Conexão com o banco estabelecida', f'Versão do banco: {versao}',
              f'Versão do Alchemy:{sqlalchemy.__version__}', sep='\n'
              )
except SQLAlchemyError as er:
    print(f'Não foi possível conectar com o banco de dados Erro: {er}')
 
class Base(DeclarativeBase):
    pass       
 

try:
    """
    Conectando a sessao local,
    Bind = engine:  
    autoflush = True: Faz um rascunho da Operação dentro do banco, passivél de fazer rollback mesmo sem estar commitado. 
    autocommit = False: Ele não commita nada até que o comando db.commit() seja passado

    Criando a calsse que crias as tabelas e A Session, que fara o trabalho de salver e popular as tabelas criadas 
    """
    Sessaoloc = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )
except StopIteration as error:
    print(f'Erro: {error}')



def get_db(): # Pegar algo dentro do banco de dados 
    """
    Comando que sera acessado pela FastApi, Para populas as tabelas
    """
    
    bd  = Sessaoloc() # vincula a variavél a Session, 
    try:
        yield bd
    finally:
        bd.close()
        






        
