# Password Audit Bot per Telegram

Un bot Telegram per verificare la sicurezza delle password in modo sicuro e rispettoso della privacy, implementando le migliori pratiche di security by design e privacy by design.

## 🔒 Caratteristiche

- **Verifica password** tramite il database Have I Been Pwned utilizzando k-Anonymity
- **Rate limiting** per proteggere da attacchi di brute force e DoS
- **Sanitizzazione input** per prevenire injection e altri attacchi
- **Logging sicuro** senza memorizzazione di dati sensibili
- **Deployment sicuro** con HTTPS via webhook
- **Architettura modulare** per facile manutenzione e aggiornamenti
- **Esecuzione containerizzata** con Docker e Docker Compose

## 🛡️ Misure di Sicurezza Implementate

- **k-Anonymity**: Le password non vengono mai inviate in chiaro durante la verifica con HIBP
- **Nessuna persistenza**: Le password non vengono mai salvate su disco o in database
- **Sanitizzazione dell'input**: Tutti gli input vengono sanitizzati prima dell'elaborazione
- **Rate limiting**: Protezione contro attacchi di forza bruta
- **Comunicazione HTTPS**: Tutte le comunicazioni avvengono tramite canali crittografati
- **Esecuzione sicura**: Container Docker con utente non privilegiato
- **Sanitizzazione dei log**: I dati sensibili non vengono mai registrati nei log
- **Gestione sicura dei certificati**: Certificati montati in sola lettura

## 📋 Requisiti

- Python 3.9+
- Docker e Docker Compose
- Certificati SSL/TLS validi
- Token di un bot Telegram
- (Opzionale ma consigliato) API Key per Have I Been Pwned

## 🚀 Installazione e Configurazione

### 1. Clona il repository

```bash
git clone https://github.com/yourusername/password-audit-bot.git
cd password-audit-bot
```

### 2. Configura le variabili d'ambiente

Copia il file `.env.example` in `.env` e configura le variabili:

```bash
cp .env.example .env
nano .env
```

Modifica le seguenti variabili:
- `TELEGRAM_BOT_TOKEN`: Il token del tuo bot Telegram ottenuto da [@BotFather](https://t.me/BotFather)
- `WEBHOOK_URL`: L'URL pubblico del tuo server (deve essere HTTPS)
- `HIBP_API_KEY`: (Opzionale) La tua API key per Have I Been Pwned

### 3. Prepara i certificati SSL

Assicurati di avere i certificati SSL validi nella cartella `certs/`:
- `fullchain.pem`: Certificato completo
- `privkey.pem`: Chiave privata

Per ottenere certificati gratuiti, puoi utilizzare Let's Encrypt:

```bash
# Esempio con Certbot
sudo certbot certonly --standalone -d your-domain.com
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem certs/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem certs/
sudo chmod 644 certs/fullchain.pem
sudo chmod 600 certs/privkey.pem
```

### 4. Avvia il bot con Docker Compose

```bash
docker-compose up -d
```

## 🔧 Sviluppo

Per lo sviluppo locale, puoi utilizzare un ambiente virtuale Python:

```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Per eseguire il bot in modalità polling (solo per sviluppo):

```bash
# Modifica MODE=polling nel file .env
python main.py
```

## 📖 Struttura del Progetto

```
telegram_bot/
├── bot/                    # Gestori dei comandi e middleware
│   ├── __init__.py
│   ├── handlers.py         # Handler per i comandi del bot
│   └── middleware.py       # Middleware per rate limiting e sicurezza
├── security/               # Moduli per la sicurezza
│   ├── __init__.py
│   ├── password_analyzer.py # Analisi della sicurezza delle password
│   └── hibp_client.py      # Client per l'API di Have I Been Pwned
├── utils/                  # Utilities
│   ├── __init__.py
│   └── logging.py          # Logger sicuro
├── certs/                  # Certificati SSL/TLS
├── config.py               # Configurazione centralizzata
├── main.py                 # Punto di ingresso principale
├── Dockerfile              # Configurazione Docker
├── docker-compose.yml      # Configurazione Docker Compose
├── requirements.txt        # Dipendenze Python
├── .env                    # Variabili d'ambiente (non versionato)
└── .env.example            # Esempio di variabili d'ambiente
```

## 📝 Comandi del Bot

- `/start` - Avvia il bot e mostra il messaggio di benvenuto
- `/check` - Verifica la sicurezza di una password
- `/tips` - Mostra consigli per creare password sicure
- `/help` - Mostra tutti i comandi disponibili
- `/cancel` - Annulla l'operazione corrente

## ⚙️ Best Practices di Security e Privacy

### Security by Design

- **Principio del privilegio minimo**: Esecuzione con utente non privilegiato
- **Difesa in profondità**: Multiple misure di sicurezza implementate
- **Fail secure**: In caso di errore, non rivela informazioni sensibili
- **Validazione input**: Tutti gli input vengono validati e sanitizzati
- **Protezione DoS**: Rate limiting per prevenire attacchi di denial of service
- **HTTPS obbligatorio**: Le comunicazioni avvengono solo tramite canali sicuri
- **Configurazione sicura**: Nessun valore sensibile hardcoded nel codice

### Privacy by Design

- **Minimizzazione dei dati**: Solo i dati essenziali vengono elaborati
- **Nessuna persistenza**: Le password non vengono mai salvate
- **k-Anonymity**: La verifica con HIBP avviene senza rivelare la password completa
- **Trasparenza**: Chiara comunicazione all'utente su come vengono gestiti i dati
- **Controllo utente**: L'utente può annullare il processo in qualsiasi momento
- **Privacy dei log**: I log non contengono dati sensibili o identificativi

## 🔄 Manutenzione

### Aggiornamento del bot

```bash
git pull
docker-compose down
docker-compose up --build -d
```

### Rinnovo dei certificati

Dopo aver rinnovato i certificati SSL:

```bash
# Copia i nuovi certificati
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem certs/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem certs/
sudo chmod 644 certs/fullchain.pem
sudo chmod 600 certs/privkey.pem

# Riavvia il container
docker-compose restart
```

## 🔍 Troubleshooting

### Il bot non risponde

1. Verifica che il bot sia in esecuzione: `docker-compose ps`
2. Controlla i log: `docker-compose logs -f`
3. Verifica che i certificati SSL siano validi e leggibili
4. Assicurati che la porta 443 sia accessibile pubblicamente
5. Controlla che l'URL del webhook sia corretto e accessibile

### Errori con l'API di HIBP

1. Verifica che la tua API key sia corretta
2. Controlla i rate limit dell'API HIBP
3. Verifica la connessione internet del server

## 🔐 Note sulla Sicurezza

- **Mai condividere il tuo token del bot** o altre credenziali
- **Aggiorna regolarmente** le dipendenze per mitigare vulnerabilità
- **Monitora i log** per potenziali tentativi di attacco
- **Limita l'accesso** al server e ai certificati SSL
- **Verifica periodicamente** che i certificati SSL siano validi

## 📜 Licenza

[MIT License](LICENSE)