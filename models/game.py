from typing import Optional
from datetime import datetime 
import enum
from models.team import Team
from sqlalchemy import ForeignKey, CheckConstraint
from persist.conexao_bd import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class StatusGame(enum.Enum):
    MARCADO = 'Marcado'
    ANDAMENTO = 'Em Andamento'
    ENCERRADO = 'Encerrado'
    



     
class Game(Base):
    
    __tablename__ = "Game"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    gol_time_casa: Mapped[Optional[int]] # nullable = True | Pode não ter valor aqui
    gol_time_visitante: Mapped[Optional[int]] # nullable = True | Pode não ter valor aqui
    data_jogo: Mapped[datetime] # Dentro do Mapped vão opções que o próprio python entende
    status: Mapped[StatusGame] = mapped_column(default=StatusGame.MARCADO)
    time_vencedor: Mapped[Optional[str]]# nullable = True |Pode não ter valor aqui
    time_casa_id: Mapped[int] = mapped_column(ForeignKey("Team.id"))
    time_visitante_id: Mapped[int] = mapped_column(ForeignKey("Team.id"))
    
    """
        Adicionar a explicação do relationship aqui [do comando, e o que ele esta fazendo]
    """
    time_casa: Mapped["Team"] = relationship(foreign_keys=[time_casa_id])
    time_visitante: Mapped["Team"] = relationship(foreign_keys=[time_visitante_id])
   
   
    """
       Adicionar a Explcação do Table_args aqui | CheckContraint [ Do Comando e o que fazem ]
    """
    __table_args__ = (
        CheckConstraint('time_casa_id != time_visitante_id', name = 'ck_times_diferentes'),
    )
    
    
    def __repr__(self):
         return f'Jogo Contendo {self.time_casa_id} e {self.time_visitante_id}, {self.data_jogo}, Id do jogo: {self.id}'
     
     
     
"""class Game(Base):
    __tablename__ = 'Game'
    
    id = Column(Integer, primary_key=True)
    gol_time_casa = Column(Integer, nullable=True) #  Poder ser 0 / nulo, na criação, mas depois sera adicionado algum valor  
    gol_time_visitante = Column(Integer, nullable=True) #  Poder ser 0 / nulo, na criação, mas depois sera adicionado algum valor 
    data_jogo = Column(DateTime, nullable=False)
    status = Column(Enum(StatusGame),nullable=False, default=StatusGame.MARCADO)
    time_vencedor = Column(String(40), nullable=True) # Poder ser 0 / nulo, na criação, mas depois sera adicionado algum valor 

    time_casa_id = Column(Integer,ForeignKey('Team.id'), nullable=False)
    time_visitante_id = Column(Integer, ForeignKey('Team.id'), nullable=False)
    time_casa = relationship("Team", foreign_keys=[time_casa_id])
    time_visitante = relationship("Team", foreign_keys=[time_visitante_id])
"""