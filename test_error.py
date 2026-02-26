import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import sentry_sdk

sentry_sdk.capture_exception(Exception("Projeto compilando"))
print("✅ Erro 'Projeto compilando' enviado para Sentry!")
