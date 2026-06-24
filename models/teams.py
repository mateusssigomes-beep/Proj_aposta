from dataclasses import dataclass, field 
from datetime import datetime


@dataclass
class Team():
    _id: int # primary key 
    _nome: str # noem do time em jogo 