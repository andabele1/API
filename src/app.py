from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexion = MySQL(app)

@app.route('/usuarios', methods = ['GET'])
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, usuario, email, contraseña, rol FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'id': fila[0], 'usuario': fila[1], 'email': fila[2], 'contraseña': fila[3], 'rol': fila[4]} 
            usuarios.append(usuario)
        return jsonify({'usuarios': usuarios, 'mensaje': "Usuario registrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    


@app.route('/usuarios/<id>', methods = ['GET'])    
def leer_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, usuario, email, contraseña, rol FROM usuarios WHERE id = '{0}'".format(id)
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
            sql = """INSERT INTO usuarios (id, usuario, email, contraseña, rol) 
            VALUES ({0}, '{1}', '{2}', '{3}', '{4}')""".format(request.json['id'],
            request.json['usuario'],request.json['email'],request.json['contraseña'],
            request.json['rol'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario registrado"})
        except Exception as ex:
            return jsonify({'mensaje': "Usuario ya registrado"})
    


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
        email = '{1}', contraseña = '{2}', rol = '{3}' WHERE id = '{4}'""".format(
        request.json['usuario'],request.json['email'],request.json['contraseña'],
        request.json['rol'], id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario actualizado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
     


def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe... </h1>", 404
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
