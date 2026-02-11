"""
Interfaz gráfica para el Gestor de Incidencias.

Este módulo usa `incidencias.py` en su totalidad sin modificarlo. Ofrece una
interfaz agradable con `tkinter` para crear, listar y cambiar el estado de
incidencias.

Ejecutar: `python S18/gui.py`
"""

import sys
import os
from tkinter import Tk, Toplevel, Text, END, LEFT, RIGHT, Y, BOTH, VERTICAL
from tkinter import StringVar
from tkinter import messagebox
from tkinter import Listbox
from tkinter import W
from tkinter import NW
from tkinter import X
from tkinter import TOP
from tkinter import BOTTOM
from tkinter import Button
from tkinter import Scrollbar
from tkinter import VERTICAL as TK_VERTICAL
from tkinter import HORIZONTAL
from tkinter import ttk

# Asegurarnos de que el directorio S18 está en sys.path para poder importar
# el módulo `incidencias` sin modificarlo.
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

import incidencias


class IncidenciasGUI:
    """Aplicación GUI que utiliza `incidencias.py` externamente."""

    def __init__(self):
        self.gestor = incidencias.GestorIncidencias()
        self.root = Tk()
        self.root.title('Gestor de Incidencias - GUI')
        self._build_ui()
        self.refresh_list()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=BOTH, expand=True)

        left = ttk.Frame(main)
        left.pack(side=LEFT, fill=BOTH, expand=True)

        right = ttk.Frame(main, width=260)
        right.pack(side=RIGHT, fill=Y)

        # Lista con scroll
        self.listbox = Listbox(left, width=90, height=20)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scroll = ttk.Scrollbar(left, orient=VERTICAL, command=self.listbox.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scroll.set)

        # Botones y acciones
        ttk.Button(right, text='Crear incidencia', command=self.open_create_window).pack(fill=X, pady=4)
        ttk.Button(right, text='Ver detalles', command=self.view_selected).pack(fill=X, pady=4)
        ttk.Button(right, text='Cerrar incidencia', command=lambda: self.change_selected('cerrar')).pack(fill=X, pady=4)
        ttk.Button(right, text='Reabrir incidencia', command=lambda: self.change_selected('abrir')).pack(fill=X, pady=4)
        ttk.Button(right, text='Cargar demo', command=self.load_demo).pack(fill=X, pady=8)
        ttk.Button(right, text='Refrescar', command=self.refresh_list).pack(fill=X, pady=4)
        ttk.Button(right, text='Salir', command=self.root.destroy).pack(fill=X, pady=8)

    def refresh_list(self):
        self.listbox.delete(0, END)
        for line in self.gestor.listar_incidencias():
            self.listbox.insert(END, line)

    def open_create_window(self):
        win = Toplevel(self.root)
        win.title('Crear incidencia')

        ttk.Label(win, text='Tipo:').grid(row=0, column=0, sticky=W, padx=6, pady=6)
        tipo_var = StringVar(value='t')
        tipo_combo = ttk.Combobox(win, textvariable=tipo_var, values=('t', 'a', 'u'), state='readonly', width=20)
        tipo_combo.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(win, text='Descripción:').grid(row=1, column=0, sticky=NW, padx=6, pady=6)
        desc_text = Text(win, height=5, width=40)
        desc_text.grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(win, text='Prioridad:').grid(row=2, column=0, sticky=W, padx=6, pady=6)
        prioridad_var = StringVar(value='media')
        prioridad_combo = ttk.Combobox(win, textvariable=prioridad_var, values=('baja', 'media', 'alta'), state='readonly', width=20)
        prioridad_combo.grid(row=2, column=1, padx=6, pady=6)

        ttk.Label(win, text='Responsable:').grid(row=3, column=0, sticky=W, padx=6, pady=6)
        responsable_entry = ttk.Entry(win, width=30)
        responsable_entry.grid(row=3, column=1, padx=6, pady=6)

        extra_label = ttk.Label(win, text='Equipo/Departamento/Usuario:')
        extra_label.grid(row=4, column=0, sticky=W, padx=6, pady=6)
        extra_entry = ttk.Entry(win, width=30)
        extra_entry.grid(row=4, column=1, padx=6, pady=6)

        def on_tipo(event=None):
            t = tipo_var.get()
            if t == 't':
                extra_label.config(text='Equipo:')
            elif t == 'a':
                extra_label.config(text='Departamento:')
            else:
                extra_label.config(text='Usuario:')

        tipo_combo.bind('<<ComboboxSelected>>', on_tipo)

        def do_create():
            tipo = tipo_var.get()
            descripcion = desc_text.get('1.0', END).strip()
            prioridad = prioridad_var.get()
            responsable = responsable_entry.get().strip() or 'Sin responsable'
            extra = extra_entry.get().strip()

            if not descripcion:
                messagebox.showwarning('Aviso', 'La descripción no puede estar vacía.')
                return

            inc = self.gestor.crear_incidencia(tipo, descripcion, prioridad, responsable, extra)
            messagebox.showinfo('Creada', f'Incidencia creada con id {inc.id}')
            self.refresh_list()
            win.destroy()

        ttk.Button(win, text='Crear', command=do_create).grid(row=5, column=0, columnspan=2, pady=10)

    def get_selected_id(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning('Aviso', 'Seleccione una incidencia de la lista.')
            return None
        line = self.listbox.get(sel[0])
        try:
            id_str = line.split(']')[0].lstrip('[')
            return int(id_str)
        except Exception:
            return None

    def view_selected(self):
        id_sel = self.get_selected_id()
        if id_sel is None:
            return
        inc = self.gestor.obtener_por_id(id_sel)
        if not inc:
            messagebox.showerror('Error', 'Incidencia no encontrada')
            return
        messagebox.showinfo('Detalles', inc.mostrar_info())

    def change_selected(self, accion):
        id_sel = self.get_selected_id()
        if id_sel is None:
            return
        ok, msg = self.gestor.cambiar_estado(id_sel, accion)
        if ok:
            messagebox.showinfo('Hecho', msg)
            self.refresh_list()
        else:
            messagebox.showerror('Error', msg)

    def load_demo(self):
        self.gestor.crear_incidencia('t', 'Pantalla azul al iniciar', 'alta', 'María', extra='PC-01')
        self.gestor.crear_incidencia('a', 'Solicitud de material', 'baja', 'Carlos', extra='Compras')
        self.gestor.crear_incidencia('u', 'No puedo acceder a la app', 'media', 'Ana', extra='ana@example.com')
        self.refresh_list()
        messagebox.showinfo('Demo', 'Se han cargado incidencias de ejemplo.')

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = IncidenciasGUI()
    app.run()
