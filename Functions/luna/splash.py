import tkinter as tk
from tkinter import ttk
import time
import random

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        
        # Frases motivacionales e irónicas
        self.frases = [
            "Si funciona, no toques nada… hasta que tu jefe lo vea.",
            "Tu código no tiene errores… solo características no documentadas.",
            "Hoy es un gran día para romper algo que ayer funcionaba perfecto.",
            "Debuguear es como ser detective en una novela donde tú escribiste el crimen… y olvidaste todo.",
            "No eres tú, es el compilador.",
            "Si el café no lo arregla, es un bug real.",
            "Sigue soñando, ese build va a compilar eventualmente.",
            "¿Quién necesita dormir cuando puedes reinventar la rueda a las 3 a.m.?",
            "Tu código es como una cebolla: hace llorar a quien lo lee.",
            "Todo es posible si ignoras suficientes advertencias.",
            "El código que escribiste hace 6 meses es como si lo hubiera escrito otra persona.",
            "Programar es 10% escribir código y 90% entender por qué no funciona.",
            "No es un bug, es una característica inesperada.",
            "La mejor optimización es no ejecutar el código.",
            "Cualquier código que escribas hoy será legacy mañana.",
            "Los mejores debuggers son printf() y una buena taza de café.",
            "El código limpio es como el arte abstracto: nadie lo entiende pero todos lo admiran.",
            "Git push --force: porque a veces la historia necesita ser reescrita.",
            "Stackoverflow es el verdadero MVP del desarrollo.",
            "Las reuniones son el mejor lugar para pensar en cómo resolver ese bug."
        ]
        
        # Configuración de la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500  # Aumentado el ancho
        window_height = 250  # Aumentado el alto
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Fondo oscuro con gradiente simulado
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.place(relwidth=1, relheight=1)
        
        # Título con versión
        self.title_label = tk.Label(
            self.root,
            text="✨ Luna Wizard IDE v1.9 ✨",
            font=("Helvetica", 20, "bold"),
            fg="#00d7ff",
            bg="#1e1e1e"
        )
        self.title_label.pack(pady=25)
        
        # Subtítulo
        self.subtitle_label = tk.Label(
            self.root,
            text="Tu compañero de programación mágico",
            font=("Helvetica", 12, "italic"),
            fg="#888888",
            bg="#1e1e1e"
        )
        self.subtitle_label.pack(pady=5)
        
        # Etiqueta para frases con borde simulado
        frame_frase = tk.Frame(self.root, bg="#333333", bd=1)
        frame_frase.pack(pady=15, padx=20)
        
        self.frase_label = tk.Label(
            frame_frase,
            text="",
            font=("Helvetica", 11),
            fg="#ffffff",
            bg="#1e1e1e",
            wraplength=450,
            pady=10,
            padx=15
        )
        self.frase_label.pack()
        
        # Barra de progreso estilizada
        style = ttk.Style()
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor="#1e1e1e",
                       background="#00d7ff",
                       darkcolor="#00d7ff",
                       lightcolor="#00d7ff")
        
        self.progress = ttk.Progressbar(
            self.root,
            length=400,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=25)
        
    def update_frase(self, progress):
        if progress < 90:
            frase = random.choice(self.frases)
        else:
            frase = "¡Preparado para crear magia con código!"
        self.frase_label.config(text=frase)
        self.root.update()
        
    def run(self):
        for i in range(101):
            if i % 10 == 0:  # Actualizar frase cada 10%
                self.update_frase(i)
            self.progress['value'] = i
            self.root.update()
            time.sleep(0.1)  # Reducido para una carga más ágil
        self.root.destroy()

def show_splash():
    splash = SplashScreen()
    splash.run()

if __name__ == "__main__":
    show_splash()
