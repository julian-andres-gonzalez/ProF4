# Sistema Software FJ - Parte 3: simulación de las operaciones
# Curso Programación 213023 - Fase 4 (UNAD)
# Autor de este archivo: Julián González
# Para ejecutar el proyecto: python main.py

import logging  # para configurar el archivo de logs

# Traemos los tres tipos de servicio y el error de reserva
from clientes_servicios import ReservaSala, AlquilerEquipo, Asesoria, ErrorReserva
# Traemos las listas y las funciones del sistema
from reservas import (lista_clientes, lista_servicios, lista_reservas,
                      registrar_cliente, crear_servicio, hacer_reserva, mostrar_error)

# Archivo donde quedan guardados los eventos y los errores
logging.basicConfig(filename="registro_fj.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")


def main():
    print("1. Cliente válido")
    ana = registrar_cliente("Ana Torres", "1061234567", "ana@correo.com")
    print("2. Cliente con correo inválido")
    luis = registrar_cliente("Luis Mora", "76321456", "luiscorreo.com")
    print("3. Cliente sin documento")
    registrar_cliente("Marta Díaz", "", "marta@correo.com")

    print("4. Servicios correctos")
    sala = crear_servicio(ReservaSala, "Sala de juntas", 50000)
    equipo = crear_servicio(AlquilerEquipo, "Video beam", 15000)
    asesoria = crear_servicio(Asesoria, "Redes y seguridad", 80000)
    print("5. Servicio con precio negativo")
    crear_servicio(ReservaSala, "Sala pequeña", -20000)
    print("6. Servicio con precio en letras")
    crear_servicio(AlquilerEquipo, "Portátil", "gratis")

    print("7. Reserva exitosa de sala")
    r1 = hacer_reserva(ana, sala, 3)
    print("8. Reserva exitosa de asesoría con 10% de descuento")
    hacer_reserva(ana, asesoria, 2, 10)
    print("9. Reserva con cliente que no quedó registrado")
    hacer_reserva(luis, sala, 2)                        # luis vale None por el paso 2
    print("10. Reserva de sala por 20 horas")
    hacer_reserva(ana, sala, 20)
    print("11. Reserva de un servicio no disponible")
    equipo.disponible = False                           # el equipo está en mantenimiento
    hacer_reserva(ana, equipo, 5)
    equipo.disponible = True                            # vuelve a estar disponible
    print("12. Reserva con descuento del 150%")
    hacer_reserva(ana, equipo, 5, 150)

    print("13. Cancelar una reserva y volver a cancelarla")
    try:
        r1.cancelar()                                   # la primera vez sí se puede
        logging.info("Reserva cancelada")               # el evento queda en el log
        print("  OK -> Reserva cancelada")
        r1.cancelar()                                   # la segunda vez lanza error
    except ErrorReserva as error:
        mostrar_error("Cancelación fallida", error)

    print(f"\nResumen: {len(lista_clientes)} clientes, {len(lista_servicios)} servicios, {len(lista_reservas)} reservas")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:                          # por si pasa algo que no esperábamos
        logging.critical(f"Error inesperado: {error}")
        print("Error inesperado:", error)
    finally:
        print("Fin del programa. Revise el archivo registro_fj.log")

