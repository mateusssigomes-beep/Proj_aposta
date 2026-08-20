from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
from Service import Bet_Ser as bet_service
from schemas.schema_bet import RegistrarBetIn, MultiplicarBetIn
from persist.bet_dao import BetDAO


betdao = BetDAO()
router = APIRouter(prefix="/apostas", tags=['Aposta'])

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