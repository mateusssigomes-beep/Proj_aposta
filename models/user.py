from sqlalchemy import Column, Integer, String, Boolean,Date, Enum
from persist.conexao_bd import Base
import enum 

# Definir se o user estara ativo ou não 
class StatusUsuario(enum.Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"
    


# modo Alchemy de fazer as tabelas
class User(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    data_nascimento = Column(Date, nullable=False) # Ver re ralmente é um tipo de dado que sai formatado pelo alchemy
    cpf = Column(String(20), nullable=False)
    senhahash = Column(String(200), nullable=False) 
    email = Column(String(40), nullable=False)
    login = Column(String(20), nullable=False)
    pontos = Column(Integer, nullable=False, default=100 )
    status = Column(Enum(StatusUsuario), nullable=False, default=StatusUsuario.ATIVO)#Para saber se esta Ativo ou Inativo Talvz Seja trocado para Enum, Assim que eusouber o que realemtne é
    admin = Column(Boolean, nullable=False, default=False)