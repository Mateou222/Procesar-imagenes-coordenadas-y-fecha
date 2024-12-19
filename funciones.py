import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def abrir_imagenes_en_carpeta(ruta_carpeta):
    """
    Abre todos los archivos de imagen en una carpeta.
    """
    imagenes = []
    try:
        for archivo in os.listdir(ruta_carpeta):
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            if os.path.isfile(ruta_completa) and archivo.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.tiff')):
                imagen = cv2.imread(ruta_completa)
                if imagen is not None:
                    imagenes.append((archivo, imagen))
                else:
                    print(f"No se pudo cargar: {archivo}")
        return imagenes
    except Exception as e:
        print(f"Error al procesar la carpeta: {e}")
        return []


def agregar_texto_con_contorno(imagen, coordenadas_metros, fecha, fuente_path, tamano_fuente=60, color_texto=(255, 255, 255), color_contorno=(0, 0, 0), desplazamiento_contorno=2):
    """
    Agrega texto con contorno en la esquina inferior derecha de la imagen utilizando Pillow.
    """
    try:
        imagen_pil = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(imagen_pil)
        fuente = ImageFont.truetype(fuente_path, tamano_fuente)

        ancho_imagen, altura_imagen = imagen_pil.size
        x = ancho_imagen - 750
        y = altura_imagen - 100

        draw.text((x, y), coordenadas_metros, font=fuente, fill=color_contorno)
        draw.text((x, y), coordenadas_metros, font=fuente, fill=color_texto)
        y -= 50
        draw.text((x, y), fecha, font=fuente, fill=color_contorno)
        draw.text((x, y), fecha, font=fuente, fill=color_texto)

        return cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error al agregar texto: {e}")
        return None