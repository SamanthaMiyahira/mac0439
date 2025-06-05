"""
Este script envia uma requisição HTTP POST para a API do Django
no endpoint 'http://localhost:8000/api/criar-reserva/' para criar
uma nova reserva de vaga de estacionamento.
"""

import requests

url = "http://localhost:8000/api/criar-reserva/"

data = {
    "cpf": "444.555.666-77",  #visitante                           
    "tipo": "recorrente",                     
    "periodo": "01:00:00"                   
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)

try:
    print("Resposta da API:", response.json())
except Exception as e:
    print("Erro ao ler JSON da resposta:", e)
