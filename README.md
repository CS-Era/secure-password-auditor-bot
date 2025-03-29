# Password Audit Bot per Telegram [![Chat with Bot](https://img.shields.io/badge/Telegram-Chat%20with%20Bot-blue?logo=telegram)](https://t.me/passwordaudit_bot)

Un bot Telegram per verificare la sicurezza delle password in modo sicuro e rispettoso della privacy, implementando le migliori pratiche di security by design e privacy by design.


## 🔒 Caratteristiche

- **Verifica password** tramite il database Have I Been Pwned utilizzando k-Anonymity
- **Rate limiting** per proteggere da attacchi di brute force e DoS
- **Sanitizzazione input** per prevenire injection e altri attacchi
- **Logging sicuro** senza memorizzazione di dati sensibili
- **Deployment sicuro** con HTTPS via webhook
- **Architettura modulare** per facile manutenzione e aggiornamenti
- **Esecuzione containerizzata** con Docker e Docker Compose


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
