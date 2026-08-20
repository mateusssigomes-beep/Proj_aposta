from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
from Service import Bet_Ser as bet_service
from schemas.schema_bet import RegistrarBetIn, MultiplicarBetIn
from persist.bet_dao import BetDAO
from persist.game_dao import GameDAO
from models.bet import StatusAposta
from persist.user_dao import UserDAO

userdao = UserDAO()
gamedao = GameDAO()
betdao = BetDAO()
router = APIRouter(prefix="/apostas", tags=['Aposta'])

def verificar_admin(x_user_id: int = Header(),db:Session = Depends(get_db)):
    """Checagem rápida"""
    user = userdao.pesquisar(x_user_id, db)
    if not user or not user.admin:
        raise HTTPException(status_code = 403, detail="Acesso restrito a Adms")
    return user

def _serializar(bet):
    return {
    "id": bet.id,
    "id_game": bet.idgame,
    "chute_gol_casa": bet.chute_gol_casa,
    "chute_gol_visitante": bet.chute_gol_visitante,
    "pontos_apostados": bet.pontos_apostados,
    "multiplier": bet.multiplier,
    "status": bet.status.name,
}

@router.post("/usuarios/{id_user}")
def registrar_aposta(id_user: int, dados: RegistrarBetIn, db: Session = Depends(get_db)):
    bet = bet_service.registrar_bet(
        id_user,
        dados.id_game,
        dados.chute_gol_casa,
        dados.chute_gol_visitante,
        dados.pontos_apostados,
        db,
    )
    
    if not bet:
        raise HTTPException(status_code = 400, detail ="não foi possível registrar a aposta")
    
    return _serializar(bet)


@router.put("/{id_bet}/usuarios/{id_user}/multiplicar")
def multiplicar_aposta(id_bet: int, id_user: int, dados: MultiplicarBetIn, db: Session = Depends(get_db)):
    sucesso = bet_service.multiplicar_bet(id_bet,id_user, dados.fator, db)
    
    if not sucesso:
        raise HTTPException(status_code= 400, detail="Não foi possível multiplicar a aposta")
    
    return {"Mensagem": "Aposta multiplcada"}    
    
@router.get("/{id_bet}")
def status_aposta(id_bet: int, db: Session = Depends(get_db)):
    bet = betdao.pesquisar(id_bet, db)

    if not bet:
        raise HTTPException(status_code=404, detail="Aposta não encontrada")
    
    return _serializar(bet)
    
    
@router.get("/usuarios/{id_user}")
def listar_apostas_usuario(id_user: int, db: Session = Depends(get_db)):
    apostas = betdao.listar_por_user(id_user, db)
    return [_serializar(aposta) for aposta in apostas]


@router.get("/jogos/{id_game}", dependencies=[Depends(verificar_admin)])
def listar_apostas_do_jogo(id_game: int, db: Session = Depends(get_db)):
    apostas = betdao.listar_por_game(id_game, db)
    return [_serializar(aposta) for aposta in apostas]
 
 
@router.get("/jogos/{id_game}/resumo")
def listar_aposta_do_jogo_r(id_game:int ,db: Session = Depends(get_db)):
    game = gamedao.pesquisar(id_game, db)
    if not game:
        raise HTTPException(status_code = 404, detail="jogo não encontrado")
        
    apostas = betdao.listar_por_game(id_game, db)
    apostadores_casa = sum(1 for a in apostas if a.chute_gol_casa > a.chute_gol_visitante)
    apostadores_visitante = sum(1 for a in apostas if a.chute_gol_casa < a.chute_gol_visitante)
    odd_casa, odd_visitante = bet_service.calcular_odd(id_game, db)
 
    return {
    "id_game": game.id,
    "time_casa": game.time_casa.nome,
    "time_visitante": game.time_visitante.nome,
    "apostadores_casa": apostadores_casa,
    "apostadores_visitante": apostadores_visitante,
    "odd_casa": round(odd_casa, 2),
    "odd_visitante": round(odd_visitante, 2),
    }
 
    
@router.get("/ranking")
def ranking_apostadores(db: Session = Depends(get_db)):
    apostas = betdao.listar_todos(db)
 
    acertos = {}
    for aposta in apostas:
        if aposta.status == StatusAposta.VENCEU:
            acertos[aposta.iduser] = acertos.get(aposta.iduser, 0) + 1
 
    ranking = []
    for id_user, total_acertos in acertos.items():
        usuario = userdao.pesquisar(id_user, db)
        if usuario:
            ranking.append({"id": usuario.id, "nome": usuario.nome, "acertos": total_acertos})
 
    ranking.sort(key=lambda u: u["acertos"], reverse=True)
    return ranking