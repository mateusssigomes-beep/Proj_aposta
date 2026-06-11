from dataclasses import dataclass, field
from user import Usuario


@dataclass
class Aposta():
    resultado: str # defini quem venceu 
    pontos: int # quantidade de pontos apostados
    status: str # status da aposta (pendente, em andamento, finalizada)
    palpites: list = field(default_factory=list) # quantidade de palpites feitos para aquela aposta
    multiplicador: float = 1.0 # odd por times 
    usuarios_apostando: int = 0 # quantidade de usuarios apostando naquele resultado
    
        
    def criar_aposta(self):
        pass 
        
    
    
    
