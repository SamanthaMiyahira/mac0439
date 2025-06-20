from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from ..services.recibo import listar_recibos_pendentes, pagar_recibo
from django.http import JsonResponse
from api.utils.mongo_utils import get_mongo_db

@api_view(['GET'])
def listar_recibos_pendentes_view(request, cpf):
    recibos = listar_recibos_pendentes(cpf)
    return Response(recibos, status=status.HTTP_200_OK)


@api_view(['POST'])
def pagar_recibo_view(request):
    cpf = request.data.get('cpf')
    recibo_id = request.data.get('recibo_id')
    metodo_pagamento = request.data.get('metodo_pagamento')
    detalhes_pagamento = request.data.get('detalhes_pagamento', None)

    if not cpf or not recibo_id or not metodo_pagamento:
        return Response({'erro': 'cpf, recibo_id e metodo_pagamento são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        sucesso = pagar_recibo(cpf, recibo_id, metodo_pagamento, detalhes_pagamento)
        if sucesso:
            return Response({'mensagem': 'Pagamento registrado com sucesso.'}, status=status.HTTP_200_OK)
        else:
            return Response({'erro': 'Recibo não encontrado ou já pago.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def listar_recibos_pagos(request, cpf):
    db = get_mongo_db()
    recibos = list(db.recibos.find({"visitante.cpf": cpf, "status": "pago"}))
    for r in recibos:
        r["_id"] = str(r["_id"])  
    return JsonResponse(recibos, safe=False)