from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..services.evento import criar_evento, incluir_placa_participantes, cancelar_reservas_do_evento, concluir_reservas_do_evento
from ..serializers.evento import EventoSerializer
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from ..utils.mongo_utils import get_mongo_db

@api_view(['POST'])
def criar_evento_view(request):
    serializer = EventoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    dados = serializer.validated_data
    try:
        evento_id = criar_evento(
            dados['titulo'],
            dados['responsavel_cpf'],
            dados['data_hora'],
            dados.get('participantes', [])
        )
        return Response({"evento_id": evento_id})
    except Exception as e:
        return Response({'erro': f'Erro interno ao criar evento: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def listar_eventos_view(request):
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client['smartpark_nosql']
        eventos = list(db.eventos.find())

        for e in eventos:
            e['_id'] = str(e['_id'])
            e = incluir_placa_participantes(e)

        return Response(eventos, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'erro': f'Erro ao acessar MongoDB: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def atualizar_status_evento_view(request, evento_id):
    novo_status = request.data.get('status')
    if novo_status not in ['pendente', 'concluido', 'cancelado']:
        return Response({'erro': 'Status inválido'}, status=400)

    db = get_mongo_db()
    result = db.eventos.update_one(
        {"_id": ObjectId(evento_id)},
        {"$set": {"metadata.status": novo_status}}
    )

    if result.modified_count:
        if novo_status == 'cancelado':
            cancelar_reservas_do_evento(evento_id)
        elif novo_status == 'concluido':
            concluir_reservas_do_evento(evento_id)

        return Response({'mensagem': f"Status do evento atualizado para {novo_status}."})
    else:
        return Response({'erro': 'Evento não encontrado ou já atualizado.'}, status=404)
