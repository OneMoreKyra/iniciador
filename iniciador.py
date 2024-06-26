import os
import importlib.util
import requests
from colorama import Fore, init
import tkinter as tk
import tkinter.simpledialog as sd
from ping3 import ping, verbose_ping
import time
import threading
import zipfile
import webbrowser
import shutil

init(autoreset=True)

ID = ""
username = os.getlogin() 
data_folder_path = f"C:\\Users\\{username}\\Sniper\\Datos"
os.makedirs(data_folder_path, exist_ok=True)
cookie_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Modulos', 'cookie.txt')

def actualizar_modulos_y_script():
    print(Fore.YELLOW + "Actualizando módulos")
    directorio = os.path.dirname(os.path.realpath(__file__))
    ruta_modulos = os.path.join(directorio, 'Modulos')
    for filename in os.listdir(ruta_modulos):
        if filename.endswith('.py'):
            os.remove(os.path.join(ruta_modulos, filename))
    url_modulos = 'https://github.com/OneMoreKyra/Modulos/archive/refs/heads/main.zip'
    r = requests.get(url_modulos)
    with open('Modulos.zip', 'wb') as f:
        f.write(r.content)
    with zipfile.ZipFile('Modulos.zip', 'r') as zip_ref:
        for member in zip_ref.namelist():
            if member.endswith('.py'):
                zip_ref.extract(member, ruta_modulos)
                os.rename(os.path.join(ruta_modulos, member), os.path.join(ruta_modulos, os.path.basename(member)))
    os.remove('Modulos.zip')
    print(Fore.GREEN + "Módulos actualizados correctamente")

    print(Fore.YELLOW + "Actualizando script de arranque")
    url_script = 'https://raw.githubusercontent.com/OneMoreKyra/iniciador/main/iniciador.py'
    r = requests.get(url_script)
    with open(os.path.realpath(__file__), 'w', encoding='utf-8') as f:
        f.write(r.text)
    print(Fore.GREEN + "Script de arranque actualizado correctamente")

def cargar_modulos():
    print(Fore.GREEN + "Cargando datos")
    shutil.copytree(data_folder_path, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos'), dirs_exist_ok=True)
    print(Fore.GREEN + "Datos cargados exitosamente")

    directorio = os.path.dirname(os.path.realpath(__file__))
    ruta_modulos = os.path.join(directorio, 'Modulos')
    modulos = [f[:-3] for f in os.listdir(ruta_modulos) if f.endswith('.py')]
    modulos.sort()
    return modulos

def ejecutar_modulo(modulo_seleccionado, ID, boton):
    print(Fore.GREEN + f"Módulo {modulo_seleccionado} iniciado como Sniper")
    directorio = os.path.dirname(os.path.realpath(__file__))
    ruta_modulo = os.path.join(directorio, 'Modulos', f"{modulo_seleccionado}.py")
    spec = importlib.util.spec_from_file_location("Sniper", ruta_modulo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    print(Fore.RED + "La ejecución se realiza en segundo plano y la duración puede ser de algunos segundos dependiendo del usuario y el módulo seleccionado")
    modulo.main(ID)
    boton.config(relief="raised")
    print(Fore.GREEN + "Exportando datos")
    shutil.copytree(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos'), data_folder_path, dirs_exist_ok=True)
    print(Fore.GREEN + "Datos exportados correctamente")

def cambiar_cookie():
    global cookie_path
    nueva_cookie = sd.askstring("Cambiar Cookie", "Introduce la nueva cookie:")
    with open(cookie_path, 'w') as file:
        file.write(nueva_cookie)
    print(Fore.GREEN + "Cookie actualizada correctamente.")

def main():
    global ID
    ID = sd.askstring("ID del usuario", "Introduce el ID del usuario a revisar:")

    ventana = tk.Tk()
    ventana.title("Sniper")
    ventana.configure(bg='#000000')  # Color de fondo negro

    label_usuario = tk.Label(ventana, text=f"ID del usuario seleccionado: {ID}", bg='#000000', fg='#ffffff')
    label_usuario.pack()

    response = requests.get(f"https://users.roblox.com/v1/users/{ID}")
    username = response.json().get("name")
    label_username = tk.Label(ventana, text=f"Username: {username}", bg='#000000', fg='#ffffff')
    label_username.pack()

    label_ip = tk.Label(ventana, text="", bg='#000000', fg='#ffffff')
    label_ip.pack()

    label_ping = tk.Label(ventana, text="", bg='#000000', fg='#ffffff')
    label_ping.pack()

    label_cookie = tk.Label(ventana, text="", bg='#000000', fg='#ffffff')
    label_cookie.pack()

    print("Iniciando la carga de módulos")
    modulos = cargar_modulos()
    for i, modulo in enumerate(modulos, start=1):
        boton = tk.Button(ventana, text=f"{i}-{modulo}", command=lambda modulo=modulo: ejecutar_modulo(modulo, ID, boton), bg='#808080', fg='#ffffff', activebackground='#A9A9A9')
        boton.pack()

    boton_cambiar_cookie = tk.Button(ventana, text="Cambiar Cookie", command=cambiar_cookie, bg='#808080', fg='#ffffff', activebackground='#A9A9A9')
    boton_cambiar_cookie.pack()

    def cambiar_id():
        global ID
        ID = sd.askstring("Cambiar ID", "Introduce el nuevo ID del usuario a revisar:")
        label_usuario.config(text=f"ID del usuario seleccionado: {ID}")
        response = requests.get(f"https://users.roblox.com/v1/users/{ID}")
        username = response.json().get("name")
        label_username.config(text=f"Username: {username}")

    boton_cambiar_id = tk.Button(ventana, text="Cambiar ID", command=cambiar_id, bg='#808080', fg='#ffffff', activebackground='#A9A9A9')
    boton_cambiar_id.pack()

    boton_cerrar = tk.Button(ventana, text="Cerrar", command=lambda: os._exit(0), bg='#808080', fg='#ffffff', activebackground='#A9A9A9')
    boton_cerrar.pack()

    def abrir_carpeta():
        print(Fore.YELLOW + "La edición de datos solo está disponible cuando el script no se está ejecutando, para evitar posibles errores, no modifiques esta carpeta si se está ejecutando")
        webbrowser.open(data_folder_path)

    boton_abrir_carpeta = tk.Button(ventana, text="Abrir Carpeta de Datos", command=abrir_carpeta, bg='#808080', fg='#ffffff', activebackground='#A9A9A9')
    boton_abrir_carpeta.pack()

    response = requests.get("https://api.ipify.org?format=json")
    ip = response.json().get("ip")
    label_ip.config(text=f"IP: {ip}")

    def actualizar_ping():
        while True:
            latency = ping("www.roblox.com")
            label_ping.config(text=f"Ping: {int(latency)} ms")
            time.sleep(5)

    threading.Thread(target=actualizar_ping).start()

    ventana.mainloop()

if __name__ == "__main__":
    actualizar_modulos_y_script()
    main()
