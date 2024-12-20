# **Nova Sport Club**

## **Autores**
- Enrique Hernandez Cabrera
- Airam Herrera Plasencia
  
# **Índice del Proyecto - Nova Sport Club**

1. [**Proyecto Final**](./Proyecto_Final_ADBD.pdf) - Documento principal del proyecto en formato PDF.
2. [**Modelo Entidad-Relación**](./Modelo_E-R) - Contiene los diagramas y recursos del modelo E-R.
3. [**Modelo Relacional**](./Modelo_Relacional) - Incluye los diagramas relacionales del proyecto.
4. [**Scripts**](./Scripts) - Scripts SQL para la base de datos incluye la creacion de la base de datos y las inserciones de los datos por separado.
5. [**Consultas**](./Consultas) - Contiene consultas ilustrativas de la base de datos relacionadas con el proyecto.
6. [**API-REST**](./API-REST) - Código fuente de la API REST.
7. [**Presupuesto**](./Presupuesto) - Contiene los cálculos y desglose del presupuesto.

---
## Funcionamiento de la API REST 

### **Requisitos previos**
- Python instalado en el sistema.
- Base de datos PostgreSQL configurada.

### **DEPENDENCIAS**
1. Crear y activar un entorno virtual en Python:
   ```
   python -m venv adbd
   adbd\Scripts\activate
   ```

2. Instalar las dependencias necesarias:
   ```
   pip install flask psycopg2
   ```

3. Ejecutar la aplicación:
   ```
   python app.py
   ```

### **Nota**
- Asegúrate de tener configurada la conexión a la base de datos PostgreSQL en el archivo del código antes de ejecutar la API.

## **Rutas de ejemplo para mostrar el funcionamiento de las rutas**
**Usando socio para las pruebas**

### Ruta POST de creacion socio

Podemos crear un socio con una petición POST

![image](https://github.com/user-attachments/assets/c30ce4c0-4f1f-4ec3-9551-50d45a6378d4)

### Ruta GET Socio todos

Podemos obtener la tabla de socios entera

![image](https://github.com/user-attachments/assets/9e6be926-2dcc-487f-8872-bd74c9a8bbab)

### Ruta GET socio por ID

Podemos obtener un socio en concreto usando su ID

![image](https://github.com/user-attachments/assets/4c9e48e9-8a77-4a67-9960-309c49455bd5)

### Ruta PUT socio por ID

Podemos actualizar los datos de un socio en concreo usando su ID

![image](https://github.com/user-attachments/assets/e252fe15-6250-4613-99ca-f2ff58ae5db0)

### RUTA DELETE socio por ID

Podemos eliminar a un socio en concreto usando su ID

Operacion del DELETE:

![image](https://github.com/user-attachments/assets/13642724-cb05-4c05-b0ac-c6cf66f42423)

Operacion de GET despues del DELETE:

![image](https://github.com/user-attachments/assets/671b2652-a228-40ef-bd37-97dac7f5f23c)

## **Rutas de la API**

### **1. Rutas de Socios**

| Método | Endpoint            | Descripción                     |
|--------|---------------------|---------------------------------|
| GET    | `/api/socios`       | Obtener todos los socios.       |
| GET    | `/api/socios/<id>`  | Obtener un socio por ID.        |
| POST   | `/api/socios`       | Crear un nuevo socio.           |
| PUT    | `/api/socios/<id>`  | Actualizar un socio existente.  |
| DELETE | `/api/socios/<id>`  | Eliminar un socio.              |

---

### **2. Rutas de Membresías**

| Método | Endpoint                | Descripción                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/api/membresias`       | Obtener todas las membresías.        |
| GET    | `/api/membresias/<id>`  | Obtener una membresía por ID.        |
| POST   | `/api/membresias`       | Crear una nueva membresía.           |
| PUT    | `/api/membresias/<id>`  | Actualizar una membresía existente.  |
| DELETE | `/api/membresias/<id>`  | Eliminar una membresía.              |

---

### **3. Rutas de Pagos**

| Método | Endpoint         | Descripción                   |
|--------|------------------|-------------------------------|
| GET    | `/api/pagos`     | Obtener todos los pagos.      |
| GET    | `/api/pagos/<id>`| Obtener un pago por ID.       |
| POST   | `/api/pagos`     | Crear un nuevo pago.          |
| PUT    | `/api/pagos/<id>`| Actualizar un pago existente. |
| DELETE | `/api/pagos/<id>`| Eliminar un pago.             |

---

### **4. Rutas de Entrenadores**

| Método | Endpoint                | Descripción                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/api/entrenadores`     | Obtener todos los entrenadores.      |
| GET    | `/api/entrenadores/<id>`| Obtener un entrenador por ID.        |
| POST   | `/api/entrenadores`     | Crear un nuevo entrenador.           |
| PUT    | `/api/entrenadores/<id>`| Actualizar un entrenador existente.  |
| DELETE | `/api/entrenadores/<id>`| Eliminar un entrenador.              |

---

### **5. Rutas de Deportes**

| Método | Endpoint           | Descripción                   |
|--------|--------------------|-------------------------------|
| GET    | `/api/deportes`    | Obtener todos los deportes.   |
| GET    | `/api/deportes/<id>`| Obtener un deporte por ID.    |
| POST   | `/api/deportes`    | Crear un nuevo deporte.       |
| PUT    | `/api/deportes/<id>`| Actualizar un deporte.        |
| DELETE | `/api/deportes/<id>`| Eliminar un deporte.          |

---

### **6. Rutas de Instalaciones**

| Método | Endpoint                  | Descripción                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/api/instalaciones`      | Obtener todas las instalaciones.     |
| GET    | `/api/instalaciones/<id>` | Obtener una instalación por ID.      |
| POST   | `/api/instalaciones`      | Crear una nueva instalación.         |
| PUT    | `/api/instalaciones/<id>` | Actualizar una instalación existente.|
| DELETE | `/api/instalaciones/<id>` | Eliminar una instalación.            |

---

### **7. Rutas de Horarios**

| Método | Endpoint        | Descripción                 |
|--------|-----------------|-----------------------------|
| GET    | `/api/horarios` | Obtener todos los horarios. |
| POST   | `/api/horarios` | Crear un nuevo horario.     |
| DELETE | `/api/horarios` | Eliminar un horario.        |

---

### **8. Rutas de Reservas**

| Método | Endpoint        | Descripción                 |
|--------|-----------------|-----------------------------|
| GET    | `/api/reservas` | Obtener todas las reservas. |
| POST   | `/api/reservas` | Crear una nueva reserva.    |
| DELETE | `/api/reservas` | Eliminar una reserva.       |

---

### **9. Rutas de Entrena**

| Método | Endpoint        | Descripción                                  |
|--------|-----------------|----------------------------------------------|
| GET    | `/api/entrena`  | Obtener todos los registros de entrenamiento.|
| POST   | `/api/entrena`  | Crear un nuevo registro de entrenamiento.    |
| DELETE | `/api/entrena`  | Eliminar un registro de entrenamiento.       |

# **Presupuesto**

## **Costos de Desarrollo**

Este apartado incluye las horas dedicadas a las distintas fases del proyecto y su correspondiente costo estimado.

| Tarea                       | Horas Estimadas | Costo por Hora (€) | Total (€) |
|-----------------------------|-----------------|--------------------|-----------|
| Análisis de Requisitos      | 8               | 15                 | 120       |
| Diseño Conceptual (ERD)     | 15              | 15                 | 225       |
| Diseño Lógico y Relacional  | 8               | 15                 | 120       |
| Implementación en PostgreSQL| 20              | 15                 | 300       |
| Desarrollo de la API REST   | 25              | 15                 | 375       |
| Pruebas y Depuración        | 15              | 15                 | 225       |
| Documentación               | 10              | 10                 | 100       |
| **Total Desarrollo**        | **-**           | **-**              | **1465**  |

---

## **Pruebas y Mantenimiento**

El proceso de pruebas y mantenimiento se distribuyó en tres actividades principales: pruebas funcionales, pruebas de carga, y corrección de errores. El desglose es el siguiente:

| Actividad            | Horas Estimadas | Costo por Hora (€) | Total (€) |
|----------------------|-----------------|--------------------|-----------|
| Pruebas funcionales  | 10              | 10                 | 100       |
| Pruebas de carga     | 5               | 10                 | 50        |
| Corrección de errores| 5               | 10                 | 50        |
| **Total Pruebas y Mantenimiento** | **-** | **-** | **200** |

---

## **Costo Total Estimado**

Finalmente, el costo total estimado para el proyecto, incluyendo todas las categorías mencionadas, se resume en la siguiente tabla:

| Concepto                | Costo (€) |
|-------------------------|-----------|
| Costos de Desarrollo    | 1465      |
| Infraestructura Tecnológica | 0     |
| Pruebas y Mantenimiento | 200       |
| **Total General**       | **1665**  |

---

## **Notas Finales**

- Las herramientas utilizadas fueron gratuitas o de código abierto (PostgreSQL, Flask, Draw.io).
- Este presupuesto refleja exclusivamente el tiempo invertido y los recursos utilizados por los integrantes del equipo.




