import requests
from persist.team_dao import TeamDAO
from models.team import Team

teamdao = TeamDAO()
CHAVE_API = "123" # gratis 
URL = "https://www.thesportsdb.com/api/v1/json/"
LIGA = "4429" # É pra ser da copa do mundo


def buscar_times_copa()-> list[dict]:
    """
    Busca a lista de times da liga configurada em LIGA.
    Retorna uma lista de dicionários brutos da API, ou [] se algo falhar.
    """
    url = f"{URL}/{CHAVE_API}/lookup_all_teams.php"
    id_liga = {"id": LIGA}
    
    try:
        reposta = requests.get(url, params=id_liga,  timeout=10)
        reposta.raise_for_status()
    except requests.RequestException as erro:
        print(f'{erro}')
        return []
 
    dados = reposta.json()
    return dados.get("teams") or []
 
def Sincroinzar_times(db) -> int:
    """
    Busca os times da API externa e cria os que ainda não existem no banco
    (checagem por nome, via TeamDAO.buscar_por_nome).
    Retorna a quantidade de times novos criados.
    """
    times_api = buscar_times_copa()
    criados = 0
    
    for time in times_api:
        nome = (time.get("strTeam") or "")[:40]
        grupo = (time.get("strLeague") or "Sem grupo")[:40]
 
        if not nome or teamdao.buscar_por_nome(nome, db):
            continue
 
        novo_time = Team(nome=nome, grupo=grupo)
        if teamdao.adicionar(novo_time, db):
            criados += 1
 
    return criados