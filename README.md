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

En cada campo se añade el usuario, un email, una contraseña que luego se va a encriptar, un rol (1 gerente, 2 desarrollador), y el nombre del usuario,
no deben haber campos repetidos en el usuario o email, si se encuentra un usuario repetido no se registrara.

### get_leer_usuarios

URL: http://127.0.0.1:5000/usuarios/{id del usuario que se quiera leer}

URL de ejemplo: http://127.0.0.1:5000/usuarios/1

Se muestran los datos del usuario especificado.

### get_listar_usuarios

URL: http://127.0.0.1:5000/usuarios

Se muestran todos los usuarios que esten en la base de datos.

### put actualizar_usuarios

URL: http://127.0.0.1:5000/usuarios/{id del usuario a actualizar}

URL de ejemplo: http://127.0.0.1:5000/usuarios/3

JSON de ejemplo:

    {
    "usuario": "prueba",
    "email": "Prueba@utadeo.edu.co",
    "nombre": "Andres Betancourt"
    }

Se actualizaran los campos usuario, email, nombre; estos no pueden se repetidos con los de otro usuario.

### delete_eliminar_usuarios

URL: http://127.0.0.1:5000/usuarios/{id del usuario que se quiera eliminar}

URL de ejemplo: http://127.0.0.1:5000/usuarios/1

Se eliminara el usuario el cual se indique, pero no se podran eliminar usuarios los cuales esten asociados a una tarea o a una historia de usuario.

## Funcionamiento de Proyectos:

### get_registrar_proyectos

URL: http://127.0.0.1:5000/proyectos/{id del usuario que va a crear el proyecto (solo los gerentes rol = 1, pueden crear proyectos)}

URL de ejemplo: http://127.0.0.1:5000/proyectos/2

JSON de ejemplo:

    {
    "nombre": "intervalos",
    "descripcion": "Busca de intervalos para mayor crecimiento empresarial",
    "fecha_inicio": "2024-02-26"
    }

En cada campo se añade el nombre, descripcion y la fecha de inicio del proyecto, estos no pueden estar repetidos con los de otro proyecto ya registrado.

### get_leer_proyectos

URL: http://127.0.0.1:5000/proyectos/{id del proyecto que se quiere visualizar}

URL de ejemplo: http://127.0.0.1:5000/proyectos/1

Se muestra el proyecto con el id especificado.

### get_listar_proyectos

URL: http://127.0.0.1:5000/proyectos

Se muestran todos los proyectos que esten en la base de datos.

### put_actualizar_proyectos

URL: http://127.0.0.1:5000/proyectos/{id del proyecto que se quiere actualizar}/{id del usuario que va a actualizar el proyecto (solo los gerentes rol = 1, pueden actualizar un proyecto)}

URL de ejemplo: http://127.0.0.1:5000/proyectos/2/2

JSON de ejemplo:

    {
    "nombre": "prueba",
    "descripcion": "Prueba"
    }

Se actualizaran los campos nombre y descripcion, el nombre no puede ser igual al de otro proyecto ya creado.

### delete_eliminar_proyectos

URL: http://127.0.0.1:5000/proyectos/{id del proyecto que se quiere eliminar}/{id del usuario que va a eliminar el proyecto (solo los gerentes rol = 1, pueden eliminar un proyecto)}

URL de ejemplo: http://127.0.0.1:5000/proyectos/1/2

Se eliminara el proyectos con el id encontrado, pero no puede haber ningun usuario asociado al proyecto.

## Funcionamiento de Usuario_proyecto:

### post_asignar_usuario

URL: http://127.0.0.1:5000/asignar_usuario/{id del gerente que va a asignar un usuario a un proyecto}/{id del proyecto al que se le va a asignar al usuario}

URL de ejemplo: http://127.0.0.1:5000/asignar_usuario/2/3

JSON de ejemplo:

    {
    "usuario_id": 3
    }
  
En el campo "usuario_id" se debe poner el id del usuario al que le van a asignar el proyecto.

### get_proyectos_usuario

URL: http://127.0.0.1:5000/proyectos_usuario/{id del usuario al cual se le quieren visualizar sus proyectos}

URL de ejemplo: http://127.0.0.1:5000/proyectos_usuario/4

Muestra los proyectos los cuales estan asociados a los usuarios

### delete_usuario_proyecto

URL: http://127.0.0.1:5000/eliminar_usuario_proyecto/{id del gerente que va a eliminar un usuario de un proyecto}/{id del proyecto en el que se va eliminar al usuario}

URL de ejemplo: http://127.0.0.1:5000/eliminar_usuario_proyecto/2/2

JSON de ejemplo:

    {
    "usuario": 3
    }

En el campo "usuario_id" se debe poner el id del usuario al que se le va a eliminar del proyecto.

## Funcionamiento de Historias de usuario:

### post_crear_historias_de_usuario

URL: http://127.0.0.1:5000/crear_historia_de_usuario

JSON de ejemplo:

    {     
    "detalles": "Prueba",
    "criterios": "Prueba",
    "proyecto": 2,
    "estado": 1,
    "usuario": 2
    }

en cada campo se añade los detalles, criterios de la historia de usuario, el proyecto al cual va estar asociado, el estado del ahistoria de usuario, 1 = nueva, 2 = en proceso, 3 = finalizada
y el gerente (rol = 1) encargado de la historia de usuario.

### leer_historias de usuario

URL: http://127.0.0.1:5000/historias_de_usuario/{id del proyecto al cual se le quieren visualizar sus historias de usuario}

URL de ejemplo: http://127.0.0.1:5000/historias_de_usuario/3

Se mostraran las historias de usuario las cuales estna asociadas au proyecto en especifico.

### delete_eliminar_historias_de_usuario

URL: http://127.0.0.1:5000/eliminar_historia_de_usuario/{id de la historia de usuario que se quiera eliminar}

URL de ejemplo: http://127.0.0.1:5000/eliminar_historia_de_usuario/2

JSON de ejemplo:

    {
    "usuario": 2,
    "proyecto": 2
    }

En el campo "usuario" se debe poner el id de un gerente (rol = 1), y en el campo proyecto se debe poner el proyecto al cual esta asociada la historia de usuario.

## Funcionamiento de Tareas:

### get_crear_tareas

URL: http://127.0.0.1:5000/crear_tarea

JSON de ejemplo:

    {
    "descripcion": "try",
    "estado": 2,
    "historia": 2,
    "usuario": 3
    }

En cada campo se añade la descripcion de la tarea, el estado, 1 = nueva, 2 = en proceso, 3 = finalizada; en la historia, la historia de usuario a la cual va a estar asociada la tarea y 
en usuario, el usuario que va a crear la tarea, cualquier usuario puede crear una tarea. 

### leer_tareas_de_historia_de_usuario

URL: http://127.0.0.1:5000/tareas_por_historia/{id de la historia a la cual se le quieren visualizar las tareas}

URL de ejemplo: http://127.0.0.1:5000/tareas_por_historia/2

Se mostraran las tareas que esten asociadas a un historia de usuario especifica.

### editar_tareas

URL: http://127.0.0.1:5000/editar_tarea/{id de la tarea que se quiere actualzar}

URL de ejemplo: http://127.0.0.1:5000/editar_tarea/3

JSON de ejemplo:

    {
    "descripcion": "Nueva descripción de la tarea"
    }

Se podra editar la descripcion de la tarea indicada.

### delete_eliminar_tareas

URL: http://127.0.0.1:5000/eliminar_tarea/{id de la tarea que se quiera eliminar}

URL de ejemplo: http://127.0.0.1:5000/eliminar_tarea/2

JSON de ejemplo:

    {
    "usuario": 3
    }

En el campo "usuario" se debera poner el id del usuario que va a eliminar la tarea, cualquier usuario puede elimnar una tarea.

## Funcionamiento de Actulizaciones historia de usuario

### post_actualizar_estado_historia

URL: http://127.0.0.1:5000/actualizar_estado_historia/{id del gerente (rol = 1 ) que va a actualizar la historia de usuario}/{id de la historia de usuario a actualizar}

URL de ejemplo: http://127.0.0.1:5000/actualizar_estado_historia/2/3
 
Se actualizara el estado de las historias de usuario y quedaran almacenadas en una bitacora de actualizaciones.


## Funcionamiento de Actualizaciones estado tareas

### put_actualizar_estado_tareas

URL: http://127.0.0.1:5000/actualizar_estado_tarea/{id de la tarea a actualizar}

URL de ejemplo: http://127.0.0.1:5000/actualizar_estado_tarea/5

Se actualizara el estado de la tarea especificada y quedaran almacenadas en una bitacora de actualizaciones.





