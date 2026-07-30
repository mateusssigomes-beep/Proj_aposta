from persist.base_dao import BaseDAO
from typing import List, Optional
from models.game import Game
from models.team import Team 
from sqlalchemy.orm import Session, joinedload, 
from sqlalchemy.exc import SQLAlchemyError


class GameDao(BaseDAO):
    
    
    def adicionar (self, objeto: Game, db: Session) -> bool:
        '''Adiciona um novo registro no banco de dados, retornando True caso tenha sucesso'''        
        pass
    
    
    def excluir(self, id: int, db: Session) -> bool:
        '''Exclui regsitros procurando pelo ID, retorando True caso tenha sucesso'''
        pass
    
    
    def atualizar (self, id_game: int, db: Session) -> bool:
        '''Edita e Atualiza os registros Existentes dentro do banco, retornando True caso tenha sucesso'''
        pass
    
    
    def pesquisar(self, id_game: int, db: Session) -> Optional[Game]:

        '''Pesquisa Regsitros Por ID, retornando o Objeto caso tenha sucesso, ou None caso não tenha nada'''
        return db.query(Game).options(
            joinedload(Game.time_casa),
            joinedload(Game.time_visitante)
        ).filter(Game.id == id_game).first()
    
    
    def listar_todos(self, db: Session) -> List[Any]:
        ''' Comando que lista todos os obejetos que já foram povoados dentro do Banco, Retorna  Obejto caso ache, e Nonoe caso não tenha nada'''
        return db.query()
