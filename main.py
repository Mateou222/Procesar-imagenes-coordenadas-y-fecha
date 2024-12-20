import datetime
from logging import root
from tkinter import messagebox
import tkinter as tk

from datetime import datetime

from tkcalendar import *

from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim

from funciones import *

import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Configura el idioma a español

def obtener_coordenadas_por_direccion(direccion):
    geolocator = Nominatim(user_agent="geoapi")
    try:
        location = geolocator.geocode(direccion, country_codes="UY")  # Restringe a Uruguay (UY es el código ISO del país)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        messagebox.showinfo(f"Error", "Error al buscar dirección: {e}")
        return None, None

def interfaz_principal():
    ventana = tk.Tk()
    ventana.title("Procesar Imágenes con Coordenadas")
    
    # Obtener el tamaño de la pantalla
    pantalla_width = ventana.winfo_screenwidth()
    pantalla_height = ventana.winfo_screenheight()
    
    # Definir el tamaño de la ventana
    ventana_width = 1100
    ventana_height = 600
    
    # Calcular la posición X y Y para centrar la ventana
    posicion_x = int((pantalla_width - ventana_width) / 2)
    posicion_y = int((pantalla_height - ventana_height) / 2)
    
    # Establecer la geometría de la ventana
    ventana.geometry(f"{ventana_width}x{ventana_height}+{posicion_x}+{posicion_y}")   
    
    ventana.columnconfigure(0, weight=1)  # Expande la primera columna
    ventana.columnconfigure(1, weight=2)  # Expande la segunda columna
    ventana.rowconfigure(0, weight=1)     # Expande la primera fila

    # Frame de opciones
    frame_opciones = tk.Frame(ventana, bg="white", relief="solid", bd=1)
    frame_opciones.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Frame de mapa
    frame_mapa = tk.Frame(ventana, bg="white", relief="solid", bd=1)
    frame_mapa.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Entradas de datos en frame_opciones
    tk.Label(frame_opciones, text="Latitud:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_latitud = tk.Entry(frame_opciones)
    entry_latitud.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(frame_opciones, text="Longitud:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_longitud = tk.Entry(frame_opciones)
    entry_longitud.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    
    tk.Label(frame_opciones, text="Altura (m):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    entry_metros = tk.Entry(frame_opciones)
    entry_metros.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
    
    tk.Label(frame_opciones, text="Fecha:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    cal = Calendar(frame_opciones, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
    
    # Campos de hora
    tk.Label(frame_opciones, text="Hora (HH:MM:SS):").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    entry_hora = tk.Entry(frame_opciones, width=5)
    entry_hora.grid(row=7, column=1, padx=5, pady=5, sticky="w")
    entry_minutos = tk.Entry(frame_opciones, width=5)
    entry_minutos.grid(row=8, column=1, padx=5, pady=5, sticky="w")
    entry_segundos = tk.Entry(frame_opciones, width=5)
    entry_segundos.grid(row=9, column=1, padx=5, pady=5, sticky="w")    

    am_pm_var = tk.StringVar(value="AM")
    am_pm_menu = tk.OptionMenu(frame_opciones, am_pm_var, "AM", "PM")
    am_pm_menu.grid(row=10, column=1, padx=5, pady=5, sticky="w")   

    # Mapa interactivo en frame_mapa
    map_widget = TkinterMapView(frame_mapa, width=600, height=500)
    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    map_widget.set_position(-34.905427, -56.196684) # Coordenadas iniciales (Montevideo)
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
            messagebox.showinfo("Error", "Dirección no encontrada.")

    map_widget.bind("<Button-1>", actualizar_coordenadas)

    # Entrada para búsqueda de dirección
    tk.Label(frame_opciones, text="Buscar Dirección:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_direccion = tk.Entry(frame_opciones, width=45)
    entry_direccion.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
    boton_buscar = tk.Button(frame_opciones, text="Buscar", command=buscar_direccion)
    boton_buscar.grid(row=0, column=2, columnspan=2, pady=1)

    def procesar():
        lat = entry_latitud.get()
        lon = entry_longitud.get()
        metros = entry_metros.get()
        fecha = cal.get_date()
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
            fecha = f"{fecha_formateada}"

            procesar_imagenes(lat, lon, metros, fecha, hora_completa)
            messagebox.showinfo("Éxito", "Las imágenes han sido procesadas correctamente.")
            # Cerrar la ventana principal
            ventana.destroy()
        else:
            messagebox.showinfo("Error", "Por favor completa todos los campos.")

    # Botón de procesar
    boton_procesar = tk.Button(frame_opciones, text="Procesar Imágenes", command=procesar, width=18, height=2, font=("Arial", 10))
    boton_procesar.grid(row=12, column=0, columnspan=2, pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    interfaz_principal()