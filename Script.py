#Modifique el nombre de algunas variables para mejor entendimiento.
#Utilice f-strings
#Moví la creación de la carpeta output_folder y la obtención de la absolute_path antes del bucle de descarga de imágenes para evitar que se cree la carpeta múltiples veces.
#Agregué comentarios para explicar de mejor manera el funcionamiento
#Agregué el manejo de errores (except requests.exceptions.RequestException) en lugar de capturar solamente RequestException.


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Tipos de libros
tag_books = ('LMP', 'MLA', 'PAA', 'PCA', 'PEA', 'SDA', 'TPA', 'CMA', 'SHA')

# URL bases para la descarga de las imágenes y la búsqueda del libro
base_url = 'https://www.conaliteg.sep.gob.mx/2023/c/'
base2_url = 'https://www.conaliteg.sep.gob.mx/2023/'

# Recorre los niveles P
for i in range(0, 8):
    # Recorre los títulos de los libros
    for tag_book in tag_books:
        try:
            # URL de los libros y búsqueda
            url = f'{base_url}P{i}{tag_book}/'
            url_busqueda = f'{base2_url}P{i}{tag_book}.htm#page/2'

            # Realizar la solicitud HTTP a la página de búsqueda
            response = requests.get(url_busqueda)
            response.raise_for_status()

            # Analizar el contenido HTML utilizando BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar las imágenes
            img_tags = soup.find_all('img')

            # Carpeta para guardar las imágenes
            output_folder = f'P{i}{tag_book}'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Ruta absoluta para la carpeta de salida
            absolute_path = os.path.abspath(output_folder)

            # Base para el número de página
            base = "000"

            # Descargar las imágenes
            for img_cont in range(1, 400):
                img_num = f"{base}{img_cont}"[-len(base):]
                img_url = f'{url}{img_num}.jpg'
                img_name = img_url.split('/')[-1]
                img_path = os.path.join(output_folder, img_name)

                response = requests.get(img_url)

                if response.status_code == 200:
                    with open(img_path, 'wb') as img_file:
                        img_file.write(response.content)
                    print(f'Imagen descargada: {img_name}')
                else:
                    break

        except requests.exceptions.RequestException as e:
            print(f'No existe el libro {url}: {e}')
            continue

        print('Descarga completada.')
        print(f'Ruta absoluta de la carpeta de imágenes descargadas: {absolute_path}')

