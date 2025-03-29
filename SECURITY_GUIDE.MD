# Guida alla Sicurezza del Password Audit Bot

Questo documento fornisce una panoramica dettagliata delle misure di sicurezza implementate nel Password Audit Bot e ulteriori raccomandazioni per l'installazione e la manutenzione sicura.

## 🔒 Principi di Sicurezza Applicati

### Principio del Privilegio Minimo

Il bot opera sempre con i privilegi minimi necessari:

- **Utente non-root**: L'applicazione viene eseguita come un utente non privilegiato all'interno del container Docker
- **Volume in sola lettura**: I certificati SSL vengono montati in sola lettura
- **Accesso limitato**: L'applicazione accede solo alle risorse necessarie

### Difesa in Profondità

Il bot implementa multiple misure di sicurezza che lavorano insieme:

- **HTTPS con TLS**: Comunicazioni crittografate
- **Rate limiting**: Protezione contro attacchi di forza bruta
- **Sanitizzazione dell'input**: Prevenzione di attacchi di injection
- **Verifica dei certificati**: Validazione dei certificati SSL
- **Timeout di connessione**: Protezione contro attacchi di denial of service

### Fail Secure

In caso di errori, il sistema si comporta in modo sicuro:

- **Nessun dato sensibile nei messaggi di errore**: Gli errori non rivelano informazioni interne
- **Validazione input conservativa**: In caso di input sospetto, l'operazione viene rifiutata
- **Gestione sicura degli errori API**: Se l'API HIBP non risponde, non si conferma che la password sia sicura

## 🛡️ Dettagli delle Implementazioni di Sicurezza

### 1. Protezione delle Password

#### k-Anonymity con HIBP

La verifica delle password tramite Have I Been Pwned utilizza il principio di k-Anonymity:

1. La password viene hashata localmente utilizzando SHA-1
2. Solo i primi 5 caratteri dell'hash vengono inviati all'API HIBP
3. L'API restituisce tutti gli hash che iniziano con quei 5 caratteri
4. Il client verifica localmente se la password completa è presente tra i risultati

Questo garantisce che:
- La password non venga mai inviata al servizio esterno
- Il servizio esterno non possa determinare la password esatta

### 2. Protezione contro Attacchi

#### Rate Limiting

Implementazione di rate limiting per contrastare attacchi di forza bruta:

- **Limitazione per utente**: Limite di richieste per utente
- **Finestra temporale**: Le limitazioni si applicano in un intervallo di tempo configurable
- **Cache TTL**: Utilizzo di TTLCache per gestire automaticamente la scadenza

#### Sanitizzazione dell'Input

Tutti gli input vengono sanitizzati prima dell'elaborazione:

- **Bleach**: Rimozione di caratteri potenzialmente pericolosi
- **Validazione dei tipi**: Controllo del tipo di dati atteso

### 3. Logging Sicuro

Implementazione di un logger sicuro che:

- **Redige dati sensibili**: Password e token vengono sostituiti con [REDACTED]
- **Pattern-matching**: Identificazione automatica di informazioni sensibili
- **Minimizzazione dei dati**: Log limitati alle informazioni necessarie

### 4. Comunicazioni Sicure

#### Webhook HTTPS

- **Certificati SSL/TLS**: Obbligatori per il funzionamento in modalità webhook
- **Webhook URL sicuro**: Devono utilizzare il protocollo HTTPS
- **Verifica dei certificati**: Verifica della validità dei certificati all'avvio

## 📝 Best Practices per l'Amministrazione

### Gestione dei Segreti

- **Variabili d'ambiente**: I segreti vengono passati come variabili d'ambiente
- **File .env**: Non versionato, creato localmente
- **Separazione delle configurazioni**: Esempio in .env.example, reali in .env

### Aggiornamenti e Patch

- **Dipendenze**: Mantieni aggiornate le dipendenze per mitigare vulnerabilità note
- **Sistema operativo container**: L'immagine base viene aggiornata all'avvio
- **Certificati**: Rinnova i certificati SSL prima della scadenza

### Monitoraggio

- **Log del container**: Monitora i log per attività sospette
- **Rate limiting**: Verifica se ci sono utenti che raggiungono frequentemente il limite di rate
- **Errori di servizio**: Controlla regolarmente gli errori di connessione ad API esterne

## 🔧 Hardening Aggiuntivo

### Livello di Container

- **Limiti di risorse**: CPU e memoria limitate per container
- **No-new-privileges**: Impedisce l'escalation di privilegi
- **Readonly filesystem**: Dove possibile, utilizza filesystem in sola lettura

### Livello di Rete

- **Firewall**: Considera l'implementazione di un firewall che limiti l'accesso solo alla porta 443
- **Rete privata**: Se possibile, posiziona il bot in una rete privata con accesso limitato
- **Reverse proxy**: Considera l'utilizzo di un reverse proxy come Nginx per filtrare richieste

### Livello di Sistema Operativo

- **Utente dedicato**: Esegui Docker con un utente dedicato non-root
- **SELinux/AppArmor**: Abilita security modules per limitare ulteriormente i privilegi
- **Aggiornamenti automatici**: Configura aggiornamenti automatici di sicurezza

## 🚨 Procedure di Risposta agli Incidenti

### Compromissione Sospetta

Se sospetti che il bot sia stato compromesso:

1. **Arresta immediatamente il container**: `docker-compose down`
2. **Revoca il token del bot Telegram**: Contatta @BotFather su Telegram
3. **Analizza i log**: Cerca attività sospette
4. **Reimposta le credenziali**: Genera nuovi token e chiavi API
5. **Ricostruisci l'ambiente**: Ricostruisci da zero l'ambiente di esecuzione

### Violazione di Dati

Poiché il bot non memorizza password o dati sensibili, il rischio di violazione è minimo. Tuttavia:

1. **Verifica l'estensione**: Determina quali dati potrebbero essere stati compromessi
2. **Notifica gli utenti**: Se necessario, informa gli utenti del bot
3. **Documenta l'incidente**: Mantieni un registro dell'incidente e delle azioni intraprese

## 📚 Riferimenti e Risorse Utili

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Telegram Bot API Security](https://core.telegram.org/bots/api#security)
- [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)