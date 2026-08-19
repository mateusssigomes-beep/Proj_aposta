import enum 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
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
    
    
    
    # def __repr__(self):
    #     return f'Status: {self.status} |\nOdd: {self.multiplier}'
    
