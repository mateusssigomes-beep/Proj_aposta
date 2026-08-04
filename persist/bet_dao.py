from persist.base_dao import BaseDAO
from typing import Any, List, Optional 
from models.bet import Bet
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class BetDAO(BaseDAO):
    
    def adicionar(self, objeto: Bet, db: Session) -> bool:
        try:
            db.add(objeto)
            db.commit()
            db.refresh(objeto)
            return True
        except SQLAlchemyError as Erro:
            print(f'{Erro}')
            db.rollback()
            return False
    
    def excluir(self, id_bet: int, db: Session) -> bool:
        bet = db.query(Bet).filter(Bet.id == id_bet).first()
        if not bet:
            return False
        try:
            db.delete(bet)
            db.commit()
            return  True
        except SQLAlchemyError as Erro:
            print(f'{Erro}')
            db.rollback()
            return False
    
    def atualizar(self, id_bet: int, objeto: Bet , db: Session) -> bool:
        bet = db.query(Bet).filter(Bet.id == id_bet).first()
        if not bet:
            return False
        try:
            bet.chute_gol_casa = objeto.chute_gol_casa
            bet.chute_gol_visitante = objeto.chute_gol_visitante
            bet.status = objeto.status
            bet.pontos_apostados = objeto.pontos_apostados
            bet.multiplier = objeto.multiplier
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f'{Erro}')
            return False
    
    def pesquisar(self, id_bet: int, db: Session) -> Optional[Bet]:
        return db.query(Bet).filter(Bet.id == id_bet).first()
    
    def listar_todos(self, db: Session) -> List[Bet]:
        return db.query(Bet).all()
    
      
    def listar_por_user(self, id_user: int,  db: Session) -> List[Bet]:
        return db.query(Bet).filter(Bet.iduser == id_user).all()
    
    def listar_por_game(self, id_game: int, db: Session) -> List[Bet]:
        return db.query(Bet).filter(Bet.idgame == id_game).all()