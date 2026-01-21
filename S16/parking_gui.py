import ttkbootstrap as tb
from tkinter import messagebox
from datetime import datetime, timedelta
import uuid


# =========================
# CLASES DEL DOMINIO
# =========================

class Plaza:
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo        # coche / moto
        self.estado = "libre"   # libre / ocupada

    def ocupar(self):
        self.estado = "ocupada"

    def liberar(self):
        self.estado = "libre"


class Vehiculo:
    def __init__(self, matricula, tipo):
        self.matricula = matricula.upper()
        self.tipo = tipo


class Ticket:
    def __init__(self, vehiculo):
        self.codigo = str(uuid.uuid4())[:8]
        self.vehiculo = vehiculo
        self.hora_entrada = datetime.now()
        self.hora_salida = None

    def cerrar(self):
        self.hora_salida = datetime.now()

    def tiempo_total(self):
        return self.hora_salida - self.hora_entrada


class Parking:
    """
    =========================
    PARTE A — INTERFAZ PÚBLICA
    =========================
    La interfaz gráfica SOLO usa estos métodos
    """

    def __init__(self):
        self.plazas = []
        self.tickets = {}

        # =========================
        # PARTE B — CAMBIO FUTURO
        # Tarifas por tipo de vehículo
        # =========================
        self.tarifas = {
            "coche": 2.50,
            "moto": 1.50
        }

    def agregar_plaza(self, plaza):
        self.plazas.append(plaza)

    # ---------- MÉTODOS PÚBLICOS ----------
    def entrar(self, matricula, tipo):
        vehiculo = Vehiculo(matricula, tipo)

        for plaza in self.plazas:
            if plaza.tipo == tipo and plaza.estado == "libre":
                plaza.ocupar()
                ticket = Ticket(vehiculo)
                self.tickets[ticket.codigo] = (ticket, plaza)
                return ticket.codigo, plaza.numero

        return None

    def salir(self, codigo_ticket):
        if codigo_ticket not in self.tickets:
            return None

        ticket, plaza = self.tickets.pop(codigo_ticket)

        # simulamos tiempo
        ticket.hora_entrada -= timedelta(minutes=90)
        ticket.cerrar()

        tiempo = ticket.tiempo_total()
        horas = tiempo.total_seconds() / 3600
        precio = self.tarifas[ticket.vehiculo.tipo]
        total = round(horas * precio, 2)

        plaza.liberar()

        return {
            "codigo": ticket.codigo,
            "matricula": ticket.vehiculo.matricula,
            "horas": int(horas),
            "minutos": int((horas % 1) * 60),
            "total": total,
            "plaza": plaza.numero
        }

    def resumen(self):
        total = len(self.plazas)
        libres = 0
        ocupadas = 0

        for plaza in self.plazas:
            if plaza.estado == "libre":
                libres += 1
            else:
                ocupadas += 1

        return total, libres, ocupadas

    def listar_plazas(self):
        lista = []
        for plaza in self.plazas:
            lista.append((plaza.numero, plaza.tipo, plaza.estado))
        return lista


# =========================
# INTERFAZ GRÁFICA
# =========================

class ParkingApp(tb.Window):
    def __init__(self, parking):
        super().__init__()
        self.title("Parking")
        self.geometry("650x800")
        self.parking = parking

        self.crear_widgets()
        self.actualizar()

    def crear_widgets(self):
        self.lbl_resumen = tb.Label(self, font=("Arial", 11, "bold"))
        self.lbl_resumen.pack(pady=10)

        self.frame_plazas = tb.Frame(self)
        self.frame_plazas.pack()

        entrada = tb.Labelframe(self, text="Entrada")
        entrada.pack(fill="x", padx=20, pady=10)

        self.entry_matricula = tb.Entry(entrada)
        self.entry_matricula.pack(pady=5)

        self.combo_tipo = tb.Combobox(entrada, values=["coche", "moto"], state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=5)

        tb.Button(entrada, text="Entrar", command=self.entrar).pack(pady=5)

        salida = tb.Labelframe(self, text="Salida")
        salida.pack(fill="x", padx=20, pady=10)

        self.entry_ticket = tb.Entry(salida)
        self.entry_ticket.pack(pady=5)

        tb.Button(salida, text="Salir", command=self.salir).pack(pady=5)

        self.texto = tb.Text(self, height=8, state="disabled")
        self.texto.pack(fill="both", padx=20, pady=10)

    def actualizar(self):
        total, libres, ocupadas = self.parking.resumen()
        self.lbl_resumen.config(
            text=f"Total: {total} | Libres: {libres} | Ocupadas: {ocupadas}"
        )

        for widget in self.frame_plazas.winfo_children():
            widget.destroy()

        for numero, tipo, estado in self.parking.listar_plazas():
            texto = f"P{numero}\n{tipo}\n{estado}"
            tb.Label(self.frame_plazas, text=texto, relief="solid", width=12)\
                .pack(side="left", padx=5, pady=5)

    def entrar(self):
        matricula = self.entry_matricula.get().strip()
        tipo = self.combo_tipo.get()

        if matricula == "":
            messagebox.showwarning("Error", "Introduce matrícula")
            return

        resultado = self.parking.entrar(matricula, tipo)

        if resultado is None:
            messagebox.showerror("Error", "No hay plazas disponibles")
            return

        codigo, plaza = resultado
        self.actualizar()

        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("end", f"Entrada correcta\nPlaza: {plaza}\nTicket: {codigo}")
        self.texto.config(state="disabled")

        self.entry_matricula.delete(0, "end")

    def salir(self):
        codigo = self.entry_ticket.get().strip()
        recibo = self.parking.salir(codigo)

        if recibo is None:
            messagebox.showerror("Error", "Ticket incorrecto")
            return

        self.actualizar()

        texto = (
            f"RECIBO\n"
            f"Ticket: {recibo['codigo']}\n"
            f"Matrícula: {recibo['matricula']}\n"
            f"Tiempo: {recibo['horas']}h {recibo['minutos']}min\n"
            f"Total: {recibo['total']} €\n"
            f"Plaza libre: {recibo['plaza']}"
        )

        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("end", texto)
        self.texto.config(state="disabled")

        self.entry_ticket.delete(0, "end")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    parking = Parking()

    # =========================
    # PARTE B — Tipos de plazas
    # =========================
    for i in range(1, 6):
        parking.agregar_plaza(Plaza(i, "coche"))
    for i in range(6, 9):
        parking.agregar_plaza(Plaza(i, "moto"))

    app = ParkingApp(parking)
    app.mainloop()
