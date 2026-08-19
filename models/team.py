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
  
  


