from datetime import datetime
import pandas as pd
from io import BytesIO
from email.mime.base import MIMEBase
from email import encoders

from config import logger
from excel_utils import carregar_planilha, salvar_logs_e_atualizacoes
from email_utils import (
    carregar_template_html,
    montar_email,
    enviar_email,
    registrar_log,
)
from email_utils import EMAIL_CC, EMAIL_BCC


def executar_cobranca_gestor(caminho_arquivo, template_path):
    df_colaboradores, df_gestores, df_log = carregar_planilha(caminho_arquivo)
    colaboradores_pendentes = df_colaboradores[
        df_colaboradores["CERTIFICADO"] == "PENDENTE"
    ]
    gestores = df_gestores.set_index("NOME")["E-MAIL"].to_dict()

    total = (
        df_colaboradores.groupby("GESTOR IMEDIATO")["NOME"]
        .count()
        .reset_index(name="qtd_total")
    )
    pendentes = (
        colaboradores_pendentes.groupby("GESTOR IMEDIATO")["NOME"]
        .count()
        .reset_index(name="qtd_pendentes")
    )
    analise = pd.merge(total, pendentes, on="GESTOR IMEDIATO", how="outer").fillna(0)
    analise["perc_conclusao"] = (
        (analise["qtd_total"] - analise["qtd_pendentes"]) / analise["qtd_total"]
    ) * 100

    cobrancas = (
        colaboradores_pendentes.groupby("GESTOR IMEDIATO")["QUANTIDADE DE COBRANÇAS"]
        .sum()
        .reset_index()
    )
    analise = pd.merge(analise, cobrancas, on="GESTOR IMEDIATO", how="left").fillna(0)
    analise["med_cobrancas"] = analise["QUANTIDADE DE COBRANÇAS"] / analise[
        "qtd_pendentes"
    ].replace(0, 1)
    analise.drop(columns=["QUANTIDADE DE COBRANÇAS"], inplace=True)

    try:
        historico = pd.read_excel(
            caminho_arquivo, sheet_name="Analise Quinzenal", engine="openpyxl"
        )
        analise = pd.merge(
            analise,
            historico[["GESTOR IMEDIATO", "perc_conclusao"]],
            on="GESTOR IMEDIATO",
            how="left",
            suffixes=("", "_antes"),
        ).fillna(0)
        analise.rename(
            columns={"perc_conclusao_antes": "perc_evolucao_antes"}, inplace=True
        )
        analise["perc_evolucao_atual"] = (
            analise["perc_conclusao"] - analise["perc_evolucao_antes"]
        )
    except Exception:
        analise["perc_evolucao_antes"] = 0
        analise["perc_evolucao_atual"] = 0

    html_template = carregar_template_html(template_path)

    for _, row in analise.iterrows():
        nome_gestor = row["GESTOR IMEDIATO"]
        email_gestor = gestores.get(nome_gestor)
        if not email_gestor or row["qtd_pendentes"] == 0:
            continue

        try:
            corpo = html_template
            corpo = corpo.replace("{gestor}", nome_gestor)
            corpo = corpo.replace("{qtd_pendentes}", str(int(row["qtd_pendentes"])))
            corpo = corpo.replace("{perc_conclusao}", f"{row['perc_conclusao']:.2f}%")
            corpo = corpo.replace("{med_cobrancas}", f"{row['med_cobrancas']:.2f}")
            corpo = corpo.replace(
                "{perc_evolucao_atual}", f"{row['perc_evolucao_atual']:.2f}%"
            )

            df_gestor = colaboradores_pendentes[
                colaboradores_pendentes["GESTOR IMEDIATO"] == nome_gestor
            ]
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df_gestor.to_excel(writer, index=False, sheet_name="Pendentes")
            buffer.seek(0)

            anexo_excel = MIMEBase(
                "application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            anexo_excel.set_payload(buffer.read())
            encoders.encode_base64(anexo_excel)
            anexo_excel.add_header(
                "Content-Disposition",
                "attachment",
                filename=f'Pendencias_XYZ_{nome_gestor.replace(" ", "_")}.xlsx',
            )

            msg = montar_email(
                destinatario=email_gestor,
                assunto="Treinamentos XYZ Ainda Não Concluídos",
                corpo_html=corpo,
                anexos=[anexo_excel],
            )

            enviar_email(msg)
            df_log = registrar_log(
                df_log, "Cobrança ao gestor", nome_gestor, "E-mail enviado com sucesso"
            )
            logger.info(f"E-mail enviado com sucesso para {nome_gestor}")

        except Exception as e:
            df_log = registrar_log(
                df_log, "Cobrança ao gestor", nome_gestor, f"Erro: {e}"
            )
            logger.error(f"Erro ao enviar e-mail para {nome_gestor}: {e}")

    salvar_logs_e_atualizacoes(
        caminho_arquivo, df_colaboradores, df_log, "Analise Quinzenal", analise
    )
