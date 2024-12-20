
/*************


INSERTAR

**************/

-- **Script de Inserciones y Consultas para Nova Sports Club**

-- **Inserciones en la Base de Datos**

-- Inserciones en Socio
INSERT INTO Socio (Nombre, Fecha_Nacimiento, Apellido1, Apellido2) VALUES
('Juan', '1990-05-20', 'Perez', 'Gomez'),
('Maria', '1985-07-15', 'Lopez', 'Lopez'),
('Pedro', '2010-01-01', 'Gonzalez', 'Martinez'),
('Carlos', '2000-11-02', 'Sanchez', 'Martinez');

-- Inserciones en Pago
INSERT INTO Pago (ID_socio, Fecha_pago, Monto, Estado, Formato_pago) VALUES
(1, '2023-12-01', 50.00, 'Completado', 'Tarjeta'),
(2, '2023-12-05', 150.00, 'Completado', 'Tarjeta'),
(3, '2023-12-10', 500.00, 'Pendiente', 'Efectivo');

-- Inserciones en Membresia
INSERT INTO Membresia (Estado, ID_socio, Frecuencia, Categoria, Fecha_Inicio) VALUES
('Activa', 1, 'Mensual', 'Adulto', '2024-12-01'),
('Activa', 2, 'Trimestral', 'Senior', '2024-12-01'),
('Activa', 3, 'Semestral', 'Infantil', '2024-12-01'),
('Activa', 4, 'Mensual', 'Adulto', '2024-01-01');

-- Inserciones en Entrenador
INSERT INTO Entrenador (Nombre, Sueldo, Seguridad_Social) VALUES
('Luis Garcia', 2000.00, 'A1234567B'),
('Ana Rodriguez', 2500.00, 'B2345678C');

-- Inserciones en Deporte
INSERT INTO Deporte (Nombre) VALUES
('Baloncesto'),
('Natacion'),
('Yoga');

-- Inserciones en Entrena
INSERT INTO Entrena (ID_entrenador, ID_deporte, ID_socio)
VALUES 
(1, 1, 1),
(2, 2, 2);


-- Inserciones en la tabla Instalacion
INSERT INTO Instalacion (Capacidad, Nombre, Direccion) VALUES
(200, 'Polideportivo Central', 'Calle Principal 123'),
(150, 'Polideportivo Norte', 'Avenida Norte 45'),
(50, 'Sala Yoga', 'Calle Secundaria 56'),
(30, 'Sala Boxeo', 'Avenida Sur 78'),
(20, 'Piscina Climatizada Central', 'Calle del Agua 90'),
(15, 'Piscina Exterior Norte', 'Calle del Lago 22');

-- Inserciones en Polideportivo
INSERT INTO Polideportivo (ID_instalacion, Capacidad, Tipo, Nombre, Direccion, Tipo_suelo) VALUES
(1, 200, 'Interior', 'Polideportivo Central', 'Calle Principal 123', 'Madera'),
(2, 150, 'Exterior', 'Polideportivo Norte', 'Avenida Norte 45', 'Cemento');

-- Inserciones en Sala
INSERT INTO Sala (ID_instalacion, Capacidad, Tipo, Nombre, Direccion, Superficie) VALUES
(3, 50, 'Interior', 'Sala Yoga', 'Calle Secundaria 56', 120.5),
(4, 30, 'Interior', 'Sala Boxeo', 'Avenida Sur 78', 60.3);

-- Inserciones en Piscina
INSERT INTO Piscina (ID_instalacion, Capacidad, Tipo, Nombre, Direccion, Temperatura) VALUES
(5, 20, 'Climatizada', 'Piscina Climatizada Central', 'Calle del Agua 90', 28.5),
(6, 15, 'Exterior', 'Piscina Exterior Norte', 'Calle del Lago 22', 24.0);

-- Inserciones en Horario
INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final) VALUES
(1, 1, 1, '2025-01-20', '10:00:00', '12:00:00'),
(2, 2, 2, '2025-01-21', '14:00:00', '16:00:00');

-- Inserciones en Reserva
INSERT INTO Reserva (ID_deporte, ID_instalacion, Fecha, Hora_ini, Hora_fin) VALUES
(1, 1, '2025-01-22', '10:00:00', '12:00:00'),
(2, 2, '2025-01-23', '14:00:00', '16:00:00');

-- **Consultas de Prueba**

-- Consulta de todos los socios
SELECT * FROM Socio;

-- Consulta de todos los pagos
SELECT * FROM Pago;

-- Consulta de todas las membresias
SELECT * FROM Membresia;

-- Consulta de todos los entrenadores
SELECT * FROM Entrenador;

-- Consulta de todos los deportes
SELECT * FROM Deporte;

-- Consulta de todos los polideportivos
SELECT * FROM Polideportivo;

-- Consulta de todas las salas
SELECT * FROM Sala;

-- Consulta de todas las piscinas
SELECT * FROM Piscina;

-- Consulta de todos los horarios
SELECT * FROM Horario;

-- Consulta de todas las reservas
SELECT * FROM Reserva;

-- Consulta de todas las personas entrenadas
SELECT * FROM Entrena;

-- Consultade todas las instalaciones
SELECT * FROM Instalacion;


/***** membresia actualizada
SELECT * FROM Membresia WHERE ID_socio = 4;

UPDATE Socio
SET Fecha_Nacimiento = '1995-01-01'
WHERE ID_socio = 4;

-- Verificar la membresía actualizada
SELECT * FROM Membresia WHERE ID_socio = 4;

UPDATE Socio
SET Fecha_Nacimiento = '1950-01-01'
WHERE ID_socio = 4;

-- Verificar la membresía actualizada
SELECT * FROM Membresia WHERE ID_socio = 4;
*****/


/***** conflicto horario entrenador
-- Horario válido (sin conflictos)
INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final)
VALUES (1, 1, 1, '2025-01-20', '10:00:00', '12:00:00');

-- Otro horario válido (sin conflictos)
INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final)
VALUES (1, 2, 2, '2025-01-20', '12:00:00', '14:00:00');

-- Este horario tiene un conflicto (solapamiento con un horario existente)
INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final)
VALUES (1, 1, 1, '2025-01-20', '11:30:00', '13:00:00'); -- Debería generar error.

********/

/* membresia activa
DELETE FROM Membresia WHERE ID_membresia = 4;

-- Resultado:
-- ERROR: El usuario 4 debe tener al menos una membresía activa.
*/
/*
INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final)
VALUES (1, 1, 1, '2025-01-20', '10:00:00', '12:00:00');

-- Resultado:
-- Inserción exitosa.

INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final)
VALUES (1, 2, 2, '2025-01-20', '11:00:00', '13:00:00');

-- Resultado:
-- ERROR: El entrenador 1 no puede entrenar diferentes deportes al mismo tiempo.
*/