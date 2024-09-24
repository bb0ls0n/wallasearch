import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlparse, parse_qs
import argparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import os

# Función para extraer el valor de "keywords" de la URL y reemplazar espacios por "_"
def extraer_keywords(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    keywords = query_params.get('keywords', [''])[0]  # Obtén el valor de 'keywords'
    return keywords.replace(' ', '_')  # Reemplaza los espacios por "_"

# Función para enviar un correo electrónico
def enviar_correo(nuevos_items, email_origen, email_destino, keywords):
    servidor = "smtp.gmail.com"
    puerto = 587
    correo_origen = email_origen
    contraseña = "xxxxxxxxxxxxxxxxxxxxx"

    if not email_destino:
        email_destino = correo_origen

    mensaje = MIMEMultipart()
    mensaje['From'] = correo_origen
    mensaje['To'] = email_destino
    mensaje['Subject'] = f"Nuevos ítems para '{keywords}' en Wallapop"

    cuerpo = "Se han encontrado los siguientes nuevos ítems:\n\n"
    for item in nuevos_items:
        cuerpo += f"{item['title']} - {item['price']} - {item['link']}\n"

    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        server = smtplib.SMTP(servidor, puerto)
        server.starttls()
        server.login(correo_origen, contraseña)
        texto = mensaje.as_string()
        server.sendmail(correo_origen, email_destino, texto)
        server.quit()
        print(f"Correo enviado correctamente a {email_destino}.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Configuración del argumento para la URL y CSV
parser = argparse.ArgumentParser(description="Wallapop scraper")
parser.add_argument('--url', type=str, required=True, help="URL de la búsqueda en Wallapop")
parser.add_argument('--email', type=str, required=False, help="Dirección de correo electrónico para enviar notificaciones (opcional)")
parser.add_argument('--csv', type=str, required=False, help="Nombre del archivo CSV para guardar y comparar los ítems (opcional)")
args = parser.parse_args()

# Extraer el valor de "keywords" de la URL
keywords = extraer_keywords(args.url)

# Nombre del archivo CSV (por defecto, basado en el keyword)
csv_filename = args.csv if args.csv else f"items_{keywords}.csv"

# Dirección de origen (tu correo de Gmail)
email_origen = "xxxxxxxxxxxxx@gmail.com"

# Dirección de destino (opcional)
email_destino = args.email

# Configurar las opciones de Chrome en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Configura el webdriver en modo headless
driver = webdriver.Chrome(options=chrome_options)

# Abrir la página
driver.get(args.url)

# Esperar para aceptar cookies
time.sleep(3)
try:
    accept_cookies_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    accept_cookies_button.click()
    print("Cookies aceptadas.")
except Exception as e:
    print(f"Error al aceptar las cookies: {e}")

# Scroll hasta cargar todos los ítems
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Esperar para que los ítems carguen completamente
time.sleep(5)

try:
    items = driver.find_elements(By.CLASS_NAME, 'ItemCardList__item')
    if items:
        print(f"Se encontraron {len(items)} ítems.")
        item_list = []
        count = 0
        for item in items:
            if count >= 10:
                break
            try:
                is_reserved = False
                reserved_badge = item.find_elements(By.CLASS_NAME, 'ItemCard__badge')
                for badge in reserved_badge:
                    if "Reservado" in badge.text:
                        is_reserved = True
                        break

                if not is_reserved:
                    title_element = item.find_elements(By.CLASS_NAME, 'ItemCard__title')
                    price_element = item.find_elements(By.CLASS_NAME, 'ItemCard__price')
                    link_element = item.get_attribute("href")
                    if title_element and price_element and link_element:
                        title = title_element[0].text.strip()
                        price = price_element[0].text.strip()
                        link = link_element
                        item_list.append({'title': title, 'price': price, 'link': link})
                        count += 1
                    else:
                        print("Faltan datos de título, precio o enlace, ítem omitido.")
            except Exception as e:
                print(f"Error al extraer datos de un ítem: {e}")

        previous_items = []
        if os.path.exists(csv_filename):
            previous_items = pd.read_csv(csv_filename).to_dict('records')

        df = pd.DataFrame(item_list)
        df.to_csv(csv_filename, index=False)
        print(f"CSV '{csv_filename}' creado con éxito. Se guardaron {count} ítems no reservados.")

        if previous_items:
            nuevos_items = [item for item in item_list if item not in previous_items]
            if nuevos_items:
                print("Hay nuevos ítems.")
                enviar_correo(nuevos_items, email_origen, email_destino, keywords)
            else:
                print("No hay nuevos ítems.")
        else:
            print("Es la primera vez que se ejecuta el script, no hay lista anterior.")
    else:
        print("No se encontraron ítems.")
except Exception as e:
    print(f"Error al esperar los ítems: {e}")

driver.quit()
