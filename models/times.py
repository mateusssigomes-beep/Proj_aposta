from dataclasses import dataclass
from aposta import Aposta    
 
@dataclass
class Jogo():
    id: int # Primary key 
    times: str # sempre dois times por jogo 
    status: str # mostrar quel time mais apostado na partida 
    gols_time1: int = 0
    gols_time2: int = 0
    usuarios_time1: int = 0
    usuarios_time2: int = 0