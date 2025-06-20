from api.models import Incidente
from django.utils import timezone

def registrar_incidente(usuario, acao, gravidade, reserva=None):
    Incidente.objects.create(
        usuario=usuario,
        acao=acao,
        gravidade=gravidade,
        data_hora=timezone.localtime(),
        reserva=reserva
    )

def incidente_acesso_nao_autorizado(usuario, reserva=None):
    registrar_incidente(
        usuario=usuario,
        acao="Tentativa de acesso não autorizado detectada.",
        gravidade=7,
        reserva=reserva
    )

def incidente_tempo_excedido(usuario, reserva=None):
    registrar_incidente(
        usuario=usuario,
        acao="Tempo de permanência excedido sem saída registrada.",
        gravidade=6,
        reserva=reserva
    )

def incidente_tentativa_fraude(usuario, reserva=None):
    registrar_incidente(
        usuario=usuario,
        acao="Tentativa de fraude identificada (ex: QRCode inválido ou placa não correspondente).",
        gravidade=9,
        reserva=reserva
    )
