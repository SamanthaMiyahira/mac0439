from rest_framework import serializers
from api.models import Reserva

class CriarReservaSerializer(serializers.Serializer):
    cpf = serializers.CharField()       
    tipo = serializers.ChoiceField(choices=[('eventual', 'Eventual'), ('recorrente', 'Recorrente')]) 
    data = serializers.DateField()
    

class ReservaDetalhesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'tipo', 'status', 'data', 'data_hora_entrada', 'data_hora_saida']
        depth = 2  
