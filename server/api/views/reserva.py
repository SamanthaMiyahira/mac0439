from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.serializers.reserva import CriarReservaSerializer
from api.models import Usuario, Veiculo, Credencial, Reserva, Vaga
from api.services.reserva import criar_reserva, liberar_vaga_e_alocar_fila
from django.utils import timezone
from api.services.incidente import incidente_acesso_nao_autorizado, incidente_tempo_excedido, incidente_tentativa_fraude
from api.serializers.reserva import ReservaDetalhesSerializer

@api_view(['POST'])
def criar_reserva_view(request):
    serializer = CriarReservaSerializer(data=request.data)
    if serializer.is_valid():
        try:
            usuario = Usuario.objects.get(cpf=serializer.validated_data['cpf'])
        except Usuario.DoesNotExist:
            return Response({'erro': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        veiculo = Veiculo.objects.filter(usuario=usuario).first()
        if not veiculo:
            return Response({'erro': 'Veículo não encontrado para este usuário'}, status=status.HTTP_404_NOT_FOUND)

        data = serializer.validated_data.get('data')
        tipo = serializer.validated_data.get('tipo')

        reserva = criar_reserva(usuario=usuario, veiculo=veiculo, data=data, tipo=tipo)
        if reserva:
            return Response({'mensagem': 'Reserva criada com sucesso', 'id_reserva': reserva.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensagem': 'Sem vagas disponíveis. Usuário na fila de espera.'}, status=status.HTTP_200_OK)
    
    else:
        print("Erros no serializer:", serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirmar_entrada_view(request):
    qrcode = request.data.get('qrcode')
    placa = request.data.get('placa')

    try:
        credencial = Credencial.objects.get(qrcode=qrcode, status='ativo')
        reserva = Reserva.objects.get(credencial=credencial)

        if reserva.veiculo.placa != placa:
            incidente_tentativa_fraude(reserva.usuario, reserva)
            return Response({'erro': 'Placa não corresponde à credencial.'}, status=status.HTTP_400_BAD_REQUEST)

        agora = timezone.now()
        if reserva.data_hora_entrada is None or reserva.data_hora_entrada.date() != agora.date():
            incidente_acesso_nao_autorizado(reserva.usuario, reserva)
            return Response({'erro': 'A entrada só pode ser confirmada no dia da reserva.'}, status=status.HTTP_400_BAD_REQUEST)

        agora = timezone.now()
        reserva.data_hora_entrada = agora
        reserva.save()

        vaga = reserva.vaga
        vaga.status = 'ocupada'
        vaga.save()

        credencial.status = 'bloqueado'
        credencial.save()

        return Response({'mensagem': 'Entrada confirmada com sucesso.'}, status=status.HTTP_200_OK)

    except Credencial.DoesNotExist:
        return Response({'erro': 'Credencial inválida ou inativa.'}, status=status.HTTP_404_NOT_FOUND)

    except Reserva.DoesNotExist:
        return Response({'erro': 'Reserva não encontrada para essa credencial.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def confirmar_saida_view(request):
    qrcode = request.data.get('qrcode')
    placa = request.data.get('placa')

    try:
        credencial = Credencial.objects.get(qrcode=qrcode, status='bloqueado')
        reserva = Reserva.objects.get(credencial=credencial)

        if reserva.veiculo.placa != placa:
            return Response({'erro': 'Placa não corresponde à credencial.'}, status=status.HTTP_400_BAD_REQUEST)

        agora = timezone.now()
        entrada = reserva.data_hora_entrada
        if entrada and (agora - entrada).total_seconds() > 12 * 3600:
            incidente_tempo_excedido(reserva.usuario, reserva)

        reserva.data_hora_saida = agora
        reserva.status = 'concluida'  
        reserva.save()

        vaga = reserva.vaga
        liberar_vaga_e_alocar_fila(vaga)
        vaga.save()

        credencial.status = 'desativado'
        credencial.save()

        return Response({'mensagem': 'Saída confirmada com sucesso.'}, status=status.HTTP_200_OK)

    except Credencial.DoesNotExist:
        return Response({'erro': 'Credencial inválida ou inativa.'}, status=status.HTTP_404_NOT_FOUND)

    except Reserva.DoesNotExist:
        return Response({'erro': 'Reserva não encontrada para essa credencial.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def reserva_detalhes_view(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        return Response({'erro': 'Reserva não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReservaDetalhesSerializer(reserva)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def reservas_por_cpf_view(request, cpf):
    try:
        reservas = Reserva.objects.filter(usuario__cpf=cpf).order_by('-data_hora_entrada')
        if not reservas.exists():
            return Response({'erro': 'Nenhuma reserva encontrada para este CPF'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReservaDetalhesSerializer(reservas, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'erro': 'Erro ao buscar reserva'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
