# test_script.py
import os
import django
from datetime import datetime, timedelta

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

# Importa dos módulos corretos (ajustado para sua estrutura)
from api.models import Usuario, Veiculo, Vaga  # Note que é 'api' e não 'seu_app'
from api.mongo_utils import criar_evento, adicionar_participante, listar_eventos  # Note o arquivo 'mongo_utils.py'

def criar_dados_teste():
    print("⏳ Criando dados de teste...")
    
    # Limpa dados existentes (opcional)
    Usuario.objects.all().delete()
    Veiculo.objects.all().delete()
    Vaga.objects.all().delete()
    
    # 1. Cria usuários
    u1 = Usuario.objects.create(
        cpf="123.456.789-00",
        nome="Maria Silva",
        email="maria@exemplo.com"
    )
    
    u2 = Usuario.objects.create(
        cpf="111.222.333-44",
        nome="Carlos Souza",
        email="carlos@exemplo.com"
    )
    
    # 2. Cria veículos
    v1 = Veiculo.objects.create(
        placa="ABC1234",
        dono=u1,
        tipo="convencional"
    )
    
    v2 = Veiculo.objects.create(
        placa="XYZ9876",
        dono=u2,
        tipo="eletrico"
    )
    
    # 3. Cria vagas
    Vaga.objects.create(id_vaga="A12", tipo="preferencial")
    Vaga.objects.create(id_vaga="B05", tipo="comum")
    
    print("✅ Dados PostgreSQL criados com sucesso!")
    
    # 4. Cria evento no MongoDB
    evento_id = criar_evento(
        titulo="Reunião de Diretoria",
        responsavel_cpf="123.456.789-00",
        vagas_reservadas=[
            {"id_vaga": "A12", "tipo": "preferencial"},
            {"id_vaga": "B05", "tipo": "comum"}
        ]
    )
    
    # 5. Adiciona participantes
    adicionar_participante(evento_id, "111.222.333-44", "XYZ9876")
    
    print(f"✅ Evento MongoDB criado com ID: {evento_id}")
    
    # 6. Lista eventos
    print("\n📋 Lista de Eventos:")
    for evento in listar_eventos():
        print(f"- {evento['titulo']} (Status: {evento['metadata']['status']})")

if __name__ == "__main__":
    criar_dados_teste()