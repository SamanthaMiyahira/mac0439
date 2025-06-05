from rest_framework import serializers

class CriarReservaSerializer(serializers.Serializer):
    cpf = serializers.CharField()       
    placa = serializers.CharField()    
    tipo = serializers.ChoiceField(choices=[('eventual', 'Eventual'), ('recorrente', 'Recorrente')]) 
    periodo = serializers.DurationField()
    
