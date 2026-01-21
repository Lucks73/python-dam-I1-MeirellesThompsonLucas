import tkinter as tk
from tkinter import ttk, messagebox
from Coche import Coche
from Aparcamiento import Aparcamiento

# Realizador por: 
#Gonzalo Fernández de Córdova Orta
#Juan Carlos Sanmiguel Carmona
#Daniel Ramos Jimeznez
#Ana Padilla González
#Anaís González Ortiz
#Lucas Meirelles Thompson

# Colores tema oscuro
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
    def __init__(self, parent, text, command, color, **kwargs):
        super().__init__(parent, height=45, bg=COLORS['bg_card'], 
                        highlightthickness=0, **kwargs)
        self.command = command
        self.color = color
        self.text = text
        self.hover = False
        
        self.bind('<Button-1>', lambda e: self.command())
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
        self.draw()
    
    def draw(self):
        self.delete('all')
        color = self.color if not self.hover else COLORS['accent_hover']
        
        # Botón con bordes redondeados
        self.create_rectangle(5, 5, self.winfo_reqwidth()-5 or 200, 40,
                            fill=color, outline='', tags='button')
        self.create_text(self.winfo_reqwidth()//2 or 100, 22,
                        text=self.text, fill='white', 
                        font=('Segoe UI', 11, 'bold'), tags='text')
    
    def on_enter(self, e):
        self.hover = True
        self.draw()
        self.config(cursor='hand2')
    
    def on_leave(self, e):
        self.hover = False
        self.draw()


class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Manager Pro")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Crear aparcamiento (2 plantas, 4 filas, 5 columnas)
        self.aparcamiento = Aparcamiento(2, 4, 5)
        
        # Estilo para widgets ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal con padding
        main_frame = tk.Frame(root, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        self.crear_header(main_frame)
        
        # Stats cards
        self.crear_stats(main_frame)
        
        # Panel de acciones
        self.crear_panel_acciones(main_frame)
        
        # Lista de vehículos
        self.crear_lista_vehiculos(main_frame)
        
    def crear_header(self, parent):
        header = tk.Frame(parent, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 25))
        
        # Título
        title = tk.Label(header, text="🚗 PARKING MANAGER PRO", 
                        font=('Segoe UI', 28, 'bold'),
                        bg=COLORS['bg_primary'], fg=COLORS['text_primary'])
        title.pack(side=tk.LEFT)
        
        # Subtítulo
        subtitle = tk.Label(header, text="Sistema de gestión inteligente",
                           font=('Segoe UI', 11),
                           bg=COLORS['bg_primary'], fg=COLORS['text_secondary'])
        subtitle.pack(side=tk.LEFT, padx=(15, 0), pady=(8, 0))
    
    def crear_stats(self, parent):
        stats_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        stats_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Crear 3 cards de estadísticas
        self.card_libres = self.crear_stat_card(stats_frame, "Plazas Libres", 
                                                COLORS['success'], 0)
        self.card_libres.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.card_ocupadas = self.crear_stat_card(stats_frame, "Ocupadas", 
                                                  COLORS['accent'], 1)
        self.card_ocupadas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.card_total = self.crear_stat_card(stats_frame, "Capacidad Total", 
                                              COLORS['warning'], 2)
        self.card_total.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.actualizar_stats()
    
    def crear_stat_card(self, parent, titulo, color, idx):
        card = tk.Frame(parent, bg=COLORS['bg_card'], relief=tk.FLAT, bd=0)
        
        # Línea superior de color
        top_line = tk.Frame(card, bg=color, height=4)
        top_line.pack(fill=tk.X)
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        label = tk.Label(content, text=titulo, font=('Segoe UI', 11),
                        bg=COLORS['bg_card'], fg=COLORS['text_secondary'])
        label.pack(anchor=tk.W)
        
        value = tk.Label(content, text="0", font=('Segoe UI', 32, 'bold'),
                        bg=COLORS['bg_card'], fg=color)
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
        
        # Padding interno
        inner = tk.Frame(panel, bg=COLORS['bg_secondary'])
        inner.pack(fill=tk.BOTH, padx=25, pady=25)
        
        # Título del panel
        tk.Label(inner, text="ACCIONES", font=('Segoe UI', 13, 'bold'),
                bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(anchor=tk.W, pady=(0, 15))
        
        # Frame para entrada
        entrada_frame = tk.Frame(inner, bg=COLORS['bg_secondary'])
        entrada_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(entrada_frame, text="Registrar Entrada", font=('Segoe UI', 10),
                bg=COLORS['bg_secondary'], fg=COLORS['text_secondary']).grid(
                row=0, column=0, sticky=tk.W, pady=(0, 8), columnspan=2)
        
        self.matricula_entry = tk.Entry(entrada_frame, font=('Segoe UI', 12),
                                        bg=COLORS['bg_card'], fg=COLORS['text_primary'],
                                        insertbackground=COLORS['text_primary'],
                                        relief=tk.FLAT, bd=0)
        self.matricula_entry.grid(row=1, column=0, sticky=tk.EW, ipady=10, ipadx=10)
        self.matricula_entry.bind('<Return>', lambda e: self.registrar_entrada())
        
        btn_entrada = ModernButton(entrada_frame, "✓ Aparcar", 
                                  self.registrar_entrada, COLORS['success'], width=150)
        btn_entrada.grid(row=1, column=1, padx=(15, 0))
        
        entrada_frame.columnconfigure(0, weight=1)
        
        # Separador
        tk.Frame(inner, bg=COLORS['border'], height=1).pack(fill=tk.X, pady=20)
        
        # Frame para salida
        salida_frame = tk.Frame(inner, bg=COLORS['bg_secondary'])
        salida_frame.pack(fill=tk.X)
        
        tk.Label(salida_frame, text="Registrar Salida", font=('Segoe UI', 10),
                bg=COLORS['bg_secondary'], fg=COLORS['text_secondary']).grid(
                row=0, column=0, sticky=tk.W, pady=(0, 8), columnspan=2)
        
        self.salida_entry = tk.Entry(salida_frame, font=('Segoe UI', 12),
                                     bg=COLORS['bg_card'], fg=COLORS['text_primary'],
                                     insertbackground=COLORS['text_primary'],
                                     relief=tk.FLAT, bd=0)
        self.salida_entry.grid(row=1, column=0, sticky=tk.EW, ipady=10, ipadx=10)
        self.salida_entry.bind('<Return>', lambda e: self.registrar_salida())
        
        btn_salida = ModernButton(salida_frame, "💳 Cobrar", 
                                 self.registrar_salida, COLORS['accent'], width=150)
        btn_salida.grid(row=1, column=1, padx=(15, 0))
        
        salida_frame.columnconfigure(0, weight=1)
    
    def crear_lista_vehiculos(self, parent):
        list_container = tk.Frame(parent, bg=COLORS['bg_secondary'])
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Header de la lista
        header = tk.Frame(list_container, bg=COLORS['bg_secondary'])
        header.pack(fill=tk.X, padx=25, pady=(20, 10))
        
        tk.Label(header, text="VEHÍCULOS EN PARKING", font=('Segoe UI', 13, 'bold'),
                bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)
        
        # Lista con scrollbar
        list_frame = tk.Frame(list_container, bg=COLORS['bg_secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(list_frame, bg=COLORS['bg_card'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.coches_listbox = tk.Listbox(list_frame, font=('TkFixedFont', 10),
                                         bg=COLORS['bg_card'], fg=COLORS['text_primary'],
                                         selectbackground=COLORS['accent'],
                                         selectforeground='white',
                                         relief=tk.FLAT, bd=0,
                                         yscrollcommand=scrollbar.set,
                                         highlightthickness=0)
        self.coches_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.coches_listbox.yview)
        
        # Función para mostrar solo las matrículas de los objetos Coche
        def mostrar_matriculas():
            self.coches_listbox.delete(0, tk.END)
            cualquier = False
            for p in range(self.aparcamiento.plantas):
                for f in range(self.aparcamiento.filas):
                    for c in range(self.aparcamiento.columnas):
                        coche = self.aparcamiento.plazas[p][f][c]
                        if coche:
                            self.coches_listbox.insert(tk.END, coche.matricula)
                            cualquier = True
            if not cualquier:
                self.coches_listbox.insert(tk.END, "No hay vehículos en el parking")
        
        # Reemplaza la versión por defecto para que todas las actualizaciones muestren solo matrículas
        self.actualizar_lista = mostrar_matriculas
        mostrar_matriculas()
    
    def actualizar_stats(self):
        total = self.aparcamiento.plantas * self.aparcamiento.filas * self.aparcamiento.columnas
        ocupadas = total - self.aparcamiento.plazas_libres
        
        self.label_libres.config(text=str(self.aparcamiento.plazas_libres))
        self.label_ocupadas.config(text=str(ocupadas))
        self.label_total.config(text=str(total))
    
    def registrar_entrada(self):
        matricula = self.matricula_entry.get().strip()
        coche = Coche(matricula)
        if not matricula:
            messagebox.showwarning("Advertencia", "Por favor, introduce una matrícula",
                                  parent=self.root)
            return
        if self.aparcamiento.hay_plazas_libres or self.aparcamiento.plazas_libres > 0:
            messagebox.showinfo("Entrada Registrada", 
                              f"✓ Vehículo {coche.matricula} aparcado correctamente",
                              parent=self.root)
            self.matricula_entry.delete(0, tk.END)
            self.aparcamiento.llenar_plaza(coche)
            self.actualizar_stats()
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", "No hay plazas libres disponibles",
                               parent=self.root)
        
        
        
    
    def registrar_salida(self):
        matricula = self.salida_entry.get().strip().upper()
        
        if not matricula:
            messagebox.showwarning("Advertencia", "Por favor, introduce una matrícula",
                                  parent=self.root)
            return
        
        coche_encontrado = None
        for p in range(self.aparcamiento.plantas):
            for f in range(self.aparcamiento.filas):
                for c in range(self.aparcamiento.columnas):
                    coche = self.aparcamiento.plazas[p][f][c]
                    if coche and coche.matricula == matricula:
                        coche_encontrado = coche
                        break
        
        if coche_encontrado:
            mensaje = self.aparcamiento.vaciar_plaza(coche_encontrado)
            messagebox.showinfo("Pago Procesado", mensaje, parent=self.root)
            self.salida_entry.delete(0, tk.END)
            self.actualizar_stats()
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", 
                               f"Vehículo {matricula} no encontrado en el parking",
                               parent=self.root)
    
    def actualizar_lista(self):
        self.coches_listbox.delete(0, tk.END)
        
        coches = []
        for p in range(self.aparcamiento.plantas):
            for f in range(self.aparcamiento.filas):
                for c in range(self.aparcamiento.columnas):
                    coche = self.aparcamiento.plazas[p][f][c]
                    if coche:
                        entrada = coche.hora_entrada.strftime("%H:%M:%S")
                        coches.append(f"[P{p+1}-F{f+1}-C{c+1}]  {coche.matricula:<12} → Entrada: {entrada}")
        
        if coches:
            for item in coches:
                self.coches_listbox.insert(tk.END, item)
        else:
            self.coches_listbox.insert(tk.END, " ")
            self.coches_listbox.insert(tk.END, "    No hay vehículos en el parking")
            self.coches_listbox.insert(tk.END, " ")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()