from datetime import datetime
from django.utils import timezone
from api.models import Reserva, Credencial, Notificacao, FilaDeEspera, Vaga, Veiculo
from .recibo import criar_recibo

def criar_reserva(usuario, veiculo, data, tipo):
    entrada = None 
    saida = None

    if isinstance(data, str):
        data = datetime.strptime(data, "%Y-%m-%d").date()

    vaga = Vaga.objects.filter(
        status='disponivel',
        tipo__in=['convencional', 'preferencial'] if veiculo.tipo == 'convencional' else ['eletrica']
    ).first()

    if vaga:
        credencial = Credencial.objects.create(
            data_emissao=timezone.localtime(),
            data_expiracao=saida,
            status='ativo',
            qrcode='https://example.com/qrcode123'
        )

        reserva = Reserva.objects.create(
            data_hora_entrada=entrada,  
            data_hora_saida=saida,
            data=data, 
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
            data_hora=timezone.localtime(),
            usuario=usuario,
            reserva=reserva
        )

        # Cria recibo se for visitante
        if getattr(usuario, "tipo", "").lower() == "visitante":

            criar_recibo(
                valor=50.00,
                data_hora=timezone.localtime().isoformat(),
                status="pendente",
                metodo_pagamento=None,
                data_pagamento=None,
                visitante={
                    "cpf": usuario.cpf,
                    "nome": usuario.nome,
                    "veiculo_placa": veiculo.placa
                },
                responsavel_emissor="sistema_automatico",
                evento=(tipo.lower() == "eventual")
            )

        return reserva
    else:
        FilaDeEspera.objects.create(
            prioridade=getattr(usuario, 'prioridade', 0) or 0,
            data_hora=timezone.localtime(),
            status='aguardando',
            usuario=usuario,
            data_reserva=data
        )

        Notificacao.objects.create(
            tipo='fila_de_espera',
            mensagem='Estacionamento cheio. Você foi adicionado à fila de espera.',
            data_hora=timezone.localtime(),
            usuario=usuario
        )
        return None
    
def liberar_vaga_e_alocar_fila(vaga):
    vaga.status = 'disponivel'
    vaga.save()

    fila = FilaDeEspera.objects.filter(status='aguardando').order_by('-prioridade', 'data_hora').first()

    if fila:
        veiculo = Veiculo.objects.filter(usuario=fila.usuario).first()
        
        if veiculo:
            reserva = criar_reserva(fila.usuario, veiculo, data=fila.data_reserva, tipo='eventual')
            
            if reserva:
                fila.status = 'realizada'
                fila.save()

                Notificacao.objects.create(
                    tipo='fila_de_espera',
                    mensagem='Uma vaga foi liberada para você! Sua reserva foi criada.',
                    data_hora=timezone.localtime(),
                    usuario=fila.usuario,
                    reserva=reserva
                )
        else:
            Notificacao.objects.create(
                tipo='erro',
                mensagem='Você não possui veículo cadastrado para criar a reserva.',
                data_hora=timezone.localtime(),
                usuario=fila.usuario
            )


