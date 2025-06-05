from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services.evento_service import criar_evento, listar_eventos, detalhar_evento

@api_view(['POST'])
def criar_evento_view(request):
    data = request.data
    evento_id = criar_evento(data['titulo'], data['responsavel_cpf'], data['vagas_reservadas'])
    return Response({"evento_id": evento_id})

@api_view(['GET'])
def listar_eventos_view(request):
    status = request.GET.get("status")
    eventos = listar_eventos(status)
    return Response(eventos)

@api_view(['GET'])
def detalhar_evento_view(request, evento_id):
    evento = detalhar_evento(evento_id)
    return Response(evento)
