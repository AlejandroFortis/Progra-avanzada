class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Cliente(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.historial_pedidos = []
        self.puntos_fidelidad = 0

    def realizar_pedido(self, pedido, inventario, promocion=None):
        if pedido.verificar_disponibilidad(inventario):
            if promocion and self.puntos_fidelidad >= 50:
                promocion.aplicar_descuento(pedido)
            self.historial_pedidos.append(pedido)
            self.puntos_fidelidad += 10
            pedido.actualizar_stock(inventario)
            pedido.actualizar_estado("En preparación")
            print("-----------------------------------------------------------")
            print("Productos:")
            for producto in pedido.productos:
                print(f"- {producto.nombre}: ${producto.precio}")
            print(f"Total con descuento: ${pedido.calcular_total()}")
            print("-----------------------------------------------------------")
        else:
            print("-----------------------------------------------------------")
            print("No hay suficiente stock para realizar el pedido.")
            print("-----------------------------------------------------------")

    def consultar_historial(self):
        print("-----------------------------------------------------------")
        print(f"Historial pedidos de {self.nombre}")
        print("-----------------------------------------------------------")
        for pedido in self.historial_pedidos:
            print(f"Pedido con total: ${pedido.calcular_total()} - Estado: {pedido.estado}")
            print("-----------------------------------------------------------")

class Empleado(Persona):
    def __init__(self, nombre, rol):
        super().__init__(nombre)
        self.rol = rol

    def actualizar_inventario(self, inventario, ingrediente, cantidad):
        inventario.agregar_ingrediente(ingrediente, cantidad) 
        print("-----------------------------------------------------------")       
        print(f"Se han añadido {cantidad} unidades de {ingrediente}") 
        print("-----------------------------------------------------------")

class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = {}

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamaño, tipo, personalizacion={}):
        super().__init__(nombre, precio)
        self.tamaño = tamaño
        self.tipo = tipo
        self.personalizacion = personalizacion
        self.ingredientes = {"Agua": 1}
        self.ingredientes.update(personalizacion)

    def descripcion(self):
        print("-----------------------------------------------------------")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio}")
        print(f"Tamaño: {self.tamaño}")
        print("Ingredientes:")
        for ingrediente in self.ingredientes:
            print(f"- {ingrediente}")
        print("-----------------------------------------------------------")

class Postre(ProductoBase):
    def __init__(self, nombre, precio, personalizacion={}, vegano=False, sin_gluten=False):
        super().__init__(nombre, precio)
        self.vegano = vegano
        self.sin_gluten = sin_gluten
        self.personalizacion = personalizacion
        self.ingredientes = {"Harina": 1}
        self.ingredientes.update(personalizacion)

    def descripcion(self):
        print("-----------------------------------------------------------")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio}")
        print(f"Vegano: {'Si' if self.vegano else 'No'}")
        print(f"Sin gluten: {'Si' if self.sin_gluten else 'No'}")
        print("Ingredientes:")
        for ingrediente in self.ingredientes:
            print(f"- {ingrediente}")
        print("-----------------------------------------------------------")

class Inventario:
    def __init__(self):
        self.stock = {}
    
    def agregar_ingrediente(self, ingrediente, cantidad):
        self.stock[ingrediente] = self.stock.get(ingrediente, 0) + cantidad

    def verificar_disponibilidad(self, ingredientes):
        faltantes = [ing for ing, cantidad in ingredientes.items() if self.stock.get(ing, 0) < cantidad]
        if faltantes:
            print("-----------------------------------------------------------")
            print(f"Faltan ingredientes: {', '.join(faltantes)}")
            print("-----------------------------------------------------------")
            return False
        return True

    def actualizar_stock(self, ingredientes):
        for ing, cantidad in ingredientes.items():
            if ing in self.stock:
                self.stock[ing] -= cantidad

    def consultar_inventario(self):
        print("-----------------------------------------------------------")
        print("Inventario actual:")
        for ing, cantidad in self.stock.items():
            print(f"- {ing}: {cantidad} unidades")
        print("-----------------------------------------------------------")


class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
        self.estado = "Pendiente"
        self.total = 0
        print("-----------------------------------------------------------")
        print(f"Se ha añadido un nuevo pedido para {self.cliente.nombre}")
        print("-----------------------------------------------------------")


    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.total += producto.precio
        print("-----------------------------------------------------------")
        print(f"Se ha añadido {producto.nombre} con costo de ${producto.precio} al pedido de {self.cliente.nombre}")
        print("-----------------------------------------------------------")

    def calcular_total(self):
        return self.total

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print("-----------------------------------------------------------")
        print(f"Nuevo estado del pedido: {self.estado}")
        print("-----------------------------------------------------------")

    def verificar_disponibilidad(self, inventario):
        return all(inventario.verificar_disponibilidad(prod.ingredientes) for prod in self.productos)

    def actualizar_stock(self, inventario):
        for prod in self.productos:
            inventario.actualizar_stock(prod.ingredientes)

class Promocion:
    def __init__(self, descripcion, descuento):
        self.descripcion = descripcion
        self.descuento = descuento
    
    def aplicar_descuento(self, pedido):
        pedido.total *= (1 - self.descuento / 100)


inventario = Inventario()
inventario.agregar_ingrediente("Café", 20)
inventario.agregar_ingrediente("Agua", 20)
inventario.agregar_ingrediente("Leche de almendra", 20)
inventario.agregar_ingrediente("Leche deslactosada", 20)
inventario.agregar_ingrediente("Leche entera", 20)
inventario.agregar_ingrediente("Azúcar", 20)
inventario.agregar_ingrediente("Chocolate", 20)
inventario.agregar_ingrediente("Harina", 20)
inventario.agregar_ingrediente("Fruta", 20)
inventario.agregar_ingrediente("Limon", 20)
inventario.consultar_inventario()