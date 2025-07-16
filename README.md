# 📧 Automação de Cobrança XYZ

Este projeto automatiza o envio de e-mails de cobrança relacionados ao programa de treinamento **XYZ**, garantindo que colaboradores e gestores sejam lembrados de suas pendências de forma eficiente, organizada e rastreável.

> 🔧 Ideal para equipes técnicas que buscam engajamento em treinamentos obrigatórios via e-mail e acompanhamento por planilhas.

---

## 🚀 Funcionalidades

* Envio semanal de e-mails para colaboradores pendentes.
* Envio quinzenal de resumo executivo para gestores.
* Análise automática de progresso e evolução.
* Atualização dinâmica da planilha Excel com logs e métricas.
* Testes automatizados com `pytest`.

---

## 🧰 Tecnologias utilizadas

* Python 3.10+
* Pandas, OpenPyXL
* SMTP (via `smtplib`)
* Dotenv
* Pytest + Mock

---

## 📦 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/ssilvagabriela/training-notifier.git
cd training-notifier
```

### 2. Crie e ative um ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie o arquivo `src/utils/.env` com:

```env
SMTP_SERVER=smtp.seuprovedor.com
PORT=587
EMAIL_REMETENTE=seu_email_remetente@empresa.com
EMAIL_CC=cc1@empresa.com,cc2@empresa.com
EMAIL_BCC=oculto@empresa.com
```

---

## 🔧 Personalização obrigatória antes do uso

Este projeto utiliza um arquivo `.env` para armazenar e-mails sensíveis e configurações SMTP.

Antes de executar o sistema:

1. **Substitua os e-mails genéricos por endereços reais da sua organização** no arquivo `.env`.

2. **Verifique a consistência dos e-mails na planilha** (colaboradores e gestores) — e-mails ausentes ou inválidos impedirão o envio.

3. **Ajuste o formato das datas**, se necessário:

   * Por padrão, o sistema aceita datas no formato `YYYY-MM-DD`.
   * Se você usa `DD/MM/YYYY`, edite `cobranca_colaborador.py` e adicione `dayfirst=True` ao `pd.to_datetime(...)`.

---

## 📌 Observações

* O sistema aborta o envio caso e-mails obrigatórios estejam ausentes.
* Todas as mensagens de envio são registradas em `logs/cobranca.log` e no terminal.

---

### 5. Execute o script manualmente

```bash
python src/main.py
```

Ou agende via `cron` / `Task Scheduler`.

---

## 🥪 Rodar os testes

```bash
pytest tests/
```

Os testes cobrem as funções principais com mocks para ambiente, planilhas e e-mails.

---

## 📁 Estrutura

```
├── src/
│   ├── cobranca_colaborador.py
│   ├── cobranca_gestor.py
│   ├── email_utils.py
│   ├── excel_utils.py
│   ├── config.py
│   └── main.py
├── tests/
│   └── test_automacao_cobranca.py
├── templates/
│   ├── cobranca_colaboradores.html
│   └── resumo_executivo.html
├── data/
│   └── exemplo_cobranca_automatizada.xlsx
├── docs/
│   └── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md  ← este arquivo
```

---

## 🧑‍💼 Autor

**Gabriela Sena**
📧 [gabisena@outlook.com](mailto:gabisena@outlook.com)
🔗 [linkedin.com/in/gabrielasena](https://linkedin.com/in/gabrielasena)

---

## 📍 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
