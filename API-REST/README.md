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

