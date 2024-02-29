from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime

app = Flask(__name__)

conexion = MySQL(app)


# USUARIOS

@app.route('/usuarios', methods = ['GET'])
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'id': fila[0], 'usuario': fila[1], 'email': fila[2], 'contraseña': fila[3], 'rol': fila[4], 'nombre': fila[5]} 
            usuarios.append(usuario)
        return jsonify({'usuarios': usuarios, 'mensaje': "Listado:"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/usuarios/<id>', methods = ['GET'])    
def leer_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            usuario = {'id': datos[0], 'usuario': datos[1], 'email': datos[2], 'contraseña': datos[3], 'rol': datos[4], 'nombre': datos[5]} 
            return jsonify({'usuario': usuario, 'mensaje': "Usuario encontrado"})
        else:
            return jsonify({'mensaje': "Usuario NO encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
        
@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        cursor = conexion.connection.cursor()
        hashed_password = generate_password_hash(request.json['contrasena'])
        
        sql = "INSERT INTO usuarios (usuario, email, contrasena, rol, nombre) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (request.json['usuario'], request.json['email'], hashed_password, request.json['rol'], request.json['nombre']))
        
        conexion.connection.commit()
        
        return jsonify({'mensaje': "Usuario registrado exitosamente"})
    except Exception as ex:
        return jsonify({'mensaje': f'Error al registrar usuario: {str(ex)}'}), 500

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario eliminado"})
    except Exception as ex:
        print("Error:", ex)
    return jsonify({'mensaje': "Error al eliminar usuario"})

@app.route('/usuarios/<id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        usuario = request.json['usuario']
        email = request.json['email']
        nombre = request.json['nombre']
        
        # Encripta la nueva contraseña si se proporciona
        nueva_contrasena = request.json.get('contrasena')
        if nueva_contrasena:
            nueva_contrasena = generate_password_hash(nueva_contrasena)
        
        sql = "UPDATE usuarios SET usuario = %s, email = %s, nombre = %s"
        params = [usuario, email, nombre]
        
        # Agregar la nueva contraseña al SQL y a los parámetros si se proporciona
        if nueva_contrasena:
            sql += ", contrasena = %s"
            params.append(nueva_contrasena)
        
        sql += " WHERE id = %s"
        params.append(id)
        
        cursor.execute(sql, params)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario actualizado"})
    except Exception as ex:
        return "Error"
    
# LOGIN

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('contrasena')

        cursor = conexion.connection.cursor()
        cursor.execute("SELECT id, contrasena FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            hashed_password = usuario[1]
            if check_password_hash(hashed_password, password):
                return jsonify({'mensaje': 'Usuario logueado correctamente'})
            else:
                return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401
        else:
            return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401

    except Exception as ex:
        return jsonify({'mensaje': 'Error en el servidor'}), 500

# PROYECTOS
    
@app.route('/proyectos', methods=['GET'])
def listar_proyecto():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT p.id, p.nombre, p.descripcion, p.fecha_inicio, u.nombre AS nombre_gerente FROM proyectos p INNER JOIN usuarios u ON p.gerente = u.id"
        cursor.execute(sql)
        datos = cursor.fetchall()
        proyectos = []
        for fila in datos:
            proyecto = {'id': fila[0], 'nombre': fila[1], 'descripcion': fila[2], 'fecha_inicio': fila[3], 'gerente': fila[4]} 
            proyectos.append(proyecto)
        return jsonify({'proyectos': proyectos, 'mensaje': "Listado:"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/proyectos/<id>', methods=['GET'])    
def leer_proyecto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT p.id, p.nombre, p.descripcion, p.fecha_inicio, u.nombre AS nombre_gerente FROM proyectos p INNER JOIN usuarios u ON p.gerente = u.id WHERE p.id = %s"
        cursor.execute(sql, (id,))
        datos = cursor.fetchone()
        if datos:
            proyecto = {'id': datos[0], 'nombre': datos[1], 'descripcion': datos[2], 'fecha_inicio': datos[3], 'gerente': datos[4]} 
            return jsonify({'proyecto': proyecto, 'mensaje': "Proyecto encontrado"})
        else:
            return jsonify({'mensaje': "Proyecto NO encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/proyectos/<id_usuario>', methods=['POST'])
def registrar_proyecto(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (id_usuario,))
        rol_usuario = cursor.fetchone()

        if rol_usuario[0] == 1:
            nombre = request.json['nombre']
            descripcion = request.json['descripcion']
            fecha_inicio = datetime.strptime(request.json['fecha_inicio'], '%Y-%m-%d').date()

            # Verificar si ya existe un proyecto con el mismo nombre
            cursor.execute("SELECT 1 FROM proyectos WHERE nombre = %s", (nombre,))
            proyecto_existente = cursor.fetchone()
            if proyecto_existente:
                return jsonify({'mensaje': 'Ya existe un proyecto con este nombre'}), 400

            # Si no hay un proyecto con el mismo nombre, proceder con la inserción
            cursor.execute("INSERT INTO proyectos (nombre, descripcion, fecha_inicio, gerente) VALUES (%s, %s, %s, %s)",
                           (nombre, descripcion, fecha_inicio, id_usuario))
            conexion.connection.commit()
            return jsonify({'mensaje': 'Proyecto creado correctamente'})
        else:
            return jsonify({'mensaje': 'Usuario no tiene permisos para crear proyectos'}), 403
    except Exception as ex:
        return jsonify({'mensaje': f"Error al registrar proyecto: {str(ex)}"}), 500

@app.route('/proyectos/<id_proyecto>/<id_usuario>', methods=['DELETE'])
def eliminar_proyecto(id_proyecto, id_usuario):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (id_usuario,))
        rol_usuario = cursor.fetchone()

        if rol_usuario and rol_usuario[0] == 1:
            sql = "DELETE FROM proyectos WHERE id = %s"
            cursor.execute(sql, (id_proyecto,))
            conexion.connection.commit()
            return jsonify({'mensaje': "Proyecto eliminado"})
        else:
            return jsonify({'mensaje': 'Usuario no tiene permisos para eliminar proyectos'}), 403
    except Exception as ex:
        return jsonify({'mensaje': "Error"}), 500

@app.route('/proyectos/<id_proyecto>/<id_usuario>', methods=['PUT'])
def actualizar_proyecto(id_proyecto, id_usuario):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (id_usuario,))
        rol_usuario = cursor.fetchone()
        if rol_usuario and rol_usuario[0] == 1:
            nombre = request.json['nombre']
            descripcion = request.json['descripcion']

            sql = "UPDATE proyectos SET nombre = %s, descripcion = %s WHERE id = %s"
            cursor.execute(sql, (nombre, descripcion, id_proyecto))
            conexion.connection.commit()
            return jsonify({'mensaje': "Proyecto actualizado"})
        else:
            return jsonify({'mensaje': 'Usuario no tiene permisos para actualizar proyectos'}), 403
    except Exception as ex:
        return jsonify({'mensaje': "Error"}), 500

# USUARIO_PROYECTO
    
@app.route('/asignar_usuario/<codigo1>/<codigo2>', methods=['POST'])
def asignar_usuario(codigo1, codigo2):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (codigo1,))
        rol_usuario = cursor.fetchone()

        if rol_usuario and rol_usuario[0] == 1:

            cursor.execute("SELECT id FROM proyectos WHERE id = %s", (codigo2,))
            proyecto_existente = cursor.fetchone()

            if proyecto_existente:
                usuario_id = request.json.get('usuario_id')

                cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
                rol_usuario_asignado = cursor.fetchone()

                if rol_usuario_asignado and rol_usuario_asignado[0] == 2:

                    cursor.execute("SELECT 1 FROM usuarios_proyectos WHERE usuario = %s AND proyecto = %s", (usuario_id, codigo2))
                    asignacion_existente = cursor.fetchone()

                    if asignacion_existente:
                        return jsonify({'mensaje': 'El usuario ya está asignado a este proyecto'}), 400
                    else:
                        cursor.execute("INSERT INTO usuarios_proyectos (usuario, proyecto) VALUES (%s, %s)", (usuario_id, codigo2))
                        conexion.connection.commit()

                        cursor.execute("SELECT usuario FROM usuarios WHERE id = %s", (usuario_id,))
                        nombre_usuario = cursor.fetchone()

                        return jsonify({'mensaje': f"Usuario {nombre_usuario[0]} asignado correctamente al proyecto {codigo2}"})
                else:
                    return jsonify({'mensaje': 'El usuario a asignar debe tener el rol 2 (desarrollador)'}), 403
            else:
                return jsonify({'mensaje': 'El proyecto especificado no existe'}), 404
        else:
            return jsonify({'mensaje': 'El usuario no tiene permisos para asignar usuarios al proyecto'}), 403
    except Exception as ex:
        return jsonify({'mensaje': 'Error en el servidor'}), 500

@app.route('/eliminar_usuario_proyecto/<int:usuario_id>/<int:proyecto_id>', methods=['DELETE'])
def eliminar_usuario_proyecto(usuario_id, proyecto_id):
    try:
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        elif usuario[0] != 1:
            return jsonify({'mensaje': 'El usuario no tiene permisos para realizar esta acción'}), 403

        if 'usuario' not in request.json:
            return jsonify({'mensaje': 'El cuerpo de la solicitud debe contener el ID del usuario'}), 400

        usuario_proyecto_id = request.json['usuario']

        cursor.execute("SELECT 1 FROM usuarios_proyectos WHERE usuario = %s AND proyecto = %s", (usuario_proyecto_id, proyecto_id))
        if cursor.fetchone() is None:
            return jsonify({'mensaje': 'El usuario no está asignado a este proyecto'}), 400
        
        cursor.execute("DELETE FROM usuarios_proyectos WHERE usuario = %s AND proyecto = %s", (usuario_proyecto_id, proyecto_id))
        conexion.connection.commit()
        
        cursor.close()

        return jsonify({'mensaje': 'Usuario eliminado del proyecto correctamente'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

@app.route('/proyectos_usuario/<usuario_id>', methods=['GET'])
def proyectos_usuario(usuario_id):
    try:
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        if usuario[0] == 1:
            cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyectos WHERE gerente = %s", (usuario_id,))
            proyectos = cursor.fetchall()
        else:
            cursor.execute("SELECT proyecto FROM usuarios_proyectos WHERE usuario = %s", (usuario_id,))
            proyectos_asignados = cursor.fetchall()

            proyectos = []
            for proyecto_asignado in proyectos_asignados:
                cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyectos WHERE id = %s", (proyecto_asignado,))
                proyecto = cursor.fetchone()
                if proyecto:
                    proyectos.append(proyecto)

        cursor.close()

        return jsonify({'proyectos': proyectos}), 200

    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500  

# HISTORIAS DE USUARIO

@app.route('/crear_historia_de_usuario', methods=['POST'])
def crear_historia_de_usuario():
    try:
        detalles = request.json.get('detalles')
        criterios = request.json.get('criterios')
        proyecto_id = request.json.get('proyecto')
        estado_id = request.json.get('estado')
        usuario_id = request.json.get('usuario')

        if not all([detalles, criterios, proyecto_id, estado_id, usuario_id]):
            return jsonify({'mensaje': 'Se requieren detalles, criterios, proyecto, estado y usuario'}), 400

        cursor = conexion.connection.cursor()

        # Verificar si el proyecto existe
        cursor.execute("SELECT 1 FROM proyectos WHERE id = %s", (proyecto_id,))
        if cursor.fetchone() is None:
            return jsonify({'mensaje': 'El proyecto especificado no existe'}), 404

        # Verificar si la historia de usuario ya existe en el proyecto
        cursor.execute("SELECT 1 FROM historias_de_usuario WHERE detalles = %s AND proyecto = %s", (detalles, proyecto_id))
        if cursor.fetchone() is not None:
            return jsonify({'mensaje': 'Ya existe una historia de usuario con los mismos detalles en este proyecto'}), 400

        # Verificar si el usuario existe y tiene el rol de gerente
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario is None or usuario[0] != 1:
            return jsonify({'mensaje': 'Solo los gerentes pueden agregar historias de usuario'}), 403

        cursor.execute("INSERT INTO historias_de_usuario (detalles, criterios, proyecto, estado, usuario) VALUES (%s, %s, %s, %s, %s)", (detalles, criterios, proyecto_id, estado_id, usuario_id))
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': 'Historia de usuario creada correctamente'}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

@app.route('/eliminar_historia_de_usuario/<int:historia_id>', methods=['DELETE'])
def eliminar_historia_de_usuario(historia_id):
    try:
        usuario_id = request.json.get('usuario')
        proyecto_id = request.json.get('proyecto')

        if usuario_id is None or proyecto_id is None:
            return jsonify({'mensaje': 'Se requieren usuario y proyecto'}), 400

        cursor = conexion.connection.cursor()

        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario is None or usuario[0] != 1:
            return jsonify({'mensaje': 'Solo los gerentes pueden eliminar historias de usuario'}), 403

        cursor.execute("SELECT 1 FROM proyectos WHERE id = %s", (proyecto_id,))
        if cursor.fetchone() is None:
            return jsonify({'mensaje': 'El proyecto especificado no existe'}), 404

        cursor.execute("SELECT 1 FROM historias_de_usuario WHERE id = %s AND proyecto = %s", (historia_id, proyecto_id))
        historia_existente = cursor.fetchone()
        if historia_existente is None:
            return jsonify({'mensaje': 'La historia de usuario especificada no existe o no pertenece al proyecto'}), 404

        # Eliminar todas las tareas asociadas a la historia de usuario
        cursor.execute("DELETE FROM tareas_ WHERE historias_de_usuario = %s", (historia_id,))
        
        # Luego, eliminar la historia de usuario
        cursor.execute("DELETE FROM historias_de_usuario WHERE id = %s", (historia_id,))
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': 'Historia de usuario eliminada correctamente'}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

@app.route('/historias_de_usuario/<int:proyecto_id>', methods=['GET'])
def leer_historias_de_usuario(proyecto_id):
    try:
        cursor = conexion.connection.cursor()

        # Obtener las historias de usuario del proyecto
        cursor.execute("SELECT id, detalles, criterios, estado FROM historias_de_usuario WHERE proyecto = %s", (proyecto_id,))
        historias = cursor.fetchall()

        cursor.close()

        if historias:
            historias_dict = [{'id': historia[0], 'detalles': historia[1], 'criterios': historia[2], 'estado': historia[3]} for historia in historias]
            return jsonify({'historias_de_usuario': historias_dict}), 200
        else:
            return jsonify({'mensaje': 'No se encontraron historias de usuario para el proyecto especificado'}), 404

    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

# TAREAS

@app.route('/crear_tarea', methods=['POST'])
def crear_tarea():
    try:
        descripcion = request.json.get('descripcion')
        estado_id = request.json.get('estado')
        historia_id = request.json.get('historia')
        usuario_id = request.json.get('usuario')

        if not all([descripcion, estado_id, historia_id, usuario_id]):
            return jsonify({'mensaje': 'Se requieren descripcion, estado, historia y usuario'}), 400

        cursor = conexion.connection.cursor()

        cursor.execute("SELECT proyecto FROM historias_de_usuario WHERE id = %s", (historia_id,))
        proyecto_id = cursor.fetchone()
        if proyecto_id is None:
            return jsonify({'mensaje': 'La historia de usuario especificada no existe'}), 404

        cursor.execute("SELECT 1 FROM estados WHERE id = %s", (estado_id,))
        if cursor.fetchone() is None:
            return jsonify({'mensaje': 'El estado especificado no existe'}), 404

        cursor.execute("SELECT 1 FROM tareas_ WHERE descripcion = %s AND historias_de_usuario = %s", (descripcion, historia_id))
        if cursor.fetchone() is not None:
            return jsonify({'mensaje': 'Ya existe una tarea con la misma descripción en esta historia de usuario'}), 409

        # Insertar la nueva tarea en la base de datos
        cursor.execute("INSERT INTO tareas_ (descripcion, estado, historias_de_usuario, usuario) VALUES (%s, %s, %s, %s)", (descripcion, estado_id, historia_id, usuario_id))
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': 'Tarea creada correctamente'}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

@app.route('/eliminar_tarea/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    try:
        usuario_id = request.json.get('usuario')
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        rol_usuario = cursor.fetchone()

        cursor.execute("SELECT 1 FROM tareas_ WHERE id = %s", (tarea_id,))
        tarea_existente = cursor.fetchone()
        if tarea_existente is None:
            return jsonify({'mensaje': 'La tarea especificada no existe'}), 404

        cursor.execute("DELETE FROM tareas_ WHERE id = %s", (tarea_id,))
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': 'Tarea eliminada correctamente'}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

@app.route('/tareas_por_historia/<int:historia_id>', methods=['GET'])
def tareas_por_historia(historia_id):
    try:
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT 1 FROM historias_de_usuario WHERE id = %s", (historia_id,))
        historia_existente = cursor.fetchone()
        if historia_existente is None:
            return jsonify({'mensaje': 'La historia de usuario especificada no existe'}), 404

        cursor.execute("SELECT id, descripcion, estado, usuario FROM tareas_ WHERE historias_de_usuario = %s", (historia_id,))
        tareas = cursor.fetchall()
        cursor.close()

        tareas_json = []
        for tarea in tareas:
            tarea_json = {
                'id': tarea[0],
                'descripcion': tarea[1],
                'estado': tarea[2],
                'usuario': tarea[3]
            }
            tareas_json.append(tarea_json)

        return jsonify({'tareas': tareas_json}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500

@app.route('/editar_tarea/<int:tarea_id>', methods=['PUT'])
def editar_tarea(tarea_id):
    try:
        # Obtener los datos de la tarea del cuerpo de la solicitud
        datos_tarea = request.json
        cursor = conexion.connection.cursor()
        # Verificar si la tarea existe
        cursor.execute("SELECT * FROM tareas_ WHERE id = %s", (tarea_id,))
        tarea_existente = cursor.fetchone()
        if tarea_existente is None:
            return jsonify({'mensaje': 'La tarea no existe'}), 404
        
        # Actualizar los detalles de la tarea en la base de datos
        cursor.execute("UPDATE tareas_ SET descripcion = %s WHERE id = %s", (datos_tarea['descripcion'], tarea_id))
        conexion.connection.commit()
        
        return jsonify({'mensaje': 'Tarea actualizada correctamente'}), 200
    
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    
# ACTUALIZACIONES_TAREAS
    
@app.route('/actualizar_estado_tarea/<int:tarea_id>', methods=['POST'])
def actualizar_estado_tarea(tarea_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT * FROM tareas_ WHERE id = %s", (tarea_id,))
        tarea_existente = cursor.fetchone()

        if tarea_existente:
            cursor.execute("SELECT estado FROM actualizacion_estado_tareas WHERE tarea = %s ORDER BY hora_actualizacion DESC LIMIT 1", (tarea_id,))
            ultimo_estado = cursor.fetchone()

            if ultimo_estado:
                nuevo_estado = ultimo_estado[0] + 1 if ultimo_estado[0] < 3 else ultimo_estado[0]

                cursor.execute("UPDATE tareas_ SET estado = %s WHERE id = %s", (nuevo_estado, tarea_id))
                conexion.connection.commit()

                hora_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO actualizacion_estado_tareas (tarea, estado, usuario, hora_actualizacion) VALUES (%s, %s, %s, %s)",
                               (tarea_id, nuevo_estado, tarea_existente[4], hora_actualizacion))
                conexion.connection.commit()

                cursor.close()

                return jsonify({'mensaje': f'Estado de la tarea actualizado correctamente a {nuevo_estado}'}), 200
            else:
                return jsonify({'mensaje': 'No se encontraron estados para esta tarea'}), 404
        else:
            return jsonify({'mensaje': 'La tarea no existe'}), 404

    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500

# ACTUALIZACIONES_HISTORIAS_DE_USUARIO
    
@app.route('/actualizar_estado_historia/<int:usuario_id>/<int:historia_usuario_id>', methods=['POST'])
def actualizar_estado_historia(usuario_id, historia_usuario_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        rol_usuario = cursor.fetchone()

        if rol_usuario and rol_usuario[0] == 1:
            cursor.execute("SELECT estado FROM tareas_ WHERE historias_de_usuario = %s", (historia_usuario_id,))
            estados_tareas = cursor.fetchall()

            if estados_tareas:
                if all(estado[0] == 1 for estado in estados_tareas):
                    nuevo_estado = 1
                elif any(estado[0] == 2 for estado in estados_tareas):
                    nuevo_estado = 2
                else:
                    nuevo_estado = 3

                cursor.execute("UPDATE historias_de_usuario SET estado = %s WHERE id = %s", (nuevo_estado, historia_usuario_id))
                conexion.connection.commit()


                hora_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO actualizacion_estado_historias_de_usuario (historias_de_usuario, estado, usuario, hora_actualizacion) VALUES (%s, %s, %s, %s)",
                               (historia_usuario_id, nuevo_estado, usuario_id, hora_actualizacion))
                conexion.connection.commit()

                return jsonify({'mensaje': f'Estado de la historia de usuario actualizado correctamente a {nuevo_estado}'}), 200
            else:
                return jsonify({'mensaje': 'No hay tareas asociadas a esta historia de usuario'}), 404
        else:
            return jsonify({'mensaje': 'No tienes permisos para actualizar el estado de esta historia de usuario'}), 403
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500  

# PAGINA

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe... </h1>", 404
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

