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
            usuario = {'id': fila[0], 'usuario': fila[1], 'email': fila[2], 'contraseña': fila[3], 'rol': fila[4]} 
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
            usuario = {'id': datos[0], 'usuario': datos[1], 'email': datos[2], 'contraseña': datos[3], 'rol': datos[4]} 
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
        return "Error"
    
@app.route('/usuarios/<id>', methods = ['DELETE'])

def eliminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM usuarios WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario eliminado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
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
    
#Esto solo lo puede hacer un administrador, el id 1
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

            cursor.execute("INSERT INTO proyectos (nombre, descripcion, fecha_inicio, gerente) VALUES (%s, %s, %s, %s)",
                           (nombre, descripcion, fecha_inicio, id_usuario))
            conexion.connection.commit()
            return jsonify({'mensaje': 'Proyecto creado correctamente'})
        else:
            return jsonify({'mensaje': 'Usuario no tiene permisos para crear proyectos'}), 403
    except Exception as ex:
        return "Error"

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


# LOGIN
   #seguir intentando despues!! 
@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('contrasena')

        cursor = conexion.connection.cursor()
        cursor.execute("SELECT id, contrasena FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Verifica que la contraseña coincida utilizando Werkzeug
            hashed_password = usuario[1]
            if check_password_hash(hashed_password, password):
                return jsonify({'mensaje': 'Usuario logueado correctamente'})
            else:
                return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401
        else:
            return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401

    except Exception as ex:
        return jsonify({'mensaje': 'Error en el servidor'}), 500

# USUARIO_PROYECTO
    
@app.route('/asignar_usuario/<codigo1>/<codigo2>', methods=['POST'])
def asignar_usuario(codigo1, codigo2):
    try:
        # Verifica si el usuario con codigo1 tiene rol 1
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (codigo1,))
        rol_usuario = cursor.fetchone()

        if rol_usuario and rol_usuario[0] == 1:
            # El usuario tiene el rol 1 (gerente), puede asignar usuarios al proyecto

            # Verifica si el proyecto con codigo2 existe
            cursor.execute("SELECT id FROM proyectos WHERE id = %s", (codigo2,))
            proyecto_existente = cursor.fetchone()

            if proyecto_existente:
                # El proyecto existe, se puede asignar un usuario
                usuario_id = request.json.get('usuario_id')

                # Verifica si el usuario_id corresponde a un usuario con rol 2
                cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
                rol_usuario_asignado = cursor.fetchone()

                if rol_usuario_asignado and rol_usuario_asignado[0] == 2:
                    # El usuario a asignar tiene el rol 2 (desarrollador), se puede agregar al proyecto

                    # Verifica si el usuario ya está asignado al proyecto
                    cursor.execute("SELECT 1 FROM usuarios_proyectos WHERE usuario = %s AND proyecto = %s", (usuario_id, codigo2))
                    asignacion_existente = cursor.fetchone()

                    if asignacion_existente:
                        return jsonify({'mensaje': 'El usuario ya está asignado a este proyecto'}), 400
                    else:
                        # Inserta el registro en la tabla usuarios_proyectos
                        cursor.execute("INSERT INTO usuarios_proyectos (usuario, proyecto) VALUES (%s, %s)", (usuario_id, codigo2))
                        conexion.connection.commit()

                        # Recupera el nombre del usuario asignado
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

        # Verificar el rol del usuario
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        elif usuario[0] != 1:
            return jsonify({'mensaje': 'El usuario no tiene permisos para realizar esta acción'}), 403

        # Verificar si el ID del usuario a eliminar está presente en el cuerpo de la solicitud
        if 'usuario' not in request.json:
            return jsonify({'mensaje': 'El cuerpo de la solicitud debe contener el ID del usuario'}), 400

        usuario_proyecto_id = request.json['usuario']

        # Verificar si el usuario está asignado a este proyecto
        cursor.execute("SELECT 1 FROM usuarios_proyectos WHERE usuario = %s AND proyecto = %s", (usuario_proyecto_id, proyecto_id))
        if cursor.fetchone() is None:
            return jsonify({'mensaje': 'El usuario no está asignado a este proyecto'}), 400
        
        # Eliminar al usuario del proyecto
        cursor.execute("DELETE FROM usuarios_proyectos WHERE usuario = %s AND proyecto = %s", (usuario_proyecto_id, proyecto_id))
        conexion.connection.commit()
        
        # Cerrar el cursor
        cursor.close()

        return jsonify({'mensaje': 'Usuario eliminado del proyecto correctamente'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en el servidor: ' + str(e)}), 500


@app.route('/proyectos_usuario/<usuario_id>', methods=['GET'])
def proyectos_usuario(usuario_id):
    try:
        # Crear el cursor dentro de la función
        cursor = conexion.connection.cursor()

        # Verificar el rol del usuario
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        if usuario[0] == 1:
            # Si es rol 1, obtener todos los proyectos donde el gerente sea el usuario
            cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyectos WHERE gerente = %s", (usuario_id,))
            proyectos = cursor.fetchall()
        else:
            # Si es rol 2, obtener todos los proyectos donde el usuario esté asignado
            cursor.execute("SELECT proyecto FROM usuarios_proyectos WHERE usuario = %s", (usuario_id,))
            proyectos_asignados = cursor.fetchall()

            proyectos = []
            for proyecto_asignado in proyectos_asignados:
                cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyectos WHERE id = %s", (proyecto_asignado,))
                proyecto = cursor.fetchone()
                if proyecto:
                    proyectos.append(proyecto)

        # Cerrar el cursor
        cursor.close()

        return jsonify({'proyectos': proyectos}), 200

    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500  


# PAGINA

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe... </h1>", 404
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

