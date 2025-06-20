from datetime import datetime
from ..models import Usuario, Veiculo
from ..utils.mongo_utils import get_mongo_db
from .reserva import criar_reserva
from django.core.exceptions import ObjectDoesNotExist
from api.models import Reserva

def criar_evento(titulo, responsavel_cpf, data_hora, participantes=None):
    db = get_mongo_db()

    if not Usuario.objects.filter(cpf=responsavel_cpf).exists():
        raise ValueError("Responsável não encontrado")
    
    responsavel = Usuario.objects.get(cpf=responsavel_cpf)
    veiculo_responsavel = Veiculo.objects.filter(usuario=responsavel).first()
    if not veiculo_responsavel:
        raise ValueError("Veículo do responsável não encontrado")

    total_vagas = 1 + (len(participantes) if participantes else 0)

    evento = {
        "titulo": titulo,
        "data_hora": data_hora,
        "responsavel_cpf": responsavel_cpf,
        "vagas_reservadas": total_vagas,
        "participantes": participantes or [],
        "metadata": {
            "data_criacao": datetime.now().isoformat(),
            "status": "pendente"
        }
    }

    result = db.eventos.insert_one(evento)
    evento_id = str(result.inserted_id)

    reserva_resp = criar_reserva(responsavel, veiculo_responsavel, data=data_hora.date(), tipo='eventual', evento_id=evento_id)
    print("Reserva do responsável criada?", reserva_resp)

    if participantes:
        for p in participantes:
            cpf = p["cpf"]
            try:
                usuario = Usuario.objects.get(cpf=cpf)
                veiculo = Veiculo.objects.filter(usuario=usuario).first()
                if not veiculo:
                    print(f"Veículo não encontrado para usuário {cpf}")
                    continue
                reserva_part = criar_reserva(usuario, veiculo, data=data_hora.date(), tipo='eventual', evento_id=evento_id)
                print(f"Reserva do participante {cpf} criada?", reserva_part)
            except ObjectDoesNotExist:
                print(f"Usuário participante {cpf} não encontrado")
                continue

    return evento_id


def incluir_placa_participantes(evento):
    participantes_com_placa = []
    for p in evento.get('participantes', []):
        cpf = p.get('cpf')
        veiculo = Veiculo.objects.filter(usuario__cpf=cpf).first()
        placa = veiculo.placa if veiculo else ''
        participantes_com_placa.append({
            'cpf': cpf,
            'placa_veiculo': placa
        })
    evento['participantes'] = participantes_com_placa
    return evento

def cancelar_reservas_do_evento(evento_id):
    reservas = Reserva.objects.filter(evento_id=evento_id)
    for reserva in reservas:
        reserva.status = 'cancelada'
        reserva.save()
        if reserva.credencial:
            reserva.credencial.status = 'desativado'
            reserva.credencial.save()

def concluir_reservas_do_evento(evento_id):
    reservas = Reserva.objects.filter(evento_id=evento_id, status='ativa')
    for reserva in reservas:
        reserva.status = 'concluida'
        reserva.save()
        if reserva.credencial:
            reserva.credencial.status = 'desativado'
            reserva.credencial.save()

