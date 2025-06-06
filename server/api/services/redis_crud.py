import json
from api.utils.redis_client import redis_client

STATUS_VALIDOS = {"disponivel", "ocupada", "reservada"}
TIPOS_VALIDOS = {"convencional", "eletrica", "preferencial"}

def criar_vaga(vaga_id, status, tipo, placa, cpf, hora_entrada):
    if status not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido: '{status}'. Status válidos: {STATUS_VALIDOS}")
    if tipo not in TIPOS_VALIDOS:
        raise ValueError(f"Tipo inválido: '{tipo}'. Tipos válidos: {TIPOS_VALIDOS}")

    key = f"vaga:{vaga_id}"
    data = {
        "status": status,
        "tipo": tipo,
        "placa": placa,
        "cpf": cpf,
        "hora_entrada": hora_entrada
    }
    redis_client.set(key, json.dumps(data))

def ler_vaga(vaga_id):
    key = f"vaga:{vaga_id}"
    data = redis_client.get(key)
    return json.loads(data) if data else None

def atualizar_vaga(vaga_id, novos_dados):
    if "status" in novos_dados and novos_dados["status"] not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido: '{novos_dados['status']}'. Válidos: {STATUS_VALIDOS}")
    if "tipo" in novos_dados and novos_dados["tipo"] not in TIPOS_VALIDOS:
        raise ValueError(f"Tipo inválido: '{novos_dados['tipo']}'. Válidos: {TIPOS_VALIDOS}")

    vaga = ler_vaga(vaga_id)
    if vaga:
        vaga.update(novos_dados)
        redis_client.set(f"vaga:{vaga_id}", json.dumps(vaga))
        return True
    return False

def deletar_vaga(vaga_id):
    redis_client.delete(f"vaga:{vaga_id}")