from dataclasses import dataclass
from datetime import datetime
from validate_docbr import CPF
#definindo o que tera dentro da calsse usuário
@dataclass
class Usuario():
    _id: int 
    _nome: str # nome do usuario real 
    _data_nascimento: datetime # idade real 
    _cpf: str # cpf do usuario real
    gmail: str # gmail, com conferencia de gmail 
    _login: str # login para o usuario entrar no sistema, com conferencia de login
    _senha: str # conferencia de senha
    admin: bool # se adimin == true se user == false, não contem quantidade de pontos 
    ranking: int = 0 # : to-do  
    
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, value):
        cpf = CPF()
        cpf.validate(value)
        if cpf == True:
            print()
    
    