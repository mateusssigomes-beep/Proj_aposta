import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from Persist.conexao_bd import Base


class StatusGame(enum.Enum):
    MARCADO = 'Marcado'
    ANDAMENTO = 'Em Andamento'
    ENCERRADO = 'Encerrado'

class Game(Base):
    __tablename__ = 'Game'
    
    id = Column(Integer, primary_key=True)
    gol_time_casa = Column(Integer, nullable=True)
    gol_time_visitante = Column(Integer, nullable=True)
    data_jogo = Column(DateTime, nullable=False)
    status = Column(Enum(StatusGame),nullable=False, default=StatusGame.MARCADO)
    time_vencedor = Column(String(40), nullable=False)
    """Provavelmente pode dar problema (Revisar o Recebimento de info para os dois parametros )"""
    time_casa_id = Column(Integer,ForeignKey('Team.id'), nullable=False)
    time_visitante_id = Column(Integer, ForeignKey('Team.id'), nullable=False)