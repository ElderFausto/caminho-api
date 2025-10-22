import time
from selenium import webdriver
# 1. Importa as ferramentas para o Chrome/Brave
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# A URL do ponto do caminho que queremos raspar
URL = "https://escriva.org/pt-br/camino/1/"

# --- CONFIGURAÇÃO DO SELENIUM PARA O BRAVE ---
# Caminho para o chromedriver
chromedriver_path = './chromedriver-linux64/chromedriver'
service = Service(executable_path=chromedriver_path)

# Caminho para o executável do Brave
brave_path = "/usr/bin/brave-browser"
options = Options()
options.binary_location = brave_path

# Opções para rodar em modo "headless" (sem abrir a janela gráfica)
# Descomente a linha abaixo para que o navegador não apareça na tela
# options.add_argument('--headless')

# Inicia o driver do Brave com as opções configuradas
driver = webdriver.Chrome(service=service, options=options)

print(f"Buscando dados de: {URL}")

try:
    # 2. O resto do código é EXATAMENTE O MESMO!
    driver.get(URL)
    time.sleep(3) 
    page_html = driver.page_source
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    texto_div = soup.find('div', class_='imperavi-body')

    if texto_div:
        ponto_texto = texto_div.get_text(separator='\n\n').strip()
        
        print("\n--- Ponto Encontrado ---")
        print(f"Ponto 1: {ponto_texto}")
        print("-----------------------\n")
    else:
        print("ERRO: A div com a classe 'imperavi-body' não foi encontrada na página.")

finally:
    print("Fechando o navegador...")
    driver.quit()