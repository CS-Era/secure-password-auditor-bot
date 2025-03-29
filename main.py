import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
from utils import SecureLogger
from bot import (
    start_command,
    help_command,
    check_command,
    cancel_command,
    tips_command,
    handle_message
)

# Logger sicuro
logger = SecureLogger(__name__)

def main() -> None:
    """
    Funzione principale che avvia il bot in modalità webhook (sicura) o polling.
    
    SECURITY: Usa webhook HTTPS per comunicazioni sicure
    """
    logger.info("Avvio del Password Audit Bot")
    
    # SECURITY: Verifica path dei certificati
    if Config.MODE == "webhook":
        if not os.path.exists(Config.SSL_CERT_PATH) or not os.path.exists(Config.SSL_KEY_PATH):
            logger.error(f"Certificati SSL non trovati in {Config.SSL_CERT_PATH} e {Config.SSL_KEY_PATH}")
            sys.exit(1)
    
    # Crea l'applicazione
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Aggiungi i gestori dei comandi
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(CommandHandler("tips", tips_command))
    
    # Aggiungi un gestore per i messaggi normali
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Avvia il bot nella modalità configurata
    if Config.MODE == "webhook":
        # Modalità webhook (più sicura)
        logger.info(f"Bot avviato in modalità webhook su porta {Config.PORT}")
        logger.info(f"Webhook URL: {Config.WEBHOOK_URL}")
        # SECURITY: Usa SSL/TLS per comunicazioni sicure
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            url_path=Config.TELEGRAM_BOT_TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.TELEGRAM_BOT_TOKEN}",
            cert=Config.SSL_CERT_PATH,
            key=Config.SSL_KEY_PATH
        )
    else:
        # Modalità polling 
        logger.warning("Bot avviato in modalità polling. Si consiglia l'uso della modalità webhook.")
        application.run_polling()

if __name__ == '__main__':
    main()