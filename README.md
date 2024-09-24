# Wallapop Web Scraper

Este script realiza web scraping en Wallapop para obtener productos específicos, compara los resultados con una ejecución previa y envía notificaciones por correo electrónico si se detectan nuevos ítems. Utiliza Selenium para la automatización de navegación web y Pandas para la gestión de datos.

## Motivación

Cuando realizas una búsqueda en Wallapop, los ítems más baratos suelen desaparecer rápidamente. Aunque puedes guardar una búsqueda en la plataforma y recibir notificaciones push en tu móvil, a veces esas notificaciones no llegan lo suficientemente rápido, lo que da lugar a que otros usuarios compren los ítems más económicos antes de que puedas reaccionar.

Este script fue creado para solucionar este problema. Te permite realizar una búsqueda automatizada en Wallapop, filtrar los ítems que no están en modo "reservado", y configurar un cron job que ejecute el script de manera regular para que te notifique de nuevos ítems en esa búsqueda específica. De esta forma, recibirás una notificación por correo con los ítems nuevos detectados, permitiéndote actuar más rápido que con las notificaciones push estándar de Wallapop.

## ¿Cómo usar el script para notificar tu búsqueda?

Es muy sencillo escoger la lista de productos que deseas trackear en Wallapop. Sigue estos pasos:

1. Abre tu navegador web y dirígete a [Wallapop](https://es.wallapop.com/).
2. Utiliza la barra de búsqueda para introducir el producto que deseas buscar.
3. Aplica los filtros que te interesen (como el rango de precios, la ubicación, o las opciones de envío) para afinar tu búsqueda.
4. Una vez que obtengas la lista de productos filtrada, copia la **URL** que aparece en la barra de direcciones del navegador.
5. Usa esta URL como parámetro del script mediante la opción `--url`:

    ```bash
    python list.py --url 'URL_COPIADA' --email 'tuemail@example.com'
    ```

De esta manera, el script buscará periódicamente los nuevos ítems que aparezcan en esa búsqueda y te notificará por correo electrónico si detecta cambios en los productos, como la aparición de ítems nuevos no reservados.

## Requisitos

- **Python 3.x**
- **Google Chrome**
- **ChromeDriver** (versión compatible con tu navegador)
- **Cuenta de Gmail con una [contraseña de aplicación](https://support.google.com/mail/answer/185833?hl=es)**

## 1. Configuración del entorno virtual

### En macOS o Linux:

1. **Crear un entorno virtual:**

    ```bash
    python3 -m venv wallapop_env
    ```

2. **Activar el entorno virtual:**

    - En macOS/Linux:

    ```bash
    source wallapop_env/bin/activate
    ```

## 2. Crear el script Python

Guarda el script en un archivo llamado `list.py`. Este script usa **Selenium** para automatizar la búsqueda en Wallapop, compara los resultados con una ejecución previa, y si detecta nuevos ítems, los envía por correo electrónico.

## 3. Dependencias necesarias

- **Chrome**: Asegúrate de que tienes instalado Google Chrome.
- **ChromeDriver**: Necesitas instalar el ChromeDriver que es compatible con la versión de Chrome instalada en tu sistema.

### Instalación de ChromeDriver:

1. Descarga la versión correspondiente de [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).
2. Descomprime el archivo y mueve el ejecutable a un directorio incluido en tu `PATH` (por ejemplo, `/usr/local/bin` en macOS/Linux).
3. Verifica la instalación:

    ```bash
    chromedriver --version
    ```

## 4. Crear el archivo `requirements.txt`

Crea un archivo `requirements.txt` con el siguiente contenido:

```txt
selenium==4.10.0
pandas==2.0.1
```

## 5. Instalar las dependencias

Con el entorno virtual activado, instala las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```

## 6. Configurar una contraseña de aplicación en Gmail

Gmail requiere una **contraseña de aplicación** para enviar correos desde un script o una aplicación externa.

1. **Activar la autenticación de dos pasos**:
   - Ve a tu [Cuenta de Google](https://myaccount.google.com/).
   - Navega a la sección de **Seguridad**.
   - Activa la **Verificación en dos pasos**.

2. **Generar una contraseña de aplicación**:
   - En la misma sección de Seguridad, selecciona **Contraseñas de aplicaciones**.
   - Selecciona **Correo** como la aplicación y **Equipo** como el dispositivo.
   - Gmail generará una contraseña de aplicación de 16 caracteres.

3. **Uso de la contraseña de aplicación en el script**:
   - En el campo `contraseña` del script, usa esta contraseña de aplicación sin espacios.

## 7. Estructura del directorio

La estructura típica del directorio será la siguiente:

```bash
wallapop_env/
│
├── list.py                   # Script Python
├── requirements.txt           # Lista de dependencias
└── items.csv                  # Archivo CSV que contiene la lista de ítems comparada
```

## 8. Ejecución del script

Una vez configurado el entorno y activadas las dependencias, puedes ejecutar el script.

1. **Asegúrate de que el entorno virtual esté activado**:

    ```bash
    source wallapop_env/bin/activate
    ```

2. **Ejecutar el script con una URL de Wallapop**:

    ```bash
    python list.py --url 'https://es.wallapop.com/app/search?latitude=40.41956&longitude=-3.69196&keywords=garmin%20edge%20530&min_sale_price=50&max_sale_price=120&order_by=newest&shipping=true&country_code=ES&filters_source=stored_filters' --email 'tuemail@example.com'
    ```

- Si no proporcionas un correo electrónico con `--email`, el correo se enviará a tu dirección de Gmail (la misma que configures como origen en el script).

- **Nota**: Dentro del script se configura el parámetro `email_origen = "tuemail@gmail.com"` como la dirección de origen y también como la dirección de destino por defecto para las notificaciones:

    ```python
    email_origen = "xxxxxxxxx@gmail.com"
    ```

- Asegúrate de actualizar este campo con tu dirección de Gmail para que el script funcione correctamente.

## 9. Automatización del script (Opcional)

Si deseas automatizar la ejecución del script, por ejemplo, cada hora, puedes configurar un cron job.

### Configuración de un cron job en macOS/Linux:

1. **Abrir el editor de cron**:

    ```bash
    crontab -e
    ```

2. **Añadir una línea para ejecutar el script cada hora**:

    ```bash
    0 * * * * /ruta/completa/a/tu/entorno/virtual/bin/python /ruta/completa/a/tu/script/list.py --url 'https://es.wallapop.com/app/search?...' --email 'tuemail@example.com' >>ruta/completa/a/tu/salida.log 2>&1
    ```

Esto ejecutará el script cada hora en el minuto 0 y redirigirá tanto la salida estándar como los errores a `salida.log`.

## 10. Notas adicionales

- El archivo `items.csv` se guarda en la misma carpeta que el script. Este archivo se utiliza para comparar los ítems en ejecuciones posteriores del script.
- El correo se envía utilizando la configuración de SMTP de Gmail con una **contraseña de aplicación**.
