"""
s17_pedidos.py

Sistema sencillo de gestión de pedidos para una tienda de videojuegos.
Contiene tres clases: Game, Store y Order.

El código es sencillo y comentado para estudiantes principiantes.
"""

from typing import Dict


class Game:
    """Representa un videojuego."""

    def __init__(self, title: str, price: float, description: str, stores=None):
        # Atributos privados para forzar encapsulación
        self._title = title
        self._price = float(price)
        self._description = description
        # lista de nombres de tiendas donde está disponible
        self._stores = list(stores) if stores else []

    def get_title(self) -> str:
        return self._title

    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return self._description

    def is_available_in(self, store_name: str) -> bool:
        """Comprueba si el juego está disponible en una tienda dada."""
        return store_name in self._stores

    def add_store(self, store_name: str):
        """Añade una tienda a la lista de disponibilidad."""
        if store_name not in self._stores:
            self._stores.append(store_name)

    def __str__(self):
        return f"{self._title} - {self._price:.2f}€"


class Store:
    """Representa una tienda que tiene un inventario de videojuegos."""

    def __init__(self, name: str):
        self._name = name
        # inventario: título -> (Game, stock)
        self._inventory: Dict[str, tuple] = {}

    def get_name(self) -> str:
        return self._name

    def add_game(self, game: Game, stock: int = 1):
        """Añade un juego al inventario o incrementa su stock."""
        if stock <= 0:
            raise ValueError("El stock debe ser positivo")
        title = game.get_title()
        if title in self._inventory:
            _, current = self._inventory[title]
            self._inventory[title] = (game, current + stock)
        else:
            game.add_store(self._name)
            self._inventory[title] = (game, stock)

    def is_available(self, game_title: str) -> bool:
        """Devuelve True si el juego está en inventario y hay stock."""
        return game_title in self._inventory and self._inventory[game_title][1] > 0

    def list_games(self):
        """Devuelve una lista simple con títulos y stock."""
        return [(title, data[1]) for title, data in self._inventory.items()]


class Order:
    """Representa un pedido que contiene juegos y tiene un estado.

    Reglas importantes:
    - Un pedido solo puede pagarse una vez.
    - Un pedido no puede enviarse si no está pagado.
    - El importe total no puede ser negativo.
    """

    CREATED = 'CREATED'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    CANCELLED = 'CANCELLED'

    def __init__(self):
        # items: título -> (Game, cantidad)
        self._items: Dict[str, tuple] = {}
        self._state = Order.CREATED
        self._total = 0.0

    def _recalculate_total(self):
        total = 0.0
        for _, (game, qty) in self._items.items():
            total += game.get_price() * qty
        if total < 0:
            raise ValueError("El total del pedido no puede ser negativo")
        self._total = total

    def add_item(self, game: Game, quantity: int = 1):
        """Añade una cantidad de un juego al pedido.

        No se puede modificar directamente desde fuera; usar este método.
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")
        title = game.get_title()
        if title in self._items:
            _, current = self._items[title]
            self._items[title] = (game, current + quantity)
        else:
            self._items[title] = (game, quantity)
        self._recalculate_total()

    def remove_item(self, game_title: str, quantity: int = 1):
        """Quita una cantidad de un juego del pedido."""
        if game_title not in self._items:
            raise KeyError("El juego no está en el pedido")
        game, current = self._items[game_title]
        if quantity <= 0 or quantity > current:
            raise ValueError("Cantidad inválida")
        if quantity == current:
            del self._items[game_title]
        else:
            self._items[game_title] = (game, current - quantity)
        self._recalculate_total()

    def pay(self):
        """Realiza el pago del pedido. Solo si está en estado CREATED y total > 0."""
        if self._state == Order.PAID:
            raise RuntimeError("El pedido ya está pagado")
        if self._state != Order.CREATED:
            raise RuntimeError("Solo se puede pagar un pedido recién creado")
        if self._total <= 0:
            raise ValueError("El pedido no tiene importe válido para pagar")
        self._state = Order.PAID

    def ship(self):
        """Envía el pedido. Solo si ya está pagado."""
        if self._state != Order.PAID:
            raise RuntimeError("No se puede enviar un pedido que no está pagado")
        self._state = Order.SHIPPED

    def cancel(self):
        """Cancela el pedido: se puede cancelar si no está enviado."""
        if self._state == Order.SHIPPED:
            raise RuntimeError("No se puede cancelar un pedido ya enviado")
        self._state = Order.CANCELLED

    def get_total(self) -> float:
        return self._total

    def get_state(self) -> str:
        return self._state

    def list_items(self):
        """Devuelve una copia simple de los items: (título, cantidad)."""
        return [(title, qty) for title, (game, qty) in self._items.items()]


import tkinter as tk
from tkinter import messagebox


def _create_sample_store():
    """Crea una tienda y algunos juegos de ejemplo."""
    g1 = Game('Aventura Épica', 39.99, 'Un juego de aventuras y exploración', stores=['Central'])
    g2 = Game('Carreras Rápidas', 29.50, 'Juego de carreras con muchos coches')
    g3 = Game('Puzzle Lógico', 9.99, 'Rompecabezas para pensar')

    tienda = Store('Central')
    tienda.add_game(g1, stock=5)
    tienda.add_game(g2, stock=2)
    tienda.add_game(g3, stock=10)
    return tienda


def start_gui():
    """Interfaz gráfica simple para usar el sistema.

    Permite añadir juegos al pedido, ver el pedido, pagar, enviar y cancelar.
    El objetivo es mantenerlo muy sencillo y entendible para principiantes.
    """
    tienda = _create_sample_store()
    pedido = Order()

    root = tk.Tk()
    root.title('Tienda de Videojuegos - Pedidos (S17)')

    # Lista de juegos en la tienda
    lbl_store = tk.Label(root, text='Inventario (tienda Central)')
    lbl_store.grid(row=0, column=0, padx=5, pady=5)
    lb_store = tk.Listbox(root, height=8, width=40)
    lb_store.grid(row=1, column=0, padx=5, pady=5)

    for title, stock in tienda.list_games():
        lb_store.insert(tk.END, f"{title} (stock: {stock})")

    # Cantidad a añadir
    lbl_qty = tk.Label(root, text='Cantidad')
    lbl_qty.grid(row=2, column=0, sticky='w', padx=5)
    qty_var = tk.StringVar(value='1')
    ent_qty = tk.Entry(root, textvariable=qty_var, width=5)
    ent_qty.grid(row=2, column=0, sticky='e', padx=5)

    # Lista de items del pedido
    lbl_order = tk.Label(root, text='Pedido (items)')
    lbl_order.grid(row=0, column=1, padx=5, pady=5)
    lb_order = tk.Listbox(root, height=8, width=40)
    lb_order.grid(row=1, column=1, padx=5, pady=5)

    lbl_total = tk.Label(root, text='Total: 0.00€')
    lbl_total.grid(row=2, column=1, padx=5, pady=5)

    def refresh_order_view():
        lb_order.delete(0, tk.END)
        for title, qty in pedido.list_items():
            lb_order.insert(tk.END, f"{title} x{qty}")
        lbl_total.config(text=f"Total: {pedido.get_total():.2f}€")

    def add_selected():
        sel = lb_store.curselection()
        if not sel:
            messagebox.showinfo('Información', 'Seleccione un juego del inventario')
            return
        idx = sel[0]
        entry = lb_store.get(idx)
        title = entry.split(' (stock:')[0]
        # buscar objeto Game en inventario
        game, stock = tienda._inventory[title]
        try:
            qty = int(qty_var.get())
        except ValueError:
            messagebox.showerror('Error', 'Cantidad inválida')
            return
        if qty <= 0:
            messagebox.showerror('Error', 'La cantidad debe ser positiva')
            return
        if stock < qty:
            messagebox.showerror('Error', 'No hay suficiente stock en la tienda')
            return
        # Añadimos al pedido (la tienda no descuenta stock en este ejemplo simplificado)
        pedido.add_item(game, qty)
        refresh_order_view()

    def remove_selected():
        sel = lb_order.curselection()
        if not sel:
            messagebox.showinfo('Información', 'Seleccione un item del pedido')
            return
        idx = sel[0]
        entry = lb_order.get(idx)
        title = entry.split(' x')[0]
        # quitar una unidad para simplificar
        try:
            pedido.remove_item(title, 1)
        except Exception as e:
            messagebox.showerror('Error', str(e))
        refresh_order_view()

    def do_pay():
        try:
            pedido.pay()
            messagebox.showinfo('Pago', 'Pedido pagado correctamente')
        except Exception as e:
            messagebox.showerror('Error al pagar', str(e))
        refresh_order_view()

    def do_ship():
        try:
            pedido.ship()
            messagebox.showinfo('Envío', 'Pedido enviado')
        except Exception as e:
            messagebox.showerror('Error al enviar', str(e))
        refresh_order_view()

    def do_cancel():
        try:
            pedido.cancel()
            messagebox.showinfo('Cancelado', 'Pedido cancelado')
        except Exception as e:
            messagebox.showerror('Error', str(e))
        refresh_order_view()

    # Botones
    btn_add = tk.Button(root, text='Añadir al pedido', command=add_selected)
    btn_add.grid(row=3, column=0, padx=5, pady=3)

    btn_remove = tk.Button(root, text='Quitar del pedido (1)', command=remove_selected)
    btn_remove.grid(row=3, column=1, padx=5, pady=3)

    btn_pay = tk.Button(root, text='Pagar', command=do_pay)
    btn_pay.grid(row=4, column=0, padx=5, pady=3)

    btn_ship = tk.Button(root, text='Enviar', command=do_ship)
    btn_ship.grid(row=4, column=1, padx=5, pady=3)

    btn_cancel = tk.Button(root, text='Cancelar', command=do_cancel)
    btn_cancel.grid(row=5, column=0, columnspan=2, pady=6)

    root.mainloop()


if __name__ == '__main__':
    # Iniciar la interfaz gráfica cuando se ejecute el script
    start_gui()
