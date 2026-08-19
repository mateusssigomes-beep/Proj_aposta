from typing import Optional
from sqlalchemy.orm import Session
from persist.bet_dao import BetDAO
from persist.game_dao import GameDAO
from persist.user_dao import UserDAO
from models.bet import Bet, StatusAposta
from models.game import Game, StatusGame
from models.user import User
from sqlalchemy.exc import SQLAlchemyError

betdao = BetDAO()
gamedao = GameDAO()
userdao = UserDAO()

def calcular_odd(id_game: int, db: Session) -> tuple[float, float]:
   """
   Calcula a odd atual (casa, visitante) com base nas apostas já registradas pro jogo.
   Parimutuel: odd_lado = 1 + (apostadores_lado_oposto / apostadores_lado).
   Quem apostou empate não entra na conta de nenhum dos dois lados.
   
   Equivale
   apostadores_casa = 0
   for pessoa in apostas:
    if pessoa.chute_gol_casa > pessoa.chute_gol_visitante:
        apostadores_casa += 1
   """
   apostas = betdao.listar_por_game(id_game, db)

   apostadores_casa = sum(1 for pessoa in apostas if pessoa.chute_gol_casa > pessoa.chute_gol_visitante)
   apostadores_visitante = sum(1 for pessoa in apostas if pessoa.chute_gol_casa < pessoa.chute_gol_visitante)

   odd_casa = 1 + (apostadores_visitante / apostadores_casa) if apostadores_casa > 0 else 1.0
   odd_visitante = 1 + (apostadores_casa / apostadores_visitante) if apostadores_visitante > 0 else 1.0

   return odd_casa, odd_visitante

 
def registrar_bet(id_user: int, id_game: int, chute_gol_casa: int, chute_gol_visitante: int, pontos_apostados: int, db: Session,) -> Optional[Bet]:
    """
    Registra uma nova aposta. Debita os pontos do usuário no momento do registro.
    Retorna a Bet criada, ou None se alguma validação falhar.
    """
    jogo = gamedao.pesquisar(id_game, db)
    if not jogo or jogo.status != StatusGame.MARCADO:
        return None
 
    usuario = userdao.pesquisar(id_user, db)
    if not usuario or usuario.pontos < pontos_apostados:
        return None
 
    odd_casa, odd_visitante = calcular_odd(id_game, db)
 
    if chute_gol_casa > chute_gol_visitante:
        multiplier = odd_casa
    elif chute_gol_casa < chute_gol_visitante:
        multiplier = odd_visitante
    else:
        multiplier = 1.0  # empate não multiplica, só devolve depois
 
    nova_aposta = Bet(
        multiplier=multiplier,
        pontos_apostados=pontos_apostados,
        chute_gol_casa=chute_gol_casa,
        chute_gol_visitante=chute_gol_visitante,
        status=StatusAposta.ANDAMENTO,
        idgame=id_game,
        iduser=id_user,
    )
    
    try:
       db.add(nova_aposta)
       usuario.pontos -= pontos_apostados
       db.commit()
       db.refresh(nova_aposta)
    except SQLAlchemyError:
       return None
       
 
    return nova_aposta
 
 
def multiplicar_bet(id_bet: int, id_user: int, fator: int, db: Session) -> bool:
    """
    Multiplica os pontos de uma aposta já existente (x2, x3, x4, x5...).
    O multiplier (odd) da aposta permanece o mesmo, snapshot original.
    """
    aposta = betdao.pesquisar(id_bet, db)
    if not aposta or aposta.iduser != id_user or aposta.status != StatusAposta.ANDAMENTO:
        return False
 
    usuario = userdao.pesquisar(id_user, db)
    if not usuario:
        return False
 
    pontos_totais_novos = aposta.pontos_apostados * fator
    diferenca = pontos_totais_novos - aposta.pontos_apostados
 
    if usuario.pontos < diferenca:
        return False
 
    aposta.pontos_apostados = pontos_totais_novos
    usuario.pontos -= diferenca
    db.commit()
 
    return True
 
 
def final_game_bet(id_game: int, db: Session) -> bool:
    """
    Chamado quando o jogo é encerrado (Game.time_vencedor já definido pelo GameService).
    Resolve o status de cada Bet e credita/devolve pontos ao usuário conforme resultado.
    """
    game = gamedao.pesquisar(id_game, db)
    if not game or game.status != StatusGame.ENCERRADO:
        return False
 
    apostas = betdao.listar_por_game(id_game, db)
 
    gol_casa_real = game.gol_time_casa
    gol_visitante_real = game.gol_time_visitante
 
    for aposta in apostas:
        usuario = userdao.pesquisar(aposta.iduser, db)
        if not usuario:
            continue
 
        palpite_casa_venceu = aposta.chute_gol_casa > aposta.chute_gol_visitante
        palpite_visitante_venceu = aposta.chute_gol_casa < aposta.chute_gol_visitante
        palpite_empate = aposta.chute_gol_casa == aposta.chute_gol_visitante
 
        real_casa_venceu = gol_casa_real > gol_visitante_real
        real_visitante_venceu = gol_casa_real < gol_visitante_real
        real_empate = gol_casa_real == gol_visitante_real
 
        acertou = (
            (palpite_casa_venceu and real_casa_venceu)
            or (palpite_visitante_venceu and real_visitante_venceu)
            or (palpite_empate and real_empate)
        )
 
        if real_empate:
            aposta.status = StatusAposta.EMPATE
            usuario.pontos += aposta.pontos_apostados  # devolve o valor apostado
        elif acertou:
            aposta.status = StatusAposta.VENCEU
            usuario.pontos += int(aposta.pontos_apostados * aposta.multiplier)
        else:
            aposta.status = StatusAposta.PERDEU
            # não credita nada, pontos já foram debitados no registro
 
    db.commit()
    return True