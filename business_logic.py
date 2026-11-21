from datetime import date, timedelta
import math
import random


class Estacion:
    def __init__(self, nombre: str, bicicletas_disponibles: int, fecha_inicio: date):
        self.nombre = nombre
        self.bicicletas_disponibles = bicicletas_disponibles
        self.fecha_inicio = fecha_inicio
        self.alquileres_por_dia = []

    def tiene_dias(self) -> bool:
        if len(self.alquileres_por_dia) > 0:
            hay_dias = True
        else:
            hay_dias = False
        return hay_dias

    def fecha_siguiente(self) -> date:
        proxima_fecha = self.fecha_inicio + timedelta(days=len(self.alquileres_por_dia))
        return proxima_fecha

    def es_cantidad_valida(self, cantidad: int) -> bool:
        if cantidad >= 0 and cantidad <= self.bicicletas_disponibles:
            valida = True
        else:
            valida = False
        return valida

    def registrar_dia(self, bicicletas_alquiladas: int):
        if not self.es_cantidad_valida(bicicletas_alquiladas):
            raise ValueError(
                "Las bicicletas alquiladas van de 0 a "
                + str(self.bicicletas_disponibles)
                + "."
            )
        self.alquileres_por_dia.append(bicicletas_alquiladas)

    def simular_dias(self, num_dias: int, minimo: int, maximo: int):
        simulados = []
        for _ in range(num_dias):
            valor = random.randint(minimo, maximo)
            self.alquileres_por_dia.append(valor)
            simulados.append(valor)
        return simulados

    def alquileres_totales(self) -> int:
        total = 0
        for cantidad in self.alquileres_por_dia:
            total = total + cantidad
        return total

    def promedio_diario_exacto(self) -> float:
        if not self.tiene_dias():
            raise ValueError("La estacion no tiene dias registrados.")
        promedio = self.alquileres_totales() / len(self.alquileres_por_dia)
        return promedio

    def porcentaje_alquiler_exacto(self) -> float:
        promedio = self.promedio_diario_exacto()
        porcentaje = (promedio / self.bicicletas_disponibles) * 100.0
        return porcentaje

    def desviacion_estandar_exacta(self) -> float:
        if not self.tiene_dias():
            raise ValueError("La estacion no tiene dias registrados.")
        promedio = self.promedio_diario_exacto()
        suma_cuadrados = 0.0
        for cantidad in self.alquileres_por_dia:
            diferencia = cantidad - promedio
            suma_cuadrados = suma_cuadrados + (diferencia * diferencia)
        varianza = suma_cuadrados / len(self.alquileres_por_dia)
        desviacion = math.sqrt(varianza)
        return desviacion

    def fechas_extremos(self):
        if not self.tiene_dias():
            raise ValueError("La estacion no tiene dias registrados.")

        indice_max = 0
        indice_min = 0
        valor_max = self.alquileres_por_dia[0]
        valor_min = self.alquileres_por_dia[0]

        for indice in range(1, len(self.alquileres_por_dia)):
            actual = self.alquileres_por_dia[indice]
            if actual > valor_max:
                valor_max = actual
                indice_max = indice
            if actual < valor_min:
                valor_min = actual
                indice_min = indice

        fecha_max = self.fecha_inicio + timedelta(days=indice_max)
        fecha_min = self.fecha_inicio + timedelta(days=indice_min)
        return fecha_max, fecha_min

    def clasificar_nivel(self, bicicletas_alquiladas: int) -> str:
        porcentaje_dia = (bicicletas_alquiladas / self.bicicletas_disponibles) * 100.0
        if porcentaje_dia < 30.0:
            nivel = "bajo"
        elif porcentaje_dia < 60.0:
            nivel = "medio"
        elif porcentaje_dia < 85.0:
            nivel = "alto"
        else:
            nivel = "total"
        return nivel

    def conteo_niveles(self):
        bajo = 0
        medio = 0
        alto = 0
        total = 0

        for cantidad in self.alquileres_por_dia:
            nivel = self.clasificar_nivel(cantidad)
            if nivel == "bajo":
                bajo = bajo + 1
            elif nivel == "medio":
                medio = medio + 1
            elif nivel == "alto":
                alto = alto + 1
            else:
                total = total + 1

        return {
            "bajo": bajo,
            "medio": medio,
            "alto": alto,
            "total": total,
        }

    def racha_mas_larga_bajo(self):
        racha_actual = 0
        inicio_actual = 0
        mejor_longitud = 0
        mejor_inicio = 0

        for indice in range(len(self.alquileres_por_dia)):
            cantidad = self.alquileres_por_dia[indice]
            nivel = self.clasificar_nivel(cantidad)
            if nivel == "bajo":
                if racha_actual == 0:
                    inicio_actual = indice
                racha_actual = racha_actual + 1
                if racha_actual > mejor_longitud:
                    mejor_longitud = racha_actual
                    mejor_inicio = inicio_actual
            else:
                racha_actual = 0

        if mejor_longitud == 0:
            return None

        fecha_inicio_racha = self.fecha_inicio + timedelta(days=mejor_inicio)
        return mejor_longitud, fecha_inicio_racha

    def estado_registro_actual(self, fecha_actual=None):
        if not self.tiene_dias():
            raise ValueError("La estacion no tiene dias registrados.")

        if fecha_actual is None:
            hoy = date.today()
        else:
            hoy = fecha_actual

        ultimo_dia_registrado = self.fecha_inicio + timedelta(
            days=len(self.alquileres_por_dia) - 1
        )
        ultimo_dia_esperado = hoy - timedelta(days=1)

        if ultimo_dia_registrado >= ultimo_dia_esperado:
            return {
                "al_dia": True,
                "ultimo_dia_registrado": ultimo_dia_registrado,
                "dias_faltantes": 0,
                "desde": None,
                "hasta": None,
            }

        primer_faltante = ultimo_dia_registrado + timedelta(days=1)
        dias_faltantes = (ultimo_dia_esperado - primer_faltante).days + 1
        return {
            "al_dia": False,
            "ultimo_dia_registrado": ultimo_dia_registrado,
            "dias_faltantes": dias_faltantes,
            "desde": primer_faltante,
            "hasta": ultimo_dia_esperado,
        }


class SistemaAlquilerBicicletas:
    def __init__(self):
        self.estaciones = []

    def tiene_estaciones(self) -> bool:
        if len(self.estaciones) > 0:
            hay_estaciones = True
        else:
            hay_estaciones = False
        return hay_estaciones

    def buscar_estacion(self, nombre_raw: str):
        nombre = nombre_raw.strip()
        for indice in range(len(self.estaciones)):
            estacion_actual = self.estaciones[indice]
            if estacion_actual.nombre == nombre:
                return estacion_actual
        return None

    def crear_estacion(
        self,
        nombre_raw: str,
        bicicletas_raw: str,
        anio_raw: str,
        mes_raw: str,
        dia_raw: str,
    ):
        nombre = nombre_raw.strip()
        if nombre == "":
            raise ValueError("El nombre no puede estar vacio.")

        if self.buscar_estacion(nombre) is not None:
            raise ValueError("Ya existe una estacion con ese nombre.")

        try:
            bicicletas = int(bicicletas_raw.strip())
        except ValueError:
            raise ValueError("Las bicicletas disponibles deben ser un numero entero.")

        if bicicletas < 1:
            raise ValueError("La estacion debe tener al menos una bicicleta disponible.")

        try:
            anio = int(anio_raw.strip())
            mes = int(mes_raw.strip())
            dia = int(dia_raw.strip())
            fecha_inicio = date(anio, mes, dia)
        except ValueError:
            raise ValueError("La fecha no es valida.")

        nueva_estacion = Estacion(nombre, bicicletas, fecha_inicio)
        self.estaciones.append(nueva_estacion)
        return nueva_estacion

    def extremos_porcentaje_alquiler(self):
        con_dias = []
        for indice in range(len(self.estaciones)):
            estacion_actual = self.estaciones[indice]
            if estacion_actual.tiene_dias():
                con_dias.append(estacion_actual)

        if len(con_dias) == 0:
            return None

        estacion_max = con_dias[0]
        porcentaje_max = estacion_max.porcentaje_alquiler_exacto()

        estacion_min = con_dias[0]
        porcentaje_min = estacion_min.porcentaje_alquiler_exacto()

        for indice in range(1, len(con_dias)):
            estacion_actual = con_dias[indice]
            porcentaje_actual = estacion_actual.porcentaje_alquiler_exacto()
            if porcentaje_actual > porcentaje_max:
                porcentaje_max = porcentaje_actual
                estacion_max = estacion_actual
            if porcentaje_actual < porcentaje_min:
                porcentaje_min = porcentaje_actual
                estacion_min = estacion_actual

        return (
            (estacion_max.nombre, round(porcentaje_max, 2)),
            (estacion_min.nombre, round(porcentaje_min, 2)),
        )

    def cargar_desde_archivos(self, ruta_estaciones: str, ruta_alquileres: str):
        if self.tiene_estaciones():
            raise ValueError("La carga solo se hace con el programa sin estaciones.")

        try:
            archivo_estaciones = open(ruta_estaciones.strip(), "r", encoding="utf-8")
        except OSError:
            raise FileNotFoundError("El archivo de estaciones no existe.")

        estaciones_cargadas = 0
        avisos = []
        numero_linea = 0

        for linea in archivo_estaciones:
            numero_linea = numero_linea + 1
            if numero_linea == 1:
                continue
            contenido = linea.rstrip("\r\n")
            if contenido.strip() == "":
                continue

            campos = contenido.split(";")
            if len(campos) != 5:
                avisos.append(
                    "Linea " + str(numero_linea) + " descartada: no tiene cinco campos."
                )
                continue

            try:
                self.crear_estacion(
                    campos[0].strip(),
                    campos[1].strip(),
                    campos[2].strip(),
                    campos[3].strip(),
                    campos[4].strip(),
                )
                estaciones_cargadas = estaciones_cargadas + 1
            except ValueError as error:
                avisos.append(
                    "Linea " + str(numero_linea) + " descartada: " + str(error)
                )

        archivo_estaciones.close()

        try:
            archivo_alquileres = open(ruta_alquileres.strip(), "r", encoding="utf-8")
        except OSError:
            return {
                "archivo_alquileres_encontrado": False,
                "estaciones_cargadas": estaciones_cargadas,
                "dias_cargados": 0,
                "avisos": avisos,
            }

        dias_cargados = 0
        numero_linea = 0

        for linea in archivo_alquileres:
            numero_linea = numero_linea + 1
            if numero_linea == 1:
                continue
            contenido = linea.rstrip("\r\n")
            if contenido.strip() == "":
                continue

            campos = contenido.split(";")
            if len(campos) != 2:
                avisos.append(
                    "Linea " + str(numero_linea) + " descartada: no tiene dos campos."
                )
                continue

            nombre_estacion = campos[0].strip()
            cantidad_texto = campos[1].strip()

            estacion = self.buscar_estacion(nombre_estacion)
            if estacion is None:
                avisos.append(
                    "Linea "
                    + str(numero_linea)
                    + " descartada: no hay una estacion con ese nombre."
                )
                continue

            try:
                cantidad = int(cantidad_texto)
            except ValueError:
                avisos.append(
                    "Linea "
                    + str(numero_linea)
                    + " descartada: las bicicletas alquiladas deben ser un numero entero."
                )
                continue

            try:
                estacion.registrar_dia(cantidad)
                dias_cargados = dias_cargados + 1
            except ValueError as error:
                avisos.append(
                    "Linea " + str(numero_linea) + " descartada: " + str(error)
                )

        archivo_alquileres.close()

        return {
            "archivo_alquileres_encontrado": True,
            "estaciones_cargadas": estaciones_cargadas,
            "dias_cargados": dias_cargados,
            "avisos": avisos,
        }