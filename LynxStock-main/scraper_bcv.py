# scraper_bcv.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3

# Deshabilitar advertencias de SSL inseguro (solo para este caso específico)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtener_tasa_bcv():
    url = "https://www.bcv.org.ve/"
    try:
        # 1. Pedir la página ignorando la verificación SSL
        respuesta = requests.get(url, timeout=10, verify=False)
        respuesta.raise_for_status()

        # 2. Analizar el HTML
        sopa = BeautifulSoup(respuesta.text, 'html.parser')

        # 3. Buscar la sección del dólar oficial
        div_dolar = sopa.find('div', id='dolar')
        if not div_dolar:
            raise ValueError("No se encontró el contenedor del dólar en la página.")

        valor_tag = div_dolar.find('strong')
        if not valor_tag:
            raise ValueError("No se encontró el valor de la tasa en el HTML.")

        # 4. Convertir el texto a número float
        tasa_texto = valor_tag.text.strip()
        tasa_texto = tasa_texto.replace('.', '')      # quitar puntos de miles
        tasa_texto = tasa_texto.replace(',', '.')      # coma decimal a punto
        tasa = float(tasa_texto)

        print(f"[{datetime.now()}] Tasa BCV obtenida: {tasa} Bs/USD")
        return tasa

    except Exception as e:
        print(f"Error al obtener tasa BCV: {e}")
        return None