import logging
from functools import wraps
import re
import time

# Pattern che possono contenere informazioni sensibili 
# SECURITY: Previene il logging di dati sensibili
SENSITIVE_PATTERNS = [
    r'password',
    r'token',
    r'apikey',
    r'secret',
    r'credential'
]

class SecureLogger:
    """
    Utility per il logging sicuro che evita di registrare informazioni sensibili.
    """
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
    def sanitize_log(self, message):
        """Rimuove informazioni potenzialmente sensibili dal messaggio di log."""
        if not isinstance(message, str):
            message = str(message)
        
        # Sostituisce i pattern sensibili con [REDACTED]
        for pattern in SENSITIVE_PATTERNS:
            regex = re.compile(f'{pattern}[=:]\s*[^\s]+', re.IGNORECASE)
            message = regex.sub(f'{pattern}=[REDACTED]', message)
        return message
        
    def info(self, message, *args, **kwargs):
        """Log di tipo info con sanitizzazione."""
        self.logger.info(self.sanitize_log(message), *args, **kwargs)
        
    def warning(self, message, *args, **kwargs):
        """Log di tipo warning con sanitizzazione."""
        self.logger.warning(self.sanitize_log(message), *args, **kwargs)
        
    def error(self, message, *args, **kwargs):
        """Log di tipo error con sanitizzazione."""
        self.logger.error(self.sanitize_log(message), *args, **kwargs)
        
    def debug(self, message, *args, **kwargs):
        """Log di tipo debug con sanitizzazione."""
        self.logger.debug(self.sanitize_log(message), *args, **kwargs)
        
    def critical(self, message, *args, **kwargs):
        """Log di tipo critical con sanitizzazione."""
        self.logger.critical(self.sanitize_log(message), *args, **kwargs)

def log_execution_time(logger):
    """
    Decorator per misurare e loggare il tempo di esecuzione di una funzione.
    Non include dati sensibili.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.debug(f"Funzione {func.__name__} eseguita in {execution_time:.4f} secondi")
            return result
        return wrapper
    return decorator