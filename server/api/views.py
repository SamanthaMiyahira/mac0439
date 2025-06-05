from django.shortcuts import render
from django.http import JsonResponse
from .utils.mongo_utils import criar_evento

# NOSQL (MongoDB)

def criar_evento_view(request):
    if request.method == 'POST':
        # Exemplo de dados (na prática, viria do request.POST/request.body)
        vagas_reservadas = [
            {"id_vaga": "A12", "tipo": "preferencial"},
            {"id_vaga": "B05", "tipo": "comum"}
        ]
        
        try:
            evento_id = criar_evento(
                titulo="Reunião Mensal",
                responsavel_cpf="123.456.789-00",
                vagas_reservadas=vagas_reservadas
            )
            return JsonResponse({"status": "success", "evento_id": evento_id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
