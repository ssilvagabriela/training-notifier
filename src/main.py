from cobranca_colaborador import executar_cobranca_colaborador
from cobranca_gestor import executar_cobranca_gestor
from config import logger

if __name__ == "__main__":
    CAMINHO_PLANILHA = "data/exemplo_cobranca_automatizada.xlsx"
    TEMPLATE_COLABORADOR = "templates/cobranca_colaboradores.html"
    TEMPLATE_GESTOR = "templates/resumo_executivo.html"
    INSTRUCOES_PDF = "data/treinamento_XYZ_orientacoes.pdf"

    logger.info("_____Iniciando execução do processo de cobrança_____")

    executar_cobranca_colaborador(
        caminho_arquivo=CAMINHO_PLANILHA,
        template_path=TEMPLATE_COLABORADOR,
        pdf_path=INSTRUCOES_PDF,
    )
    logger.info("_____Cobrança de colaboradores finalizada_____")

    executar_cobranca_gestor(
        caminho_arquivo=CAMINHO_PLANILHA, template_path=TEMPLATE_GESTOR
    )
    logger.info("_____Cobrança de gestores finalizada_____")
