from rest_framework import serializers

class ParticipanteSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=14)

class EventoSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    responsavel_cpf = serializers.CharField(max_length=14)
    data_hora = serializers.DateTimeField()
    participantes = ParticipanteSerializer(many=True, required=False, default=[])
