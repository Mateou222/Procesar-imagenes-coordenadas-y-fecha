import os
import shutil
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

    Args:
        imagen (numpy.ndarray): Imagen sobre la que se agregará texto.
        coordenadas_metros (str): Texto con coordenadas y metros.
        fecha (str): Fecha a agregar.
        fuente_path (str): Ruta al archivo de fuente personalizada (.ttf o .otf).
        tamano_fuente (int): Tamaño de la fuente. Por defecto, 1.
        color_texto (tuple): Color del texto en formato RGB.
        color_contorno (tuple): Color del contorno del texto (por defecto, negro).
        desplazamiento_contorno (int): Desplazamiento del contorno, para que se dibuje alrededor del texto.

    Returns:
        numpy.ndarray: Imagen con el texto y el contorno agregado.
    """
    try:
        # Convertir la imagen de OpenCV a Pillow
        imagen_pil = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(imagen_pil)
        
        # Cargar la fuente personalizada
        fuente = ImageFont.truetype(fuente_path, tamano_fuente)

        # Calcular el tamaño del texto para ajustar el espacio entre las líneas
        ancho_imagen, altura_imagen = imagen_pil.size
        x = ancho_imagen - 750
        y = altura_imagen - 10

        # Obtener el tamaño del texto usando textbbox (bounding box)
        bbox_fecha = draw.textbbox((x, y), fecha, font=fuente)
        bbox_coordenadas = draw.textbbox((x, y), coordenadas_metros, font=fuente)

        # Desplazar el texto hacia arriba dependiendo del tamaño de cada línea
        y -= bbox_fecha[3] - bbox_fecha[1] + 20  # Espacio después de la fecha

        # Dibujar el contorno negro alrededor del texto (en varias direcciones)
        for dx in [-desplazamiento_contorno, 0, desplazamiento_contorno]:
            for dy in [-desplazamiento_contorno, 0, desplazamiento_contorno]:
                if dx != 0 or dy != 0:  # No dibujar el contorno en el centro
                    draw.text((x + dx, y + dy), fecha, font=fuente, fill=color_contorno)
        
        # Ahora dibujar el texto principal en blanco sobre el contorno
        draw.text((x, y), fecha, font=fuente, fill=color_texto)

        # Desplazar para la siguiente línea (coordenadas)
        y -= bbox_coordenadas[3] - bbox_coordenadas[1] + 20  # Espacio después de las coordenadas

        # Dibujar el contorno negro alrededor del texto de las coordenadas
        for dx in [-desplazamiento_contorno, 0, desplazamiento_contorno]:
            for dy in [-desplazamiento_contorno, 0, desplazamiento_contorno]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), coordenadas_metros, font=fuente, fill=color_contorno)

        # Ahora dibujar el texto principal en blanco sobre el contorno
        draw.text((x, y), coordenadas_metros, font=fuente, fill=color_texto)

        # Convertir la imagen de Pillow de vuelta a OpenCV
        imagen_final = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)

        return imagen_final
    except Exception as e:
        print(f"Error al agregar texto: {e}")
        return None
    
    
def procesar_imagenes(lat, lon, metros, fecha, hora):
    # Limpio la carpeta de editadas
    if os.path.exists(".\\imagenes_editadas"):
        shutil.rmtree(".\\imagenes_editadas")
    os.makedirs(".\\imagenes_editadas")
    
    coordenadas_metros = f"{lat}, {lon}, {metros} m"
    fecha_hora = f"{fecha} {hora}"

    ruta_imagenes = "./imagenes"
    imagenes = abrir_imagenes_en_carpeta(ruta_imagenes)

    for nombre_archivo, imagen in imagenes:
        if imagen is not None:
            imagen_con_texto = agregar_texto_con_contorno(
                imagen,
                coordenadas_metros=coordenadas_metros,
                fecha=fecha_hora,
                fuente_path="calibri.ttf",
            )
            ruta_guardado = f"./imagenes_editadas/{nombre_archivo}"
            cv2.imwrite(ruta_guardado, imagen_con_texto)
            print(f"Imagen guardada: {ruta_guardado}")