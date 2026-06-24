from abc import ABC, abstractmethod
from typing import Any
class ComandosDAO(ABC):
    
    
    @abstractmethod
    def adicioanr (self, objeto: Any) -> bool:
        pass
    
    @abstractmethod
    def excluir(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def update(self, id: int, obejto: Any) -> bool:
        pass
    
    @abstractmethod
    def search(self, id: int) -> Any:
        pass