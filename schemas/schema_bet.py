
from pydantic import BaseModel



class RegistrarBetIn(BaseModel):
    id_game: int
    chute_gol_casa: int
    chute_gol_visitante: int
    pontos_apostados: int
    
    
class MultiplicarBetIn(BaseModel):
    fator: int