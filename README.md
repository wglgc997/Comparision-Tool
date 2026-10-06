# Offer Readiness QA Tool

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-FF4B4B?logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2%2B-150458?logo=pandas&logoColor=white)
![openpyxl](https://img.shields.io/badge/openpyxl-3.1.5-217346?logo=microsoftexcel&logoColor=white)
![Tests](https://img.shields.io/badge/tests-49%20passing-brightgreen)
![Status](https://img.shields.io/badge/status-MVP-blue)
![Repository](https://img.shields.io/badge/repository-private-lightgrey)

Ferramenta de QA construída com Streamlit para comparar dados de auditoria do
Offer Readiness com o conteúdo copiado de páginas de produtos Dell.

O projeto reduz a comparação manual de checkpoints, centraliza as evidências
encontradas e gera resultados exportáveis com os estados `PASS`, `FAIL` e
`REVIEW`.

## Objetivo

Auditores precisam conferir vários Offer IDs em diferentes mercados e validar
itens como Graphics, Display, Processor, Memory e Delivery. A ferramenta
permite:

- carregar uma planilha de auditoria em CSV ou XLSX;
- selecionar um Offer ID e o respectivo mercado;
- extrair os checkpoints e as regras esperadas;
- colar o conteúdo visível copiado da página Dell;
- avaliar automaticamente os checkpoints compatíveis;
- registrar a evidência usada em cada resultado;
- exportar o relatório da comparação para CSV.

## Tecnologias

| Tecnologia | Uso no projeto |
|---|---|
| Python 3.11+ | Linguagem principal |
| Streamlit | Interface web |
| pandas | Leitura, filtro e transformação dos dados |
| openpyxl | Leitura de arquivos XLSX |
| unittest | Testes automatizados |

## Estrutura

```text
Comparison Tool/
├── app.py                    # Interface Streamlit
├── comparison.py             # Comparação textual e resumos
├── pdp_parser.py              # Análise do conteúdo copiado da PDP
├── source_data.py             # Leitura e processamento de CSV/XLSX
├── rules.py                   # Catálogo de regras de validação
├── requirements.txt           # Dependências do projeto
├── data/
│   └── sample_audit.csv       # Arquivo seguro para demonstração
└── tests/
    ├── test_comparison.py
    ├── test_pdp_parser.py
    ├── test_rules.py
    ├── test_source_data.py
    └── test_upload_flow.py
```

## Requisitos

- Python 3.11 ou mais recente;
- Windows, macOS ou Linux;
- navegador moderno;
- ambiente virtual recomendado.

## Instalação

No PowerShell:

```powershell
git clone <URL_DO_REPOSITORIO_PRIVADO>
cd "Comparison Tool"

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No macOS ou Linux, substitua `.\.venv\Scripts\python.exe` por
`.venv/bin/python`.

## Execução

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

O Streamlit mostrará o endereço local, normalmente:

```text
http://localhost:8501
```

## Fluxo 1: comparação manual

Use este modo quando já possuir valores estruturados de Source e Live.

Informe um item por linha no formato `Checkpoint: Value`:

```text
Processor: Intel Core Ultra 7
Memory: 16GB DDR5
Storage: 512GB SSD
```

A comparação ignora diferenças entre letras maiúsculas e minúsculas, espaços
externos e espaços repetidos.

## Fluxo 2: auditoria com CSV/XLSX

### 1. Carregar a fonte

O arquivo precisa conter estas colunas:

| Coluna | Finalidade |
|---|---|
| `Offer ID` | Identificador da oferta |
| `Country` | Mercado da oferta |
| `Checkpoint` | Item auditado |
| `Expected Format / Rule` | Resultado ou regra esperada |

Os nomes são detectados sem considerar maiúsculas, espaços ou separadores
simples. CSVs em UTF-8 e `cp1252` são aceitos.

### 2. Selecionar a oferta

Escolha o Offer ID e o mercado nos campos apresentados pela interface. O app
mostrará as linhas filtradas e os checkpoints extraídos.

### 3. Copiar o conteúdo da PDP

Copie o conteúdo visível da página Dell e cole no campo
**Content copied from the live PDP**. Exemplo:

```text
Dell Pro 7 Series 14 Laptop
AMD Ryzen AI 5 PRO 435, 6 Cores
Windows 11 Pro
16 GB DDR5
512 GB SSD
14" Non Touch FHD (1920x1200)
Estimated delivery: October 20, 2026
```

### 4. Comparar e exportar

Clique em **Compare Uploaded Offer**. O resultado apresenta:

- regra esperada;
- evidência encontrada no conteúdo copiado;
- estado do checkpoint;
- totais de PASS, FAIL e REVIEW;
- score dos checkpoints avaliados;
- download do relatório em CSV compatível com Excel.

## Checkpoints interpretados automaticamente

O analisador atual reconhece:

- Graphics;
- Display option count;
- Delivery date;
- Delivery date threshold de até 30 dias;
- Processor;
- Operating System;
- Memory;
- Storage;
- Display.

Valores concretos também são comparados. Por exemplo, `16GB DDR5` na fonte e
`32GB DDR5` no conteúdo da PDP produzem `FAIL`.

## Estados do resultado

| Estado | Significado |
|---|---|
| `PASS` | O conteúdo atende à regra ou ao valor esperado |
| `FAIL` | O conteúdo está ausente, divergente ou fora do limite |
| `REVIEW` | O texto copiado não permite uma decisão automática segura |

Checkpoints relacionados a imagens, interação, dependências de configuração,
cálculos de preço ou layout normalmente exigem `REVIEW` manual.

## Regras de validação

O catálogo contém 65 IDs, pois o ID 51 não existe na fonte utilizada. Desses,
57 possuem definição completa. As regras sem definição permanecem visíveis
como referência e não são aplicadas automaticamente.

## Testes

Execute a suíte completa:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Validações cobertas:

- normalização e comparação de especificações;
- parsing de texto;
- resumo dos resultados;
- catálogo e filtros de regras;
- leitura de CSV e XLSX;
- fallback de encoding;
- detecção das colunas obrigatórias;
- filtros por Offer ID e mercado;
- extração dos checkpoints;
- análise do conteúdo copiado da PDP;
- datas e limite de entrega;
- fluxo integrado de upload e comparação.

## Arquivo de demonstração

Use `data/sample_audit.csv` para validar o fluxo sem expor dados reais. O
arquivo contém quatro checkpoints fictícios para o mercado `hkg_market_ZH`.

## Limitações do MVP

- não acessa nem faz scraping das páginas Dell;
- depende do conteúdo copiado pelo auditor;
- não interpreta imagens ou elementos puramente visuais;
- não executa interações na página;
- checkpoints não suportados são enviados para revisão manual;
- regras sem definição não são inferidas.

## Dados e segurança

Este repositório deve permanecer privado. Antes de fazer qualquer commit:

- não adicione planilhas reais de auditoria;
- não versione dados pessoais de auditores;
- não inclua URLs internas, tokens, cookies ou credenciais;
- use apenas dados anonimizados em exemplos e testes;
- revise `git status` antes de enviar alterações ao GitHub.

Arquivos reais podem ser utilizados localmente pelo uploader sem serem
copiados para o repositório.

## Solução de problemas

### O Offer ID não aparece

Confirme que a coluna `Offer ID` existe e que o valor não está vazio.

### O mercado não aparece

Confirme que a coluna `Country` está preenchida para o Offer ID selecionado.

### Nenhum checkpoint foi extraído

Verifique as colunas `Checkpoint` e `Expected Format / Rule`. Linhas
incompletas são ignoradas.

### O resultado ficou como REVIEW

O checkpoint não pode ser determinado com segurança pelo texto copiado.
Realize a revisão manual usando a regra e a evidência exibidas.

### A aplicação não inicia

Reinstale as dependências e confirme a versão do Python:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Escopo futuro

- ampliar os validadores automáticos por checkpoint;
- melhorar a interpretação de formatos regionais de data;
- adicionar histórico local de auditorias;
- reduzir duplicação visual entre os dois modos de comparação;
- adicionar testes de interface para uploads reais no Streamlit.

## Uso interno

Projeto destinado ao uso interno de QA. Distribuição, publicação ou mudança
de visibilidade do repositório deve seguir as políticas internas aplicáveis.
