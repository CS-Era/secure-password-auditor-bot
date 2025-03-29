import os
import logging
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione del logging di base (estensione effettuata nella classe di utilità)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configurazione del bot
class Config:
    """
    Centralizza tutte le configurazioni dell'applicazione, evitando variabili
    sparse nel codice (security by design: configurazione centralizzata).
    """

    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Nessun token trovato. Imposta la variabile d'ambiente TELEGRAM_BOT_TOKEN")

    # Modalità di esecuzione (webhook o polling)
    MODE = os.getenv("MODE", "polling")
    
    # URL del webhook
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if MODE == "webhook" and not WEBHOOK_URL:
        raise ValueError("In modalità webhook, la variabile WEBHOOK_URL deve essere impostata")
    
    # Porta per il webhook
    PORT = int(os.getenv("PORT", "443"))
    
    # Percorsi dei certificati SSL
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "certs/fullchain.pem")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH", "certs/privkey.pem")
    
    # Configurazione per HIBP API
    HIBP_API_KEY = os.getenv("HIBP_API_KEY")
    HIBP_API_URL = "https://api.pwnedpasswords.com/range/{prefix}"
    
    # Configurazione per rate limiting
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # secondi
    RATE_LIMIT_MAX_CALLS = int(os.getenv("RATE_LIMIT_MAX_CALLS", "5"))  # numero di richieste