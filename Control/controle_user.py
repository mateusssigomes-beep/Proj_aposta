#from types import SimpleNamespace # resolve problema do pydantic de receber dados em formatos incorretos
from fastapi import APIRouter, Depends, HTTPException, Header
# Router Agrupas as rotas 
# depends injeta a sessão do banco 
# HTTp Sinaliza erro pro cliente

from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
# get pra abrir e fechar as sessões
from Service import User_Ser as user_service
# traz o service pra nós 
from schemas.schema_user import CadastroIn, LoginIn, TrocarSenha
from persist.user_dao import UserDAO 

userdao = UserDAO()
router = APIRouter(prefix="/usuarios", tags=['Usuários'])


def verificar_admin(x_user_id: int = Header(),db:Session = Depends(get_db)):
    """Checagem rápida"""
    usuario = userdao.pesquisar(x_user_id, db)
    if not usuario:
        raise HTTPException(status_code = 403, detail="Acesso restrito a Adms")
    return usuario


def _serializar(usuario):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "login": usuario.login,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "status": usuario.status.name,
        "pontos": usuario.pontos,
        "admin": usuario.admin,
    }

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
    
@router.put("/{id_user}/cancelar")
def cancelar_participacao(id_user: int, db: Session = Depends(get_db)):
    sucesso = userdao.excluir(id_user, db)
 
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
 
    return {"mensagem": "Participação cancelada, usuário marcado como inativo"}
 
 
@router.get("/{id_user}/pontos")
def consultar_pontos(id_user: int, db: Session = Depends(get_db)):
    usuario = userdao.pesquisar(id_user, db)
 
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"id": usuario.id, "pontos": usuario.pontos}   
    
    
@router.put("/{id_user}/senha")
def trocar_senha(id_user: int, dados: TrocarSenha, db: Session = Depends(get_db)):
    sucesso = user_service.trocar_senha(id_user, dados.senha_atual, dados.senha_nova, db)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Não foi possível trocar a senha")
    return {"Mensagem": "Senha alterada com sucesso"}


@router.get("/", dependencies=[Depends(verificar_admin)])
def listar_usuario(db:Session = Depends(get_db)):
    usuarios = userdao.listar_todos(db)
    return [_serializar(usuario) for usuario in usuarios]

@router.get("/cpd/{cpf}", dependencies=[Depends(verificar_admin)])
def buscar_user_cpf(cpf: str, db: Session = Depends(get_db)):
    usuario = userdao.buscar_por_cpf(cpf, db)
    
    if not usuario:
        raise HTTPException(status_code=404, detail = "Deu rui pra pesquisar por cpf ")
    
    return _serializar(usuario)

