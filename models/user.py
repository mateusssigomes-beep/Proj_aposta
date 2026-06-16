from dataclasses import dataclass

#definindo o que tera dentro da calsse usuário
@dataclass
class Usuario():
    _nome: str # nome do usuario real 
    _idade: int # idade real 
    _cpf: str # cpf do usuario real
    gmail: str # gmail, com conferencia de gmail 
    _login: str # login para o usuario entrar no sistema, com conferencia de login
    _senha: str # conferencia de senha
    admin: bool # se adimin == true se user == false, não contem quantidade de pontos 
    pontos: int = 100 # quantidae de pontos que cada conta vai possuir, se for adm não tem quantidade de pontos 
    acertos: int = 0 # começa zerado para cada user, mas pode ser alterado 
    