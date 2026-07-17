
from sqlalchemy.exc import IntegrityError 
from models.Persist.conexao_bd import testa_conec, fechaconec, sessaoloc, engine, Base
from models.team import Team
from models.user import User
from models.game import Game


if __name__ == "__main__":
    testa_conec()
    # fechaconec()



Base.metadaa.create_all(bind=engine)
db = sessaoloc



