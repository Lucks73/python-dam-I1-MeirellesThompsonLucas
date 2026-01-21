"""Interfaz gráfica del gestor de aparcamiento.

Este módulo contiene la clase `ParkingGUI` que crea la ventana y todos los
componentes visuales. La GUI interactúa exclusivamente con la API pública de
`Aparcamiento` y no accede directamente a sus estructuras internas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from Aparcamiento import Aparcamiento

# Colores tema oscuro (constantes de estilo)
COLORS = {
    'bg_primary': '#1a1a2e',
    'bg_secondary': '#16213e',
    'bg_card': '#0f3460',
    'accent': '#e94560',
    'accent_hover': '#ff6b81',
    'success': '#00d4aa',
    'warning': '#ffa41b',
    'text_primary': '#eaeaea',
    'text_secondary': '#a8b2d1',
    'border': '#2d3561'
}


class ModernButton(tk.Canvas):
    """Pequeño widget que pinta un botón visual moderno.

    Implementado como `Canvas` para dar apariencia personalizada. Es puramente
    visual: al pulsar invoca la función `command` provista.
    """

    def __init__(self, parent, text, command, color, **kwargs):
        super().__init__(parent, height=45, bg=COLORS['bg_card'], highlightthickness=0, **kwargs)
        self.command = command
        self.color = color
        self.text = text
        self.hover = False

        # Bindings simples para interacción
        self.bind('<Button-1>', lambda e: self.command())
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

        self.draw()

    def draw(self):
        # Dibujar el rectángulo y el texto (cálculos simples para centrar)
        self.delete('all')
        color = self.color if not self.hover else COLORS['accent_hover']
        self.create_rectangle(5, 5, self.winfo_reqwidth()-5 or 200, 40, fill=color, outline='', tags='button')
        self.create_text(self.winfo_reqwidth()//2 or 100, 22, text=self.text, fill='white', font=('Segoe UI', 11, 'bold'), tags='text')

    def on_enter(self, e):
        self.hover = True
        self.draw()
        self.config(cursor='hand2')

    def on_leave(self, e):
        self.hover = False
        self.draw()


class ParkingGUI:
    """Clase principal de la interfaz gráfica.

    La GUI solo usa la API pública de `Aparcamiento`.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Parking Manager Pro")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORS['bg_primary'])

        # Crear el dominio (aparcamiento)
        self.aparcamiento = Aparcamiento(2, 4, 5)
        # Precargar matrículas de ejemplo (no muestra diálogos)
        self._preload_matriculas()

        # Estilo para widgets ttk
        style = ttk.Style()
        style.theme_use('clam')

        # Frame principal con padding
        main_frame = tk.Frame(root, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Construir UI
        self.crear_header(main_frame)
        self.crear_stats(main_frame)
        self.crear_panel_acciones(main_frame)
        self.crear_lista_vehiculos(main_frame)

    # --- Métodos de creación de UI (cada uno crea un bloque visible) ---
    def crear_header(self, parent):
        header = tk.Frame(parent, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 25))

        title = tk.Label(header, text="🚗 PARKING MANAGER PRO", font=('Segoe UI', 28, 'bold'), bg=COLORS['bg_primary'], fg=COLORS['text_primary'])
        title.pack(side=tk.LEFT)

        subtitle = tk.Label(header, text="Sistema de gestión inteligente", font=('Segoe UI', 11), bg=COLORS['bg_primary'], fg=COLORS['text_secondary'])
        subtitle.pack(side=tk.LEFT, padx=(15, 0), pady=(8, 0))

    def crear_stats(self, parent):
        stats_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        stats_frame.pack(fill=tk.X, pady=(0, 25))

        # Tarjetas de estadísticas (libres / ocupadas / total)
        self.card_libres = self.crear_stat_card(stats_frame, "Plazas libres", COLORS['success'], 0)
        self.card_libres.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.card_ocupadas = self.crear_stat_card(stats_frame, "Plazas ocupadas", COLORS['accent'], 1)
        self.card_ocupadas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.card_total = self.crear_stat_card(stats_frame, "Capacidad total", COLORS['warning'], 2)
        self.card_total.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.actualizar_stats()

    def crear_stat_card(self, parent, titulo, color, idx):
        card = tk.Frame(parent, bg=COLORS['bg_card'], relief=tk.FLAT, bd=0)
        top_line = tk.Frame(card, bg=color, height=4)
        top_line.pack(fill=tk.X)

        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        label = tk.Label(content, text=titulo, font=('Segoe UI', 11), bg=COLORS['bg_card'], fg=COLORS['text_secondary'])
        label.pack(anchor=tk.W)

        value = tk.Label(content, text="0", font=('Segoe UI', 32, 'bold'), bg=COLORS['bg_card'], fg=color)
        value.pack(anchor=tk.W)

        if idx == 0:
            self.label_libres = value
        elif idx == 1:
            self.label_ocupadas = value
        else:
            self.label_total = value

        return card

    def crear_panel_acciones(self, parent):
        panel = tk.Frame(parent, bg=COLORS['bg_secondary'], relief=tk.FLAT)
        panel.pack(fill=tk.X, pady=(0, 25))

        inner = tk.Frame(panel, bg=COLORS['bg_secondary'])
        inner.pack(fill=tk.BOTH, padx=25, pady=25)

        tk.Label(inner, text="Acciones", font=('Segoe UI', 13, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(anchor=tk.W, pady=(0, 15))

        entrada_frame = tk.Frame(inner, bg=COLORS['bg_secondary'])
        entrada_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(entrada_frame, text="Registrar entrada", font=('Segoe UI', 10), bg=COLORS['bg_secondary'], fg=COLORS['text_secondary']).grid(row=0, column=0, sticky=tk.W, pady=(0, 8), columnspan=2)

        self.matricula_entry = tk.Entry(entrada_frame, font=('Segoe UI', 12), bg=COLORS['bg_card'], fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'], relief=tk.FLAT, bd=0)
        self.matricula_entry.grid(row=1, column=0, sticky=tk.EW, ipady=10, ipadx=10)
        self.matricula_entry.bind('<Return>', lambda e: self.registrar_entrada())

        # Selector de tipo: etiqueta destacada y combobox pequeño
        self.tipo_var = tk.StringVar(value='comun')
        tipos = ['comun', 'minusvalida', 'electrica', 'resident', 'vip']
        tk.Label(entrada_frame, text="Tipo de matrícula:", font=('Segoe UI', 10, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['accent']).grid(row=2, column=0, sticky=tk.W, pady=(8,0))
        tipo_combo = ttk.Combobox(entrada_frame, textvariable=self.tipo_var, values=tipos, state='readonly', width=14)
        tipo_combo.grid(row=3, column=0, sticky=tk.W, pady=(2,0))

        btn_entrada = ModernButton(entrada_frame, "✓ Aparcar", self.registrar_entrada, COLORS['success'], width=150)
        btn_entrada.grid(row=1, column=1, padx=(15, 0))

        entrada_frame.columnconfigure(0, weight=1)

        tk.Frame(inner, bg=COLORS['border'], height=1).pack(fill=tk.X, pady=20)

        salida_frame = tk.Frame(inner, bg=COLORS['bg_secondary'])
        salida_frame.pack(fill=tk.X)

        tk.Label(salida_frame, text="Registrar salida", font=('Segoe UI', 10), bg=COLORS['bg_secondary'], fg=COLORS['text_secondary']).grid(row=0, column=0, sticky=tk.W, pady=(0, 8), columnspan=2)

        self.salida_entry = tk.Entry(salida_frame, font=('Segoe UI', 12), bg=COLORS['bg_card'], fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'], relief=tk.FLAT, bd=0)
        self.salida_entry.grid(row=1, column=0, sticky=tk.EW, ipady=10, ipadx=10)
        self.salida_entry.bind('<Return>', lambda e: self.registrar_salida())

        btn_salida = ModernButton(salida_frame, "💳 Cobrar", self.registrar_salida, COLORS['accent'], width=150)
        btn_salida.grid(row=1, column=1, padx=(15, 0))

        salida_frame.columnconfigure(0, weight=1)

    def crear_lista_vehiculos(self, parent):
        list_container = tk.Frame(parent, bg=COLORS['bg_secondary'])
        list_container.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(list_container, bg=COLORS['bg_secondary'])
        header.pack(fill=tk.X, padx=25, pady=(20, 10))

        tk.Label(header, text="Vehículos en el parking", font=('Segoe UI', 13, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)

        list_frame = tk.Frame(list_container, bg=COLORS['bg_secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))

        scrollbar = tk.Scrollbar(list_frame, bg=COLORS['bg_card'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox con altura fija y soporte de scroll
        self.coches_listbox = tk.Listbox(list_frame, font=('TkFixedFont', 10), bg=COLORS['bg_card'], fg=COLORS['text_primary'], selectbackground=COLORS['accent'], selectforeground='white', relief=tk.FLAT, bd=0, yscrollcommand=scrollbar.set, highlightthickness=0, height=15)
        self.coches_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.coches_listbox.yview)

        # Inicializar lista y comportamiento de scroll
        self.actualizar_lista()
        self.coches_listbox.bind('<MouseWheel>', lambda e: self.coches_listbox.yview_scroll(int(-1*(e.delta/120)), 'units'))
        self.tipo_var.set('comun')

    def actualizar_stats(self):
        """Actualizar valores visibles de las tarjetas de estado."""
        resumen = self.aparcamiento.resumen()
        self.label_libres.config(text=str(resumen['libres']))
        self.label_ocupadas.config(text=str(resumen['ocupadas']))
        self.label_total.config(text=str(resumen['total']))

    def registrar_entrada(self):
        """Leer datos de la UI y pedir al dominio que registre una entrada."""
        matricula = self.matricula_entry.get().strip()
        tipo = self.tipo_var.get() if hasattr(self, 'tipo_var') else 'comun'
        if not matricula:
            messagebox.showwarning("Advertencia", "Por favor, introduce la matrícula.", parent=self.root)
            return

        ok, msg = self.aparcamiento.entrar(matricula, tipo=tipo)
        if ok:
            messagebox.showinfo("Entrada registrada", msg, parent=self.root)
            self.matricula_entry.delete(0, tk.END)
            # Restablecer tipo por defecto a 'comun' tras crear la matrícula
            self.tipo_var.set('comun')
            self.actualizar_stats()
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    def registrar_salida(self):
        """Solicitar al dominio que procese una salida por matrícula."""
        matricula = self.salida_entry.get().strip().upper()
        if not matricula:
            messagebox.showwarning("Advertencia", "Por favor, introduce una matrícula", parent=self.root)
            return
        ok, msg = self.aparcamiento.salir(matricula)
        if ok:
            messagebox.showinfo("Pago procesado", msg, parent=self.root)
            self.salida_entry.delete(0, tk.END)
            self.actualizar_stats()
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    def actualizar_lista(self):
        """Refrescar la lista visual con la información que devuelve `Aparcamiento`."""
        self.coches_listbox.delete(0, tk.END)
        coches = self.aparcamiento.listar_coches()
        if coches:
            for item in coches:
                self.coches_listbox.insert(tk.END, item)
        else:
            self.coches_listbox.insert(tk.END, "No hay vehículos en el parking")

    def _preload_matriculas(self):
        """Precargar algunas matrículas de ejemplo usando la API del dominio.

        Implementado para facilitar pruebas manuales al iniciar la GUI.
        """
        try:
            precarga = [
                ("1234ABC", "comun"),
                ("0000MV", "minusvalida"),
                ("E-1234", "electrica"),
                ("RES-56", "resident"),
                ("VIP1", "vip"),
            ]
            for m, t in precarga:
                self.aparcamiento.entrar(m, tipo=t)
        except Exception:
            # No interrumpir la inicialización por fallos de precarga
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()