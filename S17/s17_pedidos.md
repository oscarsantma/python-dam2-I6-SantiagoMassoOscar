# Sistema de gestión de pedidos online

## Descripción del sistema
Este sistema modela de forma sencilla la gestión de pedidos online.
Un pedido puede contener varios productos, tiene un estado y un importe total.
El sistema evita estados inválidos como pagar dos veces o enviar un pedido no pagado.

## Clases del sistema

### Producto
Representa un producto que se puede vender.

**Responsabilidades:**
- Guardar nombre y precio del producto.

**Estado que protege:**
- El precio no puede ser negativo.

---

### EstadoPedido
Representa los posibles estados de un pedido.

**Responsabilidades:**
- Definir estados válidos del pedido (CREADO, PAGADO, ENVIADO).

**Estado que protege:**
- Evita estados inválidos.

---

### Pedido
Representa un pedido realizado por un cliente.

**Responsabilidades:**
- Agregar productos
- Calcular el importe total
- Cambiar de estado de forma controlada (pagar, enviar)

**Estado que protege:**
- No permite pagar dos veces
- No permite enviar si no está pagado
- No permite importe negativo
