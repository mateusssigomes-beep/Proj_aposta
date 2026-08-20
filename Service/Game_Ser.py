from typing import Optional
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from persist.game_dao import GameDAO
from persist.team_dao import TeamDAO
from models.game import Game, StatusGame
import Service.Bet_Ser as bet_service

gamedao = GameDAO()
teamdao = TeamDAO()

def criair_game(time_casa_id: int, time_visitante_id: int, data_jogo, db:Session) -> Optional[Game]:
    
    
    if time_casa_id == time_visitante_id:
        return None
    
    if not teamdao.pesquisar(time_casa_id, db) or not teamdao.pesquisar(time_visitante_id,db):
        return None
    
    novo_jogo = Game(
        data_jogo = data_jogo,
        time_casa_id = time_casa_id, 
        time_visitante_id = time_visitante_id,
    )
    
    sucesso = gamedao.adicionar(novo_jogo, db)
    if not sucesso:
        return None
    
    return novo_jogo



def iniciar_game(id_game: int, db: Session) -> bool:
    game = gamedao.pesquisar(id_game, db)
    if not game or game.status != StatusGame.MARCADO:
        return False
    
    game.status = StatusGame.ANDAMENTO
    try:
        db.commit()
        return True
    except SQLAlchemyError as erro:
        print(f'{erro}')
        db.rollback()
        return False
    



def encerrar_game(id_game: int, gol_casa : int, gol_visitante: int, db:Session ) -> bool:
    
    game = gamedao.pesquisar(id_game, db)
    if not game or game.status != StatusGame.ANDAMENTO:
        return False
    
    game.gol_time_casa = gol_casa
    game.gol_time_visitante = gol_visitante
    
    if gol_casa > gol_visitante:
        game.time_vencedor = game.time_casa.nome
    elif gol_visitante > gol_casa: 
        game.time_vencedor = game.time_visitante.nome 
    else:
        game.time_vencedor = None
        
    game.status = StatusGame.ENCERRADO
    
    try:
        db.commit()
    except SQLAlchemyError as erro:
        print(f'{erro}')
        db.rollback()
        return False
        
    return bet_service.final_game_bet(id_game, db)