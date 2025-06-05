# app/services/reserva_service.py

from datetime import timedelta
from django.utils import timezone
from api.models import Reserva, Credencial, Notificacao, FilaDeEspera, Vaga

def criar_reserva(usuario, veiculo, periodo, tipo):
    entrada = None 
    saida = None

    # Se o período puder ser inteiro (em horas) ou timedelta
    if isinstance(periodo, int):
        periodo = timedelta(hours=periodo)
    elif not isinstance(periodo, timedelta):
        periodo = timedelta(hours=2) 

    vaga = Vaga.objects.filter(
        status='disponivel',
        tipo__in=['convencional', 'preferencial'] if veiculo.tipo == 'convencional' else ['eletrica']
    ).first()

    if vaga:
        credencial = Credencial.objects.create(
            data_emissao=timezone.now(),
            data_expiracao=saida,
            status='ativo',
            qrcode='https://example.com/qrcode123'
        )

        reserva = Reserva.objects.create(
            data_hora_entrada=entrada,  
            data_hora_saida=saida,
            periodo=periodo, 
            tipo=tipo,
            usuario=usuario,
            veiculo=veiculo,
            vaga=vaga,
            credencial=credencial
        )

        vaga.status = 'reservada'
        vaga.save()

        Notificacao.objects.create(
            tipo='reserva',
            mensagem='Sua reserva foi confirmada com sucesso.',
            data_hora=timezone.now(),
            usuario=usuario,
            reserva=reserva
        )
        return reserva
    else:
        FilaDeEspera.objects.create(
            prioridade=getattr(usuario, 'prioridade', 0) or 0,
            data_hora=timezone.now(),
            status='aguardando',
            usuario=usuario
        )

        Notificacao.objects.create(
            tipo='fila_de_espera',
            mensagem='Estacionamento cheio. Você foi adicionado à fila de espera.',
            data_hora=timezone.now(),
            usuario=usuario
        )
        return None
