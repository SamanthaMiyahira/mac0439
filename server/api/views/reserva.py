from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from server.api.serializers.reserva import CriarReservaSerializer
from api.models import Usuario, Veiculo
from server.api.services.reserva import criar_reserva

@api_view(['POST'])
def criar_reserva_view(request):
    serializer = CriarReservaSerializer(data=request.data)
    if serializer.is_valid():
        try:
            usuario = Usuario.objects.get(cpf=serializer.validated_data['cpf'])
            veiculo = Veiculo.objects.get(placa=serializer.validated_data['placa'], usuario=usuario)
        except Usuario.DoesNotExist:
            return Response({'erro': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Veiculo.DoesNotExist:
            return Response({'erro': 'Veículo não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        periodo = serializer.validated_data.get('periodo')
        tipo = serializer.validated_data.get('tipo')

        reserva = criar_reserva(usuario=usuario, veiculo=veiculo, periodo=periodo, tipo=tipo)
        if reserva:
            return Response({'mensagem': 'Reserva criada com sucesso', 'id_reserva': reserva.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensagem': 'Sem vagas disponíveis. Usuário na fila de espera.'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)