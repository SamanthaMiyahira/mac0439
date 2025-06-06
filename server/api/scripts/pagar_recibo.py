"""
Este script realiza duas operações na API do Django:

1. Envia uma requisição HTTP GET para listar os recibos pendentes de um visitante,
   usando o CPF como parâmetro na URL.

2. Envia uma requisição HTTP POST para pagar um recibo específico, informando
   o CPF do visitante, o ID do recibo e o método de pagamento.
"""

import requests

BASE_URL = "http://localhost:8000/api/recibos"  # ajuste conforme seu endpoint base

cpf = "444.555.666-77"  # visitante para teste

# 1. Listar recibos pendentes
url_listar = f"{BASE_URL}/pendentes/{cpf}/"

response = requests.get(url_listar)

print("Status code (listar recibos pendentes):", response.status_code)
try:
    print("Resposta da API (recibos pendentes):", response.json())
except Exception as e:
    print("Erro ao ler JSON da resposta:", e)


# 2. Pagar o primeiro recibo que aparecer
recibos = []
try:
    recibos = response.json()
except Exception as e:
    print("Erro ao ler JSON da resposta:", e)

if recibos:
    primeiro_recibo_id = recibos[0].get('_id') or recibos[0].get('id')
    if primeiro_recibo_id:
        url_pagar = f"{BASE_URL}/pagar/"
        data_pagamento = {
            "cpf": cpf,
            "recibo_id": primeiro_recibo_id,
            "metodo_pagamento": "PIX"
        }

        response_pagamento = requests.post(url_pagar, json=data_pagamento)

        print("Status code (pagar recibo):", response_pagamento.status_code)
        try:
            print("Resposta da API (pagamento):", response_pagamento.json())
        except Exception as e:
            print("Erro ao ler JSON da resposta:", e)
    else:
        print("ID do primeiro recibo não encontrado.")
else:
    print("Nenhum recibo pendente encontrado para pagamento.")

