# Password Audit Bot for Telegram [![Chat with Bot](https://img.shields.io/badge/Telegram-Chat%20with%20Bot-blue?logo=telegram)](https://t.me/passwordaudit_bot)

A Telegram bot to verify password security in a safe and privacy-respecting manner, implementing best practices of security by design and privacy by design.

## 🔒 Features

- **Password verification** via Have I Been Pwned database using k-Anonymity
- **Rate limiting** to protect against brute force and DoS attacks
- **Input sanitization** to prevent injection and other attacks
- **Secure logging** without storing sensitive data
- **Secure deployment** with HTTPS via webhook
- **Modular architecture** for easy maintenance and updates
- **Containerized execution** with Docker and Docker Compose


## 📖 Project Structure

```
telegram_bot/
├── bot/                    # Command handlers and middleware
│   ├── __init__.py
│   ├── handlers.py         # Bot command handlers
│   └── middleware.py       # Middleware for rate limiting and security
├── security/               # Security modules
│   ├── __init__.py
│   ├── password_analyzer.py # Password security analysis
│   └── hibp_client.py      # Have I Been Pwned API client
├── utils/                  # Utilities
│   ├── __init__.py
│   └── logging.py          # Secure logger
├── certs/                  # SSL/TLS certificates
├── config.py               # Centralized configuration
├── main.py                 # Main entry point
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not versioned)
└── .env.example            # Environment variables example
```

## 📝 Bot Commands

- `/start` - Start the bot and show the welcome message
- `/check` - Verify a password's security
- `/tips` - Show tips for creating secure passwords
- `/help` - Show all available commands
- `/cancel` - Cancel the current operation


## ⚙️ Security and Privacy Best Practices

### Security by Design

- **Principle of least privilege**: Execution with non-privileged user
- **Defense in depth**: Multiple security measures implemented
- **Fail secure**: In case of error, does not reveal sensitive information
- **Input validation**: All inputs are validated and sanitized
- **DoS protection**: Rate limiting to prevent denial of service attacks
- **HTTPS mandatory**: Communications occur only through secure channels
- **Secure configuration**: No sensitive values hardcoded in the code


### Privacy by Design

- **Data minimization**: Only essential data is processed
- **No persistence**: Passwords are never saved
- **k-Anonymity**: Verification with HIBP occurs without revealing the complete password
- **Transparency**: Clear communication to the user about how data is handled
- **User control**: The user can cancel the process at any time
- **Log privacy**: Logs do not contain sensitive or identifying data
