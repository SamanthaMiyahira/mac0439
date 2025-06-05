from bson import ObjectId
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

def adicionar_participante(evento_id, cpf, placa_veiculo):
    db = get_mongo_db()

    if not Usuario.objects.filter(cpf=cpf).exists():
        raise ValueError("Participante não encontrado")
    
    if not Veiculo.objects.filter(placa=placa_veiculo).exists():
        raise ValueError("Veículo não encontrado")

    participante_data = {
        "cpf": cpf,
        "placa_veiculo": placa_veiculo
    }

    db.eventos.update_one(
        {"_id": ObjectId(evento_id)},
        {"$push": {"participantes": participante_data}}
    )

def listar_eventos(status=None):
    db = get_mongo_db()
    query = {}
    if status:
        query["metadata.status"] = status

    eventos = db.eventos.find(query)
    resultado = []

    for evento in eventos:
        resultado.append({
            "evento_id": str(evento["_id"]),
            "titulo": evento["titulo"],
            "data_hora": evento["data_hora"],
            "responsavel_cpf": evento["responsavel_cpf"],
            "status": evento["metadata"]["status"]
        })

    return resultado

def detalhar_evento(evento_id):
    db = get_mongo_db()
    evento = db.eventos.find_one({"_id": ObjectId(evento_id)})

    if not evento:
        raise ValueError("Evento não encontrado")

    try:
        responsavel = Usuario.objects.get(cpf=evento["responsavel_cpf"])
        responsavel_nome = responsavel.nome
    except Usuario.DoesNotExist:
        responsavel_nome = "Desconhecido"

    participantes_detalhados = []
    for p in evento["participantes"]:
        try:
            user = Usuario.objects.get(cpf=p["cpf"])
            veic = Veiculo.objects.get(placa=p["placa_veiculo"])
            participantes_detalhados.append({
                "cpf": user.cpf,
                "nome": user.nome,
                "veiculo": {
                    "placa": veic.placa,
                    "tipo": veic.tipo
                }
            })
        except (Usuario.DoesNotExist, Veiculo.DoesNotExist):
            continue

    return {
        "evento_id": str(evento["_id"]),
        "titulo": evento["titulo"],
        "data_hora": evento["data_hora"],
        "responsavel": {
            "cpf": evento["responsavel_cpf"],
            "nome": responsavel_nome
        },
        "vagas_reservadas": evento["vagas_reservadas"],
        "participantes": participantes_detalhados,
        "status": evento["metadata"]["status"],
        "data_criacao": evento["metadata"]["data_criacao"]
    }
