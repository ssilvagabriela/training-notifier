import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime
from pathlib import Path

from config import SMTP_SERVER, PORT
from config import EMAIL_REMETENTE, EMAIL_CC, EMAIL_BCC


def carregar_template_html(caminho):
    with open(caminho, "r", encoding="utf-8") as file:
        return file.read()


def montar_email(destinatario, assunto, corpo_html, anexos=None, cc=None, bcc=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg["Cc"] = ", ".join(cc if cc is not None else EMAIL_CC)
    msg["Bcc"] = bcc if bcc is not None else EMAIL_BCC
    msg.attach(MIMEText(corpo_html, "html"))
    for anexo in anexos or []:
        msg.attach(anexo)
    return msg


def enviar_email(mensagem):
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls()
        server.send_message(mensagem)


def registrar_log(df_log, tipo, nome, log):
    return pd.concat(
        [
            df_log,
            pd.DataFrame(
                [
                    {
                        "TIPO DE ENVIO": tipo,
                        "NOME": nome,
                        "DATA": datetime.now().strftime("%d/%m/%Y"),
                        "LOG": log,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
