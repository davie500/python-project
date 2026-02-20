#!/bin/sh
set -e

echo "Aguardando PostgreSQL ficar disponivel..."

python - <<'PY'
import os
import time
import psycopg2

host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB") or os.getenv("POSTGRES_DATABASE")

for i in range(60):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db,
        )
        conn.close()
        print("PostgreSQL OK")
        break
    except Exception as e:
        print(f"({i+1}/60) PostgreSQL indisponivel: {e}")
        time.sleep(2)
else:
    raise SystemExit("PostgreSQL nao ficou disponivel a tempo.")
PY

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Subindo Django..."
python manage.py runserver 0.0.0.0:8000
