"""
Esta função é chamada automaticamente durante a criação de uma reserva 
quando o usuário é do tipo 'visitante'. Assim, sempre que um visitante 
faz uma reserva, o sistema gera um recibo associado a essa reserva.

Ela cria um documento no banco MongoDB, na coleção 'recibos', com os dados 
do pagamento e do visitante.
"""

from datetime import datetime
from ..utils.mongo_utils import get_mongo_db
from bson import ObjectId

def criar_recibo(
    valor,
    data_hora,
    status,
    metodo_pagamento,
    visitante,
    detalhes_pagamento=None,
    data_pagamento=None,  
    evento=None,
    responsavel_emissor="sistema_automatico"
):
    db = get_mongo_db()

    if not all(k in visitante for k in ("cpf", "nome", "veiculo_placa")):
        raise ValueError("Dados do visitante incompletos")

    recibo = {
        "valor": valor,
        "data_hora": data_hora,
        "status": status,  # pago, pendente, cancelado
        "metodo_pagamento": metodo_pagamento,  # PIX, CARTAO, INTEGRACAO_FINANCEIRA
        "data_pagamento": data_pagamento,
        "visitante": {
            "cpf": visitante["cpf"],
            "nome": visitante["nome"],
            "veiculo_placa": visitante["veiculo_placa"]
        },
        "metadata": {
            "data_emissao": datetime.now().isoformat(),
            "responsavel_emissor": responsavel_emissor
        }
    }

    if detalhes_pagamento:
        recibo["detalhes_pagamento"] = detalhes_pagamento

    if evento:
        recibo["evento"] = {
            "evento_id": evento.get("evento_id"),
            "titulo": evento.get("titulo")
        }

    result = db.recibos.insert_one(recibo)
    return str(result.inserted_id)

def listar_recibos_pendentes(cpf_visitante):
    db = get_mongo_db()
    filtro = {
        "visitante.cpf": cpf_visitante,
        "status": "pendente"
    }
    recibos = list(db.recibos.find(filtro))

    for r in recibos:
        r["_id"] = str(r["_id"])

    return recibos

def pagar_recibo(cpf_visitante, recibo_id, metodo_pagamento, detalhes_pagamento=None):
    db = get_mongo_db()
    filtro = {
        "_id": ObjectId(recibo_id),
        "visitante.cpf": cpf_visitante,
        "status": "pendente"
    }
    atualizacao = {
        "$set": {
            "status": "pago",
            "metodo_pagamento": metodo_pagamento,
            "data_pagamento": datetime.now().isoformat()
        }
    }
    if detalhes_pagamento:
        atualizacao["$set"]["detalhes_pagamento"] = detalhes_pagamento
    
    resultado = db.recibos.update_one(filtro, atualizacao)

    if resultado.modified_count == 1:
        return True
    else:
        return False

