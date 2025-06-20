from rest_framework import serializers
from api.models import Reserva, Veiculo, Credencial, Vaga

class CriarReservaSerializer(serializers.Serializer):
    cpf = serializers.CharField()       
    tipo = serializers.ChoiceField(choices=[('eventual', 'Eventual'), ('recorrente', 'Recorrente')]) 
    data = serializers.DateField()

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['placa', 'tipo'] 

class CredencialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credencial
        fields = ['id', 'qrcode', 'status']

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = ['tipo', 'localizacao']  

class ReservaDetalhesSerializer(serializers.ModelSerializer):
    veiculo = VeiculoSerializer()
    credencial = CredencialSerializer()
    vaga = VagaSerializer()

    class Meta:
        model = Reserva
        fields = ['id', 'tipo', 'status', 'data', 'veiculo', 'credencial', 'vaga']
