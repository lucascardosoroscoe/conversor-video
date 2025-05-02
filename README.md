# 🎧 FastAPI Audio Converter

Este projeto é uma API desenvolvida com FastAPI que permite o upload de vídeos, conversão automática para áudio `.ogg` com codec `opus` via FFmpeg, e armazenamento dos arquivos no MinIO. O processamento é assíncrono via Celery + Redis e todos os metadados são salvos no PostgreSQL.

---

## 🚀 Funcionalidades
- Upload de arquivos de vídeo
- Conversão automática para `.ogg` com FFmpeg
- Armazenamento do vídeo original e do áudio convertido no MinIO
- Rastreamento de status de tarefas com Celery + Redis
- Banco de dados PostgreSQL com registros de uploads
- Filtros de listagem por status, nome do arquivo e intervalo de datas

---

## 🛠️ Tecnologias Utilizadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Redis](https://redis.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [MinIO](https://min.io/)
- [FFmpeg](https://ffmpeg.org/)
- Docker + Docker Compose

---

## 📦 Como rodar o projeto

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd conversor-video
```

### 2. Crie o arquivo `.env`
```env
MINIO_ENDPOINT_URL=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=uploads
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

### 3. Suba a aplicação com Docker Compose
```bash
docker-compose up --build
```

Aguarde até que todos os containers estejam em funcionamento.

---

## 🌐 Acessos e Testes

### ▶️ FastAPI Docs (Swagger UI)
```
http://localhost:8000/docs
```

### 💾 MinIO Console
```
http://localhost:9001
```
Login: `minioadmin` / `minioadmin`

⚠️ Crie o bucket chamado `uploads` se ele ainda não existir.

---

## 📤 Endpoints

### POST `/upload-video`
- Envia um vídeo para conversão e processamento assíncrono.
- Retorna `task_id` para rastrear o status.

### GET `/task-status/{task_id}`
- Consulta o status de uma tarefa enviada anteriormente.

### GET `/uploads`
- Lista todos os uploads com filtros opcionais:
  - `status` (PENDING, STARTED, SUCCESS, FAILURE)
  - `filename` (busca parcial)
  - `start_date`, `end_date` (formato ISO: 2024-05-01T00:00:00)
  - `skip`, `limit` (para paginação)

---

## 🗃️ Estrutura de Diretórios

```bash
├── app
│   ├── api
│   │   ├── video.py
│   │   └── uploads.py
│   ├── services
│   │   ├── converter.py
│   │   └── storage.py
│   ├── models.py
│   ├── tasks.py
│   ├── database.py
│   ├── config.py
│   ├── main.py
│   └── celery_worker.py
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
└── README.md
```

---

## ✅ Próximas Melhorias (Sugeridas)
- Interface web para uploads e consulta dos arquivos
- Autenticação de usuários
- Download direto dos arquivos do MinIO via link temporário
- Geração automática de relatórios (PDF ou JSON)

---

## 👨‍💻 Desenvolvido por
Seu nome ou equipe aqui 👋# 🎧 FastAPI Audio Converter

Este projeto é uma API desenvolvida com FastAPI que permite o upload de vídeos, conversão automática para áudio `.ogg` com codec `opus` via FFmpeg, e armazenamento dos arquivos no MinIO. O processamento é assíncrono via Celery + Redis e todos os metadados são salvos no PostgreSQL.

---

## 🚀 Funcionalidades
- Upload de arquivos de vídeo
- Conversão automática para `.ogg` com FFmpeg
- Armazenamento do vídeo original e do áudio convertido no MinIO
- Rastreamento de status de tarefas com Celery + Redis
- Banco de dados PostgreSQL com registros de uploads
- Filtros de listagem por status, nome do arquivo e intervalo de datas

---

## 🛠️ Tecnologias Utilizadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Redis](https://redis.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [MinIO](https://min.io/)
- [FFmpeg](https://ffmpeg.org/)
- Docker + Docker Compose

---

## 📦 Como rodar o projeto

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd fastapi_audio_converter
```

### 2. Crie o arquivo `.env`
```env
MINIO_ENDPOINT_URL=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=uploads
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

### 3. Suba a aplicação com Docker Compose
```bash
docker-compose up --build
```

Aguarde até que todos os containers estejam em funcionamento.

---

## 🌐 Acessos e Testes

### ▶️ FastAPI Docs (Swagger UI)
```
http://localhost:8000/docs
```

### 💾 MinIO Console
```
http://localhost:9001
```
Login: `minioadmin` / `minioadmin`

⚠️ Crie o bucket chamado `uploads` se ele ainda não existir.

---

## 📤 Endpoints

### POST `/upload-video`
- Envia um vídeo para conversão e processamento assíncrono.
- Retorna `task_id` para rastrear o status.

### GET `/task-status/{task_id}`
- Consulta o status de uma tarefa enviada anteriormente.

### GET `/uploads`
- Lista todos os uploads com filtros opcionais:
  - `status` (PENDING, STARTED, SUCCESS, FAILURE)
  - `filename` (busca parcial)
  - `start_date`, `end_date` (formato ISO: 2024-05-01T00:00:00)
  - `skip`, `limit` (para paginação)

---

## 🗃️ Estrutura de Diretórios

```bash
├── app
│   ├── api
│   │   ├── video.py
│   │   └── uploads.py
│   ├── services
│   │   ├── converter.py
│   │   └── storage.py
│   ├── models.py
│   ├── tasks.py
│   ├── database.py
│   ├── config.py
│   ├── main.py
│   └── celery_worker.py
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
└── README.md
```

---

## ✅ Próximas Melhorias (Sugeridas)
- Interface web para uploads e consulta dos arquivos
- Autenticação de usuários
- Download direto dos arquivos do MinIO via link temporário
- Geração automática de relatórios (PDF ou JSON)

---

## 👨‍💻 Desenvolvido por
Lucas Roscoe - FHR Softwares
