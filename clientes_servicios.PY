# Sistema Software FJ - Parte 1: excepciones, clientes y servicios
# Curso Programación 213023 - Fase 4 (UNAD)
# Autor de este archivo: Carlos Arteaga

from abc import ABC, abstractmethod  # para crear clases abstractas


# ---------- Excepciones personalizadas ----------
class ErrorSistema(Exception):       # error general, de aquí heredan las demás
    pass

class ErrorCliente(ErrorSistema):    # datos de cliente incorrectos
    pass

class ErrorServicio(ErrorSistema):   # servicio mal creado o mal calculado
    pass

class ErrorReserva(ErrorSistema):    # reserva que no se puede hacer
    pass


# ---------- Clase abstracta general ----------
class Entidad(ABC):
    def __init__(self, nombre):
        self._nombre = nombre        # todas las entidades tienen nombre

    @property
    def nombre(self):
        return self._nombre          # solo lectura

    @abstractmethod
    def describir(self):             # cada clase hija lo escribe a su manera
        pass


# ---------- Cliente ----------
class Cliente(Entidad):
    def __init__(self, nombre, documento, correo):
        if not nombre or not documento or not correo:   # no puede faltar ningún dato
            raise ErrorCliente("Faltan datos del cliente")
        if not str(documento).isdigit():                # el documento solo lleva números
            raise ErrorCliente("El documento solo debe tener números")
        if "@" not in correo:                           # revisión básica del correo
            raise ErrorCliente("El correo no es válido: " + correo)
        super().__init__(nombre)       # guarda el nombre en la clase padre
        self.__documento = documento   # atributo privado (encapsulado)
        self.__correo = correo         # atributo privado (encapsulado)

    def describir(self):
        return f"Cliente {self.nombre} (doc. {self.__documento})"


# ---------- Servicio (abstracta) y sus tres tipos ----------
class Servicio(Entidad):
    def __init__(self, nombre, precio_hora):
        super().__init__(nombre)
        try:
            self._precio_hora = float(precio_hora)      # el precio debe ser un número
        except (TypeError, ValueError) as error:
            raise ErrorServicio("El precio debe ser un número") from error  # error encadenado
        if self._precio_hora <= 0:                      # no se aceptan precios negativos
            raise ErrorServicio("El precio debe ser mayor que cero")
        self.disponible = True                          # empieza disponible

    @abstractmethod
    def validar(self, horas):          # cada servicio valida su duración
        pass

    @abstractmethod
    def calcular_costo(self, horas):   # cada servicio cobra distinto (polimorfismo)
        pass

    # "Sobrecarga": en Python se hace con parámetros opcionales
    # costo_total(2) / costo_total(2, 19) / costo_total(2, 19, 10)
    def costo_total(self, horas, impuesto=0, descuento=0):
        if descuento < 0 or descuento > 100:            # un descuento así no tiene sentido
            raise ErrorServicio("Descuento fuera de rango, cálculo inconsistente")
        base = self.calcular_costo(horas)               # costo según el tipo de servicio
        base = base - base * descuento / 100            # se resta el descuento
        return base + base * impuesto / 100             # se suma el impuesto


class ReservaSala(Servicio):
    def validar(self, horas):
        if horas < 1 or horas > 8:                      # máximo una jornada
            raise ErrorServicio("Una sala se reserva entre 1 y 8 horas")

    def calcular_costo(self, horas):
        return self._precio_hora * horas                # solo precio por horas

    def describir(self):
        return f"Sala: {self.nombre}"


class AlquilerEquipo(Servicio):
    def validar(self, horas):
        if horas < 1 or horas > 48:                     # máximo dos días
            raise ErrorServicio("Un equipo se alquila entre 1 y 48 horas")

    def calcular_costo(self, horas):
        return self._precio_hora * horas + 10000        # se suma el seguro del equipo

    def describir(self):
        return f"Equipo: {self.nombre}"


class Asesoria(Servicio):
    def validar(self, horas):
        if horas < 1 or horas > 4:                      # son sesiones cortas
            raise ErrorServicio("Una asesoría dura entre 1 y 4 horas")

    def calcular_costo(self, horas):
        return self._precio_hora * horas * 1.10         # recargo del 10% por ser especializada

    def describir(self):
        return f"Asesoría: {self.nombre}"


# ---------- Prueba rápida de este archivo ----------
# Solo se ejecuta si se corre este archivo directamente: python clientes_servicios.py
if __name__ == "__main__":
    try:
        cliente = Cliente("Ana Torres", "1061234567", "ana@correo.com")  # cliente correcto
        print(cliente.describir())
        sala = ReservaSala("Sala de juntas", 50000)                      # servicio correcto
        print(sala.describir(), "- 3 horas con IVA:", sala.costo_total(3, 19))
        Cliente("Luis Mora", "76321456", "luiscorreo.com")               # este debe fallar
    except ErrorSistema as error:
        print("Error controlado:", error)                                # el programa no se cae