from dataclasses import dataclass  # sera usado posteriormente 

@dataclass
class Aposta():
    def __init__(self, resultado: str , pontos: int , palppites: int , multiplicador: float, satatus: str, usuarios_apostando: int) -> None:
        self._resutlado = resultado
        self._pontos = pontos
        self._palpites = palppites
        self._multiplicador = multiplicador
        self._status = satatus
        self._usuarios_apostando = usuarios_apostando
        
        
    
    
    
