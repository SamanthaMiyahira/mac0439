"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views.evento import criar_evento_view, listar_eventos_view, atualizar_status_evento_view
from api.views.reserva import criar_reserva_view, confirmar_entrada_view, confirmar_saida_view, reserva_detalhes_view, reservas_por_cpf_view, consultar_fila_espera_por_cpf_view
from api.views.recibo import listar_recibos_pendentes_view, pagar_recibo_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/criar-reserva/', criar_reserva_view, name='criar_reserva'),
    path('api/confirmar-entrada/', confirmar_entrada_view, name='confirmar_entrada'),
    path('api/confirmar-saida/', confirmar_saida_view, name='confirmar_saida'),
    path('api/criar-evento/', criar_evento_view, name='criar_evento'),
    path('api/recibos/pendentes/<str:cpf>/', listar_recibos_pendentes_view, name='listar_recibos_pendentes'),
    path('api/recibos/pagar/', pagar_recibo_view, name='pagar_recibo'),
    path('api/reserva/<int:id>/', reserva_detalhes_view, name='reserva_detalhes'),
    path('api/reservas/cpf/<str:cpf>/', reservas_por_cpf_view, name='reservas_por_cpf'),
    path('api/eventos/', listar_eventos_view, name='listar_eventos'),
    path('api/eventos/<str:evento_id>/status/', atualizar_status_evento_view),
    path('api/fila-espera/<str:cpf>/', consultar_fila_espera_por_cpf_view, name='buscar_fila_espera_por_cpf'),
]
