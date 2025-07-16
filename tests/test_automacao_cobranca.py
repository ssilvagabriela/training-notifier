import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
from automacao_cobranca import (
    carregar_variaveis_ambiente,
    carregar_planilha,
    enviar_email,
    executar_cobranca_colaborador,
    executar_cobranca_gestor,
)

# =======================
# TESTES BÁSICOS
# =======================


@patch("automacao_cobranca.load_dotenv")
@patch("automacao_cobranca.os.getenv")
def test_carregar_variaveis_ambiente(mock_getenv, mock_dotenv):
    mock_getenv.side_effect = lambda k: {"SMTP_SERVER": "smtp.test.com", "PORT": "587"}[
        k
    ]
    smtp, port = carregar_variaveis_ambiente()
    assert smtp == "smtp.test.com"
    assert port == "587"


@patch("automacao_cobranca.pd.read_excel")
def test_carregar_planilha(mock_read_excel):
    mock_read_excel.return_value = {
        "Zero Outage": pd.DataFrame({"NOME": ["Alice"], "CERTIFICADO": ["PENDENTE"]}),
        "Gestores": pd.DataFrame(
            {"NOME": ["Gestor A"], "E-MAIL": ["gestor@example.com"]}
        ),
        "Logs": pd.DataFrame(columns=["TIPO DE ENVIO", "NOME", "DATA", "LOG"]),
    }
    colaboradores, gestores, logs = carregar_planilha("dummy.xlsx")
    assert not colaboradores.empty
    assert not gestores.empty
    assert logs.empty


# =======================
# TESTE DE ENVIO DE E-MAIL
# =======================


@patch("automacao_cobranca.smtplib.SMTP")
def test_enviar_email(mock_smtp):
    msg = MagicMock()
    smtp_instance = mock_smtp.return_value.__enter__.return_value
    enviar_email(msg)
    smtp_instance.starttls.assert_called_once()
    smtp_instance.send_message.assert_called_once_with(msg)


# =======================
# TESTE DE COBRANÇA COLABORADOR
# =======================


@patch("automacao_cobranca.salvar_logs_e_atualizacoes")
@patch("automacao_cobranca.enviar_email")
@patch(
    "automacao_cobranca.open",
    new_callable=mock_open,
    read_data="<p>Olá {colaborador}</p>",
)
@patch("automacao_cobranca.carregar_planilha")
def test_executar_cobranca_colaborador(
    mock_planilha, mock_openfile, mock_envio, mock_salvar
):
    df_colab = pd.DataFrame(
        {
            "NOME": ["Fulano"],
            "E-MAIL": ["fulano@example.com"],
            "CERTIFICADO": ["PENDENTE"],
            "ÚLTIMA COBRANÇA FEITA EM": [""],
            "QUANTIDADE DE COBRANÇAS": [0],
            "GESTOR IMEDIATO": ["Gestor A"],
        }
    )
    df_gestores = pd.DataFrame({"NOME": ["Gestor A"], "E-MAIL": ["gestor@example.com"]})
    df_log = pd.DataFrame(columns=["TIPO DE ENVIO", "NOME", "DATA", "LOG"])
    mock_planilha.return_value = (df_colab, df_gestores, df_log)

    executar_cobranca_colaborador("dummy.xlsx", "template.html", "anexo.pdf")

    assert mock_envio.called
    assert mock_salvar.called


# =======================
# TESTE DE COBRANÇA GESTOR
# =======================


@patch("automacao_cobranca.salvar_logs_e_atualizacoes")
@patch("automacao_cobranca.enviar_email")
@patch("automacao_cobranca.open", new_callable=mock_open, read_data="<p>{gestor}</p>")
@patch("automacao_cobranca.carregar_planilha")
@patch("automacao_cobranca.pd.read_excel")
def test_executar_cobranca_gestor(
    mock_historico, mock_planilha, mock_openfile, mock_envio, mock_salvar
):
    df_colab = pd.DataFrame(
        {
            "NOME": ["Fulano"],
            "E-MAIL": ["fulano@example.com"],
            "CERTIFICADO": ["PENDENTE"],
            "QUANTIDADE DE COBRANÇAS": [2],
            "GESTOR IMEDIATO": ["Gestor A"],
        }
    )
    df_gestores = pd.DataFrame({"NOME": ["Gestor A"], "E-MAIL": ["gestor@example.com"]})
    df_log = pd.DataFrame(columns=["TIPO DE ENVIO", "NOME", "DATA", "LOG"])
    df_historico = pd.DataFrame(
        {"GESTOR IMEDIATO": ["Gestor A"], "perc_conclusao": [50.0]}
    )

    mock_planilha.return_value = (df_colab, df_gestores, df_log)
    mock_historico.return_value = df_historico

    executar_cobranca_gestor("dummy.xlsx", "template.html")

    assert mock_envio.called
    assert mock_salvar.called
