#!/usr/bin/env python
"""
manage.py - Ponto de entrada para comandos administrativos do Django.

Este arquivo é o utilitário de linha de comando do Django, usado para executar
tarefas administrativas como:
  - python manage.py runserver     -> Inicia o servidor de desenvolvimento
  - python manage.py migrate       -> Aplica migrações do banco de dados
  - python manage.py createsuperuser -> Cria um usuário administrador
  - python manage.py shell         -> Abre o shell interativo do Django
  - python manage.py makemigrations -> Gera arquivos de migração

O arquivo define a variável DJANGO_SETTINGS_MODULE para apontar para o módulo
de configurações do projeto (core.settings).
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
