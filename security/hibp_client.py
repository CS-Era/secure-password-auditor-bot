import hashlib
import requests
import time
from functools import lru_cache
import bleach
from config import Config
from utils import SecureLogger, log_execution_time

# Logger sicuro
logger = SecureLogger(__name__)

class HIBPClient:
    """
    Client per l'API di Have I Been Pwned, implementando il pattern k-Anonymity
    per proteggere la privacy dell'utente.
    """
    def __init__(self, api_url=Config.HIBP_API_URL, api_key=Config.HIBP_API_KEY):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            'User-Agent': 'PasswordAuditBot/1.0',
        }
        
        # Aggiungi l'header HIBP-API-Key se disponibile
        if self.api_key:
            self.headers['hibp-api-key'] = self.api_key
            
    @staticmethod
    def hash_password(password):
        """
        Crea un hash SHA-1 della password.
        
        Args:
            password (str): La password da hashare
            
        Returns:
            str: L'hash SHA-1 in formato uppercase
        """
        # SECURITY: Esegue hashing lato client per non trasmettere la password in chiaro
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        return password_hash
    
    @staticmethod
    def sanitize_input(input_str):
        """
        Sanitizza l'input per prevenire attacchi di injection.
        
        Args:
            input_str (str): La stringa da sanitizzare
            
        Returns:
            str: La stringa sanitizzata
        """
        return bleach.clean(input_str, strip=True)
    
    @log_execution_time(logger)
    @lru_cache(maxsize=128)  # Implementazione di caching per ridurre le chiamate API
    def check_password(self, password):
        """
        Verifica se una password è stata compromessa usando k-Anonymity.
        
        Args:
            password (str): La password da verificare
            
        Returns:
            tuple: (bool, int) - (compromessa true/false, quante volte)
        """
        # Sanitizza l'input
        password = self.sanitize_input(password)
        
        # Genera l'hash SHA-1
        password_hash = self.hash_password(password)
        
        # SECURITY & PRIVACY: Implementazione k-Anonymity
        # Invia solo i primi 5 caratteri dell'hash, il resto viene verificato localmente
        prefix = password_hash[:5]
        suffix = password_hash[5:]
        
        # Ottiene gli hash con lo stesso prefisso
        try:
            # SECURITY: Impostazione di timeout per prevenire attacchi DoS
            response = requests.get(
                self.api_url.format(prefix=prefix),
                headers=self.headers,
                timeout=10  # Timeout di sicurezza
            )
            
            # Controlla lo status code
            response.raise_for_status()
            
            # Analizza la risposta (formato: HASH_SUFFIX:COUNT)
            hash_counts = {}
            for line in response.text.splitlines():
                parts = line.split(':')
                if len(parts) == 2:
                    hash_suffix, count = parts
                    hash_counts[hash_suffix] = int(count)
            
            # Verifica se l'hash della password è tra quelli compromessi
            if suffix in hash_counts:
                return True, hash_counts[suffix]
            else:
                return False, 0
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante la connessione a HIBP: {e}")
            return None, 0
            
    def securely_clear_password(self, password_var):
        """
        Cancella in modo sicuro le variabili che contengono password dalla memoria.
        Questa è solo una best practice, ma in Python non è possibile garantire
        la rimozione completa a causa del garbage collector.
        
        Args:
            password_var (str): Riferimento alla variabile contenente la password
        """
        # PRIVACY: Tenta di rimuovere dati sensibili dalla memoria
        if isinstance(password_var, str):
            # Sovrascrivi la variabile con valori casuali
            import random
            import string
            random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len(password_var)))
            password_var = random_str
            
            # Forza la garbage collection
            import gc
            password_var = None
            gc.collect()