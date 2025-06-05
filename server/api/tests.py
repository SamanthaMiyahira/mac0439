from django.test import TestCase
from django.conf import settings
from bson import ObjectId
from datetime import datetime
from unittest import mock

from .models import Usuario, Vaga
from . import mongo_utils

class CriarEventoTestCase(TestCase):
    def setUp(self):
        # Criação de um usuário responsável válido
        self.usuario_responsavel = Usuario.objects.create(
            nome="João da Silva",
            cpf="12345678901",
            email="joao@example.com",
            tipo="funcionario"
        )

        # Criação de vaga válida
        self.vaga = Vaga.objects.create(
            localizacao="Estacionamento A",
            tipo="visitante",
            status="disponivel"
        )

    def test_criacao_evento_sucesso(self):
        evento_id = mongo_utils.criar_evento(
            titulo="Reunião de Equipe",
            responsavel_cpf=self.usuario_responsavel.cpf,
            vagas_reservadas=[self.vaga.id]
        )

        self.assertIsInstance(evento_id, str)
        db = mongo_utils.get_mongo_db()
        evento = db.eventos.find_one({"_id": ObjectId(evento_id)})

        self.assertIsNotNone(evento)
        self.assertEqual(evento["titulo"], "Reunião de Equipe")
        self.assertEqual(evento["responsavel"]["cpf"], self.usuario_responsavel.cpf)
        self.assertEqual(evento["vagas_reservadas"], [self.vaga.id])
        self.assertEqual(evento["metadata"]["status"], "pendente")

    def test_responsavel_nao_encontrado(self):
        with self.assertRaises(ValueError) as context:
            mongo_utils.criar_evento(
                titulo="Evento Teste",
                responsavel_cpf="99999999999",
                vagas_reservadas=[self.vaga.id]
            )
        self.assertEqual(str(context.exception), "Responsável não encontrado")