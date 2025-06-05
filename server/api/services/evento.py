"""
A função 'criar_evento' cria um evento e registra suas informações em um documento no MongoDB.
"""

from datetime import datetime
from ..models import Usuario, Veiculo
from ..utils.mongo_utils import get_mongo_db
from .reserva import criar_reserva

def criar_evento(titulo, responsavel_cpf, vagas_reservadas, data_hora, participantes=None):
    db = get_mongo_db()

    if not Usuario.objects.filter(cpf=responsavel_cpf).exists():
        raise ValueError("Responsável não encontrado")
    
    responsavel = Usuario.objects.get(cpf=responsavel_cpf)
    veiculo_responsavel = Veiculo.objects.filter(usuario=responsavel).first()
    if not veiculo_responsavel:
        raise ValueError("Veículo do responsável não encontrado")

    criar_reserva(responsavel, veiculo_responsavel, periodo=2, tipo='eventual')

    if participantes:
        for p in participantes:
            cpf = p["cpf"]
            placa = p["placa_veiculo"]

            if not Usuario.objects.filter(cpf=cpf).exists():
                continue
            if not Veiculo.objects.filter(placa=placa).exists():
                continue

            usuario = Usuario.objects.get(cpf=cpf)
            veiculo = Veiculo.objects.get(placa=placa)

            criar_reserva(usuario, veiculo, periodo=2, tipo='eventual')

    evento = {
        "titulo": titulo,
        "data_hora": data_hora,
        "responsavel_cpf": responsavel_cpf,
        "vagas_reservadas": vagas_reservadas,
        "participantes": participantes or [],
        "metadata": {
            "data_criacao": datetime.now().isoformat(),
            "status": "pendente"
        }
    }

    result = db.eventos.insert_one(evento)
    return str(result.inserted_id)