from os import system

from business_logic import SistemaAlquilerBicicletas

system("cls")
print("========================================")
print("Bienvenido a Bici Caribe")
print("========================================")

sistema = SistemaAlquilerBicicletas()
continuar = True

while continuar:
    print("\n--- Menu Bici Caribe ---")
    print("1. Crear una estacion")
    print("2. Registrar las bicicletas alquiladas del dia siguiente")
    print("3. Simular dias")
    print("4. Ver el informe de una estacion")
    print("5. Ver la estacion con el porcentaje de alquiler mas alto y el mas bajo")
    print("6. Cargar las estaciones y los alquileres desde archivos")
    print("7. Salir")

    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        nombre = input("Nombre de la estacion: ")
        bicicletas_texto = input("Bicicletas disponibles: ")
        anio_texto = input("Anio de inicio: ")
        mes_texto = input("Mes de inicio: ")
        dia_texto = input("Dia de inicio: ")

        try:
            estacion_creada = sistema.crear_estacion(
                nombre, bicicletas_texto, anio_texto, mes_texto, dia_texto
            )
            print("Estacion '" + estacion_creada.nombre + "' creada correctamente.")
        except ValueError as error:
            print(error)

    elif opcion == "2":
        nombre = input("Nombre de la estacion: ")
        estacion = sistema.buscar_estacion(nombre)
        if estacion is None:
            print("No hay una estacion con ese nombre.")
        else:
            fecha_dia = estacion.fecha_siguiente()
            print("Fecha del dia a registrar: " + fecha_dia.isoformat())
            dia_guardado = False
            while not dia_guardado:
                cantidad_texto = input("Bicicletas alquiladas: ").strip()
                try:
                    cantidad = int(cantidad_texto)
                    estacion.registrar_dia(cantidad)
                    dia_guardado = True
                    print(
                        "Dia "
                        + fecha_dia.isoformat()
                        + " registrado en '"
                        + estacion.nombre
                        + "' con "
                        + str(cantidad)
                        + " bicicletas alquiladas."
                    )
                except ValueError as error:
                    if str(error).startswith("Las bicicletas alquiladas"):
                        print(error)
                    else:
                        print("Las bicicletas alquiladas deben ser un numero entero.")

    elif opcion == "3":
        nombre = input("Nombre de la estacion: ")
        estacion = sistema.buscar_estacion(nombre)
        if estacion is None:
            print("No hay una estacion con ese nombre.")
        else:
            dias_texto = input("Numero de dias a simular: ").strip()
            try:
                num_dias = int(dias_texto)
            except ValueError:
                print("El numero de dias debe ser un numero entero.")
                num_dias = None

            if num_dias is not None:
                if num_dias < 1:
                    print("Se debe simular al menos un dia.")
                else:
                    min_texto = input("Bicicletas alquiladas minimas: ").strip()
                    try:
                        minimo = int(min_texto)
                    except ValueError:
                        print("Las bicicletas alquiladas deben ser un numero entero.")
                        minimo = None

                    if minimo is not None:
                        if not estacion.es_cantidad_valida(minimo):
                            print(
                                "Las bicicletas alquiladas van de 0 a "
                                + str(estacion.bicicletas_disponibles)
                                + "."
                            )
                        else:
                            max_texto = input(
                                "Bicicletas alquiladas maximas: "
                            ).strip()
                            try:
                                maximo = int(max_texto)
                            except ValueError:
                                print(
                                    "Las bicicletas alquiladas deben ser un numero entero."
                                )
                                maximo = None

                            if maximo is not None:
                                if not estacion.es_cantidad_valida(maximo):
                                    print(
                                        "Las bicicletas alquiladas van de 0 a "
                                        + str(estacion.bicicletas_disponibles)
                                        + "."
                                    )
                                elif minimo > maximo:
                                    print("El minimo no puede ser mayor que el maximo.")
                                else:
                                    simulados = estacion.simular_dias(
                                        num_dias, minimo, maximo
                                    )
                                    print(
                                        "Se simularon "
                                        + str(len(simulados))
                                        + " dias en '"
                                        + estacion.nombre
                                        + "': "
                                        + str(simulados)
                                        + "."
                                    )

    elif opcion == "4":
        nombre = input("Nombre de la estacion: ")
        estacion = sistema.buscar_estacion(nombre)
        if estacion is None:
            print("No hay una estacion con ese nombre.")
        else:
            print("Estacion: " + estacion.nombre)
            print(
                "Bicicletas disponibles: " + str(estacion.bicicletas_disponibles)
            )
            if not estacion.tiene_dias():
                print("La estacion no tiene dias registrados.")
            else:
                fecha_max, fecha_min = estacion.fechas_extremos()
                niveles = estacion.conteo_niveles()
                racha = estacion.racha_mas_larga_bajo()
                estado_reg = estacion.estado_registro_actual()

                print(
                    "Dias registrados: " + str(len(estacion.alquileres_por_dia))
                )
                print(
                    "Alquileres totales: " + str(estacion.alquileres_totales())
                )
                print(
                    "Promedio de bicicletas alquiladas por dia: "
                    + str(round(estacion.promedio_diario_exacto(), 2))
                )
                print(
                    "Porcentaje de alquiler: "
                    + str(round(estacion.porcentaje_alquiler_exacto(), 2))
                    + " %"
                )
                print(
                    "Desviacion estandar: "
                    + str(round(estacion.desviacion_estandar_exacta(), 2))
                )
                print("Dia de mas bicicletas alquiladas: " + fecha_max.isoformat())
                print(
                    "Dia de menos bicicletas alquiladas: " + fecha_min.isoformat()
                )
                print(
                    "Dias por nivel de alquiler -> Bajo: "
                    + str(niveles["bajo"])
                    + ", Medio: "
                    + str(niveles["medio"])
                    + ", Alto: "
                    + str(niveles["alto"])
                    + ", Total: "
                    + str(niveles["total"])
                )

                if racha is None:
                    print(
                        "Racha mas larga en alquiler bajo: no hubo ningun dia en alquiler bajo."
                    )
                else:
                    longitud, fecha_inicio_racha = racha
                    if longitud == 1:
                        unidad = "dia"
                    else:
                        unidad = "dias"
                    print(
                        "Racha mas larga en alquiler bajo: "
                        + str(longitud)
                        + " "
                        + unidad
                        + ", inicio el "
                        + fecha_inicio_racha.isoformat()
                    )

                print(
                    "Ultimo dia registrado: "
                    + estado_reg["ultimo_dia_registrado"].isoformat()
                )
                if estado_reg["al_dia"]:
                    print("Estado del registro: al dia.")
                else:
                    print(
                        "Dias sin registrar: "
                        + str(estado_reg["dias_faltantes"])
                        + " (del "
                        + estado_reg["desde"].isoformat()
                        + " al "
                        + estado_reg["hasta"].isoformat()
                        + ")"
                    )

    elif opcion == "5":
        resultado = sistema.extremos_porcentaje_alquiler()
        if resultado is None:
            print("Ninguna estacion tiene dias registrados.")
        else:
            (nombre_max, pct_max), (nombre_min, pct_min) = resultado
            print(
                "Porcentaje de alquiler mas alto: "
                + nombre_max
                + " ("
                + str(pct_max)
                + " %)"
            )
            print(
                "Porcentaje de alquiler mas bajo: "
                + nombre_min
                + " ("
                + str(pct_min)
                + " %)"
            )

    elif opcion == "6":
        if sistema.tiene_estaciones():
            print("La carga solo se hace con el programa sin estaciones.")
        else:
            ruta_estaciones = input("Ruta del archivo de estaciones: ")
            try:
                ruta_alquileres = input("Ruta del archivo de alquileres: ")
                resultado = sistema.cargar_desde_archivos(
                    ruta_estaciones, ruta_alquileres
                )
                avisos = resultado["avisos"]
                for indice in range(len(avisos)):
                    print(avisos[indice])

                if not resultado["archivo_alquileres_encontrado"]:
                    print("El archivo de alquileres no existe.")
                    print(
                        "Estaciones cargadas: "
                        + str(resultado["estaciones_cargadas"])
                    )
                    print("Dias cargados: 0 (sin dias registrados).")
                else:
                    print(
                        "Estaciones cargadas: "
                        + str(resultado["estaciones_cargadas"])
                    )
                    print("Dias cargados: " + str(resultado["dias_cargados"]))
            except FileNotFoundError as error:
                print(error)

    elif opcion == "7":
        continuar = False

    else:
        print("La opcion no es valida.")