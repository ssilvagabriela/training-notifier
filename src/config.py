import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# .env
dotenv_path = Path(__file__).resolve().parent / "utils" / ".env"
load_dotenv(dotenv_path=dotenv_path)

SMTP_SERVER = os.getenv("SMTP_SERVER")
PORT = os.getenv("PORT")

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_CC = os.getenv("EMAIL_CC", "").split(",")
EMAIL_BCC = os.getenv("EMAIL_BCC")

# Configuração de logging (arquivo + console)
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "cobranca.log"

logger = logging.getLogger("cobranca")
logger.setLevel(logging.INFO)

# Log no arquivo
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Log no terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)
