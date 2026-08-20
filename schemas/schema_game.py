from pydantic import BaseModel
from datetime import datetime


class CriarJogoIn(BaseModel):
    time_casa_id: int
    time_visitante_id: int
    data_jogo: datetime
    
    
class EncerrarJogoIn(BaseModel):
    gol_casa: int
    gol_visitante: int