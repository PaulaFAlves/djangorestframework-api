from datetime import date
import requests
from django.conf import settings
import logging

def is_feriado(data: date) -> bool:
  logging.info(f"Fazendo requisicao para BrasilAPI para a data {data.isoformat()}")
  if settings.TESTING == True:
    if data.day == 25 and data.month == 12:
      return True
    return False

  ano = data.year
  r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}/") 

  if r.status_code != 200:
    logging.error("Algum erro aconteceu na BrasilAPI")
    return False

  feriados = r.json()
  for feriado in feriados:
    data_feriado_as_str = feriado["date"]
    data_feriado = date.fromisoformat(data_feriado_as_str)

    if data_feriado == data:
      return True

  return False