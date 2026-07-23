from abc import ABC, abstractmethod
from typing import Any,List  
from sqlalchemy.orm import Session
class BaseDAO(ABC):
    
    @abstractmethod
    def adicionar (self, objeto: Any, db: Session) -> bool:
        '''Adiciona um novo registro no banco de dados, retornando True caso tenha sucesso'''        
        pass
    
    @abstractmethod
    def excluir(self, id: int, db: Session) -> bool:
        '''Exclui regsitros procurando pelo ID, retorando True caso tenha sucesso'''
        pass
    
    @abstractmethod
    def atualizar (self, id: int, db: Session) -> bool:
        '''Edita e Atualiza os registros Existentes dentro do banco, retornando True caso tenha sucesso'''
        pass
    
    @abstractmethod
    def pesquisar(self, id: int, db: Session) -> Any:

        '''Pesquisa Regsitros Por ID, retornando o Objeto caso tenha sucesso, ou None caso não tenha nada'''
        pass
    
    @abstractmethod
    def listar_todos(self, db: Session) -> List[Any]:
        ''' Comando que lista todos os obejetos que já foram povoados dentro do Banco, Retorna  Obejto caso ache, e Nonoe caso não tenha nada'''
        pass
    
   