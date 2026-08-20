#from types import SimpleNamespace # resolve problema do pydantic de receber dados em formatos incorretos
from fastapi import APIRouter, Depends, HTTPException
# Router Agrupas as rotas 
# depends injeta a sessão do banco 
# HTTp Sinaliza erro pro cliente

from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
# get pra abrir e fechar as sessões
from Service import User_Ser as user_service
# traz o service pra nós 
from schemas.schema_user import CadastroIn, LoginIn, TrocarSenha

router = APIRouter(prefix="/usuarios", tags=['Usuários'])


@router.post("/cadastro")
def cadastrar_usuario(dados: CadastroIn, db:Session = Depends(get_db)):
    usuario, erro = user_service.cadastrar(dados, db)
    if erro :
        raise HTTPException(status_code=400, detail=erro.value)
    
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "login": usuario.login,
        "pontos": usuario.pontos,
    }
    
    
@router.post("/login")
def login(dados: LoginIn, db: Session = Depends(get_db)):
    usuario = user_service.autenticar(dados.login, dados.senha, db)
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Login ou senha inválido")
    
    return{
        "id": usuario.id,
        "nome": usuario.nome,
        "login": usuario.login,
        "pontos": usuario.pontos,
        
    }
    
    
@router.put("/{id_user}/senha")
def trocar_senha(id_user: int, dados: TrocarSenha, db: Session = Depends(get_db)):
    sucesso = user_service.trocar_senha(id_user, dados.senha_atual, dados.senha_nova, db)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Não foi possível trocar a senha")
    return {"Mensagem": "Senha alterada com sucesso"}