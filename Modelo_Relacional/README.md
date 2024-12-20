# Modelo_Relacional

 **SOCIO**
(ID_SOCIO, Nombre, Fecha_Nacimiento, Apellido1, Apellido2, Edad GENERATED ALWAYS AS (EXTRACT(YEAR FROM AGE(Fecha_Nacimiento))) STORED)
- **(PK):** ID_SOCIO


**MEMBRESIA**

(ID_Membresia, ID_Socio, Frecuencia, Categoria, Fecha_Inicio, Estado, 
 Fecha_Vencimiento GENERATED ALWAYS AS (CASE WHEN Frecuencia = 'Mensual' THEN CURRENT_DATE + INTERVAL '1 MONTH' WHEN Frecuencia = 'Trimestral' THEN CURRENT_DATE + INTERVAL '3 MONTH' END),
 Coste_Total GENERATED ALWAYS AS (50 * CASE WHEN Categoria = 'Infantil' THEN 0.90 WHEN Categoria = 'Senior' THEN 0.95 ELSE 1 END))
- **(PK):** ID_Membresia, ID_Socio
- **(FK):** ID_Socio


## **PAGO**
```
(ID_Pago, ID_Socio, Fecha_Pago, Monto, Estado, Formato_Pago)
- **(PK):** ID_Pago
- **(FK):** ID_Socio
```

---

## **ENTRENADOR**
```
(ID_Entrenador, Nombre, Sueldo, Seguridad_Social)
- **(PK):** ID_Entrenador
```

---

## **DEPORTE**
```
(ID_Deporte, Nombre)
- **(PK):** ID_Deporte
```

---

## **POLIDEPORTIVO**
```
(ID_Instalacion, Capacidad, Tipo, Nombre, Dirección, Tipo_Suelo)
- **(PK):** ID_Instalacion
```

---

## **SALA**
```
(ID_Instalacion, Capacidad, Tipo, Nombre, Dirección, Superficie)
- **(PK):** ID_Instalacion
```

---

## **PISCINA**
```
(ID_Instalacion, Capacidad, Tipo, Nombre, Dirección, Superficie)
- **(PK):** ID_Instalacion
```

---

## **HORARIO**
```
(ID_Entrenador, ID_Deporte, ID_Instalacion, Fecha, Hora_Inicio, Hora_Final)
- **(PK):** ID_Entrenador, ID_Deporte, ID_Instalacion
- **(FK):** ID_Entrenador, ID_Deporte, ID_Instalacion
```

---

## **RESERVA**
```
(ID_Deporte, ID_Instalacion, Fecha, Hora_Ini, Hora_Fin)
- **(PK):** ID_Deporte, ID_Instalacion
- **(FK):** ID_Deporte, ID_Instalacion
```

