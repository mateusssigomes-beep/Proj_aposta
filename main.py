
from sqlalchemy.exc import IntegrityError 
from persist.conexao_bd import Sessaoloc, engine, Base
from models.team import Team
from models.user import User
from models.game import Game
from datetime import datetime


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = Sessaoloc()
    def teste():
        #Adicionando o time 
        time_teste = Team(nome = 'Barcelona', grupo = 'B', vitoria = 5, empate = 0, derrota = 0)
        time_teste2 = Team(nome = 'Gremio', grupo = 'B', vitoria = 5, empate = 3, derrota = 0 )
        #db acessando Sessaoloc = Session para injetar dentro do banco de dados 
        db.add(time_teste)
        db.add(time_teste2)
        db.commit()
        print(f'{time_teste}\n{time_teste2}')
        # Adicionando um Jogo com dois times tendo o mesmo id
        jogo = Game(
            data_jogo = datetime(2026, 7, 20, 17),
            time_casa_id = time_teste.id,
            time_visitante_id = time_teste2.id
        )
        db.add(jogo)
        id_jogo = 1
        jogo = db.query(Game).filter(Game.id == id_jogo).first()
        print(f"{jogo.time_casa.nome} vs {jogo.time_visitante.nome} — {jogo.data_jogo}")
        try:
            db.commit()
            db.rollback()
            print('Erro: Aceitou suas Foreign Keys, iguais')
        except IntegrityError as erro:
            db.rollback()
            print('Banco rejeitu sua adição de Jogos')
            print(f'Detalhe do Erro: {erro}')
            
        db.close()
        
    def dropBase():
        try:
            Base.metadata.drop_all(bind = engine)
            print('Tabelas destruidas')
            db.close()
        except IntegrityError as erro:
            print(f'Erro: {erro}')
            
    def createAll():
        try:
            Base.metadata.create_all(bind = engine)
            print('Tabelas Contruidas Novamente')
            db.close()
        except IntegrityError as erro:
            print(f'Erro: {erro}')     
    
    
    
    # teste()
    # dropBase()
    # createAll()