from pydantic import BaseModel
from datetime import date

class CadastroIn(BaseModel):
    nome: str 
    data_nascimento: date
    cpf: str 
    email: str 
    login: str 
    senha: str 
    
    
class LoginIn(BaseModel):
    login: str 
    senha: str   
    
class TrocarSenha(BaseModel):
    senha_atual: str
    senha_nova: str
    
    