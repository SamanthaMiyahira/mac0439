from rest_framework import serializers

class ParticipanteSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=14)
    placa_veiculo = serializers.CharField(max_length=10)

class EventoSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    responsavel_cpf = serializers.CharField(max_length=14)
    vagas_reservadas = serializers.IntegerField()
    data_hora = serializers.DateTimeField()
    participantes = ParticipanteSerializer(many=True, required=False, default=[])
