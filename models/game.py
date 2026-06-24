from dataclasses import dataclass
from models.bet import Aposta    
from datetime import datetime
@dataclass
class Jogo():
    id: int # Primary key
    id_team: int # Foreign key para o time em jogo
    status: str # mostrar quel time mais apostado na partida 
    data_do_jogo: datetime 
    