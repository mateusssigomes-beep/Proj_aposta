
from persist.game_dao import GameDAO
import Service.Game_Ser as game_service
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from persist.conexao_bd import get_db
from schemas.schema_game import CriarJogoIn, EncerrarJogoIn
from Service import api_externa
from persist.user_dao import UserDAO
router = APIRouter(prefix="/jogos", tags=['Jogos'])
gamedao = GameDAO()
userdao = UserDAO()

def verificar_admin(x_user_id: int = Header(),db:Session = Depends(get_db)):
    """Checagem rápida"""
    user = userdao.pesquisar(x_user_id, db)
    if not user or not user.admin:
        raise HTTPException(status_code = 403, detail="Acesso restrito a Adms")
    return user

def _serializar(game):
    return { 
            "id": game.id,
            "time_casa": game.time_casa.nome,
            "time_visitante": game.time_visitante.nome,
            "data_jogo": game.data_jogo,
            "status": game.status.nome,
            "gol_time_casa": game.gol_time_casa,
            "gol_time_visitante": game.gol_time_visitante,
            "time_vencedor": game.time_vencedor,
            }

@router.get("/")
def listar_jogo(db:Session = Depends(get_db)):
    games = gamedao.listar_todos(db)
    return [_serializar(game) for game in games]

@router.get("/time/{nome_time}")
def jogos_do_time(nome_time: str, db: Session = Depends(get_db)):
    games = gamedao.listar_todos(db)
    from models.game import StatusGame
    resultado = [
        _serializar(game) for game in games
        if game.status == StatusGame.ENCERRADO
        and (game.time_casa.nome == nome_time or game.time_visitante.nome == nome_time)
    ]
    return resultado

@router.post("/" ,dependencies=[Depends(verificar_admin)])
def criar_jogo(dados: CriarJogoIn, db: Session = Depends(get_db)):
    game = game_service.criair_game(dados.time_casa_id, dados.time_visitante_id, dados.data_jogo, db)
    if not game:
        raise HTTPException(status_code = 400, detail="Não foi possível criar o jogo")
    
    return _serializar(game)
    
@router.put("/{id_game}/iniciar",dependencies=[Depends(verificar_admin)])
def iniciar_jogo(id_game: int , db:Session = Depends(get_db)):
    sucesso = game_service.iniciar_game(id_game, db)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Não foi possível inicair o jogo")
    return {"Mensagem": "Jogo iniciado"}

@router.put("/{id_game}/encerrar",dependencies=[Depends(verificar_admin)])
def encerrar_jogo(id_game: int, dados: EncerrarJogoIn, db: Session = Depends(get_db)):
    sucesso = game_service.encerrar_game(id_game, dados.gol_casa, dados.gol_visitante, db)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Não foi possível encerrar o jogo")
    return {"Mensagem": "Jogo encerrado com Sucesso"}

@router.post("/sincronizar", dependencies=[Depends(verificar_admin)])
def sincronizar_times(db: Session = Depends(get_db)):
    criados = api_externa.Sincroinzar_times(db)
    return {"mensagem": f"{criados} time(s) novo(s) criado(s)"}