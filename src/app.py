from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL

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

@app.route('/usuarios', methods = ['POST'])    
def registrar_usuario():
        try:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO usuarios (id, usuario, email, contrasena, rol) 
            VALUES ({0}, '{1}', '{2}', '{3}', {4})""".format(request.json['id'],
            request.json['usuario'],request.json['email'],request.json['contraseña'],
            request.json['rol'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario registrado"})
        except Exception as ex:
            return jsonify({'mensaje': "Error"})
    
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

@app.route('/usuarios/<id>', methods = ['PUT'])
def actualizar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """UPDATE usuarios SET usuario = '{0}', 
        email = '{1}', contrasena = '{2}', rol = {3} WHERE id = {4}""".format(
        request.json['usuario'],request.json['email'],request.json['contraseña'],
        request.json['rol'], id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario actualizado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    

# PROYECTOS
    
@app.route('/proyectos', methods = ['GET'])
def listar_proyecto():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM proyectos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        proyectos = []
        for fila in datos:
            proyecto = {'id': fila[0], 'nombre': fila[1], 'descripcion': fila[2], 'fecha_inicio': fila[3], 'gerente': fila[4]} 
            proyectos.append(proyecto)
        return jsonify({'proyectos': proyectos, 'mensaje': "Listado:"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/proyectos/<id>', methods = ['GET'])    
def leer_proyecto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM proyectos WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            proyecto = {'id': datos[0], 'nombre': datos[1], 'descripcion': datos[2], 'fecha_inicio': datos[3], 'gerente': datos[4]} 
            return jsonify({'proyecto': proyecto, 'mensaje': "Proyecto encontrado"})
        else:
            return jsonify({'mensaje': "Proyecto NO encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
#Esto solo lo puede hacer un administrador, el id 1
@app.route('/proyectos', methods = ['POST'])    
def registrar_proyecto():
        try:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO proyectos (id, nombre, descripcion, fecha_inicio, gerente) 
            VALUES ({0}, '{1}', '{2}', '{3}', {4})""".format(request.json['id'],
            request.json['nombre'],request.json['descripcion'],request.json['fecha_inicio'],
            request.json['gerente'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Proyecto registrado"})
        except Exception as ex:
            return jsonify({'mensaje': "Error"})
       
@app.route('/proyectos/<id>', methods = ['DELETE'])
def eliminar_proyecto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM proyectos WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Proyecto eliminado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/proyectos/<id>', methods = ['PUT'])
def actualizar_proyecto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """UPDATE proyectos SET nombre = '{0}', 
        descripcion = '{1}', fecha_inicio = '{2}', gerente = {3} WHERE id = {4}""".format(
        request.json['nombre'],request.json['descripcion'],request.json['fecha_inicio'],
        request.json['gerente'], id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': " actualizado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


# PAGINA

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe... </h1>", 404
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()


