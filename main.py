import datetime
from logging import root
import os
import shutil
from tkinter import messagebox
import cv2
import tkinter as tk

from datetime import datetime

from tkcalendar import *

from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim

from funciones import *

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Configura el idioma a español

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
    


def obtener_coordenadas_por_direccion(direccion):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(direccion)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def interfaz_principal():
    ventana = tk.Tk()
    ventana.title("Procesar Imágenes con Coordenadas")
    ventana.geometry("1100x600")

    frame_opciones = tk.Frame(ventana)
    frame_opciones.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    frame_mapa = tk.Frame(ventana)
    frame_mapa.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Entradas de datos
    tk.Label(frame_opciones, text="Latitud:").pack()
    entry_latitud = tk.Entry(frame_opciones)
    entry_latitud.pack()

    tk.Label(frame_opciones, text="Longitud:").pack()
    entry_longitud = tk.Entry(frame_opciones)
    entry_longitud.pack()

    tk.Label(frame_opciones, text="Altura (m):").pack()
    entry_metros = tk.Entry(frame_opciones)
    entry_metros.pack()
    
    tk.Label(frame_opciones, text="Fecha:").pack()
    cal = Calendar(frame_opciones, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack()
    
    # Campos de hora
    tk.Label(frame_opciones, text="Hora (HH:MM:SS AM/PM):").pack()
    entry_hora = tk.Entry(frame_opciones, width=5)
    entry_hora.pack()
    entry_minutos = tk.Entry(frame_opciones, width=5)
    entry_minutos.pack()
    entry_segundos = tk.Entry(frame_opciones, width=5)
    entry_segundos.pack()

    # Menú desplegable para AM/PM
    am_pm_var = tk.StringVar(value="AM")
    am_pm_menu = tk.OptionMenu(frame_opciones, am_pm_var, "AM", "PM")
    am_pm_menu.pack()
    

    # Mapa interactivo
    map_widget = TkinterMapView(frame_mapa, width=600, height=500)
    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    map_widget.set_position(-34.905427, -56.196684)  # Coordenadas iniciales (Montevideo)
    map_widget.pack(fill=tk.BOTH, expand=True)

    marker = None

    def actualizar_coordenadas(evento):
        nonlocal marker
        lat, lon = map_widget.get_position()
        if marker:
            map_widget.remove_marker(marker)
        marker = map_widget.set_marker(lat, lon, text="Seleccionado")
        entry_latitud.delete(0, tk.END)
        entry_latitud.insert(0, f"{lat:.6f}")
        entry_longitud.delete(0, tk.END)
        entry_longitud.insert(0, f"{lon:.6f}")

    def buscar_direccion():
        direccion = entry_direccion.get()
        lat, lon = obtener_coordenadas_por_direccion(direccion)
        if lat and lon:
            map_widget.set_position(lat, lon)
            actualizar_coordenadas(None)
        else:
            print("Dirección no encontrada.")

    map_widget.bind("<Button-1>", actualizar_coordenadas)

    # Entrada para búsqueda de dirección
    tk.Label(frame_opciones, text="Buscar Dirección:").pack(pady=5)
    entry_direccion = tk.Entry(frame_opciones)
    entry_direccion.pack()
    boton_buscar = tk.Button(frame_opciones, text="Buscar", command=buscar_direccion)
    boton_buscar.pack(pady=5)

    def procesar():
        lat = entry_latitud.get()
        lon = entry_longitud.get()
        metros = entry_metros.get()
        fecha = "2024-07-22"
        cal.get_date()
        hora = entry_hora.get()
        minutos = entry_minutos.get()
        segundos = entry_segundos.get()
        am_pm = am_pm_var.get()
        if lat and lon and metros and fecha and hora:
            
            # Convertir la fecha seleccionada en un objeto datetime
            fecha_objeto = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_formateada = fecha_objeto.strftime("%d %b %Y")  # Ejemplo: 13 dic 2024

            # Construir la cadena de hora con AM/PM
            hora_completa = f"{hora}:{minutos}:{segundos} {am_pm.upper()}"
            fecha_hora = f"{fecha_formateada} {hora_completa}"

            procesar_imagenes(lat, lon, metros, fecha_hora, hora)
            messagebox.showinfo("Éxito", "Las imágenes han sido procesadas correctamente.")
        else:
            print("Por favor completa todos los campos.")

    boton_procesar = tk.Button(frame_opciones, text="Procesar Imágenes", command=procesar)
    boton_procesar.pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    interfaz_principal()