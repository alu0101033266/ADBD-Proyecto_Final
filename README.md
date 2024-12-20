# ADBD-Proyecto_Final

##  Consultas de ejemplo del funcionamiento de la Base de Datos

### Consulta 1: El pago esta fuera del tiempo:
Si intentamos insertar un pago fuera  del tiempo saldrá un error:

![image](https://github.com/user-attachments/assets/0f018ee3-852b-4c5f-a207-6ceecc018212)


### Consulta 2: El monto no es suficiente:
Si intentamos insertar un pago con un monto erróneo saldrá un error:

![image](https://github.com/user-attachments/assets/8dd533b9-ce57-4e5a-be20-49c32ea87e33)

### Consulta 3: Si actualizamos la edad del socio se actualiza correspondiente su membresia:
actualizamos la fecha de nacimiento del socio y se genera automaticamente la nueva edad y procede a cambiar la membresia automaticamente

![image](https://github.com/user-attachments/assets/38c78c97-1c67-4883-81b3-d0e52b329a58)

### Consulta 4: Conflicto de horario:
Si se solapan 2 horarios en un mismo dia no se inserta el ultimo registro

![image](https://github.com/user-attachments/assets/2297ad47-6074-4e0a-975e-d03983f622af)

### Consulta 5: Un entrenador no puede entrenar 2 deportes a la vez:
Si se inserta un horario para un entrenador donde tenga que entrenar 2 deportes a la vez este registro no se insertará:

![image](https://github.com/user-attachments/assets/501f6bc6-4836-4ba2-8730-b2116f5a720c)

### Consulta 6: Un socio tiene que tener si o si una membresía:
Nos aseguramos de  que no existen socios sin membresías 

![image](https://github.com/user-attachments/assets/573f375e-d66b-483c-b1fd-1c8a5bb48dfe)


### Consulta 7: Fechas futuras:
No es posible insertar socios que tengan una fecha de nacimiento futura

![image](https://github.com/user-attachments/assets/303f6fdd-e2b1-4994-9f71-c051e99d1c50)

### Consulta 8: Monto negativo:
No es posible insertar cantidades negativas como el monto

![image](https://github.com/user-attachments/assets/cf4cb20b-c4ff-48bb-b282-8800c72af778)

### Consulta 9: Borrar en cascada de Socio
A la hora de eliminar una entrada de Socio se deberia eliminar toda la información de su membresía y sus pagos

Antes del delete:

![image](https://github.com/user-attachments/assets/4036bd7d-07fa-4cbe-a0de-47f315e9392b)

 Despues del delete:

 ![image](https://github.com/user-attachments/assets/2645ce17-798a-42ed-a8e4-7bed99c18ab6)

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




