from persist.base_dao import BaseDAO
from typing import  List , Optional
from models.user import User, StatusUsuario
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class UserDAO(BaseDAO):
    
    
    def adicionar(self, objeto: User, db: Session)-> bool: 
        '''
        Comando de adicionar, Com base no objeto recebido, retornando True ou False
        Adiciona, Commita(Salva a alteração), refresh para ver como esta a tebela com o objeto adicionado nela
        
        bd esta conectado diretamente com o Session 
        
        '''
        try:
            db.add(objeto) 
            db.commit()
            db.refresh(objeto)
            return True
        except SQLAlchemyError as erro:
            db.rollback()
            print(f'Erro: {erro}')
            return False
        
    def excluir(self, id_user: int, db: Session)-> bool:
        '''
        Usa primariamente a mesma lógica de filtro do Search | Retornando True e False, Ele não exclui verdadeiramente do banco, Apenas a tualiza o status User para INATIVO 
        '''
        usuario = db.query(User).filter(User.id == id_user).first()
        if not usuario:
            return False
        try:
            usuario.status = StatusUsuario.INATIVO
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f"Erro: {Erro}")
            db.rollback()
            return False

    def excluir_permanente(self, id_user: int, db: Session)-> bool:
        """
        Método que realmente exclui do banco de dados, Retornando True (Certo) e False (Falha)
        
        Método de com alvo de uso:
            manunteção 
            administração 
            limpeza
        """
        usuario = db.query(User).filter(User.id == id_user).first()
        if not usuario:
            return False
        try:
            db.delete(usuario)
            db.commit()
            return True
        except SQLAlchemyError as Erro:
            print(f"Erro: {Erro}")
            db.rollback()
            return False
    
    def atualizar(self, id_user: int, objeto: User, db: Session)-> bool:
        """
        Edita e Atuliza os Registros Esxitentes ,Retorna True caso tenha sucesso, False caso não 
        """
        usuario = db.query(User).filter(User.id == id_user).first()
        if not usuario:
            return False
        try:
            usuario.nome = objeto.nome
            usuario.data_nascimento = objeto.data_nascimento
            usuario.cpf = objeto.cpf
            usuario.email = objeto.email
            usuario.login = objeto.login
            usuario.status = objeto.status
            db.commit()
            return True
        except SQLAlchemyError as erro:
            print(f'Erro: {erro}')
            db.rollback()
            return False
    
    def pesquisar(self, id_user: int, db: Session)->Optional[User]: #->  Retorna None caso não econtre nem um User
    #return db.query(Classe).filter(Classe.campo == valor).first()
     return db.query(User).filter(User.id == id_user).first()
   
    def buscar_por_login(self, login: str, db: Session) -> Optional[User]:
        """Busca um usuário pelo campo login. Usado no fluxo de autenticação."""
        return db.query(User).filter(User.login == login).first()  
   
    def listar_todos(self, db:Session) -> List[User]:
        """
        """                
        return db.query(User).all()
    

    