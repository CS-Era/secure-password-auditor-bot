from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from utils import SecureLogger, log_execution_time
from security import PasswordAnalyzer
from .middleware import rate_limit_middleware, secure_context_middleware

# Logger sicuro
logger = SecureLogger(__name__)

# Analyzer per le password
password_analyzer = PasswordAnalyzer()

@rate_limit_middleware
@secure_context_middleware
@log_execution_time(logger)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Gestisce il comando /start e introduce l'utente al bot.
    Implementa middleware per rate limiting e sicurezza.
    """
    user = update.effective_user
    logger.info(f"L'utente {user.id} ha avviato il bot")
    
    welcome_message = (
        f"👋 Benvenuto {user.first_name} al Password Audit Bot!\n\n"
        "Questo bot ti aiuta a verificare la sicurezza delle tue password "
        "senza mai memorizzarle o inviarle a server esterni in chiaro.\n\n"
        "Usa /check per verificare una password\n"
        "Usa /tips per ricevere consigli su password sicure\n"
        "Usa /help per vedere tutti i comandi disponibili\n\n"
        "🔒 *Nota sulla privacy*: Le tue password non vengono mai salvate. "
        "Per la verifica con il database di Have I Been Pwned, "
        "viene utilizzato il metodo k-Anonymity che protegge completamente la tua privacy."
    )
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

@rate_limit_middleware
@secure_context_middleware
@log_execution_time(logger)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Gestisce il comando /help mostrando tutti i comandi disponibili.
    Implementa middleware per rate limiting e sicurezza.
    """
    help_message = (
        "🔍 *Comandi disponibili*:\n\n"
        "/start - Avvia il bot e mostra il messaggio di benvenuto\n"
        "/check - Verifica la sicurezza di una password\n"
        "/tips - Mostra consigli per creare password sicure\n"
        "/help - Mostra questo messaggio\n"
        "/cancel - Annulla l'operazione corrente\n\n"
        "🔒 *Nota sulla privacy*: Le tue password non vengono mai salvate. "
        "Per la verifica con il database di Have I Been Pwned, "
        "viene utilizzato il metodo k-Anonymity che protegge completamente la tua privacy."
    )
    
    await update.message.reply_text(help_message, parse_mode='Markdown')

@rate_limit_middleware
@secure_context_middleware
@log_execution_time(logger)
async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Avvia il processo di verifica della password.
    Implementa middleware per rate limiting e sicurezza.
    """
    await update.message.reply_text(
        "📝 Inviami la password che vuoi verificare.\n\n"
        "🔒 *Nota sulla privacy*: La tua password non verrà mai salvata. "
        "Verrà elaborata in modo sicuro e poi rimossa dalla memoria.\n\n"
        "Usa /cancel per annullare.",
        parse_mode='Markdown'
    )
    
    # Imposta lo stato per attendere la password
    context.user_data['waiting_for_password'] = True

@rate_limit_middleware
@secure_context_middleware
@log_execution_time(logger)
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Annulla l'operazione corrente.
    Implementa middleware per rate limiting e sicurezza.
    """
    # PRIVACY: Rimuovi eventuali stati e dati temporanei
    context.user_data.clear()
    
    await update.message.reply_text(
        "❌ Operazione annullata. Tutti i dati temporanei sono stati eliminati.",
        reply_markup=ReplyKeyboardRemove()
    )

@rate_limit_middleware
@secure_context_middleware
@log_execution_time(logger)
async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Mostra consigli per creare password sicure.
    Implementa middleware per rate limiting e sicurezza.
    """
    tips = password_analyzer.generate_password_tips()
    
    tips_message = "🛡️ *Consigli per password sicure*:\n\n"
    for i, tip in enumerate(tips, 1):
        tips_message += f"{i}. {tip}\n"
    
    await update.message.reply_text(tips_message, parse_mode='Markdown')

@rate_limit_middleware
@secure_context_middleware
@log_execution_time(logger)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Gestisce i messaggi in arrivo, inclusa la password per la verifica.
    Implementa middleware per rate limiting e sicurezza.
    
    SECURITY: Sanitizza gli input e applica rate limiting
    PRIVACY: Non memorizza o logga password
    """
    # Verifica se stiamo aspettando una password
    if context.user_data.get('waiting_for_password'):
        # Log sicuro (non include la password)
        logger.info(f"Ricevuta password da analizzare dall'utente {update.effective_user.id}")
        
        # Prendi il testo del messaggio (la password da verificare)
        password = update.message.text
        
        # PRIVACY: Rimuovi lo stato di attesa
        del context.user_data['waiting_for_password']
        
        # Invia un messaggio che stiamo elaborando
        processing_message = await update.message.reply_text(
            "🔍 Elaborazione in corso...\n"
            "Sto verificando la sicurezza della password."
        )
        
        # Analizza la password
        try:
            result = password_analyzer.analyze_password(password)
            
            # Formatta la risposta
            if result['secure']:
                status_emoji = "✅"
                status_text = "Sicura"
            elif result['hibp_compromised'] is True:
                status_emoji = "⚠️"
                status_text = "Compromessa"
            else:
                status_emoji = "❌"
                status_text = "Non sicura"
                
            response = (
                f"{status_emoji} *Stato*: {status_text}\n"
                f"🔒 *Forza*: {result['strength']} ({result['score']}/100)\n"
            )
            
            # Aggiungi info su HIBP se disponibile
            if result['hibp_compromised'] is True:
                response += f"🚨 *Trovata in {result['hibp_count']} violazioni di dati*\n"
            elif result['hibp_compromised'] is False:
                response += "✅ *Non trovata in violazioni di dati note*\n"
            else:
                response += "⚠️ *Impossibile verificare con il database delle violazioni*\n"
                
            # Aggiungi motivi
            if result['reasons']:
                response += "\n*Problemi riscontrati*:\n"
                for reason in result['reasons']:
                    response += f"- {reason}\n"
                    
            # Aggiungi suggerimenti
            if result['suggestions']:
                response += "\n*Suggerimenti*:\n"
                for suggestion in result['suggestions']:
                    response += f"- {suggestion}\n"
                    
            # Se la password non è sicura, proponi di verificarne un'altra
            if not result['secure']:
                response += (
                    "\nVuoi verificare un'altra password? Usa il comando /check."
                )
            
            # Elimina il messaggio di elaborazione e invia il risultato
            await processing_message.delete()
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Errore durante l'analisi della password: {str(e)}")
            await processing_message.delete()
            await update.message.reply_text(
                "❌ Si è verificato un errore durante l'analisi. "
                "Riprova più tardi o contatta l'amministratore del bot."
            )
            
        # PRIVACY: Elimina in modo sicuro la password
        password = None
        
    else:
        # Messaggio generico se non stiamo aspettando una password
        await update.message.reply_text(
            "Non ho capito il tuo messaggio. Usa /help per vedere i comandi disponibili."
        )