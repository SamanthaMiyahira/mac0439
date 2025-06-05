from django.contrib import admin
from .models import (  
    Usuario, 
    Veiculo, 
    Vaga,
    Funcionario,
    Credencial,
    Reserva,
    FilaDeEspera,
    Incidente,
    Notificacao
)

admin.site.register(Usuario)
admin.site.register(Veiculo)
admin.site.register(Vaga)
admin.site.register(Funcionario)
admin.site.register(Credencial)
admin.site.register(Reserva)
admin.site.register(FilaDeEspera)
admin.site.register(Incidente)
admin.site.register(Notificacao)