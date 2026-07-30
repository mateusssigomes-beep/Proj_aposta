from persist.base_dao import BaseDAO
from typing import List, Optional
from models.team import Team
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError




class TeamDAO(BaseDAO):
        
    def adicionar (self, objeto: Team, db: Session) -> bool:
        '''Adiciona um novo registro no banco de dados, retornando True caso tenha sucesso'''        
        try:
            db.add(objeto)
            db.commit()
            db.refresh(objeto)
            return True
        except SQLAlchemyError as Erro:
            print(f'Eroo: {Erro}')
            return False
        
    
    
    def excluir(self, id_team: int, db: Session) -> bool:
        """
        Hard delete. Time não tem regra de negócio pedindo soft delete (diferente de User).
        Cuidado: se houver Game referenciando esse Team, a FK vai barrar a exclusão.
        """
        team = db.query(Team).filter(Team.id == id_team).first()
        if not team:
            return False
        try: 
            db.delete(team)
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f'Erro: `{Erro}')
            db.rollback()
            return False 

    
    
    def atualizar (self, id_team: int, objeto: Team, db: Session) -> bool:
        '''Edita e Atualiza os registros Existentes dentro do banco, retornando True caso tenha sucesso'''
        team = db.query(Team).filter(Team.id == id_team).first()
        if not team:
            return False
        try:
            team.nome = objeto.nome
            team.grupo = objeto.grupo
            team.vitoria  = objeto.vitoria
            team.derrota = objeto.derrota
            team.empate = objeto.empate
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f'Erro: {Erro}')
            db.rollback()
            return False
            
    
    
    def pesquisar(self, id_team: int, db: Session) -> Optional[Team]:

        '''Pesquisa Regsitros Por ID, Otional procura pelo objeto mas se não encontrar ele Retorna None'''
        return db.query(Team).filter(Team.id == id_team).first()
    
    def buscar_por_nome(self, nome: str, db: Session)-> Optional[Team]:
        """Busca um time pelo nome. Útil pra evitar duplicdade ao cadastrar"""
        return db.query(Team).filter(Team.nome == nome).first()
    
    def listar_todos(self, db: Session) -> List[Team]:
        ''' Comando que lista todos os obejetos que já foram povoados dentro do Banco, Retorna  Obejto caso ache, e Nonoe caso não tenha nada'''
        return db.query(Team).all()
    
    