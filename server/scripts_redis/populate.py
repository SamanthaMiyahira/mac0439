import random
from datetime import datetime, timedelta
from server.api.services.mapa import criar_vaga
import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
# django.setup()

tipos_vaga = ["convencional", "eletrica", "preferencial"]
status_vaga = ["disponivel", "ocupada", "reservada"]

def gerar_placa():
    letras = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = ''.join(random.choices("0123456789", k=4))
    return f"{letras}{numeros}"

def gerar_cpf():
    return ''.join(random.choices("0123456789", k=11))

def gerar_hora_entrada():
    agora = datetime.now()
    entrada = agora - timedelta(minutes=random.randint(0, 240))
    return entrada.strftime("%Y-%m-%d %H:%M")

def popular_redis(qtd=20):
    for i in range(1, qtd + 1):
        vaga_id = f"A{i:02}"  # A01, A02, ..., A20
        criar_vaga(
            vaga_id=vaga_id,
            status=random.choice(status_vaga),
            tipo=random.choice(tipos_vaga),
            placa=gerar_placa(),
            cpf=gerar_cpf(),
            hora_entrada=gerar_hora_entrada()
        )
    print(f"{qtd} vagas inseridas no Redis com sucesso.")

popular_redis()
