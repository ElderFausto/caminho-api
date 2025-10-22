# Caminho - São Josemaria Escrivá

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma API RESTful pública, construída com **Python** e **FastAPI**, que serve os 999 pontos do livro "Caminho" de São Josemaria Escrivá. A aplicação foi projetada com uma arquitetura de duas etapas para garantir alta performance e eficiência, separando a coleta de dados da entrega.

## 🏛️ Arquitetura: Scraper + API

Este projeto foi intencionalmente dividido em duas partes para seguir as melhores práticas de desenvolvimento e web scraping:

1.  **`scraper.py` (O Coletor):** Um script de raspagem de dados que utiliza **Selenium** para navegar pelo site [escriva.org](https://escriva.org/pt-br/camino/) e extrair todos os 999 pontos. Ele é executado **uma única vez** para gerar um "banco de dados" local em formato JSON (`caminho.json`). Essa abordagem é respeitosa com o servidor do site de origem, evitando sobrecarga.

2.  **`api.py` (O Servidor):** Uma API **FastAPI** extremamente rápida que, ao ser iniciada, carrega o arquivo `caminho.json` para a memória. Todas as requisições subsequentes são atendidas diretamente da memória, resultando em tempos de resposta quase instantâneos, sem a necessidade de acessar a internet ou um banco de dados a cada chamada.

## 🚀 Funcionalidades e Endpoints

A API oferece três maneiras de interagir com os dados:

### 1. Obter um Ponto Específico
Retorna um ponto pelo seu número.

-   **Endpoint:** `GET /pontos/{numero_ponto}`
-   **Exemplo:** [http://localhost:8000/pontos/27](http://localhost:8000/pontos/27)

### 2. Obter um Ponto Aleatório
Ideal para "pensamento do dia" ou inspiração diária.

-   **Endpoint:** `GET /ponto-aleatorio`
-   **Exemplo:** [http://localhost:8000/ponto-aleatorio](http://localhost:8000/ponto-aleatorio)

### 3. Buscar por um Termo
Retorna uma lista de todos os pontos que contêm a palavra pesquisada (não diferencia maiúsculas de minúsculas).

-   **Endpoint:** `GET /buscar`
-   **Parâmetro:** `termo`
-   **Exemplo:** [http://localhost:8000/buscar?termo=alma](http://localhost:8000/buscar?termo=alma)

### Documentação Interativa
Graças ao FastAPI, a API é 100% autodocumentada. Acesse a interface do Swagger UI para explorar e testar todos os endpoints:
-   **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠️ Tecnologias Utilizadas

-   **Python 3.10+**
-   **Web Scraping:**
    -   **Selenium:** Para automação de navegador e extração de conteúdo de páginas com JavaScript.
    -   **BeautifulSoup4:** Para parsing do HTML.
-   **API:**
    -   **FastAPI:** Framework web moderno e de alta performance.
    -   **Uvicorn:** Servidor ASGI para rodar a aplicação.
-   **Gerenciamento:**
    -   **venv:** Para isolamento de ambiente.
    -   **pip:** Para gerenciamento de pacotes.

## ⚙️ Como Executar o Projeto Localmente

### 1. Pré-requisitos
-   Python 3.10 ou superior.
-   Um navegador compatível com Selenium (este projeto foi configurado com **Brave/Chrome**).
-   O `chromedriver` correspondente à versão do seu navegador.

### 2. Configuração do Ambiente
```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/caminho-api.git](https://github.com/seu-usuario/caminho-api.git)
cd caminho-api

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Coleta de Dados (Executar apenas uma vez)
Este passo irá gerar o arquivo `caminho.json`. Ele pode demorar cerca de 10-15 minutos.
```bash
# Certifique-se de que o 'chromedriver' está na pasta raiz do projeto
# e que ele tem permissão de execução (chmod +x chromedriver)
python3 scraper.py
```

### 4. Iniciar a API
Com o arquivo `caminho.json` gerado, inicie o servidor da API.
```bash
python3 -m uvicorn api:app --reload
```
✅ A API estará disponível em `http://localhost:8000`.
