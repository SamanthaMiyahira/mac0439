import requests
from datetime import datetime, timedelta

url = "http://localhost:8000/api/criar-evento/"

data = {
    "titulo": "Evento de Teste com Participantes",
    "responsavel_cpf": "888.999.000-11",
    "vagas_reservadas": 5,
    "data_hora": (datetime.now() + timedelta(days=1)).isoformat(),  # evento amanhã
    "participantes": [
        {
            "cpf": "987.654.321-00",
            "placa_veiculo": "XYZ4E56"
        },
        {
            "cpf": "555.666.777-88",
            "placa_veiculo": "STU9V01"
        }
    ]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Evento criado com sucesso!")
    print("ID do Evento:", response.json()["evento_id"])
else:
    print("Erro ao criar evento:", response.status_code)
    print(response.json())
