-- creacion

-- Script de Creación de Estructura para Nova Sports Club

-- 0. Función inmutable para calcular edad
CREATE OR REPLACE FUNCTION calcular_edad(fecha DATE)
RETURNS INT AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(fecha));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- 1. Creación de Tablas con Checks y Restricciones
SET client_encoding = 'UTF8';
-- Crear tabla de Socios
CREATE TABLE Socio (
    ID_Socio SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL CHECK (LENGTH(Nombre) > 0 AND LENGTH(Nombre) <= 100),
    Fecha_Nacimiento DATE NOT NULL,
    Apellido1 VARCHAR(100) NOT NULL CHECK (LENGTH(Apellido1) > 0 AND LENGTH(Apellido1) <= 100),
    Apellido2 VARCHAR(100)
);
-- Crear tabla de Pagos
CREATE TABLE Pago (
    ID_pago SERIAL PRIMARY KEY,
    ID_socio INT,
    Fecha_pago DATE,
    Monto NUMERIC(10,2) CHECK (Monto > 0),
    Estado VARCHAR(15) CHECK (Estado IN ('Completado', 'Pendiente')),
    Formato_pago VARCHAR(15) CHECK (Formato_pago IN ('Tarjeta', 'Efectivo')),
    FOREIGN KEY (ID_socio) REFERENCES Socio(ID_Socio) ON DELETE CASCADE
);

-- Crear tabla de Membresías
CREATE TABLE Membresia (
    Estado VARCHAR(15) CHECK (Estado IN ('Activa', 'Vencida')),
    ID_membresia SERIAL,
    ID_socio INT NOT NULL,
    Frecuencia VARCHAR(15) CHECK (Frecuencia IN ('Mensual', 'Trimestral', 'Semestral')),
    Categoria VARCHAR(15) CHECK (Categoria IN ('Infantil', 'Adulto', 'Senior')),
    Fecha_Inicio DATE CHECK (Fecha_Inicio <= CURRENT_DATE),
    Fecha_Vencimiento DATE GENERATED ALWAYS AS (
        CASE
            WHEN Frecuencia = 'Mensual' THEN Fecha_Inicio + INTERVAL '1 MONTH'
            WHEN Frecuencia = 'Trimestral' THEN Fecha_Inicio + INTERVAL '3 MONTH'
            WHEN Frecuencia = 'Semestral' THEN Fecha_Inicio + INTERVAL '6 MONTH'
        END
    ) STORED,
    Coste_Total NUMERIC(10,2) GENERATED ALWAYS AS (
        50 * 
        CASE
            WHEN Categoria = 'Infantil' THEN 0.90
            WHEN Categoria = 'Senior' THEN 0.95
            ELSE 1
        END *
        CASE
            WHEN Frecuencia = 'Mensual' THEN 1
            WHEN Frecuencia = 'Trimestral' THEN 0.95
            WHEN Frecuencia = 'Semestral' THEN 0.90
        END
    ) STORED,
    PRIMARY KEY (ID_membresia, ID_socio),
    FOREIGN KEY (ID_socio) REFERENCES Socio(ID_Socio) ON DELETE CASCADE
);

-- Crear tabla de Entrenadores
CREATE TABLE Entrenador (
    ID_Entrenador SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Sueldo NUMERIC(10,2) CHECK (Sueldo > 0),
    Seguridad_Social VARCHAR(50),
    CONSTRAINT chk_nombre_entrenador CHECK (Nombre ~ '^[A-Za-zÁÉÍÓÚÑáéíóúñ ]+$'),
    CONSTRAINT chk_seguridad_social CHECK (Seguridad_Social ~ '^[A-Z0-9]+$')
);

-- Crear tabla de Deportes
CREATE TABLE Deporte (
    ID_deporte SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL
);

-- Crear tabla instalacion
CREATE TABLE Instalacion (
    ID_instalacion SERIAL PRIMARY KEY,
    Capacidad INT CHECK (Capacidad > 0),
    Nombre VARCHAR(100) UNIQUE CHECK (LENGTH(Nombre) > 0 AND LENGTH(Nombre) <= 100),
    Direccion VARCHAR(100) CHECK (Direccion ~ '^[A-Za-z0-9\s,.]+$')
);



-- Crear tabla de Polideportivo
CREATE TABLE Polideportivo (
    ID_instalacion INT PRIMARY KEY,
    Capacidad INT CHECK (Capacidad > 0),
    Tipo VARCHAR(50),
    Nombre VARCHAR(100) CHECK (LENGTH(Nombre) > 0 AND LENGTH(Nombre) <= 100),
    Direccion VARCHAR(100) CHECK (direccion ~ '^[A-Za-z0-9\s,.]+$'),
    Tipo_suelo VARCHAR(50),
    FOREIGN KEY (ID_instalacion) REFERENCES Instalacion(ID_instalacion) ON DELETE CASCADE
);

-- Crear tabla de Sala
CREATE TABLE Sala (
    ID_instalacion INT PRIMARY KEY,
    Capacidad INT CHECK (Capacidad > 0),
    Tipo VARCHAR(50),
    Nombre VARCHAR(100) CHECK (LENGTH(Nombre) > 0 AND LENGTH(Nombre) <= 100),
    direccion VARCHAR(100) CHECK (direccion ~ '^[A-Za-z0-9\s,.]+$'),
    Superficie NUMERIC(10,2),
    FOREIGN KEY (ID_instalacion) REFERENCES Instalacion(ID_instalacion) ON DELETE CASCADE
);

-- Crear tabla de Piscina
CREATE TABLE Piscina (
    ID_instalacion INT PRIMARY KEY,
    Capacidad INT CHECK (Capacidad > 0),
    Tipo VARCHAR(50),
    Nombre VARCHAR(100) CHECK (LENGTH(Nombre) > 0 AND LENGTH(Nombre) <= 100),
    direccion VARCHAR(100) CHECK (direccion ~ '^[A-Za-z0-9\s,.]+$'),
    Temperatura NUMERIC(5,2) CHECK (Temperatura BETWEEN 0 AND 50),
    FOREIGN KEY (ID_instalacion) REFERENCES Instalacion(ID_instalacion) ON DELETE CASCADE
);


-- Crear tabla de Horarios
CREATE TABLE Horario (
    ID_entrenador INT,
    ID_deporte INT,
    ID_instalacion INT,
    Fecha DATE CHECK (Fecha >= CURRENT_DATE),
    Hora_inicio TIME CHECK (Hora_inicio < Hora_final),
    Hora_final TIME,
    PRIMARY KEY (ID_entrenador, ID_deporte, ID_instalacion),
    FOREIGN KEY (ID_entrenador) REFERENCES Entrenador(ID_Entrenador) ON DELETE SET NULL,
    FOREIGN KEY (ID_deporte) REFERENCES Deporte(ID_deporte) ON DELETE RESTRICT,
    FOREIGN KEY (ID_instalacion) REFERENCES Instalacion(ID_instalacion) ON DELETE RESTRICT,
    CONSTRAINT unique_deporte_horario UNIQUE (ID_deporte, Fecha, Hora_inicio)
);


CREATE TABLE Entrena (
    ID_entrenador INT,
    ID_deporte INT,
    ID_socio INT,
    PRIMARY KEY (ID_entrenador, ID_deporte, ID_socio),
    FOREIGN KEY (ID_entrenador) REFERENCES Entrenador(ID_Entrenador) ON DELETE CASCADE,
    FOREIGN KEY (ID_deporte) REFERENCES Deporte(ID_deporte) ON DELETE CASCADE,
    FOREIGN KEY (ID_socio) REFERENCES Socio(ID_Socio) ON DELETE CASCADE
);


-- Crear tabla de Reservas
CREATE TABLE Reserva (
    ID_deporte INT,
    ID_instalacion INT,
    Fecha DATE CHECK (Fecha >= CURRENT_DATE),
    Hora_ini TIME CHECK (Hora_ini < Hora_fin),
    Hora_fin TIME,
    PRIMARY KEY (ID_deporte, ID_instalacion, Fecha, Hora_ini),
    FOREIGN KEY (ID_deporte) REFERENCES Deporte(ID_deporte) ON DELETE RESTRICT,
    FOREIGN KEY (ID_instalacion) REFERENCES Instalacion(ID_instalacion) ON DELETE RESTRICT,
    CONSTRAINT unique_reserva UNIQUE (ID_deporte, ID_instalacion, Fecha, Hora_ini)
);




-- 2. Triggers para Actualización Automática

-- se eliminan membresias antes de socio

CREATE OR REPLACE FUNCTION eliminar_membresias_antes_de_socio()
RETURNS TRIGGER AS $$
BEGIN
    -- Borrar todas las membresías asociadas al socio que se va a eliminar
    DELETE FROM Membresia WHERE ID_socio = OLD.ID_socio;

    RETURN OLD; -- Permitir que la operación DELETE continúe
END;
$$ LANGUAGE plpgsql;

-- Crear el disparador en la tabla Socio
CREATE TRIGGER trg_eliminar_membresias
BEFORE DELETE ON Socio
FOR EACH ROW
EXECUTE FUNCTION eliminar_membresias_antes_de_socio();


-- Trigger para actualizar la categoría
-- Función para actualizar la categoría de membresía basada en la edad del socio
CREATE OR REPLACE FUNCTION actualizar_categoria_membresia()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar la categoría de membresía asociada al socio
    UPDATE Membresia
    SET Categoria = CASE
        WHEN calcular_edad(NEW.Fecha_Nacimiento) < 18 THEN 'Infantil'
        WHEN calcular_edad(NEW.Fecha_Nacimiento) BETWEEN 18 AND 59 THEN 'Adulto'
        ELSE 'Senior'
    END
    WHERE ID_socio = NEW.ID_socio;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear el Trigger asociado a la tabla Socio
CREATE TRIGGER trg_actualizar_categoria_membresia
AFTER UPDATE OF Fecha_Nacimiento ON Socio
FOR EACH ROW
EXECUTE FUNCTION actualizar_categoria_membresia();

-- Trigger para la verificacion de conflictos de horario_entrenador

CREATE OR REPLACE FUNCTION verificar_conflicto_horarios_entrenador()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si ya existe un horario conflictivo para el mismo entrenador
    IF EXISTS (
        SELECT 1
        FROM Horario
        WHERE ID_entrenador = NEW.ID_entrenador
          AND Fecha = NEW.Fecha
          AND (
              (NEW.Hora_inicio >= Hora_inicio AND NEW.Hora_inicio < Hora_final) OR
              (NEW.Hora_final > Hora_inicio AND NEW.Hora_final <= Hora_final) OR
              (NEW.Hora_inicio <= Hora_inicio AND NEW.Hora_final >= Hora_final)
          )
    ) THEN
        RAISE EXCEPTION 'Conflicto de horarios para el entrenador % en la fecha %', NEW.ID_entrenador, NEW.Fecha;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_verificar_conflicto_horarios_entrenador
BEFORE INSERT OR UPDATE ON Horario
FOR EACH ROW
EXECUTE FUNCTION verificar_conflicto_horarios_entrenador();

-- El entrenador no puede entrenar 2 deportes a la vez

CREATE OR REPLACE FUNCTION validar_conflicto_deportes_entrenador()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si el entrenador ya está entrenando otro deporte en el mismo horario
    IF EXISTS (
        SELECT 1
        FROM Horario
        WHERE ID_entrenador = NEW.ID_entrenador
          AND Fecha = NEW.Fecha
          AND (
              (NEW.Hora_inicio >= Horario.Hora_inicio AND NEW.Hora_inicio < Horario.Hora_final) OR
              (NEW.Hora_final > Horario.Hora_inicio AND NEW.Hora_final <= Horario.Hora_final) OR
              (NEW.Hora_inicio <= Horario.Hora_inicio AND NEW.Hora_final >= Horario.Hora_final)
          )
          AND ID_deporte != NEW.ID_deporte -- Validar que sean deportes diferentes
    ) THEN
        RAISE EXCEPTION 'El entrenador % no puede entrenar diferentes deportes al mismo tiempo.', NEW.ID_entrenador;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_conflicto_deportes_entrenador
BEFORE INSERT OR UPDATE ON Horario
FOR EACH ROW
EXECUTE FUNCTION validar_conflicto_deportes_entrenador();


-- Al menos  una membresia activa el socio

CREATE OR REPLACE FUNCTION validar_membresia_activa()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si el usuario tiene membresías activas
    IF EXISTS (
        SELECT 1 
        FROM Membresia
        WHERE ID_socio = OLD.ID_socio AND Estado = 'Activa'
    ) THEN
        RAISE EXCEPTION 'El usuario % debe tener al menos una membresía activa.', OLD.ID_socio;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_eliminacion_socio
BEFORE DELETE ON Socio
FOR EACH ROW
EXECUTE FUNCTION validar_membresia_activa();



-- Trigger para vactualizar el estado_membresia

CREATE OR REPLACE FUNCTION actualizar_estado_membresia()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualiza el estado solo si es diferente al esperado
    IF (NEW.Estado IS DISTINCT FROM 'Activa' AND CURRENT_DATE BETWEEN NEW.Fecha_Inicio AND NEW.Fecha_Vencimiento) THEN
        NEW.Estado := 'Activa';
    ELSIF (NEW.Estado IS DISTINCT FROM 'Vencida' AND CURRENT_DATE NOT BETWEEN NEW.Fecha_Inicio AND NEW.Fecha_Vencimiento) THEN
        NEW.Estado := 'Vencida';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trg_actualizar_estado_membresia
AFTER INSERT OR UPDATE ON Membresia
FOR EACH ROW
EXECUTE FUNCTION actualizar_estado_membresia();

-- Trigger para validar pagos
CREATE OR REPLACE FUNCTION validar_pago_correcto()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Monto < (SELECT Coste_Total FROM Membresia WHERE ID_socio = NEW.ID_socio) THEN
        RAISE EXCEPTION 'El monto pagado no es suficiente.';
    END IF;
    IF NEW.Fecha_pago > (SELECT Fecha_Vencimiento FROM Membresia WHERE ID_socio = NEW.ID_socio) THEN
        RAISE EXCEPTION 'El pago está fuera de tiempo.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validar_pago_correcto
BEFORE INSERT OR UPDATE ON Pago
FOR EACH ROW
EXECUTE FUNCTION validar_pago_correcto();

-- trigger para el conflicto de horarios de reserva y horarios
CREATE OR REPLACE FUNCTION verificar_conflicto_horarios()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si ya existe un horario que se solape con la nueva reserva
    IF EXISTS (
        SELECT 1
        FROM Horario
        WHERE Horario.ID_instalacion = NEW.ID_instalacion
          AND Horario.Fecha = NEW.Fecha
          AND (
              (NEW.Hora_ini >= Horario.Hora_inicio AND NEW.Hora_ini < Horario.Hora_final) OR
              (NEW.Hora_fin > Horario.Hora_inicio AND NEW.Hora_fin <= Horario.Hora_final) OR
              (NEW.Hora_ini <= Horario.Hora_inicio AND NEW.Hora_fin >= Horario.Hora_final)
          )
    ) THEN
        RAISE EXCEPTION 'No se puede reservar: conflicto con un horario existente en la instalación %', NEW.ID_instalacion;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_verificar_reserva_horario
BEFORE INSERT ON Reserva
FOR EACH ROW
EXECUTE FUNCTION verificar_conflicto_horarios();

--3 restriciones 

ALTER TABLE Membresia
ADD CONSTRAINT unique_id_socio UNIQUE (ID_socio);

ALTER TABLE Socio
ADD CONSTRAINT chk_fecha_nacimiento_pasada
CHECK (Fecha_Nacimiento <= CURRENT_DATE);
