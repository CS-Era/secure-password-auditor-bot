FROM python:3.11-slim as base

# SECURITY: Aggiornamento del sistema e installazione minima di dipendenze
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# SECURITY: Creazione di un utente non-root per eseguire l'applicazione
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Directory di lavoro
WORKDIR /app

# Copia i requisiti
COPY requirements.txt .

# SECURITY: Installa le dipendenze in modo sicuro
RUN pip install --no-cache-dir -r requirements.txt && \
    # Rimuove le cache di pip per ridurre la dimensione dell'immagine
    pip cache purge && \
    # Imposta i permessi corretti
    mkdir -p /app/certs && \
    chown -R appuser:appuser /app

# Copia il codice sorgente con un utente non privilegiato
USER appuser
COPY --chown=appuser:appuser . .

# SECURITY: Verifica che i certificati esistano
HEALTHCHECK --interval=5m --timeout=3s \
  CMD test -f certs/fullchain.pem && test -f certs/privkey.pem || exit 1

# Espone la porta standard HTTPS
EXPOSE 443

# Comando di avvio
CMD ["python", "main.py"]