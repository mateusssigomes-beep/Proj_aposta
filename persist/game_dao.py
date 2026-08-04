from persist.base_dao import BaseDAO
from typing import List, Optional
from models.game import Game
from models.team import Team 
from sqlalchemy.orm import Session, joinedload 
from sqlalchemy.exc import SQLAlchemyError


class GameDao(BaseDAO):
    
    def adicionar (self, objeto: Game, db: Session) -> bool:
        '''Adiciona um novo registro no banco de dados, retornando True caso tenha sucesso'''        
        try:
            db.add(objeto)
            db.commit()
            db.refresh(objeto)
            return True
        except SQLAlchemyError as Erro:
            print(f'Erro: {Erro}')
            return False
    
    def excluir(self, id_game: int, db: Session) -> bool:
        '''Exclui regsitros procurando pelo ID, retorando True caso tenha sucesso'''
        game = db.query(Game).filter(Game.id == id_game).first()
        if not game:
            return False
        try:
            db.delete(game)
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f'Erro: {Erro}')
            return False
     
    def atualizar (self, id_game: int, objeto: Game, db: Session) -> bool:
        '''Edita e Atualiza os registros Existentes dentro do banco, retornando True caso tenha sucesso'''
        game = db.query(Game).filter(Game.id == id_game).first()
        if not game:
            return False
        try:
            game.data_jogo = objeto.data_jogo
            game.status = objeto.status
            game.time_vencedor = objeto.time_vencedor
            game.gol_time_casa = objeto.gol_time_casa
            game.gol_time_visitante = objeto.gol_time_visitante
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f'{Erro}')
            db.rollback()
            return False

    def pesquisar(self, id_game: int, db: Session) -> Optional[Game]:

        '''Pesquisa Regsitros Por ID, retornando o Objeto caso tenha sucesso, ou None caso não tenha nada
        
        Explicar do por que Usar o JoinedLoad() Para as FKs de Model: [Como funciona e o que esta fazendo aqui]
        '''
        return db.query(Game).options(
            joinedload(Game.time_casa),
            joinedload(Game.time_visitante)
        ).filter(Game.id == id_game).first()
    
    def listar_todos(self, db: Session) -> List[Game]:
        ''' Comando que lista todos os obejetos que já foram povoados dentro do Banco, Retorna  Obejto caso ache, e Nonoe caso não tenha nada'''
        return db.query().options(
            joinedload(Game.time_casa),
            joinedload(Game.gol_time_visitante)
        ).all()
