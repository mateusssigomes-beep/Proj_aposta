from typing import Optional
from models.user import User, StatusUsuario
from persist.user_dao import UserDAO
from sqlalchemy.orm import Session
from datetime import date
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
import enum



ph = PasswordHasher()
user_dao = UserDAO()

class ErroCadastro(enum.Enum):
    IDADE_INVALIDA = "Usuário deve ter 18 anos ou mais"
    SENHA_FRACA = "Senha não atende aos requisitos mínimos"
    LOGIN_EXISTENTE = "Login já cadastrado"
    EMAIL_EXISTENTE = "Email já cadastrado"
    CPF_EXISTENTE = "CPF já cadastrado"
    ERRO_INTERNO = "Erro Genérico"

def validar_idade(data:date)-> bool:
    hoje = date.today()
    idade = hoje.year - data.year
    if (hoje.month, hoje.day) < (data.month, data.day):
        idade -= 1 
    return idade >= 18

def validar_forca_senha(senha: str) -> bool:
    if len(senha) < 8:
        return False
    
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_especial = any(not c.isalnum() for c in senha)  # não é letra nem número
    
    return tem_maiuscula and tem_minuscula and tem_numero and tem_especial

def cadastrar(dados, db:Session)-> tuple[Optional[User], Optional[ErroCadastro]]:
    # Regra: User deve ser maior de 18
    if not validar_idade(dados.data_nascimento):
        return None, ErroCadastro.IDADE_INVALIDA
    #regra: Senha deve possuir os requisitos mínimos 
    if not validar_forca_senha(dados.senha):
        return None, ErroCadastro.SENHA_FRACA
    #Tratamento CPF
    cpf_tratado = ''.join(filter(str.isdigit, dados.cpf))
    #Regra: Login não pode estar cadastrado
    if user_dao.buscar_por_login(dados.login, db):
        return None, ErroCadastro.LOGIN_EXISTENTE
    # Regra: Cpf não pode exsitir antes do cadastro 
    if user_dao.buscar_por_cpf(dados.cpf_tratado,db):
        return None, ErroCadastro.CPF_EXISTENTE
    # Regra Email Não pode estar existir antes do cadastro 
    if user_dao.buscar_por_email(dados.email, db):
        return None, ErroCadastro.EMAIL_EXISTENTE
    
    hash_senha = ph.hash(dados.senha)
    
    novo_usuario = User(
        
        nome = dados.nome,
        data_nascimento = dados.data_nascimento,
        cpf = dados.cpf_tratado,
        senha_hash = hash_senha,
        email = dados.email,
        login = dados.login,
    )
    sucesso = user_dao.adicionar(novo_usuario, db)
    if not sucesso:
        return None, ErroCadastro.ERRO_INTERNO 
    
    return novo_usuario, None 

def autenticar(login:str, senha: str, db:Session) -> Optional[User]:
    usuario = user_dao.buscar_por_login(login, db)
    if not usuario or usuario.status != StatusUsuario.ATIVO:
        return None
    
    try:
        ph.verify(usuario.senha_hash, senha)
        return usuario
    except VerificationError:
        return None

def trocar_senha(id_user: int , senha_atual: str, senha_nova: str, db:Session) -> bool:
    usuario = user_dao.pesquisar(id_user, db)
    if not usuario:
        return False
    
    if not validar_forca_senha(senha_nova):
        return False
    
    try:
        ph.verify(usuario.senha_hash, senha_atual)
    except VerificationError:
        return False
    
    novo_hash = ph.hash(senha_nova)
    return user_dao.atualizar_senha(id_user, novo_hash, db)