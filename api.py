import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- 1. Carregamento dos Dados ---
# Esta função será executada apenas uma vez, quando a API iniciar.
def load_data():
    try:
        with open('caminho.json', 'r', encoding='utf-8') as f:
            print("Carregando dados do arquivo caminho.json...")
            data = json.load(f)
            print("Dados carregados com sucesso!")
            return data
    except FileNotFoundError:
        print("ERRO: O arquivo caminho.json não foi encontrado.")
        return []

# Carrega os dados para a memória
pontos_data = load_data()

# --- Criação da Aplicação FastAPI ---
app = FastAPI(
    title="Caminho API",
    description="Uma API para acessar os 999 pontos de 'Caminho' de São Josemaria Escrivá.",
    version="1.0.0"
)

# --- Configuração do CORS ---
# Permite que qualquer origem (qualquer site ou app) acesse sua API.
# Ideal para uma API pública.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# --- Endpoint de "Saúde" (Health Check) ---
# Um endpoint simples para verificar se a API está no ar.
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Bem-vindo à Caminho API!",
        "total_pontos": len(pontos_data)
    }