# API

## Funcionamiento de Usuarios:

### get_registrar_usuarios:

URL: http://127.0.0.1:5000/registrar_usuarios
JSON de ejemplo:

    {
    "usuario": "Andresd",
    "email": "Andresd@gmail.com",
    "contrasena": "123456",
    "rol": 2,
    "nombre": "Andres Betancourt"
    }

en cada campo se añade el usuario, un email, una contraseña que luego se va a encriptar, un rol (1 gerente, 2 desarrollador), y el nombre del usuario,
no deben ahber campos repetidos en el usuario o email, si se encuentra un asuario repetido no se registrara.

### get_leer_usuarios

URL: http://127.0.0.1:5000/usuarios/<id del usuario que se quiera leer>

URL de ejemplo: http://127.0.0.1:5000/usuarios/1

Se muestran los datos del usuario especificado.

### get_listar_usuarios

URL: http://127.0.0.1:5000/usuarios

Se muestran todos los usuarios que esten en la base de datos.

### put actualizar_usuarios

URL: http://127.0.0.1:5000/usuarios/<id del usuario a actualizar>

URL de emplo: http://127.0.0.1:5000/usuarios/3

JSON de ejemplo:

    {
    "usuario": "prueba",
    "email": "Prueba@utadeo.edu.co",
    "nombre": "Andres Betancourt"
    }

Se actualizaran los campos usuario, email, nombre; estos no pueden se repetidos con los de otro usuario.

### delete_eliminar_usuarios

URL: http://127.0.0.1:5000/usuarios/<id del usuario que se quiera eliminar>

URL de ejemplo: http://127.0.0.1:5000/usuarios/1

Se eliminara el usuario el cual se indique, pero no se podran eliminar usuarios los cuales esten asociados a una tarea o a una historia de usuario.

## Funcionamiento de Proyectos:

### get_registrar_proyectos

URL: http://127.0.0.1:5000/proyectos/<id del usuario que va a crear el proyecto (solo los gerentes id = 1, pueden crear proyectos)>

URL de ejemplo: http://127.0.0.1:5000/proyectos/2

JSON de ejemplo:

    {
    "nombre": "intervalos",
    "descripcion": "Busca de intervalos para mayor crecimiento empresarial",
    "fecha_inicio": "2024-02-26"
    }

En cada campo se añade el nombre, descripcion y la fecha de inicio del proyecto, estos no pueden estar repetidos con los de otro proyecto ya registrado.

### get_leer_proyectos

URL: http://127.0.0.1:5000/proyectos/<id del proyecto que se quiere visualizar>

URL de ejemplo: http://127.0.0.1:5000/proyectos/1

Se muestra el proyecto con el id especificado.

### get_listar_proyectos

URL: http://127.0.0.1:5000/proyectos

Se muestran todos los proyectos que esten en la base de datos.

### put_actualizar_proyectos

URL: http://127.0.0.1:5000/proyectos/<id del proyecto que se quiere actualizar>/<id del usuario que va a actualizar el proyecto (solo los gerentes id = 1, pueden actualizar un proyecto)>

URL de ejemplo: http://127.0.0.1:5000/proyectos/2/2

JSON de ejemplo:

    {
    "nombre": "prueba",
    "descripcion": "Prueba"
    }

Se actualizaran los campos nombre y descripcion, estos no pueden ser iguales a los de otro proyecto ya creado.

### delete_eliminar_proyectos

URL: http://127.0.0.1:5000/proyectos/<id del proyecto que se quiere elimniar>/<id del usuario que va a eliminar el proyecto (solo los gerentes id = 1, pueden eliminar un proyecto)>

URL de ejemplo: http://127.0.0.1:5000/proyectos/1/2

Se eliminara el proyectos con el id encontrado.

  