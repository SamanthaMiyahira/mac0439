"""
Este script envia uma requisição HTTP POST para a API do Django
no endpoint '/api/confirmar-entrada/' para registrar a entrada
do veículo no estacionamento.

A confirmação é feita com a credencial e a placa do veículo.
"""

import requests

url = "http://localhost:8000/api/confirmar-entrada/"

data = {
    "qrcode": "https://example.com/qrcode123", 
    "placa": "YZA5B67"                          
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)

try:
    print("Resposta da API:", response.json())
except Exception as e:
    print("Erro ao ler JSON da resposta:", e)
