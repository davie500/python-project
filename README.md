# Projeto LLM - Django + MySQL

Aplicação web Django containerizada com banco de dados MySQL.

## Tecnologias Utilizadas

- **Python** 3.12
- **Django** 5.x
- **MySQL** 8.0
- **Docker** & **Docker Compose**

## Pré-requisitos

Certifique-se de ter instalado:

- [Docker](https://docs.docker.com/get-docker/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0+)

## Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd projeto-llm
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do MySQL
MYSQL_DATABASE=projeto_llm
MYSQL_USER=django_user
MYSQL_PASSWORD=sua_senha_segura
MYSQL_ROOT_PASSWORD=sua_senha_root_segura
MYSQL_HOST=db
MYSQL_PORT=3306

# Configurações do Django
DJANGO_SECRET_KEY=sua_chave_secreta_django
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
```

> **Importante:** Em ambiente de produção, utilize senhas fortes e defina `DEBUG=0`.

### 3. Inicie os containers

```bash
docker compose up --build
```

O sistema irá:
1. Construir a imagem Docker do Django
2. Iniciar o container do MySQL
3. Aguardar o MySQL ficar disponível
4. Executar as migrations automaticamente
5. Iniciar o servidor Django na porta 8000

### 4. Acesse a aplicação

- **Aplicação:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin

## Estrutura do Projeto

```
projeto-llm/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py      # Configurações do Django
│   │   ├── urls.py          # Rotas principais
│   │   └── wsgi.py          # Configuração WSGI
│   └── manage.py            # CLI do Django
├── docker-compose.yml       # Orquestração dos containers
├── Dockerfile               # Imagem do Django
├── entrypoint.sh            # Script de inicialização
├── requirements.txt         # Dependências Python
└── README.md
```

## Comandos Úteis

### Gerenciamento de Containers

```bash
# Iniciar em segundo plano
docker compose up -d

# Parar os containers
docker compose down

# Ver logs
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f web
docker compose logs -f db

# Reconstruir após alterações no Dockerfile ou requirements
docker compose up --build
```

### Comandos Django

```bash
# Acessar o shell do container Django
docker compose exec web bash

# Executar migrations
docker compose exec web python manage.py migrate

# Criar superusuário
docker compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker compose exec web python manage.py collectstatic

# Acessar o shell do Django
docker compose exec web python manage.py shell

# Criar nova app Django
docker compose exec web python manage.py startapp nome_da_app
```

### Banco de Dados

```bash
# Acessar o MySQL via CLI
docker compose exec db mysql -u django_user -p

# Fazer backup do banco
docker compose exec db mysqldump -u django_user -p projeto_llm > backup.sql

# Restaurar backup
docker compose exec -T db mysql -u django_user -p projeto_llm < backup.sql
```

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `MYSQL_DATABASE` | Nome do banco de dados | `projeto_llm` |
| `MYSQL_USER` | Usuário do MySQL | `django_user` |
| `MYSQL_PASSWORD` | Senha do usuário MySQL | `senha_segura` |
| `MYSQL_ROOT_PASSWORD` | Senha root do MySQL | `senha_root` |
| `MYSQL_HOST` | Host do MySQL | `db` |
| `MYSQL_PORT` | Porta do MySQL | `3306` |
| `DJANGO_SECRET_KEY` | Chave secreta do Django | `chave-aleatoria` |
| `DEBUG` | Modo debug (1=ativo, 0=inativo) | `1` |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por vírgula) | `localhost,127.0.0.1` |

## Solução de Problemas

### MySQL não inicia

Verifique se a porta 3306 não está em uso por outro serviço:

```bash
sudo lsof -i :3306
```

### Erro de conexão com o banco

1. Verifique se o arquivo `.env` existe e está configurado corretamente
2. Aguarde o healthcheck do MySQL completar (pode levar alguns segundos)
3. Verifique os logs: `docker compose logs db`

### Limpar dados e recomeçar

```bash
# Remove containers, volumes e redes
docker compose down -v

# Reconstrói tudo do zero
docker compose up --build
```

## Produção

Para deploy em produção, considere:

1. Definir `DEBUG=0` no `.env`
2. Usar senhas fortes e únicas
3. Configurar um servidor web como Nginx como proxy reverso
4. Usar Gunicorn ao invés do servidor de desenvolvimento do Django
5. Configurar HTTPS/SSL
6. Implementar backups automáticos do banco de dados

---

Desenvolvido com Django e Docker.
