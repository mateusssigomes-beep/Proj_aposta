import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, CheckConstraint
from persist.conexao_bd import Base


class StatusGame(enum.Enum):
    MARCADO = 'Marcado'
    ANDAMENTO = 'Em Andamento'
    ENCERRADO = 'Encerrado'
    

class Game(Base):
    __tablename__ = 'Game'
    
    id = Column(Integer, primary_key=True)
    gol_time_casa = Column(Integer, nullable=True) # ISSO VAI SE ADICIONADO DEPOIS QUE UM JOGO FOR CRIADO
    gol_time_visitante = Column(Integer, nullable=True)  
    data_jogo = Column(DateTime, nullable=False)
    status = Column(Enum(StatusGame),nullable=False, default=StatusGame.MARCADO)
    time_vencedor = Column(String(40), nullable=True)
    """Provavelmente pode dar problema (Revisar o Recebimento de dados para os dois parametros )"""
    time_casa_id = Column(Integer,ForeignKey('Team.id'), nullable=False)
    time_visitante_id = Column(Integer, ForeignKey('Team.id'), nullable=False)
    
    
    """
    table args = 
    CheckConstraint = 
    name = 
    
    """
    __table_args__ = (
        CheckConstraint('time_casa_id != time_visitante_id', name = 'ck_times_diferentes'),
    )