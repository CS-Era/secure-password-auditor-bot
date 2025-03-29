import re
import string
import math
from .hibp_client import HIBPClient
from utils import SecureLogger

# Logger sicuro
logger = SecureLogger(__name__)

class PasswordAnalyzer:
    """
    Classe per l'analisi della sicurezza delle password.
    Utilizza diversi criteri e il database HIBP.
    
    SECURITY: Implementa analisi completa delle password in base a criteri di sicurezza
    PRIVACY: Non memorizza le password, le analizza solo in memoria temporanea
    """
    def __init__(self):
        self.hibp_client = HIBPClient()
        
    def analyze_password(self, password):
        """
        Analizza una password e restituisce un'analisi dettagliata.
        
        Args:
            password (str): La password da analizzare
            
        Returns:
            dict: Risultati dell'analisi
        """
        # Verifica che la password non sia vuota o troppo breve
        if not password or len(password) < 4:
            return {
                'secure': False,
                'hibp_compromised': False,
                'hibp_count': 0,
                'strength': 'Molto debole',
                'reasons': ['La password è troppo corta.'],
                'suggestions': ['Usa una password di almeno 12 caratteri.']
            }
            
        # Verifica con HIBP
        try:
            # SECURITY & PRIVACY: Verifica compromissione tramite k-Anonymity
            is_compromised, breach_count = self.hibp_client.check_password(password)
        except Exception as e:
            logger.error(f"Errore durante la verifica HIBP: {str(e)}")
            is_compromised = None
            breach_count = 0
        
        # Calcola il punteggio della password
        score, feedback = self._evaluate_password_strength(password)
        
        # Determina la forza della password
        strength = self._get_strength_label(score)
        
        # MIGLIORAMENTO: Abbassata la soglia per considerare una password sicura
        # da 80 a 70, purché non sia stata compromessa
        is_secure = (score >= 70) and (is_compromised is False)
        
        # Preparazione del risultato
        reasons = feedback['reasons']
        suggestions = feedback['suggestions']
        
        # Aggiungi informazioni sulla compromissione HIBP
        if is_compromised is True:
            reasons.append(f"La password è stata trovata in {breach_count} violazioni di dati.")
            suggestions.append("Cambia immediatamente questa password ovunque la stai utilizzando.")
        elif is_compromised is None:
            suggestions.append("Non è stato possibile verificare la password con il database delle violazioni.")
        
        # PRIVACY: Pulisci la memoria (best practice)
        self.hibp_client.securely_clear_password(password)
        
        return {
            'secure': is_secure,
            'hibp_compromised': is_compromised,
            'hibp_count': breach_count,
            'strength': strength,
            'score': score,
            'reasons': reasons,
            'suggestions': suggestions
        }
    
    def _evaluate_password_strength(self, password):
        """
        Valuta la forza di una password in base a vari criteri.
        
        Args:
            password (str): La password da valutare
            
        Returns:
            tuple: (score, feedback) dove score è un numero da 0 a 100 e
                  feedback è un dizionario con 'reasons' e 'suggestions'
        """
        score = 0
        reasons = []
        suggestions = []
        
        # Criterio: Lunghezza
        length = len(password)
        # MIGLIORAMENTO: Punteggio più graduale per la lunghezza
        if length >= 16:
            score += 40
        elif length >= 12:
            score += 30
        elif length >= 10:
            score += 25
        elif length >= 8:
            score += 20
        elif length >= 6:
            score += 10
        else:
            reasons.append("La password è troppo corta.")
            suggestions.append("Usa una password di almeno 12 caratteri.")
        
        # Criterio: Complessità
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_digits = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[^A-Za-z0-9]', password))
        
        complexity_score = 0
        if has_lowercase:
            complexity_score += 10
        else:
            reasons.append("Mancano lettere minuscole.")
            suggestions.append("Aggiungi lettere minuscole (a-z).")
            
        if has_uppercase:
            complexity_score += 10
        else:
            reasons.append("Mancano lettere maiuscole.")
            suggestions.append("Aggiungi lettere maiuscole (A-Z).")
            
        if has_digits:
            complexity_score += 10
        else:
            reasons.append("Mancano numeri.")
            suggestions.append("Aggiungi numeri (0-9).")
            
        if has_special:
            complexity_score += 10
        else:
            reasons.append("Mancano caratteri speciali.")
            suggestions.append("Aggiungi caratteri speciali (!, @, #, $, ecc.).")
        
        score += complexity_score
        
        # SECURITY: Controlla pattern comuni nelle password
        common_patterns = [
            r'123456',
            r'qwerty',
            r'password',
            r'admin',
            r'welcome',
            r'abcdef',
            r'123321',
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                score -= 20
                reasons.append(f"La password contiene un pattern comune ({pattern}).")
                suggestions.append("Evita sequenze di caratteri comuni.")
                break
        
        # Criterio: Ripetizioni
        if re.search(r'(.)\1{2,}', password):  # 3+ caratteri ripetuti
            score -= 15
            reasons.append("La password contiene caratteri ripetuti.")
            suggestions.append("Evita di ripetere lo stesso carattere più volte.")
        
        # MIGLIORAMENTO: Calcolo dell'entropia più accurato
        charset_size = 0
        if has_lowercase:
            charset_size += 26
        if has_uppercase:
            charset_size += 26
        if has_digits:
            charset_size += 10
        if has_special:
            charset_size += 33  # Approssimazione dei caratteri speciali su una tastiera standard
        
        if charset_size > 0:
            # Calcolo entropia più realistico basato sulla formula log2(charset_size^length)
            # Ma ponderato per mantenere il punteggio entro 0-100
            entropy = length * math.log2(charset_size)
            entropy_score = min(25, int(entropy / 40 * 25))
            score += entropy_score
            
            # MIGLIORAMENTO: Bonus per mix di tipi di caratteri
            char_types = sum([has_lowercase, has_uppercase, has_digits, has_special])
            if char_types >= 3 and length >= 8:
                score += 5
            if char_types == 4 and length >= 10:
                score += 5
        
        # Limita il punteggio a 100
        score = min(100, max(0, score))
        
        # Aggiungi suggerimenti generali se necessario
        if score < 60 and "usa una password di almeno 12 caratteri" not in " ".join(suggestions).lower():
            suggestions.append("Considera l'uso di un gestore di password per generare e memorizzare password complesse.")
        
        return score, {'reasons': reasons, 'suggestions': suggestions}
    
    def _get_strength_label(self, score):
        """
        Converte un punteggio numerico in un'etichetta di forza.
        
        Args:
            score (int): Il punteggio da 0 a 100
            
        Returns:
            str: L'etichetta corrispondente
        """
        # MIGLIORAMENTO: Etichette di forza più granulari
        if score >= 90:
            return "Molto forte"
        elif score >= 75:
            return "Forte"
        elif score >= 60:
            return "Buona"
        elif score >= 40:
            return "Media"
        elif score >= 25:
            return "Debole"
        else:
            return "Molto debole"
    
    def generate_password_tips(self):
        """
        Restituisce consigli per la creazione di password sicure.
        
        Returns:
            list: Lista di consigli
        """
        return [
            "Usa una password di almeno 12 caratteri.",
            "Combina lettere maiuscole, minuscole, numeri e caratteri speciali.",
            "Evita informazioni personali come nomi, date di nascita o parole di dizionario.",
            "Usa password diverse per ogni servizio.",
            "Considera l'uso di un gestore di password per generare e memorizzare password complesse.",
            "Attiva l'autenticazione a due fattori (2FA) quando disponibile.",
            "Cambia le password regolarmente, soprattutto per gli account sensibili.",
            "Evita sequenze di caratteri comuni come '123456' o 'qwerty'.",
            "Usa frasi password: combinazioni di parole casuali facili da ricordare ma difficili da indovinare."
        ]