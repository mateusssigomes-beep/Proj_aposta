from sqlalchemy import String,Date, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum 
from datetime import date 
from persist.conexao_bd import Base 

# Definir se o user estara ativo ou não 
class StatusUsuario(enum.Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"


class User(Base):
    __tablename__ = "User"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=False)
    data_nascimento: Mapped[date] 
    cpf: Mapped[str] = mapped_column(String(40), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(100))  
    email: Mapped[str] = mapped_column(String(100), unique=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    status: Mapped[StatusUsuario] = mapped_column(default=StatusUsuario.ATIVO)
    pontos: Mapped[int] = mapped_column(default=100)
    admin: Mapped[bool] = mapped_column(default=False) # False, User não é Admin | True, User é Admin 
    
    def __repr__(self):
        return f'Nome: {self.nome}, Login: {self.login}, Data de Nascimento: {self.data_nascimento}'
    
    

    
    
    """
    método Escrito no Antigo Formato de SQLalchemy
class User(Base):
    __tablename__ = 'User'
    # id : Mapped[int] = mapped_column(primary_key=True)
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    data_nascimento = Column(Date, nullable=False) # Ver re ralmente é um tipo de dado que sai formatado pelo alchemy
    cpf = Column(String(20), nullable=False, unique=True) 
    senhahash = Column(String(200), nullable=False) 
    email = Column(String(40), nullable=False, unique=True) 
    login = Column(String(20), nullable=False, unique=True) 
    pontos = Column(Integer, nullable=False, default=100 )
    status = Column(Enum(StatusUsuario), nullable=False, 
    default=StatusUsuario.ATIVO)#Para saber se esta Ativo ou Inativo Talvz Seja trocado para Enum, Assim que eusouber o que realemtne é
    admin = Column(Boolean, nullable=False, default=False)
    """
    