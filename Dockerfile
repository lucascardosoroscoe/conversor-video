FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y git ffmpeg
RUN pip install git+https://github.com/openai/whisper.git


COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]