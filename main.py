
from sqlalchemy.exc import IntegrityError 
from persist.conexao_bd import sessaoloc, engine, Base
from models.team import Team
from models.user import User
from models.game import Game


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = sessaoloc()
    
    #Adicionando o time 
    time_teste = Team(nome = 'Barcelona', grupo = 'B', vitoria = 5, empate = 0, derrota = 0)
    #db acessando sessaoloc = Session para injetar dentro do banco de dados 
    db.add(time_teste)
    db.commit()
    print(f'{time_teste} Adicionado a lista de times')
    # Adicionando um Jogo com dois times tendo o mesmo id
    jogo = Game(
        data_jogo = '20/07/2026 17:00',
        time_casa_id = time_teste.id,
        time_visitante_id = time_teste.id
    )
    db.add(jogo)
    try:
        db.commit()
        print('Erro: Aceitou suas Foreign Keys, iguais')
    except IntegrityError as erro:
        db.rollback()
        print('Banco rejeitu sua adição de Jogos')
        print(f'Detalhe do Erro: {erro}')
        
    db.close()