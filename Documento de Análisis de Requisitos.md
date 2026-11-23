# Documento de Análisis de Requisitos
**Proyecto:** Sistema de Gestión de Alquiler de Bicicletas – Bici Caribe (`Bici-Caribe-Sistema`)  
**Asignatura:** Fundamentos de Programación – Universidad del Magdalena  
**Alternativa:** Alternativa I – Bici Caribe  
**Integrantes:** Matías José Bossio Castillo, Diego Mendoza y Fabian Rua 
**Repositorio:** https://github.com/MatiasBC-afk/Bici-Caribe-Sistema  

---

## 1. Descripción General del Dominio y Reglas del Negocio

La empresa **Bici Caribe** gestiona el alquiler diario de bicicletas para turistas en distintas estaciones de Santa Marta (como Malecón, Rodadero o Marina). Cada estación tiene un nombre único, un número fijo de bicicletas disponibles ($\ge 1$) y una fecha de inicio de operaciones.

### Reglas transversales del sistema
1. **Unicidad e identificación de estaciones:** El nombre de cada estación es único. Las comparaciones de nombres distinguen mayúsculas, minúsculas y tildes, pero ignoran espacios en blanco al principio y al final (`.strip()`).
2. **Validación previa de existencia:** En todos los requisitos que solicitan el nombre de una estación existente (requisitos 2, 3, 4–9), si no hay coincidencia exacta, el sistema informa que no existe una estación con ese nombre y retorna de inmediato al menú principal.
3. **Continuidad cronológica del registro:** Cada bicicleta se alquila como máximo una vez al día por jornada completa. Los registros de días comienzan en la fecha de inicio de la estación y avanzan día tras día de manera consecutiva, sin saltos de fecha.
4. **Fórmulas de los indicadores de estación:**
   * **Alquileres totales:** Suma de las bicicletas alquiladas en todos los días registrados:
     $$\text{Total} = \sum_{i=1}^{N} x_i$$
   * **Promedio diario:** Alquileres totales divididos entre el número de días registrados ($N$):
     $$\bar{x} = \frac{\text{Total}}{N}$$
   * **Porcentaje de alquiler:** Promedio diario dividido entre las bicicletas disponibles ($C$) y multiplicado por 100:
     $$P = \left(\frac{\bar{x}}{C}\right) \times 100$$
   * **Desviación estándar poblacional:** Raíz cuadrada del promedio de los cuadrados de las diferencias respecto al promedio diario:
     $$\sigma = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \bar{x})^2}{N}}$$
5. **Clasificación de nivel de alquiler diario:** Cada día registrado se clasifica según el porcentaje $p_i = \left(\frac{x_i}{C}\right) \times 100$ de bicicletas disponibles alquiladas ese día:

| Nivel de alquiler | Rango de porcentaje diario ($p_i$) |
| :--- | :--- |
| **Bajo** | $p_i < 30\%$ |
| **Medio** | $30\% \le p_i < 60\%$ |
| **Alto** | $60\% \le p_i < 85\%$ |
| **Total** | $p_i \ge 85\%$ |

---

## 2. Especificación Detallada de Requisitos

### Requisito 1: Crear una estación
* **Descripción:** Permite registrar una nueva estación en el sistema sin días registrados inicialmente.
* **Entradas:**
  * Nombre de la estación (`str`).
  * Número de bicicletas disponibles (`int`).
  * Año, mes y día de la fecha de inicio del registro (`int`, leídos por separado).
* **Reglas del dominio y orden de validación:** Se verifican cuatro condiciones en orden estricto. Si alguna falla, se muestra únicamente el mensaje de la primera condición incumplida, no se crea la estación y se retorna al menú:
  1. El nombre (sin espacios externos) no está vacío y no existe otra estación con ese mismo nombre.
  2. Las bicicletas disponibles corresponden a un número entero válido.
  3. Las bicicletas disponibles son al menos $1$ ($\ge 1$).
  4. El año, mes y día son números enteros que forman una fecha válida del calendario gregoriano.
* **Salidas:** Mensaje de confirmación de creación de la estación (con 0 días registrados) o mensaje de error de la primera validación que falló.

---

### Requisito 2: Registrar las bicicletas alquiladas del día siguiente
* **Descripción:** Agrega el registro de bicicletas alquiladas correspondiente al día calendario inmediatamente posterior al último registrado en la estación.
* **Entradas:**
  * Nombre de la estación (`str`).
  * Cantidad de bicicletas alquiladas en el día (`int`).
* **Reglas del dominio:**
  * Si la estación no existe, se informa y se retorna al menú.
  * La fecha a registrar se calcula como $\text{fecha\_inicio} + N\text{ días}$, donde $N$ es la cantidad de días ya registrados.
  * Las bicicletas alquiladas deben ser un entero en el intervalo $[0, C]$, donde $C$ es la capacidad de bicicletas disponibles de la estación.
  * **Ciclo de reintento:** Mientras el valor ingresado no sea entero o esté fuera del rango $[0, C]$, el sistema muestra el error correspondiente y vuelve a solicitar el dato para esa misma fecha.
* **Salidas:** Fecha del día siguiente (`AAAA-MM-DD`), avisos de validación en caso de error, y confirmación del registro agregado antes de regresar al menú.

---

### Requisito 3: Simular días
* **Descripción:** Genera y agrega múltiples días consecutivos al registro de una estación con valores aleatorios de bicicletas alquiladas.
* **Entradas:**
  * Nombre de la estación (`str`).
  * Número de días a simular (`int`).
  * Bicicletas alquiladas mínimas (`int`).
  * Bicicletas alquiladas máximas (`int`).
* **Reglas del dominio:**
  * Si la estación no existe, se avisa y se vuelve al menú.
  * **Validación inmediata paso a paso:** Cada dato numérico se valida apenas se lee. Si no cumple su regla, el sistema muestra el motivo y vuelve al menú sin leer los datos restantes ni modificar la estación:
    1. Número de días: entero $\ge 1$.
    2. Mínimo: entero en $[0, C]$.
    3. Máximo: entero en $[0, C]$ y además $\text{mínimo} \le \text{máximo}$.
  * Se agregan consecutivamente los días solicitados, cada uno con un entero aleatorio uniforme en $[\text{mínimo}, \text{máximo}]$ (ambos inclusive).
* **Salidas:** Mensaje de confirmación de los días simulados agregados o aviso específico del primer dato inválido.

---

### Requisito 4: El informe de una estación
* **Descripción:** Presenta el resumen estadístico y operativo de una estación específica.
* **Entradas:**
  * Nombre de la estación (`str`).
* **Reglas del dominio:**
  * Si la estación no existe, se avisa y se retorna al menú.
  * Muestra siempre el nombre de la estación y sus bicicletas disponibles.
  * Si la estación tiene $0$ días registrados, informa que no tiene días registrados y finaliza el informe sin mostrar indicadores adicionales.
  * El promedio diario y el porcentaje de alquiler se redondean con `round(valor, 2)` (sin completar con ceros a la derecha; por ejemplo, `64.0`).
* **Salidas:** Nombre, bicicletas disponibles, días registrados, alquileres totales, promedio diario, porcentaje de alquiler y los indicadores definidos en los requisitos 5 al 9.

---

### Requisito 5: La desviación estándar
* **Descripción:** Calcula la dispersión de las bicicletas alquiladas respecto al promedio diario de la estación.
* **Entradas:**
  * Serie de bicicletas alquiladas por día $[x_1, x_2, \dots, x_N]$ y promedio diario $\bar{x}$.
* **Reglas del dominio:**
  * Se aplica la fórmula de desviación estándar poblacional ($\div N$).
  * Cuando $N = 1$, la desviación estándar es `0.0`.
  * El resultado se presenta redondeado con `round(valor, 2)`.
* **Salidas:** Valor numérico de la desviación estándar dentro del informe de la estación.

---

### Requisito 6: El día de más y el de menos bicicletas alquiladas
* **Descripción:** Identifica las fechas extremas de demanda en el historial de la estación.
* **Entradas:**
  * Registros diarios de bicicletas alquiladas y sus fechas correspondientes.
* **Reglas del dominio:**
  * Busca el día con el valor máximo y el día con el valor mínimo de bicicletas alquiladas.
  * **Regla de desempate:** Si varios días empatan en el máximo o en el mínimo, se selecciona el primero en orden cronológico.
* **Salidas:** Fecha (`AAAA-MM-DD`) del día con más bicicletas alquiladas y fecha (`AAAA-MM-DD`) del día con menos bicicletas alquiladas.

---

### Requisito 7: Los días en cada nivel de alquiler
* **Descripción:** Contabiliza la distribución de los días registrados según los cuatro niveles de ocupación definidos por la empresa.
* **Entradas:**
  * Registros diarios de bicicletas alquiladas y capacidad $C$ de la estación.
* **Reglas del dominio:**
  * Clasifica cada día en Bajo, Medio, Alto o Total según su porcentaje diario $p_i$.
  * Se reportan los cuatro contadores en orden fijo, incluyendo aquellos cuyo conteo sea $0$.
* **Salidas:** Cantidad de días en cada nivel en el orden: **Bajo, Medio, Alto y Total**.

---

### Requisito 8: La racha más larga en alquiler bajo
* **Descripción:** Determina la secuencia continua más extensa de días con ocupación crítica (nivel Bajo).
* **Entradas:**
  * Secuencia cronológica de niveles de alquiler de cada día registrado.
* **Reglas del dominio:**
  * Una racha es una sucesión ininterrumpida de días consecutivos en nivel **Bajo**.
  * **Regla de desempate:** Si existen dos o más rachas con la misma longitud máxima, prevalece la que inició en la fecha más temprana.
  * Si la estación no registra ningún día en nivel Bajo, se emite un aviso específico.
* **Salidas:** Duración en días y fecha de inicio (`AAAA-MM-DD`) de la racha más larga en alquiler bajo, o mensaje indicando que no hubo días en alquiler bajo.

---

### Requisito 9: Los días sin registrar
* **Descripción:** Evalúa el rezago del registro de la estación frente a la fecha actual del sistema.
* **Entradas:**
  * Fecha del último día registrado de la estación y fecha actual del computador (`date.today()`).
* **Reglas del dominio:**
  * Como cada jornada se registra una vez finalizada, el registro esperado al día llega hasta $\text{fecha\_actual} - 1\text{ día}$.
  * Si $\text{último\_día\_registrado} \ge \text{fecha\_actual} - 1\text{ día}$ (incluyendo fechas futuras producto de simulaciones), se indica que el registro está al día.
  * En caso contrario, se calculan los días pendientes desde $\text{último\_día\_registrado} + 1\text{ día}$ hasta $\text{fecha\_actual} - 1\text{ día}$.
* **Salidas:** Fecha del último día registrado y, según corresponda, aviso de registro al día o cantidad de días faltantes junto con el intervalo de fechas sin registrar.

---

### Requisito 10: Varias estaciones en el mismo programa
* **Descripción:** Permite administrar simultáneamente múltiples estaciones independientes durante la ejecución del programa.
* **Entradas:**
  * Operaciones de creación, carga desde archivo y consulta por nombre de estación.
* **Reglas del dominio:**
  * Las estaciones se almacenan en memoria conservando su orden de creación o carga.
  * Cada estación mantiene de forma aislada su capacidad, fecha de inicio y lista de alquileres diarios.
  * No se permite sobrescribir ni duplicar una estación existente.
* **Salidas:** Ejecución independiente por estación y mensajes de advertencia ante nombres inexistentes o duplicados.

---

### Requisito 11: El porcentaje de alquiler más alto y el más bajo
* **Descripción:** Compara el desempeño global entre todas las estaciones activas del sistema.
* **Entradas:**
  * Colección de estaciones registradas en el programa.
* **Reglas del dominio:**
  * Solo se consideran las estaciones que tengan al menos $1$ día registrado.
  * La comparación de máximos y mínimos se efectúa usando los porcentajes de alquiler **sin redondear**.
  * **Regla de desempate:** Ante igualdad de porcentaje máximo o mínimo, se conserva la estación que fue creada o cargada primero.
  * Si no hay estaciones o ninguna tiene días registrados, se informa mediante un aviso.
* **Salidas:** Nombre y porcentaje de alquiler (redondeado con `round(..., 2)`) de la estación con mayor porcentaje y de la estación con menor porcentaje, o aviso de ausencia de estaciones con días registrados.

---

### Requisito 12: Cargar las estaciones desde un archivo
* **Descripción:** Importa masivamente la configuración inicial de estaciones desde un archivo CSV.
* **Entradas:**
  * Ruta del archivo CSV de estaciones (`str`).
* **Reglas del dominio:**
  * **Precondición:** Solo puede ejecutarse si el programa no tiene ninguna estación cargada o creada previamente; de lo contrario, avisa y vuelve al menú sin pedir rutas.
  * Si el archivo indicado no existe, avisa y retorna al menú sin solicitar el archivo de alquileres.
  * Lectura en codificación `UTF-8`, delimitador `;`, omitiendo la línea 1 (encabezado) y saltando líneas vacías sin aviso.
  * Cada línea válida debe tener 5 campos limpios con `.strip()`: `estación;bicicletas_disponibles;año;mes;día`.
  * **Tolerancia a fallos por línea:** Las líneas erróneas se descartan reportando su número de línea y la primera causa de error en el orden: (1) cantidad de campos distinta de 5, (2) nombre vacío, (3) estación ya existente, (4) bicicletas disponibles no enteras, (5) bicicletas disponibles $< 1$, (6) fecha inválida.
* **Salidas:** Detalle de líneas descartadas (número y motivo) y conteo final de estaciones cargadas correctamente.

---

### Requisito 13: Cargar los alquileres desde un archivo
* **Descripción:** Importa los registros diarios de bicicletas alquiladas para las estaciones previamente cargadas.
* **Entradas:**
  * Ruta del archivo CSV de alquileres (`str`), solicitada inmediatamente después de cargar estaciones en el Requisito 12.
* **Reglas del dominio:**
  * Si el archivo no existe, avisa y conserva en memoria las estaciones ya cargadas sin días registrados.
  * Lectura en `UTF-8`, delimitador `;`, ignorando el encabezado (línea 1) y las líneas vacías.
  * Cada línea válida contiene 2 campos limpios con `.strip()`: `estación;bicicletas_alquiladas`, y se añade como el día siguiente consecutivo de la estación indicada.
  * **Tolerancia a fallos por línea:** Las líneas inválidas se descartan indicando número de línea y causa en el orden: (1) cantidad de campos distinta de 2, (2) estación inexistente, (3) bicicletas alquiladas no enteras, (4) bicicletas alquiladas fuera de $[0, C]$.
* **Salidas:** Detalle de líneas descartadas (número y causa) y cantidad total de días cargados.

---

### Requisito 14: El menú
* **Descripción:** Interfaz principal de consola que articula todas las funcionalidades del sistema.
* **Entradas:**
  * Opción seleccionada por el usuario (`str`).
* **Reglas del dominio:**
  * Muestra exactamente 7 opciones numeradas del `1` al `7` en orden fijo:
    1. Crear una estación
    2. Registrar las bicicletas alquiladas del día siguiente
    3. Simular días
    4. Ver el informe de una estación
    5. Ver la estación con el porcentaje de alquiler más alto y la estación con el más bajo
    6. Cargar las estaciones y los alquileres desde archivos
    7. Salir
  * Tras atender cualquier opción válida (`1`–`6`) o ante una entrada no válida, vuelve a mostrar el menú.
  * Finaliza la ejecución únicamente cuando se ingresa `7`.

* **Salidas:** Menú de opciones, mensajes de opción inválida y flujo hacia cada requisito seleccionado.

