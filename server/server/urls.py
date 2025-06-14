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
from api.views.evento import criar_evento_view
from api.views.reserva import criar_reserva_view, confirmar_entrada_view, confirmar_saida_view
from api.views.recibo import listar_recibos_pendentes_view, pagar_recibo_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/criar-reserva/', criar_reserva_view, name='criar_reserva'),
    path('api/confirmar-entrada/', confirmar_entrada_view, name='confirmar_entrada'),
    path('api/confirmar-saida/', confirmar_saida_view, name='confirmar_saida'),
    path('api/criar-evento/', criar_evento_view, name='criar_evento'),
    path('api/recibos/pendentes/<str:cpf>/', listar_recibos_pendentes_view, name='listar_recibos_pendentes'),
    path('api/recibos/pagar/', pagar_recibo_view, name='pagar_recibo'),
]
