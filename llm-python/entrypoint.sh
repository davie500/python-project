#!/bin/sh
set -e

echo "Aguardando MySQL ficar disponível..."

python - <<'PY'
import os, time
import MySQLdb

host = os.getenv("MYSQL_HOST", "db")
port = int(os.getenv("MYSQL_PORT", "3306"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DATABASE")

for i in range(60):
    try:
        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db)
        conn.close()
        print("MySQL OK")
        break
    except Exception as e:
        print(f"({i+1}/60) MySQL indisponível: {e}")
        time.sleep(2)
else:
    raise SystemExit("MySQL não ficou disponível a tempo.")
PY

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Subindo Django..."
python manage.py runserver 0.0.0.0:8000

