CREATE TABLE estados (
    id     INTEGER NOT NULL,
    estado TEXT NOT NULL
);

ALTER TABLE estados ADD CONSTRAINT estados_pk PRIMARY KEY (id);

CREATE TABLE historias_de_usuario (
    id        INTEGER AUTO_INCREMENT PRIMARY KEY,
    detalles  TEXT NOT NULL,
    criterios TEXT NOT NULL,
    proyecto  INTEGER,
    estado    INTEGER,
    usuario   INTEGER
);


CREATE TABLE proyectos (
    id           INTEGER AUTO_INCREMENT PRIMARY KEY,
    nombre       TEXT NOT NULL,
    descripcion  TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    gerente      INTEGER
);


CREATE TABLE roles (
    id  INTEGER AUTO_INCREMENT PRIMARY KEY,
    rol TEXT NOT NULL
);


CREATE TABLE tareas_ (
    id               INTEGER AUTO_INCREMENT PRIMARY KEY,
    descripcion      TEXT NOT NULL,
    estado           INTEGER,
    historias_de_usuario INTEGER,
    usuario      INTEGER NOT NULL
);


CREATE TABLE actualizacion_estado_historias_de_usuario (
    id                 INTEGER AUTO_INCREMENT PRIMARY KEY,
    historias_de_usuario   INTEGER,
    estado             INTEGER,
    usuario            INTEGER,
    hora_actualizacion DATE NOT NULL
);


CREATE TABLE actualizacion_estado_tareas (
    id                 INTEGER AUTO_INCREMENT PRIMARY KEY,
    tarea              INTEGER,
    estado             INTEGER,
    usuario            INTEGER,
    hora_actualizacion DATE NOT NULL
);


CREATE TABLE usuarios (
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    usuario    TEXT NOT NULL,
    email      TEXT NOT NULL,
    contrasena TEXT NOT NULL,
    rol        INTEGER
);


CREATE TABLE usuarios_proyectos (
    id       INTEGER AUTO_INCREMENT PRIMARY KEY,
    usuario  INTEGER,
    proyecto INTEGER
);



ALTER TABLE historias_de_usuario
    ADD CONSTRAINT historias_usuarios_proyectos_fk FOREIGN KEY (proyecto)
        REFERENCES proyectos (id);

ALTER TABLE historias_de_usuario
    ADD CONSTRAINT historias_de_usuario_usuarios_fk FOREIGN KEY (usuario)
        REFERENCES usuarios (id);

ALTER TABLE tareas_
    ADD CONSTRAINT tareas_historias_de_usuario_fk FOREIGN KEY (historias_de_usuario)
        REFERENCES historias_de_usuario (id);

ALTER TABLE tareas_
    ADD CONSTRAINT tareas_usuarios_fk FOREIGN KEY (usuario)
        REFERENCES usuarios (id);

ALTER TABLE actualizacion_estado_historias_de_usuario
    ADD CONSTRAINT update_estado_historia_estados_fk FOREIGN KEY (estado)
        REFERENCES estados (id);

ALTER TABLE actualizacion_estado_historias_de_usuario
    ADD CONSTRAINT update_estado_historia_historias_usuarios_fk FOREIGN KEY (historias_de_usuario)
        REFERENCES historias_de_usuario (id);

ALTER TABLE actualizacion_estado_tareas
    ADD CONSTRAINT actualizacion_estado_tareas_fk FOREIGN KEY (estado)
        REFERENCES estados (id);

ALTER TABLE actualizacion_estado_tareas
    ADD CONSTRAINT actualizacion_estado_tareas_tareas_fk FOREIGN KEY (tarea)
        REFERENCES tareas_ (id);

ALTER TABLE usuarios_proyectos
    ADD CONSTRAINT usuarios_proyectos_proyectos_fk FOREIGN KEY (proyecto)
        REFERENCES proyectos (id);

ALTER TABLE usuarios_proyectos
    ADD CONSTRAINT usuarios_proyectos_usuarios_fk FOREIGN KEY (usuario)
        REFERENCES usuarios (id);

ALTER TABLE usuarios
    ADD CONSTRAINT usuarios_roles_fk FOREIGN KEY (rol)
        REFERENCES roles (id);

ALTER TABLE usuarios
ADD CONSTRAINT correo_unico UNIQUE (email);

INSERT INTO estados (id, estado) VALUES (1, 'Nuevo');
INSERT INTO estados (id, estado) VALUES (2, 'En proceso');
INSERT INTO estados (id, estado) VALUES (3, 'Finalizado');

INSERT INTO roles (id, rol) VALUES (1, 'Gerente');
INSERT INTO roles (id, rol) VALUES (2, 'Desarrollador');