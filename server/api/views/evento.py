from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..services.evento import criar_evento, listar_eventos, detalhar_evento
from ..serializers.evento import EventoSerializer

@api_view(['POST'])
def criar_evento_view(request):
    serializer = EventoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    dados = serializer.validated_data
    evento_id = criar_evento(
        dados['titulo'],
        dados['responsavel_cpf'],
        dados['vagas_reservadas'],
        dados['data_hora'],
        dados.get('participantes', [])
    )
    return Response({"evento_id": evento_id})
