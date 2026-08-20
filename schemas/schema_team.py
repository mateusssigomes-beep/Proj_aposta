from pydantic import BaseModel
 
 
class CriarTimeIn(BaseModel):
    nome: str
    grupo: str
 