#!/bin/sh
set -e

echo "Aguardando Postgres ficar disponível..."

python - <<'PY'
import os, time
import psycopg2

host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")

for i in range(60):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db)
        conn.close()
        print("Postgres OK")
        break
    except Exception as e:
        print(f"({i+1}/60) Postgres indisponível: {e}")
        time.sleep(2)
else:
    raise SystemExit("Postgres não ficou disponível a tempo.")
PY

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Subindo Django..."
python manage.py runserver 0.0.0.0:8000
