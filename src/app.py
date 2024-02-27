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



# PAGINA

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe... </h1>", 404
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()


#LOGIN
    
@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('contrasena')

        # Busca el usuario en la base de datos por su correo electrónico
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