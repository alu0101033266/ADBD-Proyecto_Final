# ADBD-Proyecto_Final

##  Consultas de ejemplo del funcionamiento de la Base de Datos

### Consulta 1: El pago esta fuera del tiempo:
Si intentamos insertar un pago fuera  del tiempo saldrá un error:
![image](https://github.com/user-attachments/assets/0f018ee3-852b-4c5f-a207-6ceecc018212)


### Consulta 2: El monto no es suficiente:
Si intentamos insertar un pago con un monto erróneo saldrá un error:

![image](https://github.com/user-attachments/assets/8dd533b9-ce57-4e5a-be20-49c32ea87e33)

### Consulta 3: Si actualizamos la edad del socio se actualiza correspondiente su membresia:

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



