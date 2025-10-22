import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# --- CONFIGURAÇÃO DO SELENIUM ---
chromedriver_path = './chromedriver-linux64/chromedriver'
service = Service(executable_path=chromedriver_path)
brave_path = "/usr/bin/brave-browser"
options = Options()
options.binary_location = brave_path
# Descomente a linha abaixo para rodar sem abrir a janela do navegador
# options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)
todos_os_pontos = []
URL_BASE = "https://escriva.org/pt-br/camino/"

# --- RASPAGEM ---
try:
    for numero_ponto in range(1, 1000):
        url_completa = f"{URL_BASE}{numero_ponto}/"
        print(f"Raspando ponto {numero_ponto} de 999...")

        try:
            driver.get(url_completa)
            # Pausa para ir para a próxima página
            time.sleep(0.5) 
            
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            texto_div = soup.find('div', class_='imperavi-body')

            if texto_div:
                # Pega o texto apenas das tags <p> dentro da div
                paragrafos = texto_div.find_all('p')
                # Junta o texto de cada parágrafo com uma linha em branco entre eles
                ponto_texto = '\n\n'.join([p.get_text().strip() for p in paragrafos])
                
                ponto_data = {
                    "numero": numero_ponto,
                    "texto": ponto_texto
                }
                todos_os_pontos.append(ponto_data)
            else:
                print(f"AVISO: Não foi possível encontrar o texto para o ponto {numero_ponto}.")

        except Exception as e:
            # Este 'except' trata erros de um único ponto sem parar o script inteiro
            print(f"ERRO ao processar o ponto {numero_ponto}: {e}")
            continue # Continua para o próximo ponto do loop

finally:
    # O driver.quit() agora é chamado apenas uma vez, no final de tudo.
    print("Raspagem concluída. Fechando o navegador...")
    driver.quit()

# --- SALVANDO---
try:
    with open('caminho.json', 'w', encoding='utf-8') as f:
        json.dump(todos_os_pontos, f, indent=2, ensure_ascii=False)
    
    print(f"\nSUCESSO! {len(todos_os_pontos)} pontos foram salvos no arquivo 'caminho.json'.")

except Exception as e:
    print(f"\nERRO ao salvar o arquivo JSON: {e}")