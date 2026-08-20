from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError 
from persist.conexao_bd import Sessaoloc, engine, Base
from models.team import Team
from models.user import User
from models.game import Game
from models.bet import Bet
from datetime import datetime
from Control.controle_user import router as router_user
from Control.controle_game import router as router_game
from Control.controle_bet import router as router_bet
from Service import api_externa
import Service.Game_Ser as game_service
from persist.team_dao import TeamDAO

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Apostas - Copa do Mundo 2026")

app.include_router(router_user)
app.include_router(router_game)
app.include_router(router_bet)



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
        print(f"{jogo.time_casa_id} vs {jogo.time_visitante.nome} — {jogo.data_jogo}")
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
    
    
    
    def seed():
        '''
        Popula o banco pro teste: sincroniza times da API externa,
        cria um jogo entre os 2 primeiros times e já encerra ele
        (histórico pronto pra HU7, times prontos pra Admin usar no HA4).
        '''
        criados = api_externa.Sincroinzar_times(db)
        print(f'{criados} time(s) sincronizado(s) da API')

        teamdao = TeamDAO()
        times = teamdao.listar_todos(db)
        if len(times) < 2:
            print('Não há times suficientes pra criar um jogo de teste')
            return

        jogo = game_service.criair_game(times[0].id, times[1].id, datetime.now(), db)
        if not jogo:
            print('Não foi possível criar o jogo de teste')
            return

        game_service.encerrar_game(jogo.id, 2, 1, db)
        print(f'Jogo de teste criado e encerrado: {times[0].nome} 2 x 1 {times[1].nome}')

    # teste()
    # dropBase()
    # createAll()
    seed()