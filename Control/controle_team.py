from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
from persist.team_dao import TeamDAO
from persist.user_dao import UserDAO
from models.team import Team
from schemas.schema_team import CriarTimeIn
from Service import api_externa
 
router = APIRouter(prefix="/times", tags=["Times"])
teamdao = TeamDAO()
userdao = UserDAO()
 
 
def verificar_admin(x_user_id: int = Header(...), db: Session = Depends(get_db)):
    """
    Checagem provisória de admin, via header X-User-Id.
    Não substitui autenticação de verdade (token) - fica marcado como pendência
    pra evoluir depois. Serve só pra barrar rotas de Admin por enquanto.
    """
    usuario = userdao.pesquisar(x_user_id, db)
 
    if not usuario or not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
 
    return usuario
 
 
def _serializar(time):
    return {
        "id": time.id,
        "nome": time.nome,
        "grupo": time.grupo,
        "vitoria": time.vitoria,
        "empate": time.empate,
        "derrota": time.derrota,
    }
 
 
@router.get("/")
def listar_times(db: Session = Depends(get_db)):
    times = teamdao.listar_todos(db)
    return [_serializar(time) for time in times]
 
 
@router.post("/", dependencies=[Depends(verificar_admin)])
def criar_time(dados: CriarTimeIn, db: Session = Depends(get_db)):
    if teamdao.buscar_por_nome(dados.nome, db):
        raise HTTPException(status_code=400, detail="Time já cadastrado")
 
    novo_time = Team(nome=dados.nome, grupo=dados.grupo)
 
    sucesso = teamdao.adicionar(novo_time, db)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Não foi possível criar o time")
 
    return _serializar(novo_time)
 
 
@router.post("/sincronizar", dependencies=[Depends(verificar_admin)])
def sincronizar_times(db: Session = Depends(get_db)):
    criados = api_externa.Sincroinzar_times(db)
    return {"mensagem": f"{criados} time(s) novo(s) criado(s)"}