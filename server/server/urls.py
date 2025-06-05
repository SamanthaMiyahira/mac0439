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
from server.api.views.evento import criar_evento_view, listar_eventos_view, detalhar_evento_view
from server.api.views.evento import criar_reserva_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eventos/', criar_evento_view, name='criar_evento'),
    path('eventos/listar/', listar_eventos_view, name='listar_eventos'),
    path('eventos/<str:evento_id>/', detalhar_evento_view, name='detalhar_evento'),
    path('api/criar-reserva/', criar_reserva_view, name='criar_reserva')
]
