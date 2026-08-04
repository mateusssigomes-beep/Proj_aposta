from sqlalchemy import  Integer, String
from persist.conexao_bd import Base
from sqlalchemy.orm import Mapped, mapped_column 
from typing import Optional

    


class Team(Base):
    __tablename__ = "Team"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(40))
    grupo: Mapped[str] = mapped_column(String(40))
    vitoria: Mapped[int] = mapped_column(default=0)
    empate: Mapped[int] = mapped_column(default=0) 
    derrota: Mapped[int] = mapped_column(default=0)
  
    def __repr__(self):
        """
        Retorno em String do Obejto, Usado para Visualizar o que esta  retornando
        """
        return f"Time: {self.nome} | Grupo: {self.grupo} | Contendo:\n{self.vitoria} Vitórias |\n {self.derrota} Derrotas |\n{self.empate} Empates"




"""class Team(Base):
    __tablename__ = "Team"
    
    id = Column(Integer, primary_key = True)
    nome = Column(String(40), nullable=False)
    grupo = Column(String(40), nullable=False)
    vitoria = Column(Integer,default=0 ,nullable=False)
    empate = Column(Integer,default=0 ,nullable=False)
    derrota = Column(Integer,default=0, nullable=False)
"""