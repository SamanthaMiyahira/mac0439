from django.test import TestCase
from django.core.exceptions import ValidationError  # Usado para erros de validação no modelo
from django.db import IntegrityError                # Usado para erros em nível de banco (ex: UNIQUE, FK)
from django.utils import timezone
from datetime import timedelta
from api.models import (
    Usuario, Funcionario, Veiculo, Vaga,
    Credencial, Reserva, FilaDeEspera,
    Incidente, Notificacao
)

class ModelConstraintsTest(TestCase):

    def setUp(self):
        # Criação de um usuário válido para uso nos testes
        self.usuario = Usuario.objects.create(
            cpf="12345678901",
            nome="João Teste",
            tipo="visitante",
            email="joao@example.com",
            prioridade=1,
            foto="https://example.com/foto.jpg"
        )

    def test_usuario_foto_invalida(self):
        # Testa validação de URL inválida na foto
        self.usuario.foto = "not-a-url"
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()  # Valida os campos do modelo

    def test_usuario_prioridade_negativa(self):
        # Testa se valor negativo em prioridade levanta erro (restrição: >= 0)
        self.usuario.prioridade = -1
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_usuario_tipo_invalido(self):
        # Testa um valor inválido para o campo tipo (fora das opções do choices)
        self.usuario.tipo = "superadmin"
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_veiculo_url_invalida(self):
        # Testa URL inválida na imagem da placa
        veiculo = Veiculo(
            placa="ABC1234",
            modelo="Model X",
            marca="Tesla",
            tipo="eletrico",
            imagem_placa="invalid-url",
            usuario=self.usuario
        )
        with self.assertRaises(ValidationError):
            veiculo.full_clean()

    def test_veiculo_tipo_invalido(self):
        # Testa um tipo de veículo inválido
        veiculo = Veiculo(
            placa="XYZ9999",
            modelo="Corolla",
            marca="Toyota",
            tipo="voador",  # Valor fora do choices
            imagem_placa="https://placa.com/image.jpg",
            usuario=self.usuario
        )
        with self.assertRaises(ValidationError):
            veiculo.full_clean()

    def test_credencial_qrcode_url_invalida(self):
        # Testa URL inválida no campo qrcode da credencial
        credencial = Credencial(
            data_emissao=timezone.now(),
            data_expiracao=timezone.now() + timedelta(days=1),
            status="ativo",
            qrcode="bad-url"
        )
        with self.assertRaises(ValidationError):
            credencial.full_clean()

    def test_fila_de_espera_prioridade_negativa(self):
        # Testa valor negativo para prioridade na fila de espera
        with self.assertRaises(ValidationError):
            FilaDeEspera(
                prioridade=-5,
                data_hora=timezone.now(),
                status="aguardando",
                usuario=self.usuario
            ).full_clean()

    def test_incidente_gravidade_fora_intervalo(self):
        # Testa gravidade fora do intervalo permitido (1 a 10)
        reserva = Reserva.objects.create(
            data_hora_entrada=timezone.now(),
            periodo=timedelta(hours=2),
            tipo="eventual",
            usuario=self.usuario
        )
        incidente = Incidente(
            gravidade=15,  # fora do intervalo
            acao="Avisar segurança",
            data_hora=timezone.now(),
            usuario=self.usuario,
            reserva=reserva
        )
        with self.assertRaises(ValidationError):
            incidente.full_clean()

    def test_notificacao_tipo_invalido(self):
        # Testa tipo inválido de notificação
        notificacao = Notificacao(
            tipo="apagao",  # não faz parte do choices
            mensagem="Problema detectado",
            data_hora=timezone.now(),
            usuario=self.usuario
        )
        with self.assertRaises(ValidationError):
            notificacao.full_clean()

    def test_reserva_on_delete_usuario_cascade(self):
        # Testa se a exclusão do usuário apaga a reserva (on_delete=models.CASCADE)
        reserva = Reserva.objects.create(
            data_hora_entrada=timezone.now(),
            periodo=timedelta(hours=1),
            tipo="eventual",
            usuario=self.usuario
        )
        self.usuario.delete()
        # A reserva deve ser deletada automaticamente
        with self.assertRaises(Reserva.DoesNotExist):
            Reserva.objects.get(pk=reserva.pk)

    def test_reserva_on_delete_veiculo_set_null(self):
        # Testa se ao deletar o veículo a FK da reserva vira NULL (on_delete=models.SET_NULL)
        veiculo = Veiculo.objects.create(
            placa="AAA0000",
            modelo="Civic",
            marca="Honda",
            tipo="convencional",
            usuario=self.usuario
        )
        reserva = Reserva.objects.create(
            data_hora_entrada=timezone.now(),
            periodo=timedelta(hours=1),
            tipo="eventual",
            usuario=self.usuario,
            veiculo=veiculo
        )
        veiculo.delete()
        reserva.refresh_from_db()
        self.assertIsNone(reserva.veiculo)
