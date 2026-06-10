from dataclasses import dataclass  # sera usado posteriormente

class Jogo():
    def __init__(self, id: int, times: str, gols_time1: int, gols_time2: int, status: str, usuarios_time1: int, usuarios_time2: int) -> None:
        self._id = id
        self._times = times
        self._gols_time1 = gols_time1
        self._gols_time2 = gols_time2
        self._status = status
        self._usuarios_time1 = usuarios_time1
        self._usuarios_time2 = usuarios_time2