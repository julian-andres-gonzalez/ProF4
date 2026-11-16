# Sistema Software FJ - Parte 2: reservas y funciones del sistema
# Curso Programación 213023 - Fase 4 (UNAD)
# Autor de este archivo: Julián González

import logging  # para escribir en el archivo de logs

# Traemos las clases que están en el archivo de clientes y servicios
from clientes_servicios import Cliente, Servicio, ErrorCliente, ErrorServicio, ErrorReserva


# ---------- Reserva ----------
class Reserva:
    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ErrorReserva("La reserva necesita un cliente y un servicio válidos")
        self.cliente = cliente       # objeto Cliente
        self.servicio = servicio     # objeto Servicio (cualquiera de los tres)
        self.horas = horas           # duración en horas
        self.estado = "PENDIENTE"    # estado inicial

    def confirmar(self):
        if not self.servicio.disponible:                # servicio ocupado o dañado
            raise ErrorReserva("El servicio no está disponible")
        try:
            self.servicio.validar(self.horas)           # cada servicio valida distinto
        except (ErrorServicio, TypeError) as error:
            raise ErrorReserva("La duración no es válida") from error  # error encadenado
        self.estado = "CONFIRMADA"

    def cancelar(self):
        if self.estado == "CANCELADA":                  # no se cancela dos veces
            raise ErrorReserva("La reserva ya estaba cancelada")
        self.estado = "CANCELADA"

    def procesar(self, impuesto=19, descuento=0):
        if self.estado != "CONFIRMADA":                 # primero debe confirmarse
            raise ErrorReserva("Solo se procesan reservas confirmadas")
        try:
            total = self.servicio.costo_total(self.horas, impuesto, descuento)
        except ErrorServicio as error:
            raise ErrorReserva("No se pudo calcular el costo") from error  # error encadenado
        self.estado = "PROCESADA"
        return total                                    # valor a pagar


# ---------- Listas del sistema ----------
lista_clientes = []    # clientes registrados
lista_servicios = []   # servicios creados
lista_reservas = []    # reservas realizadas


# ---------- Funciones de apoyo ----------
def mostrar_error(titulo, error):
    mensaje = f"{titulo}: {error}"
    if error.__cause__:                                 # si viene de otro error, se muestra
        mensaje += f" | causa: {error.__cause__}"
    logging.error(mensaje)                              # queda en el archivo de logs
    print("  ERROR ->", mensaje)


def registrar_cliente(nombre, documento, correo):
    try:                                                # ejemplo de try / except / else
        cliente = Cliente(nombre, documento, correo)
    except ErrorCliente as error:
        mostrar_error("Cliente no registrado", error)
        return None
    else:                                               # solo entra si no hubo error
        lista_clientes.append(cliente)
        logging.info("Registrado: " + cliente.describir())
        print("  OK ->", cliente.describir())
        return cliente


def crear_servicio(clase, nombre, precio_hora):
    try:                                                # ejemplo de try / except
        servicio = clase(nombre, precio_hora)           # clase puede ser ReservaSala, AlquilerEquipo o Asesoria
        lista_servicios.append(servicio)
        logging.info("Servicio creado: " + servicio.describir())
        print("  OK ->", servicio.describir())
        return servicio
    except ErrorServicio as error:
        mostrar_error("Servicio no creado", error)
        return None


def hacer_reserva(cliente, servicio, horas, descuento=0):
    try:                                                # ejemplo de try / except / finally
        reserva = Reserva(cliente, servicio, horas)
        reserva.confirmar()
        total = reserva.procesar(19, descuento)         # IVA del 19%
        lista_reservas.append(reserva)
        texto = f"Reserva de {cliente.nombre}: {servicio.describir()}, {horas} horas, total ${total:,.0f}"
        logging.info(texto)
        print("  OK ->", texto)
        return reserva
    except ErrorReserva as error:
        mostrar_error("Reserva fallida", error)
        return None
    finally:                                            # se ejecuta siempre
        logging.info("Fin del intento de reserva")
# ProF4
Fase 4 - Componente práctico - Prácticas simuladas
