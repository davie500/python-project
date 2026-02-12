"""
wsgi.py - Configuração WSGI (Web Server Gateway Interface) do projeto.

WSGI é o padrão Python para comunicação entre servidores web e aplicações.
Este arquivo expõe a variável 'application' que servidores como Gunicorn,
uWSGI ou Apache mod_wsgi utilizam para servir a aplicação em produção.

Uso em produção (exemplo com Gunicorn):
  gunicorn core.wsgi:application --bind 0.0.0.0:8000

O servidor de desenvolvimento (runserver) NÃO usa este arquivo diretamente,
mas servidores de produção precisam dele para iniciar a aplicação Django.
"""
import os

from django.core.wsgi import get_wsgi_application

# Define o módulo de settings padrão para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria a aplicação WSGI que será usada pelo servidor
application = get_wsgi_application()
