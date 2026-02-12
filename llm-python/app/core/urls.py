"""
urls.py - Configuração de rotas/URLs do projeto Django.

Este arquivo define o mapeamento entre URLs e suas respectivas views.
Cada URL é associada a uma função ou classe que processa a requisição.

Rotas configuradas:
  - /        -> health_check: Endpoint de verificação de saúde da API
  - /admin/  -> Painel administrativo do Django

Para adicionar novas rotas:
  1. Importe a view correspondente
  2. Adicione um path() na lista urlpatterns

Para apps separados, use include() para modularizar as rotas:
  path('api/', include('meu_app.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def health_check(request):
    """
    Endpoint de health check para verificar se a API está funcionando.
    Útil para load balancers e monitoramento.
    """
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),  # Painel administrativo do Django
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("chat.urls")),
    path('health/', health_check, name='health_check'),  # Endpoint para health check
]
