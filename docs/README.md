# Documentação Técnica - Automação de Cobrança Treinamento

Este projeto automatiza o envio de e-mails de cobrança semanal e quinzenal relacionados ao programa de treinamento XYZ, com base em uma planilha Excel como fonte de dados. A automação é ideal para equipes que desejam garantir o engajamento e conclusão do treinamento por parte de seus colaboradores.

---

## 📌 Funcionalidades

* Envio semanal de e-mails de cobrança para colaboradores com treinamento pendente.
* Envio quinzenal de relatório executivo para gestores com resumo do status de sua equipe.
* Geração de log de envios com data, tipo e resultado.
* Atualização automática da planilha base com nova data de cobrança e número de tentativas.
* Templates de e-mail HTML personalizados.

---

## 🧱 Estrutura do Projeto

```
zero-outage-cobranca/
├── src/
│   ├── automacao_cobranca.py         # Código principal da automação
│   └── utils/
│       └── .env                      # Variáveis de ambiente (NÃO subir no Git)
│
├── templates/
│   ├── cobranca_colaboradores.html  # Template do e-mail para colaborador
│   └── resumo_executivo.html        # Template do e-mail para gestor
│
├── data/
│   └── exemplo_cobranca_automatizada.xlsx  # Planilha fictícia de exemplo
│
├── tests/
│   └── test_automacao_cobranca.py   # Testes automatizados com pytest
│
├── docs/
│   └── README.md                    # Este arquivo
├── README.md                        # Instruções para o GitHub
├── requirements.txt                 # Dependências Python
├── .gitignore                       # Arquivos a ignorar no Git
├── LICENSE                          # Licença (MIT)
```

---

## ⚙️ Configuração e Execução

### 1. Instalar dependências:

```bash
pip install -r requirements.txt
```

### 2. Criar arquivo `.env` em `src/utils/`:

```
SMTP_SERVER=smtp.seuprovedor.com
PORT=587
```

### 3. Executar o script principal:

```bash
python src/automacao_cobranca.py
```

*Para agendamento automático, utilize `cron`, `Task Scheduler` ou outro orquestrador.*

---

## 🧪 Testes Automatizados

```bash
pytest tests/
```

Os testes cobrem carregamento de dados, variáveis de ambiente e comportamento simulado de envio de e-mails com `unittest.mock`.

---

## 🛡️ Boas Práticas e Segurança

* O arquivo `.env` nunca deve ser versionado.
* Dados reais de colaboradores não devem ser incluídos em repositórios públicos.
* Logs e anexos devem seguir diretrizes de privacidade da organização.

---

## 📄 Licença

Distribuído sob a Licença MIT. Consulte o arquivo `LICENSE` para mais informações.

---

## 👩‍💻 Autor

Gabriela Sena
Email: [gabisena@outlook.com](mailto:gabisena@outlook.com)
LinkedIn: [linkedin.com/in/gabrielasena](https://linkedin.com/in/gabrielasena)
