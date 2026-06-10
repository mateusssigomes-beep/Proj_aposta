# from dataclasses import dataclass sera usado posteriormente

# @dataclass

#definindo o que tera dentro da calsse usuário
class Usario():
    def __init__(self, nome: str , idade: int, cpf: str , gmail: str, login: str, senha: str, admin: bool, pontos: int, acertos: int  ) -> None:
        self.nome = nome 
        self.idade = idade
        self._cpf = cpf
        self._gmail = gmail 
        self._login = login 
        self._senha = senha 
        self._admin = admin
        self.ponto = pontos 
        self.acertos = acertos 
        
        
        
        
        
        
    