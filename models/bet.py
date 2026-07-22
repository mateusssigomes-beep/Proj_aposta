import enum 
from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from persist.conexao_bd import Base


class StatusAposta(enum.Enum):
    PERDEU = 'Perdeu'
    ANDAMENTO = 'Andamento'
    VENCEU = 'Venceu'
    EMPATE = 'Empatado'

class Aposta(Base):
    __tablename__ = 'Bet'
    
    id = Column(Integer, primary_key=True)
    multiplier = Column(Float, nullable=False)
    pontos_apostados = Column(Integer ,nullable=False)
    # pontos_ganhos = Column(Integer ,nullable = True ) # ISSO  AQUI SÓ É ADICIOADO QUANDO A APOSTA ACABA
    # pontos_retornados = Column(Integer, nullable = True)
    chute_time_casa = Column(Integer , nullable = False)
    chute_time_visitante = Column(Integer, nullable= False)
    status = Column(Enum(StatusAposta), nullable=False, default=StatusAposta.ANDAMENTO)
    idGame = Column(Integer, ForeignKey('Game.id'),nullable=False)
    idUser = Column(Integer, ForeignKey('User.id'),nullable=False )

    
