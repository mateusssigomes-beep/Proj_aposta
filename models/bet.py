import enum 
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, ForeignKey, String
from persist.conexao_bd import Base


class StatusAposta(enum.Enum):
    PERDEU = 'Perdeu'
    ANDAMENTO = 'Andamento'
    VENCEU = 'Venceu'
    EMPATE = 'Empatado'


class Bet(Base):
    __tablename__ = "Bet"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    multiplier: Mapped[float]
    # pontos_ganhos: Mapped[Optional[int]] # nullable = True 
    # pontos_retornados: Mapped[Optional[int]] # nullable = True 
    pontos_apostados: Mapped[int]
    chute_gol_casa: Mapped[int]
    chute_gol_visitante: Mapped[int]
    status: Mapped[StatusAposta] = mapped_column(default=StatusAposta.ANDAMENTO)
    idgame: Mapped[int] = mapped_column(ForeignKey('Game.id'))
    iduser: Mapped[int] = mapped_column(ForeignKey('User.id'))
    
    
    
    def __repr__(self):
        return f'Status: {self.status} |\nOdd: {self.multiplier}'
        
"""class Aposta(Base):
    __tablename__ = 'Bet'
    
    id = Column(Integer, primary_key=True)
    multiplier = Column(Float, nullable=False)
    pontos_apostados = Column(Integer ,nullable=False)
    pontos_ganhos = Column(Integer ,nullable = True )
    pontos_retornados = Column(Integer, nullable = True)
    chute_time_casa = Column(Integer , nullable = False)
    chute_time_visitante = Column(Integer, nullable= False)
    status = Column(Enum(StatusAposta), nullable=False, default=StatusAposta.ANDAMENTO)
    idGame = Column(Integer, ForeignKey('Game.id'),nullable=False)
    idUser = Column(Integer, ForeignKey('User.id'),nullable=False )
"""
    
