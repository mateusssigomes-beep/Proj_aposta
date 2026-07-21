from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base 
import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError

"""
Conexão modo SQLalchemy, Usando o Url do banco de dados  e Drive
Nesta conexão será usado como Drive o Psycopg2
"""
URL_BANCO = ("postgresql+psycopg2://postgres:123456@127.0.0.1:5432/db_projaposta")
"""
Engine sera o core da conexão com  o banco, ele tende a conter as pools para cada chamada de sistema. 
Também faz a tradução da lingaguem python para SQL, como um tradutor, Ele contem varias funcionalidades dentro de si.
Elém de ser Lazy(Preguisoço), ele só entra em Ação quando chamado, masmo após criar ele não tem atuação dentro do banco de dados
"""
try:
    engine = create_engine(URL_BANCO, echo=True) # create_engine recebe os parametros de Url do banco para conexão e echo=True, que tem como função mostrar todas as geraçõe SQL
    with engine.connect() as conn:
        versao = conn.execute(text("SELECT version();"))
        print(f'Conexão com o banco estabelecida \nVersão do banco: {versao}'
              f'Versão do Alchemy:{sqlalchemy.__version__}'
              )
except SQLAlchemyError as er:
    print(f'Não foi possível conectar com o banco de dados Erro: {er}')
        

"""
Conectando a sessao local,
Bind = engine:  
autoflush = True: Faz um rascunho da Operação dentro do banco, passivél de fazer rollback mesmo sem estar commitado. 
autocommit = False: Ele não commita nada até que o comando db.commit() seja passado
"""

# sessaoloc = sessionmaker(bind=engine, autoflush=True, autocommit=False)


"""
Crando a calsse que crias as tabelas
"""
try:
    sessaoloc = sessionmaker(bind=engine, autoflush=True, autocommit=False)
    Base = declarative_base()
    print('Base criado e pronto para uso'
          'Sessão Criada')
except StopIteration as error:
    print(f'Erro: {error}')


"""
Método teste para saber se a conexão foi bem sucedida ou não
"""
# def testa_conec():
#     try:
#         """Traz a versão do Banco de dados""" 
#         with engine.connect() as conn:
#             db_version = conn.execute(text("SELECT version();")).fetchone()
        
#         """Retorna print para saber se a conexão foi bem sucedida e os dadso da conxão e versão do SQLalchemy """
#         print(f'Conectado ao banco de dados \nVersão do banco de dados: {db_version}')
#         print(f'Versão do Alchemy Usado: {sqlalchemy.__version__}')
        
#         """Retorna o erro do próprio alchemy caso a conexão tenha falhado"""                              
#     except SQLAlchemyError as error:
#         print(f"não foi possível estabeler conexão com banco: {error}")

'''
Teste de fechar conexão
'''
# def fechaconec():
#     with engine.connect() as conn:
#         fechamento = conn.close()
#         print(f'Conexão com banco foi cortada, {fechamento}')
"""
Comando que sera acessado pela FastApi, Para populas as tabelas
"""

def get_db(): # Pegar algo dentro do banco de dados 
    bd  = sessaoloc() # vincula a variavél a Session, 
    '''
     
    '''
    try:
        yield bd
    finally:
        bd.close()
        
