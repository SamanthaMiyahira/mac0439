from django.contrib import admin
from .models import Usuario, Veiculo, Vaga 

# Registre cada modelo
admin.site.register(Usuario)
admin.site.register(Veiculo)
admin.site.register(Vaga)