from persist.comandos_dao import ComandosDAO
from typing import  List , Optional
from models.user import User, StatusUsuario
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class UserDAO(ComandosDAO):
    
    
    '''
    Comando e pesquiss por id, tendo três tipo de 'filtro', 
    '''
    
    def pesquisar(self, id: int, db: Session)->Optional[User]: #->  Retorna None caso não econtre nem um User
        #return db.query(Classe).filter(Classe.campo == valor).first()
        return db.query(User).filter(User.id == id).first()
    
    '''
    
    '''
    
    def adicionar(self, objeto: User ,db: Session)-> bool: 
        try:
            db.add(objeto)
            db.commit()
            db.refresh(objeto)
            return True 
        except SQLAlchemyError as erro:
            print(f'Erro: {erro}')
            db.rollback()
            return False 
                
        '''
        
        '''
        
    def excluir(self, id: int, db: Session)-> bool:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return False
        usuario.status = StatusUsuario.INATIVO
        db.commit()
        return True

    '''
    
    '''

    def excluir_permanente(self, id: int, db: Session)-> bool:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return False
        db.delete(usuario)
        db.commit()
        return True
    
    '''
    
    '''
    
    def atualizar(self, id: int,objeto: User, db: Session)-> bool:
        usuario = db.query(User).filter(User.id == id).first()
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
    
    '''
    
    '''
        
    def listar_todos(self, db:Session) -> List[User]:
        return db.query(User).all()
    

    