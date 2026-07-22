from abc import ABC, abstractmethod
from typing import Any,List  

class ComandosDAO(ABC):
    """
    Garante que todas as classes DAO Obrigatóriamente herdem e Usem os métodos que estão na classe (DAO) abstrata
    """
    
    @abstractmethod
    def adicionar (self, objeto: Any) -> bool:
        '''Adiciona um novo registro no banco de dados, retornando True caso tenha sucesso'''        
        pass
    
    @abstractmethod
    def excluir(self, id: int) -> bool:
        '''Exclui regsitros procurando pelo ID, retorando True caso tenha sucesso'''
        pass
    
    @abstractmethod
    def editar(self, id: int, objeto: Any) -> bool:
        '''Edita e Atualiza os registros Existentes dentro do banco, retornando True caso tenha sucesso'''
        pass
    
    @abstractmethod
    def pesquisar(self, id: int) -> Any:
        return
        '''Pesquisa Regsitros Por ID, retornando o Objeto caso tenha sucesso, ou None caso não tenha nada'''
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Any]:
        ''' Comando que lista todos os obejetos que já foram povoados dentro do Banco, Retorna  Obejto caso ache, e Nonoe caso não tenha nada'''
        pass