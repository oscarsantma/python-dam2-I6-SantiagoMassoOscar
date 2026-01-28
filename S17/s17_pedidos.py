# --------------------
# Clase Producto
# --------------------
class Producto:
    def __init__(self, nombre, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.__nombre = nombre
        self.__precio = precio

    def get_precio(self):
        return self.__precio

    def get_nombre(self):
        return self.__nombre


# --------------------
# Clase EstadoPedido
# --------------------
class EstadoPedido:
    CREADO = "creado"
    PAGADO = "pagado"
    ENVIADO = "enviado"


# --------------------
# Clase Pedido
# --------------------
class Pedido:
    def __init__(self):
        self.__productos = []
        self.__estado = EstadoPedido.CREADO

    def agregar_producto(self, producto):
        if self.__estado != EstadoPedido.CREADO:
            print("No se pueden agregar productos después de pagar")
            return
        self.__productos.append(producto)

    def calcular_total(self):
        total = 0
        for producto in self.__productos:
            total += producto.get_precio()
        return total

    def pagar(self):
        if self.__estado == EstadoPedido.PAGADO:
            print("El pedido ya está pagado")
            return
        if self.calcular_total() <= 0:
            print("No se puede pagar un pedido con importe 0")
            return
        self.__estado = EstadoPedido.PAGADO
        print("Pedido pagado correctamente")

    def enviar(self):
        if self.__estado != EstadoPedido.PAGADO:
            print("El pedido debe estar pagado para enviarse")
            return
        self.__estado = EstadoPedido.ENVIADO
        print("Pedido enviado")

    def mostrar_estado(self):
        print("Estado del pedido:", self.__estado)

    def mostrar_total(self):
        print("Importe total:", self.calcular_total())


# --------------------
# MAIN
# --------------------
if __name__ == "__main__":
    producto1 = Producto("Teclado", 50)
    producto2 = Producto("Mouse", 30)

    pedido = Pedido()
    pedido.agregar_producto(producto1)
    pedido.agregar_producto(producto2)

    pedido.mostrar_total()
    pedido.mostrar_estado()

    pedido.pagar()
    pedido.enviar()
    pedido.mostrar_estado()
