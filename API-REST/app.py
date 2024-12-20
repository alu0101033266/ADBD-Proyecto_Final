from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        database="nova_sports_club",
        user="postgres",
        password="hyssen54"  # Cambia la contraseña si es necesario
    )

# **Rutas de la API REST**

####################### RUTAS DE SOCIO ################################

# Obtener todos los socios
@app.route('/api/socios', methods=['GET'])
def get_socios():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Socio;')
    socios = cur.fetchall()
    cur.close()
    conn.close()

    socios_list = [
        {"id": socio["id_socio"], "nombre": socio["nombre"], "apellido1": socio["apellido1"],
         "apellido2": socio["apellido2"], "fecha_nacimiento": str(socio["fecha_nacimiento"])}
        for socio in socios
    ]
    return jsonify(socios_list), 200

# Obtener un socio por ID
@app.route('/api/socios/<int:id>', methods=['GET'])
def get_socio(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Socio WHERE ID_Socio = %s;', (id,))
    socio = cur.fetchone()
    cur.close()
    conn.close()

    if socio is None:
        return jsonify({"error": "Socio no encontrado"}), 404

    socio_dict = {
        "id": socio["id_socio"], "nombre": socio["nombre"], "apellido1": socio["apellido1"],
        "apellido2": socio["apellido2"], "fecha_nacimiento": str(socio["fecha_nacimiento"])
    }
    return jsonify(socio_dict), 200

# Crear un nuevo socio
@app.route('/api/socios', methods=['POST'])
def create_socio():
    data = request.get_json()

    if not data or "nombre" not in data or "apellido1" not in data or "fecha_nacimiento" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Socio (Nombre, Fecha_Nacimiento, Apellido1, Apellido2) VALUES (%s, %s, %s, %s) RETURNING ID_Socio;',
        (data["nombre"], data["fecha_nacimiento"], data["apellido1"], data.get("apellido2"))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "message": "Socio creado exitosamente"}), 201

# Actualizar un socio
@app.route('/api/socios/<int:id>', methods=['PUT'])
def update_socio(id):
    data = request.get_json()

    if not data or "nombre" not in data or "apellido1" not in data or "fecha_nacimiento" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE Socio SET Nombre = %s, Fecha_Nacimiento = %s, Apellido1 = %s, Apellido2 = %s WHERE ID_Socio = %s;',
        (data["nombre"], data["fecha_nacimiento"], data["apellido1"], data.get("apellido2"), id)
    )
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Socio no encontrado"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Socio actualizado exitosamente"}), 200

# Eliminar un socio
@app.route('/api/socios/<int:id>', methods=['DELETE'])
def delete_socio(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Socio WHERE ID_Socio = %s;', (id,))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Socio no encontrado"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Socio eliminado exitosamente"}), 200


####################### RUTAS DE MEMBRESIA ################################

# **1. Obtener todas las membresías**
@app.route('/api/membresias', methods=['GET'])
def get_all_membresias():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Membresia;')
    membresias = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(membresias)

# **2. Obtener una membresía específica por ID**
@app.route('/api/membresias/<int:id>', methods=['GET'])
def get_membresia(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Membresia WHERE ID_membresia = %s;', (id,))
    membresia = cur.fetchone()
    cur.close()
    conn.close()

    if membresia is None:
        return jsonify({'error': 'Membresía no encontrada'}), 404
    return jsonify(membresia)

# **3. Crear una nueva membresía**
@app.route('/api/membresias', methods=['POST'])
def create_membresia():
    data = request.json

    # Validar que todos los campos necesarios estén presentes
    required_fields = ['ID_socio', 'Frecuencia', 'Categoria', 'Fecha_Inicio']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Falta el campo requerido: {field}'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Membresia (ID_socio, Frecuencia, Categoria, Fecha_Inicio, Estado)
            VALUES (%s, %s, %s, %s, %s) RETURNING ID_membresia;
            ''',
            (data['ID_socio'], data['Frecuencia'], data['Categoria'], data['Fecha_Inicio'], 'Activa')
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Membresía creada exitosamente', 'ID_membresia': new_id}), 201

# **4. Actualizar una membresía existente**
@app.route('/api/membresias/<int:id>', methods=['PUT'])
def update_membresia(id):
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Validar si la membresía existe
        cur.execute('SELECT * FROM Membresia WHERE ID_membresia = %s;', (id,))
        membresia = cur.fetchone()
        if not membresia:
            return jsonify({'error': 'Membresía no encontrada'}), 404

        # Actualizar los campos proporcionados
        cur.execute(
            '''
            UPDATE Membresia
            SET Frecuencia = %s, Categoria = %s, Fecha_Inicio = %s, Estado = %s
            WHERE ID_membresia = %s;
            ''',
            (
                data.get('Frecuencia', membresia[2]),  # Valor actual si no se envía
                data.get('Categoria', membresia[3]),
                data.get('Fecha_Inicio', membresia[4]),
                data.get('Estado', membresia[0]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Membresía actualizada exitosamente'})

# **5. Eliminar una membresía**
@app.route('/api/membresias/<int:id>', methods=['DELETE'])
def delete_membresia(id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Verificar si la membresía existe
        cur.execute('SELECT * FROM Membresia WHERE ID_membresia = %s;', (id,))
        membresia = cur.fetchone()
        if not membresia:
            return jsonify({'error': 'Membresía no encontrada'}), 404

        # Eliminar la membresía
        cur.execute('DELETE FROM Membresia WHERE ID_membresia = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Membresía eliminada exitosamente'})

    ####################### RUTAS DE PAGO ################################

# Obtener todos los pagos
@app.route('/api/pagos', methods=['GET'])
def get_pagos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Pago;')
    pagos = cur.fetchall()
    cur.close()
    conn.close()

    pagos_list = [
        {"id_pago": pago["id_pago"], "id_socio": pago["id_socio"], "fecha_pago": str(pago["fecha_pago"]),
         "monto": pago["monto"], "estado": pago["estado"], "formato_pago": pago["formato_pago"]}
        for pago in pagos
    ]
    return jsonify(pagos_list), 200

# Obtener un pago por ID
@app.route('/api/pagos/<int:id>', methods=['GET'])
def get_pago(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Pago WHERE ID_pago = %s;', (id,))
    pago = cur.fetchone()
    cur.close()
    conn.close()

    if pago is None:
        return jsonify({"error": "Pago no encontrado"}), 404

    pago_dict = {
        "id_pago": pago["id_pago"], "id_socio": pago["id_socio"], "fecha_pago": str(pago["fecha_pago"]),
        "monto": pago["monto"], "estado": pago["estado"], "formato_pago": pago["formato_pago"]
    }
    return jsonify(pago_dict), 200

# Crear un nuevo pago
@app.route('/api/pagos', methods=['POST'])
def create_pago():
    data = request.get_json()

    required_fields = ["id_socio", "fecha_pago", "monto", "estado", "formato_pago"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Pago (ID_socio, Fecha_pago, Monto, Estado, Formato_pago)
            VALUES (%s, %s, %s, %s, %s) RETURNING ID_pago;
            ''',
            (data["id_socio"], data["fecha_pago"], data["monto"], data["estado"], data["formato_pago"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_pago": new_id, "message": "Pago creado exitosamente"}), 201

# Actualizar un pago
@app.route('/api/pagos/<int:id>', methods=['PUT'])
def update_pago(id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Pago WHERE ID_pago = %s;', (id,))
        pago = cur.fetchone()
        if not pago:
            return jsonify({"error": "Pago no encontrado"}), 404

        cur.execute(
            '''
            UPDATE Pago
            SET ID_socio = %s, Fecha_pago = %s, Monto = %s, Estado = %s, Formato_pago = %s
            WHERE ID_pago = %s;
            ''',
            (
                data.get("id_socio", pago[1]),
                data.get("fecha_pago", pago[2]),
                data.get("monto", pago[3]),
                data.get("estado", pago[4]),
                data.get("formato_pago", pago[5]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Pago actualizado exitosamente"}), 200

# Eliminar un pago
@app.route('/api/pagos/<int:id>', methods=['DELETE'])
def delete_pago(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Pago WHERE ID_pago = %s;', (id,))
        pago = cur.fetchone()
        if not pago:
            return jsonify({"error": "Pago no encontrado"}), 404

        cur.execute('DELETE FROM Pago WHERE ID_pago = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Pago eliminado exitosamente"}), 200

####################### RUTAS DE ENTRENADOR ################################

# Obtener todos los entrenadores
@app.route('/api/entrenadores', methods=['GET'])
def get_entrenadores():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Entrenador;')
    entrenadores = cur.fetchall()
    cur.close()
    conn.close()

    entrenadores_list = [
        {"id_entrenador": entrenador["id_entrenador"], "nombre": entrenador["nombre"], 
         "sueldo": entrenador["sueldo"], "seguridad_social": entrenador["seguridad_social"]}
        for entrenador in entrenadores
    ]
    return jsonify(entrenadores_list), 200

# Obtener un entrenador por ID
@app.route('/api/entrenadores/<int:id>', methods=['GET'])
def get_entrenador(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Entrenador WHERE ID_Entrenador = %s;', (id,))
    entrenador = cur.fetchone()
    cur.close()
    conn.close()

    if entrenador is None:
        return jsonify({"error": "Entrenador no encontrado"}), 404

    entrenador_dict = {
        "id_entrenador": entrenador["id_entrenador"], "nombre": entrenador["nombre"], 
        "sueldo": entrenador["sueldo"], "seguridad_social": entrenador["seguridad_social"]
    }
    return jsonify(entrenador_dict), 200

# Crear un nuevo entrenador
@app.route('/api/entrenadores', methods=['POST'])
def create_entrenador():
    data = request.get_json()

    required_fields = ["nombre", "sueldo", "seguridad_social"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Entrenador (Nombre, Sueldo, Seguridad_Social)
            VALUES (%s, %s, %s) RETURNING ID_Entrenador;
            ''',
            (data["nombre"], data["sueldo"], data["seguridad_social"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_entrenador": new_id, "message": "Entrenador creado exitosamente"}), 201

# Actualizar un entrenador
@app.route('/api/entrenadores/<int:id>', methods=['PUT'])
def update_entrenador(id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Entrenador WHERE ID_Entrenador = %s;', (id,))
        entrenador = cur.fetchone()
        if not entrenador:
            return jsonify({"error": "Entrenador no encontrado"}), 404

        cur.execute(
            '''
            UPDATE Entrenador
            SET Nombre = %s, Sueldo = %s, Seguridad_Social = %s
            WHERE ID_Entrenador = %s;
            ''',
            (
                data.get("nombre", entrenador[1]),
                data.get("sueldo", entrenador[2]),
                data.get("seguridad_social", entrenador[3]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Entrenador actualizado exitosamente"}), 200

# Eliminar un entrenador
@app.route('/api/entrenadores/<int:id>', methods=['DELETE'])
def delete_entrenador(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Entrenador WHERE ID_Entrenador = %s;', (id,))
        entrenador = cur.fetchone()
        if not entrenador:
            return jsonify({"error": "Entrenador no encontrado"}), 404

        cur.execute('DELETE FROM Entrenador WHERE ID_Entrenador = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Entrenador eliminado exitosamente"}), 200
####################### RUTAS DE DEPORTE ################################

# Obtener todos los deportes
@app.route('/api/deportes', methods=['GET'])
def get_deportes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Deporte;')
    deportes = cur.fetchall()
    cur.close()
    conn.close()

    deportes_list = [
        {"id_deporte": deporte["id_deporte"], "nombre": deporte["nombre"]}
        for deporte in deportes
    ]
    return jsonify(deportes_list), 200

# Obtener un deporte por ID
@app.route('/api/deportes/<int:id>', methods=['GET'])
def get_deporte(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Deporte WHERE ID_Deporte = %s;', (id,))
    deporte = cur.fetchone()
    cur.close()
    conn.close()

    if deporte is None:
        return jsonify({"error": "Deporte no encontrado"}), 404

    deporte_dict = {"id_deporte": deporte["id_deporte"], "nombre": deporte["nombre"]}
    return jsonify(deporte_dict), 200

# Crear un nuevo deporte
@app.route('/api/deportes', methods=['POST'])
def create_deporte():
    data = request.get_json()

    if "nombre" not in data:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Deporte (Nombre)
            VALUES (%s) RETURNING ID_Deporte;
            ''',
            (data["nombre"],)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_deporte": new_id, "message": "Deporte creado exitosamente"}), 201

# Actualizar un deporte
@app.route('/api/deportes/<int:id>', methods=['PUT'])
def update_deporte(id):
    data = request.get_json()

    if "nombre" not in data:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Deporte WHERE ID_Deporte = %s;', (id,))
        deporte = cur.fetchone()
        if not deporte:
            return jsonify({"error": "Deporte no encontrado"}), 404

        cur.execute(
            '''
            UPDATE Deporte
            SET Nombre = %s
            WHERE ID_Deporte = %s;
            ''',
            (data["nombre"], id)
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Deporte actualizado exitosamente"}), 200

# Eliminar un deporte
@app.route('/api/deportes/<int:id>', methods=['DELETE'])
def delete_deporte(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Deporte WHERE ID_Deporte = %s;', (id,))
        deporte = cur.fetchone()
        if not deporte:
            return jsonify({"error": "Deporte no encontrado"}), 404

        cur.execute('DELETE FROM Deporte WHERE ID_Deporte = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Deporte eliminado exitosamente"}), 200

####################### RUTAS DE INSTALACION ################################

# Obtener todas las instalaciones
@app.route('/api/instalaciones', methods=['GET'])
def get_instalaciones():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Instalacion;')
    instalaciones = cur.fetchall()
    cur.close()
    conn.close()

    instalaciones_list = [
        {"id_instalacion": instalacion["id_instalacion"], "capacidad": instalacion["capacidad"], 
         "nombre": instalacion["nombre"], "direccion": instalacion["direccion"]}
        for instalacion in instalaciones
    ]
    return jsonify(instalaciones_list), 200

# Obtener una instalación por ID
@app.route('/api/instalaciones/<int:id>', methods=['GET'])
def get_instalacion(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Instalacion WHERE ID_Instalacion = %s;', (id,))
    instalacion = cur.fetchone()
    cur.close()
    conn.close()

    if instalacion is None:
        return jsonify({"error": "Instalación no encontrada"}), 404

    instalacion_dict = {
        "id_instalacion": instalacion["id_instalacion"], "capacidad": instalacion["capacidad"], 
        "nombre": instalacion["nombre"], "direccion": instalacion["direccion"]
    }
    return jsonify(instalacion_dict), 200

# Crear una nueva instalación
@app.route('/api/instalaciones', methods=['POST'])
def create_instalacion():
    data = request.get_json()

    required_fields = ["capacidad", "nombre", "direccion"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Instalacion (Capacidad, Nombre, Direccion)
            VALUES (%s, %s, %s) RETURNING ID_Instalacion;
            ''',
            (data["capacidad"], data["nombre"], data["direccion"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_instalacion": new_id, "message": "Instalación creada exitosamente"}), 201

# Actualizar una instalación
@app.route('/api/instalaciones/<int:id>', methods=['PUT'])
def update_instalacion(id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Instalacion WHERE ID_Instalacion = %s;', (id,))
        instalacion = cur.fetchone()
        if not instalacion:
            return jsonify({"error": "Instalación no encontrada"}), 404

        cur.execute(
            '''
            UPDATE Instalacion
            SET Capacidad = %s, Nombre = %s, Direccion = %s
            WHERE ID_Instalacion = %s;
            ''',
            (
                data.get("capacidad", instalacion[1]),
                data.get("nombre", instalacion[2]),
                data.get("direccion", instalacion[3]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Instalación actualizada exitosamente"}), 200

# Eliminar una instalación
@app.route('/api/instalaciones/<int:id>', methods=['DELETE'])
def delete_instalacion(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Instalacion WHERE ID_Instalacion = %s;', (id,))
        instalacion = cur.fetchone()
        if not instalacion:
            return jsonify({"error": "Instalación no encontrada"}), 404

        cur.execute('DELETE FROM Instalacion WHERE ID_Instalacion = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Instalación eliminada exitosamente"}), 200
####################### RUTAS DE POLIDEPORTIVO ################################

# Obtener todos los polideportivos
@app.route('/api/polideportivos', methods=['GET'])
def get_polideportivos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Polideportivo;')
    polideportivos = cur.fetchall()
    cur.close()
    conn.close()

    polideportivos_list = [
        {"id_instalacion": polideportivo["id_instalacion"], "capacidad": polideportivo["capacidad"], 
         "tipo": polideportivo["tipo"], "nombre": polideportivo["nombre"], 
         "direccion": polideportivo["direccion"], "tipo_suelo": polideportivo["tipo_suelo"]}
        for polideportivo in polideportivos
    ]
    return jsonify(polideportivos_list), 200

# Obtener un polideportivo por ID
@app.route('/api/polideportivos/<int:id>', methods=['GET'])
def get_polideportivo(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Polideportivo WHERE ID_Instalacion = %s;', (id,))
    polideportivo = cur.fetchone()
    cur.close()
    conn.close()

    if polideportivo is None:
        return jsonify({"error": "Polideportivo no encontrado"}), 404

    polideportivo_dict = {
        "id_instalacion": polideportivo["id_instalacion"], "capacidad": polideportivo["capacidad"], 
        "tipo": polideportivo["tipo"], "nombre": polideportivo["nombre"], 
        "direccion": polideportivo["direccion"], "tipo_suelo": polideportivo["tipo_suelo"]
    }
    return jsonify(polideportivo_dict), 200

# Crear un nuevo polideportivo
@app.route('/api/polideportivos', methods=['POST'])
def create_polideportivo():
    data = request.get_json()

    required_fields = ["capacidad", "tipo", "nombre", "direccion", "tipo_suelo"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Polideportivo (Capacidad, Tipo, Nombre, Direccion, Tipo_Suelo)
            VALUES (%s, %s, %s, %s, %s) RETURNING ID_Instalacion;
            ''',
            (data["capacidad"], data["tipo"], data["nombre"], data["direccion"], data["tipo_suelo"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_instalacion": new_id, "message": "Polideportivo creado exitosamente"}), 201

# Actualizar un polideportivo
@app.route('/api/polideportivos/<int:id>', methods=['PUT'])
def update_polideportivo(id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Polideportivo WHERE ID_Instalacion = %s;', (id,))
        polideportivo = cur.fetchone()
        if not polideportivo:
            return jsonify({"error": "Polideportivo no encontrado"}), 404

        cur.execute(
            '''
            UPDATE Polideportivo
            SET Capacidad = %s, Tipo = %s, Nombre = %s, Direccion = %s, Tipo_Suelo = %s
            WHERE ID_Instalacion = %s;
            ''',
            (
                data.get("capacidad", polideportivo[1]),
                data.get("tipo", polideportivo[2]),
                data.get("nombre", polideportivo[3]),
                data.get("direccion", polideportivo[4]),
                data.get("tipo_suelo", polideportivo[5]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Polideportivo actualizado exitosamente"}), 200

# Eliminar un polideportivo
@app.route('/api/polideportivos/<int:id>', methods=['DELETE'])
def delete_polideportivo(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Polideportivo WHERE ID_Instalacion = %s;', (id,))
        polideportivo = cur.fetchone()
        if not polideportivo:
            return jsonify({"error": "Polideportivo no encontrado"}), 404

        cur.execute('DELETE FROM Polideportivo WHERE ID_Instalacion = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Polideportivo eliminado exitosamente"}), 200
    ####################### RUTAS DE SALA ################################

# Obtener todas las salas
@app.route('/api/salas', methods=['GET'])
def get_salas():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Sala;')
    salas = cur.fetchall()
    cur.close()
    conn.close()

    salas_list = [
        {"id_instalacion": sala["id_instalacion"], "capacidad": sala["capacidad"], 
         "tipo": sala["tipo"], "nombre": sala["nombre"], 
         "direccion": sala["direccion"], "superficie": sala["superficie"]}
        for sala in salas
    ]
    return jsonify(salas_list), 200

# Obtener una sala por ID
@app.route('/api/salas/<int:id>', methods=['GET'])
def get_sala(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Sala WHERE ID_Instalacion = %s;', (id,))
    sala = cur.fetchone()
    cur.close()
    conn.close()

    if sala is None:
        return jsonify({"error": "Sala no encontrada"}), 404

    sala_dict = {
        "id_instalacion": sala["id_instalacion"], "capacidad": sala["capacidad"], 
        "tipo": sala["tipo"], "nombre": sala["nombre"], 
        "direccion": sala["direccion"], "superficie": sala["superficie"]
    }
    return jsonify(sala_dict), 200

# Crear una nueva sala
@app.route('/api/salas', methods=['POST'])
def create_sala():
    data = request.get_json()

    required_fields = ["capacidad", "tipo", "nombre", "direccion", "superficie"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Sala (Capacidad, Tipo, Nombre, Direccion, Superficie)
            VALUES (%s, %s, %s, %s, %s) RETURNING ID_Instalacion;
            ''',
            (data["capacidad"], data["tipo"], data["nombre"], data["direccion"], data["superficie"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_instalacion": new_id, "message": "Sala creada exitosamente"}), 201

# Actualizar una sala
@app.route('/api/salas/<int:id>', methods=['PUT'])
def update_sala(id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Sala WHERE ID_Instalacion = %s;', (id,))
        sala = cur.fetchone()
        if not sala:
            return jsonify({"error": "Sala no encontrada"}), 404

        cur.execute(
            '''
            UPDATE Sala
            SET Capacidad = %s, Tipo = %s, Nombre = %s, Direccion = %s, Superficie = %s
            WHERE ID_Instalacion = %s;
            ''',
            (
                data.get("capacidad", sala[1]),
                data.get("tipo", sala[2]),
                data.get("nombre", sala[3]),
                data.get("direccion", sala[4]),
                data.get("superficie", sala[5]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Sala actualizada exitosamente"}), 200

# Eliminar una sala
@app.route('/api/salas/<int:id>', methods=['DELETE'])
def delete_sala(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Sala WHERE ID_Instalacion = %s;', (id,))
        sala = cur.fetchone()
        if not sala:
            return jsonify({"error": "Sala no encontrada"}), 404

        cur.execute('DELETE FROM Sala WHERE ID_Instalacion = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Sala eliminada exitosamente"}), 200

####################### RUTAS DE PISCINA ################################

# Obtener todas las piscinas
@app.route('/api/piscinas', methods=['GET'])
def get_piscinas():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Piscina;')
    piscinas = cur.fetchall()
    cur.close()
    conn.close()

    piscinas_list = [
        {"id_instalacion": piscina["id_instalacion"], "capacidad": piscina["capacidad"], 
         "tipo": piscina["tipo"], "nombre": piscina["nombre"], 
         "direccion": piscina["direccion"], "temperatura": piscina["temperatura"]}
        for piscina in piscinas
    ]
    return jsonify(piscinas_list), 200

# Obtener una piscina por ID
@app.route('/api/piscinas/<int:id>', methods=['GET'])
def get_piscina(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Piscina WHERE ID_Instalacion = %s;', (id,))
    piscina = cur.fetchone()
    cur.close()
    conn.close()

    if piscina is None:
        return jsonify({"error": "Piscina no encontrada"}), 404

    piscina_dict = {
        "id_instalacion": piscina["id_instalacion"], "capacidad": piscina["capacidad"], 
        "tipo": piscina["tipo"], "nombre": piscina["nombre"], 
        "direccion": piscina["direccion"], "temperatura": piscina["temperatura"]
    }
    return jsonify(piscina_dict), 200

# Crear una nueva piscina
@app.route('/api/piscinas', methods=['POST'])
def create_piscina():
    data = request.get_json()

    required_fields = ["capacidad", "tipo", "nombre", "direccion", "temperatura"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Piscina (Capacidad, Tipo, Nombre, Direccion, Temperatura)
            VALUES (%s, %s, %s, %s, %s) RETURNING ID_Instalacion;
            ''',
            (data["capacidad"], data["tipo"], data["nombre"], data["direccion"], data["temperatura"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"id_instalacion": new_id, "message": "Piscina creada exitosamente"}), 201

# Actualizar una piscina
@app.route('/api/piscinas/<int:id>', methods=['PUT'])
def update_piscina(id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Piscina WHERE ID_Instalacion = %s;', (id,))
        piscina = cur.fetchone()
        if not piscina:
            return jsonify({"error": "Piscina no encontrada"}), 404

        cur.execute(
            '''
            UPDATE Piscina
            SET Capacidad = %s, Tipo = %s, Nombre = %s, Direccion = %s, Temperatura = %s
            WHERE ID_Instalacion = %s;
            ''',
            (
                data.get("capacidad", piscina[1]),
                data.get("tipo", piscina[2]),
                data.get("nombre", piscina[3]),
                data.get("direccion", piscina[4]),
                data.get("temperatura", piscina[5]),
                id
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Piscina actualizada exitosamente"}), 200

# Eliminar una piscina
@app.route('/api/piscinas/<int:id>', methods=['DELETE'])
def delete_piscina(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Piscina WHERE ID_Instalacion = %s;', (id,))
        piscina = cur.fetchone()
        if not piscina:
            return jsonify({"error": "Piscina no encontrada"}), 404

        cur.execute('DELETE FROM Piscina WHERE ID_Instalacion = %s;', (id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Piscina eliminada exitosamente"}), 200
####################### RUTAS DE HORARIO ################################

# Obtener todos los horarios
@app.route('/api/horarios', methods=['GET'])
def get_horarios():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Horario;')
    horarios = cur.fetchall()
    cur.close()
    conn.close()

    horarios_list = [
        {"id_entrenador": horario["id_entrenador"], "id_deporte": horario["id_deporte"], 
         "id_instalacion": horario["id_instalacion"], "fecha": str(horario["fecha"]),
         "hora_inicio": str(horario["hora_inicio"]), "hora_final": str(horario["hora_final"])}
        for horario in horarios
    ]
    return jsonify(horarios_list), 200

# Crear un horario
@app.route('/api/horarios', methods=['POST'])
def create_horario():
    data = request.get_json()

    required_fields = ["id_entrenador", "id_deporte", "id_instalacion", "fecha", "hora_inicio", "hora_final"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Horario (ID_entrenador, ID_deporte, ID_instalacion, Fecha, Hora_inicio, Hora_final)
            VALUES (%s, %s, %s, %s, %s, %s);
            ''',
            (data["id_entrenador"], data["id_deporte"], data["id_instalacion"], data["fecha"], data["hora_inicio"], data["hora_final"])
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Horario creado exitosamente"}), 201

# Eliminar un horario
@app.route('/api/horarios', methods=['DELETE'])
def delete_horario():
    data = request.get_json()

    required_fields = ["id_entrenador", "id_deporte", "id_instalacion"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            DELETE FROM Horario
            WHERE ID_entrenador = %s AND ID_deporte = %s AND ID_instalacion = %s;
            ''',
            (data["id_entrenador"], data["id_deporte"], data["id_instalacion"])
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Horario eliminado exitosamente"}), 200

####################### RUTAS DE RESERVA ################################

# Obtener todas las reservas
@app.route('/api/reservas', methods=['GET'])
def get_reservas():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Reserva;')
    reservas = cur.fetchall()
    cur.close()
    conn.close()

    reservas_list = [
        {"id_deporte": reserva["id_deporte"], "id_instalacion": reserva["id_instalacion"], 
         "fecha": str(reserva["fecha"]), "hora_ini": str(reserva["hora_ini"]), 
         "hora_fin": str(reserva["hora_fin"])}
        for reserva in reservas
    ]
    return jsonify(reservas_list), 200

# Crear una reserva
@app.route('/api/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()

    required_fields = ["id_deporte", "id_instalacion", "fecha", "hora_ini", "hora_fin"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Reserva (ID_deporte, ID_instalacion, Fecha, Hora_ini, Hora_fin)
            VALUES (%s, %s, %s, %s, %s);
            ''',
            (data["id_deporte"], data["id_instalacion"], data["fecha"], data["hora_ini"], data["hora_fin"])
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Reserva creada exitosamente"}), 201

# Eliminar una reserva
@app.route('/api/reservas', methods=['DELETE'])
def delete_reserva():
    data = request.get_json()

    required_fields = ["id_deporte", "id_instalacion", "fecha", "hora_ini"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            DELETE FROM Reserva
            WHERE ID_deporte = %s AND ID_instalacion = %s AND Fecha = %s AND Hora_ini = %s;
            ''',
            (data["id_deporte"], data["id_instalacion"], data["fecha"], data["hora_ini"])
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Reserva eliminada exitosamente"}), 200

####################### RUTAS DE ENTRENA ################################

# Obtener todos los registros de Entrena
@app.route('/api/entrena', methods=['GET'])
def get_entrena():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Entrena;')
    entrenas = cur.fetchall()
    cur.close()
    conn.close()

    entrenas_list = [
        {"id_entrenador": entrena["id_entrenador"], "id_deporte": entrena["id_deporte"], 
         "id_socio": entrena["id_socio"]}
        for entrena in entrenas
    ]
    return jsonify(entrenas_list), 200

# Crear un registro de Entrena
@app.route('/api/entrena', methods=['POST'])
def create_entrena():
    data = request.get_json()

    required_fields = ["id_entrenador", "id_deporte", "id_socio"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO Entrena (ID_entrenador, ID_deporte, ID_socio)
            VALUES (%s, %s, %s);
            ''',
            (data["id_entrenador"], data["id_deporte"], data["id_socio"])
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Registro de Entrena creado exitosamente"}), 201

# Eliminar un registro de Entrena
@app.route('/api/entrena', methods=['DELETE'])
def delete_entrena():
    data = request.get_json()

    required_fields = ["id_entrenador", "id_deporte", "id_socio"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''
            DELETE FROM Entrena
            WHERE ID_entrenador = %s AND ID_deporte = %s AND ID_socio = %s;
            ''',
            (data["id_entrenador"], data["id_deporte"], data["id_socio"])
        )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Registro de Entrena eliminado exitosamente"}), 200

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
