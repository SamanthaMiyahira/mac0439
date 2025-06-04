from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from datetime import datetime

def get_mongo_db():
    client = MongoClient(settings.MONGO_CONFIG['host'])
    return client[settings.MONGO_CONFIG['dbname']]

# Evento

def criar_evento(titulo, responsavel_cpf, vagas_reservadas):
    db = get_mongo_db()
    
    # Busca dados do responsável no PostgreSQL
    from .models import Usuario
    try:
        responsavel = Usuario.objects.get(cpf=responsavel_cpf)
    except Usuario.DoesNotExist:
        raise ValueError("Responsável não encontrado")
    
    evento = {
        "titulo": titulo,
        "data_hora": datetime.now().isoformat(),
        "responsavel": {
            "cpf": responsavel.cpf,
            "nome": responsavel.nome
        },
        "vagas_reservadas": vagas_reservadas,
        "participantes": [],
        "metadata": {
            "data_criacao": datetime.now().isoformat(),
            "status": "pendente"
        }
    }
    
    result = db.eventos.insert_one(evento)
    return str(result.inserted_id)

def adicionar_participante(evento_id, cpf, placa_veiculo):
    db = get_mongo_db()
    
    # Verifica se usuário e veículo existem no PostgreSQL
    from .models import Usuario, Veiculo
    try:
        participante = Usuario.objects.get(cpf=cpf)
        veiculo = Veiculo.objects.get(placa=placa_veiculo)
    except (Usuario.DoesNotExist, Veiculo.DoesNotExist) as e:
        raise ValueError("Participante ou veículo não encontrado")
    
    participante_data = {
        "cpf": participante.cpf,
        "nome": participante.nome,
        "veiculo": {
            "placa": veiculo.placa,
            "tipo": veiculo.tipo
        }
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
    
    return list(db.eventos.find(query, {
        "titulo": 1,
        "data_hora": 1,
        "responsavel.nome": 1,
        "metadata.status": 1,
        "_id": 0,
        "evento_id": {"$toString": "$_id"}  
    }))