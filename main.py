from datetime import datetime
import shutil
from tkinter import messagebox
from funciones import *
import tkinter as tk
from tkcalendar import Calendar
import locale


def procesar_imagenes():
    # Limpio la carpeta de editadas
    if os.path.exists(".\\imagenes_editadas"):
        shutil.rmtree(".\\imagenes_editadas")
    os.makedirs(".\\imagenes_editadas")
    
    latitud = entry_latitud.get()
    longitud = entry_longitud.get()
    metros = entry_metros.get()
    fecha_seleccionada = cal.get_date()
    hora = entry_hora.get()
    minutos = entry_minutos.get()
    segundos = entry_segundos.get()
    am_pm = am_pm_var.get()

    if not latitud or not longitud or not metros or not fecha_seleccionada or not hora:
        messagebox.showerror("Error", "Por favor completa todos los campos.")
        return
    
    # Establecer la localización en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    
    # Convertir la fecha seleccionada en un objeto datetime
    fecha_objeto = datetime.strptime(fecha_seleccionada, "%Y-%m-%d")  # Formato que devuelve el calendario
    fecha_formateada = fecha_objeto.strftime("%d %b %Y")  # Ejemplo: 13 dic 2024

    # Construir la cadena de hora con AM/PM
    hora_completa = f"{hora}:{minutos}:{segundos} {am_pm.upper()}"
    coordenadas_metros = f"{latitud}, {longitud}, {metros} m"
    fecha_hora = f"{fecha_formateada} {hora_completa}"
        
    # Abrir la imagen
    ruta_imagenes = ".\\imagenes"
    imagenes = abrir_imagenes_en_carpeta(ruta_imagenes)

    # Ruta a la fuente personalizada (.ttf o .otf)
    fuente_path = "calibri.ttf"  # Cambia esta ruta

    # Procesar las imágenes cargadas
    for nombre_archivo, imagen in imagenes:  # Ahora debería funcionar correctamente
        if imagen is not None:
            # Agregar texto con contorno en la esquina inferior derecha
            imagen_con_texto = agregar_texto_con_contorno(
                imagen,
                coordenadas_metros,
                fecha_hora,
                fuente_path=fuente_path,
                tamano_fuente=60,   # Tamaño de la fuente
                color_texto=(255, 255, 255),  # Blanco en formato RGB
                color_contorno=(0, 0, 0),  # Contorno negro
                desplazamiento_contorno=2   # Desplazamiento del contorno
            )

            # Guardar la imagen con texto
            ruta_guardado = f".\\imagenes_editadas\\{nombre_archivo}"
            cv2.imwrite(ruta_guardado, imagen_con_texto)
            print(f"Imagen guardada: {ruta_guardado}")
        else:
            print(f"No se pudo procesar la imagen: {nombre_archivo}")
    messagebox.showinfo("Éxito", "Las imágenes han sido procesadas correctamente.")
    root.destroy()  # Cerrar la ventana principal

# Crear la ventana principal
root = tk.Tk()
root.title("Editor de Imágenes")

# Campos de entrada
tk.Label(root, text="Latitud:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_latitud = tk.Entry(root, width=30)
entry_latitud.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Longitud:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_longitud = tk.Entry(root, width=30)
entry_longitud.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Metros:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_metros = tk.Entry(root, width=30)
entry_metros.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Fecha:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.grid(row=3, column=1, padx=10, pady=5)

# Campos de hora
tk.Label(root, text="Hora (HH:MM:SS AM/PM):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_hora = tk.Entry(root, width=5)
entry_hora.grid(row=4, column=1, padx=10, pady=5, sticky="w")
entry_minutos = tk.Entry(root, width=5)
entry_minutos.grid(row=4, column=1, padx=60, pady=5, sticky="w")
entry_segundos = tk.Entry(root, width=5)
entry_segundos.grid(row=4, column=1, padx=110, pady=5, sticky="w")

# Menú desplegable para AM/PM
am_pm_var = tk.StringVar(value="AM")
am_pm_menu = tk.OptionMenu(root, am_pm_var, "AM", "PM")
am_pm_menu.grid(row=4, column=1, padx=160, pady=5, sticky="w")

# Botón para procesar
boton_procesar = tk.Button(root, text="Procesar Imágenes", command=procesar_imagenes)
boton_procesar.grid(row=5, column=0, columnspan=2, pady=20)

# Iniciar la interfaz
root.mainloop()


