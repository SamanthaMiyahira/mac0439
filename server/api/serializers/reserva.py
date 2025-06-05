from rest_framework import serializers

class CriarReservaSerializer(serializers.Serializer):
    cpf = serializers.CharField()       
    tipo = serializers.ChoiceField(choices=[('eventual', 'Eventual'), ('recorrente', 'Recorrente')]) 
    data = serializers.DateField()
    
