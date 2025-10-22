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
# Permite que qualquer origem (qualquer site ou app) a API.
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
    
# --- uscar um Ponto Específico ---
@app.get("/pontos/{numero_ponto}")
def get_ponto_por_numero(numero_ponto: int):
    """Retorna um ponto específico de 1 a 999"""
    if not 1 <= numero_ponto <= 999:
        raise HTTPException(status_code=400, detail="Número do ponto inválido. Por favor, use um número entre 1 and 999.")
    
    # O arquivo JSON é uma lista, e listas começam no índice 0.
    # Portanto, o ponto 1 está no índice 0.
    ponto = pontos_data[numero_ponto - 1]
    
    if ponto:
        return ponto
    else:
        # Este caso é improvável se o JSON estiver correto, mas é uma boa prática.
        raise HTTPException(status_code=404, detail="Ponto não encontrado.")
      
# --- Buscar um Ponto Aleatório ---
@app.get("/ponto-aleatorio")
def get_ponto_aleatorio():
    """Retorna um ponto aleatório da lista."""
    if not pontos_data:
        raise HTTPException(status_code=500, detail="Não há dados de pontos disponíveis.")
    
    return random.choice(pontos_data)

# --- Buscar por Tema ---
@app.get("/buscar")
def buscar_pontos_por_termo(termo: str):
    """Busca por pontos que contenham o tema pesquisado no texto."""
    if not termo or len(termo) < 3:
        raise HTTPException(status_code=400, detail="O termo de busca deve ter pelo menos 3 caracteres.")

    # A busca é case-insensitive (não diferencia maiúsculas de minúsculas)
    termo_lower = termo.lower()
    
    resultados = [
        ponto for ponto in pontos_data 
        if termo_lower in ponto['texto'].lower()
    ]
    
    return {
        "termo_buscado": termo,
        "total_encontrado": len(resultados),
        "resultados": resultados
    }