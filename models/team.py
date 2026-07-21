from sqlalchemy import Column, Integer, String
from persist.conexao_bd import Base

class Team(Base):
    __tablename__ = "Team"
    
    id = Column(Integer, primary_key = True)
    nome = Column(String(40), nullable=False)
    grupo = Column(String(40), nullable=False)
    vitoria = Column(Integer, nullable=False)
    empate = Column(Integer, nullable=False)
    derrota = Column(Integer, nullable=False)
    
    
    
    
    
