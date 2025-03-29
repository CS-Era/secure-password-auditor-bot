from functools import wraps
from cachetools import TTLCache
import time
from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from utils import SecureLogger

# Logger sicuro
logger = SecureLogger(__name__)

# SECURITY: Cache per il rate limiting con tempo di scadenza automatico
rate_limit_cache = TTLCache(maxsize=1000, ttl=Config.RATE_LIMIT_WINDOW)

def rate_limit_middleware(func):
    """
    Decorator per implementare il rate limiting sui gestori di messaggi.
    Limita il numero di messaggi che un utente può inviare in un determinato periodo.
    
    SECURITY: Protegge contro attacchi di tipo brute force e DoS
    
    Args:
        func: La funzione del gestore da wrappare
    
    Returns:
        Function: La funzione wrappata con rate limiting
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # Ottieni l'ID utente
        user_id = update.effective_user.id
        
        # Ottieni il timestamp corrente
        current_time = time.time()
        
        # Ottieni la lista dei timestamp per l'utente o creane una nuova
        user_timestamps = rate_limit_cache.get(user_id, [])
        
        # Filtra i timestamp all'interno della finestra di rate limiting
        user_timestamps = [ts for ts in user_timestamps if current_time - ts < Config.RATE_LIMIT_WINDOW]
        
        # Aggiungi il timestamp corrente
        user_timestamps.append(current_time)
        
        # Aggiorna la cache
        rate_limit_cache[user_id] = user_timestamps
        
        # Verifica se l'utente ha superato il limite
        if len(user_timestamps) > Config.RATE_LIMIT_MAX_CALLS:
            logger.warning(f"Rate limit superato per l'utente {user_id}")
            await update.message.reply_text(
                "⚠️ Hai inviato troppi messaggi in poco tempo. "
                f"Riprova fra {Config.RATE_LIMIT_WINDOW} secondi."
            )
            return
        
        # Se non ha superato il limite, esegui la funzione originale
        return await func(update, context, *args, **kwargs)
    
    return wrapper

def secure_context_middleware(func):
    """
    Decorator per assicurarsi che il contesto non contenga informazioni sensibili
    dopo l'esecuzione della funzione.
    
    PRIVACY: Rimuove dati sensibili dal contesto dopo l'uso
    
    Args:
        func: La funzione del gestore da wrappare
    
    Returns:
        Function: La funzione wrappata con pulizia del contesto
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # Esegui la funzione originale
        result = await func(update, context, *args, **kwargs)
        
        # Pulisci eventuali dati sensibili dal contesto
        if hasattr(context, 'user_data') and 'password' in context.user_data:
            del context.user_data['password']
            
        return result
    
    return wrapper