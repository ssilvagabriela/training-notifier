from datetime import datetime
import pandas as pd
from email.mime.application import MIMEApplication

from config import logger
from excel_utils import carregar_planilha, salvar_logs_e_atualizacoes
from email_utils import (
    carregar_template_html,
    montar_email,
    enviar_email,
    registrar_log,
)


def executar_cobranca_colaborador(caminho_arquivo, template_path, pdf_path):
    df_colaboradores, df_gestores, df_log = carregar_planilha(caminho_arquivo)

    df_colaboradores["ÚLTIMA COBRANÇA FEITA EM"] = pd.to_datetime(
        df_colaboradores["ÚLTIMA COBRANÇA FEITA EM"], errors="coerce", format="%Y-%m-%d"
    )
    df_colaboradores["ÚLTIMA COBRANÇA FEITA EM"] = df_colaboradores[
        "ÚLTIMA COBRANÇA FEITA EM"
    ].astype(str)
    df_colaboradores["QUANTIDADE DE COBRANÇAS"] = (
        df_colaboradores["QUANTIDADE DE COBRANÇAS"].fillna(0).astype(int)
    )

    colaboradores_pendentes = df_colaboradores[
        df_colaboradores["CERTIFICADO"] == "PENDENTE"
    ]
    gestores = df_gestores.set_index("NOME")["E-MAIL"].to_dict()
    html_template = carregar_template_html(template_path)

    for _, row in colaboradores_pendentes.iterrows():
        nome = row["NOME"]
        email_colaborador = row["E-MAIL"]
        email_gestor = gestores.get(row["GESTOR IMEDIATO"])

        try:
            if not email_colaborador or not email_gestor:
                raise ValueError("E-mail do colaborador ou gestor ausente.")

            corpo = html_template.replace("{colaborador}", nome)
            with open(pdf_path, "rb") as file:
                pdf = MIMEApplication(file.read(), _subtype="pdf")
                pdf.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename="ZO_V2_Instruções.pdf",
                )

            msg = montar_email(
                destinatario=email_colaborador,
                assunto="[Ação Necessária] Seu Treinamento XYZ Ainda Não Foi Concluído",
                corpo_html=corpo,
                anexos=[pdf],
                cc=[email_gestor],  # adiciona ao CC principal
            )

            enviar_email(msg)
            df_colaboradores.loc[
                df_colaboradores["NOME"] == nome, "ÚLTIMA COBRANÇA FEITA EM"
            ] = datetime.now().strftime("%d/%m/%Y")
            df_colaboradores.loc[
                df_colaboradores["NOME"] == nome, "QUANTIDADE DE COBRANÇAS"
            ] += 1
            df_log = registrar_log(
                df_log, "Cobrança ao colaborador", nome, "E-mail enviado com sucesso"
            )
            logger.info(f"E-mail enviado com sucesso para {nome}")

        except Exception as e:
            df_log = registrar_log(
                df_log, "Cobrança ao colaborador", nome, f"Erro: {e}"
            )
            logger.error(f"Erro ao enviar e-mail para {nome}: {e}")

    salvar_logs_e_atualizacoes(caminho_arquivo, df_colaboradores, df_log)
