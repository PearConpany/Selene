import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, font, messagebox
from io import StringIO
import contextlib
from typing import List, Dict
from pathlib import Path, PurePath
from pathlib import Path; import sys
BASE = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
PNG  = BASE / "Functions" / "luna" / "2.png"
ICO  = BASE / "Functions" / "luna" / "2.ico"


from Functions.core.interpreter import run_lines, Env

# ─── Paletas ──────────────────────────────────────────────────────────────
LIGHT = {"bg": "#ffffff", "fg": "#000000", "out": "#0f0"}
DARK  = {"bg": "#1e1e1e", "fg": "#d4d4d4", "out": "#0f0"}

def launch() -> None:
    root = tk.Tk()
    # ─── Icono en la barra de tareas y ventana principal ────────────────────
    # ─── Icono en la barra de tareas y ventana principal ────────────────────
    ico_path = Path(__file__).parent / "2.ico"
    if ico_path.exists():
        try:
            root.iconbitmap(default=str(ico_path))
            # Establecer el ícono como predeterminado para todas las ventanas
            root.call('wm', 'iconbitmap', '.', str(ico_path))
        except Exception:
            pass
    root.title("Luna 1.1 – stable")
    
    colors = dict(LIGHT)
    base   = font.Font(family="Consolas", size=11)

    # ─── Barra de herramientas (tb) ───────────────────────────────────────
    tb = tk.Frame(root)
    tb.pack(fill="x")

    # ─── Notebook (pestañas) ──────────────────────────────────────────────
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    # ─── Consola de salida ──────────────────────────────────────────────────
    out = tk.Text(root, height=8, bg="#111", fg=colors["out"],
                  state="disabled", font=base)
    out.pack(fill="x", side="bottom")

    # ─── Barra de estado ──────────────────────────────────────────────────
    status = tk.Label(root, text="Ln 1, Col 1", anchor="w",
                      bg=colors["bg"], fg=colors["fg"])
    status.pack(fill="x", side="bottom")

    # ─── vectores de pestañas y entornos ──────────────────────────────────
    editors: List[tk.Text] = []
    envs:    List[dict]    = []

    # ─── helpers ──────────────────────────────────────────────────────────
    def cur() -> int:
        return nb.index("current")

    def _apply_theme():
        for ed in editors:
            ed.configure(bg=colors["bg"], fg=colors["fg"])
            # Actualizar color de números de línea
            line_numbers = ed.master.winfo_children()[0]
            if isinstance(line_numbers, tk.Text):
                line_numbers.configure(bg=colors["bg"], fg="#666")
        status.configure(bg=colors["bg"], fg=colors["fg"])
        out.configure(fg=colors["out"])

    def _update_status(event=None):
        if not editors: return
        line, col = editors[cur()].index("insert").split(".")
        status.config(text=f"Ln {line}, Col {int(col)+1}")

    # ─── Pestañas ─────────────────────────────────────────────────────────
    def new_tab(content: str = ""):
        frame = tk.Frame(nb)
        
        # Contenedor para números de línea y editor
        container = tk.Frame(frame)
        container.pack(fill="both", expand=True)
        
        # Widget para números de línea
        line_numbers = tk.Text(container, width=4, padx=3, takefocus=0,
                             bg=colors["bg"], fg="#666",
                             font=base, cursor="arrow")
        line_numbers.pack(side="left", fill="y")
        
        # Editor principal
        txt = tk.Text(container, wrap="none", undo=True,
                     bg=colors["bg"], fg=colors["fg"], font=base)
        txt.pack(side="right", fill="both", expand=True)
        
        # Scrollbar que sincroniza ambos widgets
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scrollbar
        scrollbar.config(command=txt.yview)
        txt.config(yscrollcommand=scrollbar.set)
        line_numbers.config(yscrollcommand=scrollbar.set)
        
        def update_line_numbers(event=None):
            line_numbers.config(state="normal")
            line_numbers.delete("1.0", "end")
            lines = txt.get("1.0", "end-1c").split("\n")
            for i in range(len(lines)):
                if i == len(lines) - 1:
                    line_numbers.insert("end", f"{i+1}")
                else:
                    line_numbers.insert("end", f"{i+1}\n")
            line_numbers.config(state="disabled")
        
        def sync_scroll(*args):
            line_numbers.yview_moveto(args[0])
            txt.yview_moveto(args[0])
        
        # Vincular eventos
        txt.bind("<KeyPress>", update_line_numbers)
        txt.bind("<KeyRelease>", lambda e: (_update_status(e), update_line_numbers(e)))
        txt.bind("<<Modified>>", update_line_numbers)
        txt.bind("<<Selection>>", _update_status)
        txt.bind("<Return>", update_line_numbers)
        txt.bind("<BackSpace>", update_line_numbers)
        txt.bind("<Delete>", update_line_numbers)
        scrollbar.config(command=sync_scroll)
        
        # Configurar texto inicial
        txt.insert("1.0", content)
        update_line_numbers()
        
        nb.add(frame, text="Nuevo")
        editors.append(txt)
        envs.append({})
        nb.select(len(editors)-1)
        _update_status()

    def close_tab():
        if not editors: return
        idx = cur()
        nb.forget(idx)
        editors.pop(idx); envs.pop(idx)

    new_tab()  # pestaña inicial

    def _do_input_dialog(prompt: str, limit: int) -> str:
        dialog = tk.Toplevel(root)
        dialog.title("Entrada Elesen")
        dialog.transient(root)
        
        # Centramos la ventana
        dialog.geometry("300x150")
        x = root.winfo_x() + (root.winfo_width() - 300) // 2
        y = root.winfo_y() + (root.winfo_height() - 150) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Widgets
        tk.Label(dialog, text=prompt, wraplength=250).pack(pady=10)
        entry = tk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.focus_set()
        
        result = None
        
        def on_submit():
            nonlocal result
            result = entry.get()[:limit]
            dialog.destroy()
        
        def on_cancel():
            nonlocal result
            result = ""
            dialog.destroy()
        
        # Botones
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Enviar", command=on_submit).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=on_cancel).pack(side=tk.LEFT)
        
        # Manejamos Enter y Escape
        dialog.bind("<Return>", lambda e: on_submit())
        dialog.bind("<Escape>", lambda e: on_cancel())
        
        # Hacemos la ventana modal
        dialog.grab_set()
        dialog.wait_window()
        
        return result or ""

    def _do_input(env: Env, args: str):
        parts = args.split()
        var = parts[0] if parts else "entrada"
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 128
        
        val = _do_input_dialog(f"{var} (máx {limit} caracteres):", limit)
        env[var] = val

    # ─── ejecución ────────────────────────────────────────────────────────
    def _do_save_dialog(prompt: str = "Guardar archivo") -> str:
        """Muestra un diálogo para guardar archivo y retorna la ruta seleccionada"""
        file_path = filedialog.asksaveasfilename(
            title=prompt,
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        return file_path

    def _do_registro(env: Env, args: str):
        """Maneja la instrucción registro mostrando un diálogo de guardado"""
        try:
            # Evaluamos la expresión
            expr = args.split("=", 1)[1].strip()
            contenido = str(_eval(expr, env))
            
            # Mostramos el diálogo de guardado
            file_path = _do_save_dialog("Guardar registro")
            if not file_path:  # Usuario canceló
                return
                
            # Escribimos el contenido
            with open(file_path, "a", encoding="utf-8") as fp:
                fp.write(contenido + "\n")
            
            # Actualizamos la salida para mostrar éxito
            out.config(state="normal")
            out.insert("end", f"✔️ Archivo guardado en: {file_path}\n")
            out.see("end")
            out.config(state="disabled")
            
        except Exception as e:
            print(f"⚠️  Error al registrar: {str(e)}")

    # Modificamos run_code para incluir el nuevo manejador de registro
    def run_code(event=None):
        try:
            code = editors[cur()].get("1.0", "end-1c").splitlines()
            buf = StringIO()
            
            # Agregamos el manejador de registro al entorno
            envs[cur()]["_do_registro"] = lambda args: _do_registro(envs[cur()], args)
            
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                run_lines(code, envs[cur()])
            output = buf.getvalue() or "✔️ Ejecutado sin salida\n"
        except Exception as e:
            output = f"🛑 Error en la ejecución: {str(e)}\n"
        
        out.config(state="normal")
        out.delete("1.0", "end")
        out.insert("end", output)
        out.see("end")
        out.config(state="disabled")
        return "break"

    # ─── Archivo ──────────────────────────────────────────────────────────
    def open_file():
        p = filedialog.askopenfilename(
            filetypes=[("Selene", ".se"), ("Todos", "*.*")])
        if p:
            with open(p, encoding="utf-8") as f:
                new_tab(f.read())

    def save_file():
        p = filedialog.asksaveasfilename(defaultextension=".se")
        if not p: return
        with open(p, "w", encoding="utf-8") as f:
            f.write(editors[cur()].get("1.0", "end-1c"))

    # ─── Editar ───────────────────────────────────────────────────────────
    def copy():   editors[cur()].event_generate("<<Copy>>")
    def cut():    editors[cur()].event_generate("<<Cut>>")
    def paste():  editors[cur()].event_generate("<<Paste>>")
    def select_all():
        ed = editors[cur()]
        ed.tag_add("sel", "1.0", "end"); ed.mark_set("insert", "1.0")

    def search_replace():
        q = simpledialog.askstring("Buscar", "Texto:")
        if not q: return
        r = simpledialog.askstring("Reemplazar", "Con:") or ""
        ed = editors[cur()]
        ed.replace("1.0", "end", ed.get("1.0", "end").replace(q, r))

    # ─── Vista ────────────────────────────────────────────────────────────
    console_visible = tk.BooleanVar(value=True)

    def toggle_console():
        if console_visible.get():
            out.pack_forget()
        else:
            out.pack(fill="x", side="bottom")
        console_visible.set(not console_visible.get())

    def toggle_theme():
        nonlocal colors
        colors = DARK if colors["bg"] == LIGHT["bg"] else LIGHT
        _apply_theme()

    # ─── Configuración (simple) ───────────────────────────────────────────
    def show_prefs():
        win = tk.Toplevel(root); win.title("Preferencias")
        tk.Label(win, text="Tipografía:").grid(row=0, column=0, sticky="e")
        size_var = tk.IntVar(value=base["size"])
        tk.Spinbox(win, textvariable=size_var, from_=8, to=24, width=5)\
            .grid(row=0, column=1, sticky="w")

        def apply():
            base.configure(size=size_var.get())
            for ed in editors: ed.configure(font=base)
            win.destroy()

        tk.Button(win, text="Aplicar", command=apply).grid(
            row=1, columnspan=2, pady=6)

    # ─── Ayuda ────────────────────────────────────────────────────────────
    def about():
        messagebox.showinfo(
            "Acerca de",
            "Luna Wizard IDE estable\n"
            "Motor Elesen Wizard 1.1\n\n"
            "© 2025 Elian Alfonso López\n"
            "sitio oficial: github.com/elesen/ide"
        )

    # ─── Menú ─────────────────────────────────────────────────────────────
    menubar = tk.Menu(root)

    m_file = tk.Menu(menubar, tearoff=0)
    m_file.add_command(label="Nuevo", accelerator="Ctrl+N", command=new_tab)
    m_file.add_command(label="Abrir…", accelerator="Ctrl+O", command=open_file)
    m_file.add_command(label="Guardar", accelerator="Ctrl+S", command=save_file)
    m_file.add_separator(); m_file.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Archivo", menu=m_file)

    m_edit = tk.Menu(menubar, tearoff=0)
    m_edit.add_command(label="Cortar", accelerator="Ctrl+X", command=cut)
    m_edit.add_command(label="Copiar", accelerator="Ctrl+C", command=copy)
    m_edit.add_command(label="Pegar", accelerator="Ctrl+V", command=paste)
    m_edit.add_separator()
    m_edit.add_command(label="Buscar/Reemplazar…", accelerator="Ctrl+F",
                       command=search_replace)
    m_edit.add_command(label="Seleccionar todo", accelerator="Ctrl+A",
                       command=select_all)
    menubar.add_cascade(label="Editar", menu=m_edit)

    m_view = tk.Menu(menubar, tearoff=0)
    m_view.add_checkbutton(label="Mostrar consola",
                           variable=console_visible, command=toggle_console)
    m_view.add_command(label="Tema claro/oscuro", accelerator="Ctrl+T",
                       command=toggle_theme)
    menubar.add_cascade(label="Vista", menu=m_view)

    m_cfg = tk.Menu(menubar, tearoff=0)
    m_cfg.add_command(label="Preferencias…", command=show_prefs)
    menubar.add_cascade(label="Configuración", menu=m_cfg)

    m_help = tk.Menu(menubar, tearoff=0)
    m_help.add_command(label="Acerca de", command=about)
    menubar.add_cascade(label="Ayuda", menu=m_help)

    root.config(menu=menubar)

    # ─── Botones de la barra ─────────────────────────────────────────────
    tk.Button(tb, text="▶ Ejecutar", command=run_code).pack(side="left")
    tk.Button(tb, text="➕", command=new_tab).pack(side="left")
    tk.Button(tb, text="✕", command=close_tab).pack(side="left")

    # ─── Atajos de teclado ───────────────────────────────────────────────
    root.bind("<Control-Return>", run_code)
    root.bind("<Control-n>",     lambda e: new_tab())
    root.bind("<Control-w>",     lambda e: close_tab())
    root.bind("<Control-o>",     lambda e: open_file())
    root.bind("<Control-s>",     lambda e: save_file())
    root.bind("<Control-f>",     lambda e: search_replace())
    root.bind("<Control-t>",     lambda e: toggle_theme())
    root.bind("<Control-a>",     lambda e: select_all() or "break")

    _apply_theme()
    root.after(100, _update_status)
    root.mainloop()
