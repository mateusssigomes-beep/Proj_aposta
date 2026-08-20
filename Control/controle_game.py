from persist.game_dao import GameDAO
import Service.Game_Ser as game_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
from schemas.schema_game import CriarJogoIn, EncerrarJogoIn

router = APIRouter(prefix="jogos", tags=['Jogos'])
gamedao = GameDAO()

def _serializar(game):
    return { }



@router.get("/")
def listar_jogo(db:Session = Depends(get_db)):
    games = gamedao.listar_todos(db)
    return [_serializar(game) for game in games]



@router.post("/")
def criar_jogo(dados: CriarJogoIn, db: Session = Depends(get_db)):
    game = game_service.criair_game(dados.time_casa_id, dados.time_visitante_id, dados.data_jogo, db)
    if not game:
        raise HTTPException(status_code = 400, detail="Não foi possível criar o jogo")
    
    
@router.put("/{id_game}/iniciar")
def iniciar_jogo(id_game: int , db:Session = Depends(get_db)):
    sucesso = game_service.iniciar_game(id_game, db)
    if not sucesso:
        raise HTTPE

@router.put("/{id_game}/encerrar")
def encerrar_jogo(id_game: int, dados: EncerrarJogoIn, db: Session = Depends(get_db)):
    sucesso = game_service.encerrar_game(id_game, dados.gol_casa, dados.gol_visitante, db)