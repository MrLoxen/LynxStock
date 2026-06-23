# app.py
from flask import Flask, jsonify
from models import db, TasaBCV
from routes import api
from scraper_bcv import obtener_tasa_bcv
import sys
import os
import threading
import time
import ctypes
from ctypes import wintypes
import subprocess
import shutil
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave-secreta-personalizada-2026'
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
app.register_blueprint(api)

# Variable global para guardar el proceso del navegador
navegador_proceso = None

# --- Función para actualizar la tasa en la base de datos ---
def actualizar_tasa_bcv():
    with app.app_context():
        nueva_tasa = obtener_tasa_bcv()
        if nueva_tasa is not None:
            tasa = TasaBCV(tasa=nueva_tasa)
            db.session.add(tasa)
            db.session.commit()
            print(f"[{datetime.now()}] Tasa BCV guardada: {nueva_tasa}")
        else:
            print("No se pudo actualizar la tasa BCV (sin internet o fallo de scraping).")

# --- Hilo de fondo que actualiza la tasa cada 6 horas ---
def programar_actualizacion_tasa():
    actualizar_tasa_bcv()
    while True:
        time.sleep(21600)   # 6 horas
        actualizar_tasa_bcv()

# --- Abrir navegador en modo kiosko (Chrome/Edge) y guardar el proceso ---
def abrir_kiosko():
    global navegador_proceso
    url = 'http://127.0.0.1:5050'
    chrome_paths = [
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
        shutil.which('chrome'),
        shutil.which('google-chrome'),
    ]
    edge_paths = [
        'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
        'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
        shutil.which('msedge'),
    ]

    navegador = None
    for path in chrome_paths:
        if path and os.path.exists(path):
            navegador = path
            break
    if not navegador:
        for path in edge_paths:
            if path and os.path.exists(path):
                navegador = path
                break

    if navegador:
        navegador_proceso = subprocess.Popen([navegador, '--kiosk', url, '--new-window'])
        # Hilo para cambiar el ícono de la ventana
        threading.Thread(target=cambiar_icono_ventana, daemon=True).start()
    else:
        import webbrowser
        webbrowser.open_new(url)

# --- Ruta para apagar la aplicación ---
@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    global navegador_proceso
    # Cerrar el navegador si está abierto
    if navegador_proceso is not None:
        try:
            navegador_proceso.terminate()  # señal de cierre amable
            navegador_proceso.wait(timeout=3)
        except:
            navegador_proceso.kill()       # forzar si no responde
    # Detener el servidor de Flask en un hilo aparte para responder la petición
    threading.Thread(target=detener_servidor).start()
    return '', 200

def detener_servidor():
    # Esperar un momento para asegurar que la respuesta se envió
    time.sleep(0.5)
    os._exit(0)  # Cierra la aplicación por completo

# --- Ruta para minimizar la aplicación (versión robusta) ---
@app.route('/api/minimize', methods=['POST'])
def minimize():
    # Función callback para EnumWindows
    def enum_callback(hwnd, lParam):
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if "Lynx Stock" in title:
                # Minimizar ventana (SW_MINIMIZE = 6)
                ctypes.windll.user32.ShowWindow(hwnd, 6)
                return False  # detener enumeración
        return True  # continuar

    # EnumWindows espera una función de callback
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    enum_windows = ctypes.windll.user32.EnumWindows
    enum_windows(WNDENUMPROC(enum_callback), 0)

    # Si no encontró ninguna, igual retornamos éxito porque ya intentó
    return '', 200

def cambiar_icono_ventana():
    # Esperar un poco para que la ventana del navegador esté completamente cargada
    time.sleep(2)
    # Buscar la ventana cuyo título contenga "Lynx Stock"
    hwnd = None
    # Primero intentar búsqueda exacta
    hwnd = ctypes.windll.user32.FindWindowW(None, "Lynx Stock")
    if not hwnd:
        # Si no encuentra, buscar con EnumWindows (respaldo)
        def enum_callback(hwnd_candidate, lParam):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd_candidate)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd_candidate, buff, length + 1)
                if "Lynx Stock" in buff.value:
                    nonlocal hwnd
                    hwnd = hwnd_candidate
                    return False  # detener enumeración
            return True
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_callback), 0)

    if hwnd:
        # Obtener la ruta del ícono
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'lynx.ico')
        if os.path.exists(icon_path):
            # Cargar el ícono (IMAGE_ICON = 1, LR_LOADFROMFILE = 0x00000010)
            hicon = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, 0x00000010)
            if hicon:
                # Enviar mensaje WM_SETICON (0x0080)
                # ICON_SMALL = 0, ICON_BIG = 1
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, hicon)  # icono pequeño (barra de título)
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, hicon)  # icono grande (alt-tab)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Hilo de tasa BCV
    hilo_tasa = threading.Thread(target=programar_actualizacion_tasa, daemon=True)
    hilo_tasa.start()

    # Hilo de apertura del navegador en kiosko
    threading.Timer(2.0, abrir_kiosko).start()

    app.run(port=5050, debug=False, use_reloader=False)