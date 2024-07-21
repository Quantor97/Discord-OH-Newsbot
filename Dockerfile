# Verwende ein offizielles Python-Laufzeit-Image als Basis
FROM python:3.10-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt und installiere die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere die NewsBot-Dateien
COPY . /app/NewsBot

# Stelle sicher, dass die Umgebungsvariablen aus der .env-Datei geladen werden
ENV PYTHONUNBUFFERED=1

# Führe die Event- und News-Bots aus
CMD ["sh", "-c", "python main.py"]