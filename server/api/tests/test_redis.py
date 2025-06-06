from django.test import TestCase
from api.services.redis_crud import (
    criar_vaga,
    ler_vaga,
    atualizar_vaga,
    deletar_vaga
)
from api.utils.redis_client import redis_client

class RedisCRUDTest(TestCase):

    def setUp(self):
        self.vaga_id = "A09"
        self.dados_iniciais = {
            "status": "disponivel",
            "tipo": "convencional",
            "placa": "ABC1234",
            "cpf": "12345678900",
            "hora_entrada": "2025-06-05 18:00"
        }
        # Garante que não exista a chave antes de cada teste
        redis_client.delete(f"vaga:{self.vaga_id}")

    def test_criar_vaga(self):
        criar_vaga(self.vaga_id, **self.dados_iniciais)
        vaga = ler_vaga(self.vaga_id)
        self.assertIsNotNone(vaga)
        self.assertEqual(vaga["status"], "disponivel")
        self.assertEqual(vaga["placa"], "ABC1234")

    def test_ler_vaga_inexistente(self):
        vaga = ler_vaga("vaga_inexistente")
        self.assertIsNone(vaga)

    def test_atualizar_vaga_existente(self):
        criar_vaga(self.vaga_id, **self.dados_iniciais)
        atualizado = atualizar_vaga(self.vaga_id, {"status": "ocupada"})
        vaga = ler_vaga(self.vaga_id)
        self.assertTrue(atualizado)
        self.assertEqual(vaga["status"], "ocupada")

    def test_atualizar_vaga_inexistente(self):
        atualizado = atualizar_vaga("vaga_nao_existe", {"status": "ocupada"})
        self.assertFalse(atualizado)

    def test_deletar_vaga(self):
        criar_vaga(self.vaga_id, **self.dados_iniciais)
        deletar_vaga(self.vaga_id)
        vaga = ler_vaga(self.vaga_id)
        self.assertIsNone(vaga)

    # testar se dados invalidos para status nao sao aceitos ao criar
    def test_criar_vaga_status_invalido(self):
        dados_invalidos = self.dados_iniciais.copy()
        dados_invalidos["status"] = "livre"  # status inválido

        with self.assertRaises(ValueError) as context:
            criar_vaga(self.vaga_id, **dados_invalidos)

        self.assertIn("Status inválido", str(context.exception))

    # testar se dados invalidos para tipo nao sao aceitos ao criar
    def test_criar_vaga_tipo_invalido(self):
        dados_invalidos = self.dados_iniciais.copy()
        dados_invalidos["tipo"] = "vip"  # tipo inválido

        with self.assertRaises(ValueError) as context:
            criar_vaga(self.vaga_id, **dados_invalidos)

        self.assertIn("Tipo inválido", str(context.exception))
        
    # testar se dados invalidos para status nao sao aceitos ao atualizar
    def test_atualizar_vaga_com_status_invalido(self):
        criar_vaga(self.vaga_id, **self.dados_iniciais)

        with self.assertRaises(ValueError) as context:
            atualizar_vaga(self.vaga_id, {"status": "indefinido"})

        self.assertIn("Status inválido", str(context.exception))

    # limpa os dados após cada teste
    def tearDown(self):
        redis_client.delete(f"vaga:{self.vaga_id}")
