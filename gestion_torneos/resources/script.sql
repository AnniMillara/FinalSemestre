CREATE DATABASE gestion_torneos;
USE gestion_torneos;

CREATE TABLE tipo_usuarios (
    id_tipo_usuario INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion_tipo VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0
);

CREATE TABLE paises (
    id_pais INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
    nombre_pais VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0
);

CREATE TABLE ciudades (
    id_ciudad INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL,
    pais_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (pais_id) REFERENCES paises(id_pais)
);

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    ciudad_id INT NOT NULL,
    edad INT NOT NULL,
    tipo_usuario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (tipo_usuario_id) REFERENCES tipo_usuarios(id_tipo_usuario),
    FOREIGN KEY (ciudad_id) REFERENCES ciudades(id_ciudad)
);

CREATE TABLE equipos (
    id_equipo INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
    nombre_equipo VARCHAR(100) NOT NULL,
    fecha_creacion DATE NOT NULL,  -- ← Esta columna es obligatoria
    capitan_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (capitan_id) REFERENCES usuarios(id_usuario)
);

CREATE TABLE equipo_usuarios (
    id_equipo_usuario INT AUTO_INCREMENT NOT NULL PRIMARY KEY,  -- ← Corregido: AUTO_INCREMENT
    equipo_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (equipo_id) REFERENCES equipos(id_equipo),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
);

CREATE TABLE torneos (
    id_torneo INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nombre_torneo VARCHAR(100) NOT NULL,
    juego VARCHAR(50) NOT NULL,
    premio VARCHAR(255),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    organizador_id INT NOT NULL,
    ciudad_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (organizador_id) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (ciudad_id) REFERENCES ciudades(id_ciudad)
);

CREATE TABLE torneo_equipos (
    id_torneo_equipo INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    torneo_id INT NOT NULL,
    equipo_id INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (torneo_id) REFERENCES torneos(id_torneo),
    FOREIGN KEY (equipo_id) REFERENCES equipos(id_equipo),
    UNIQUE KEY unique_torneo_equipo (torneo_id, equipo_id)
);

CREATE TABLE partidas (
    id_partida INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    torneo_id INT NOT NULL,
    equipo_local_id INT NOT NULL,
    equipo_visitante_id INT NOT NULL,
    fecha_partida DATETIME NOT NULL,
    ronda INT NOT NULL,
    resultado_local INT NOT NULL DEFAULT 0,
    resultado_visitante INT NOT NULL DEFAULT 0,
    duracion_minutos INT NOT NULL,
    ganador_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (torneo_id) REFERENCES torneos(id_torneo),
    FOREIGN KEY (equipo_local_id) REFERENCES equipos(id_equipo),
    FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id_equipo),
    FOREIGN KEY (ganador_id) REFERENCES equipos(id_equipo)
);

CREATE TABLE sanciones (
    id_sancion INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
    usuario_id INT NOT NULL,
    torneo_id INT NOT NULL,
    partida_id INT NULL,
    motivo VARCHAR(255) NOT NULL,
    fecha_sancion DATE NOT NULL,
    dias_suspension INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (torneo_id) REFERENCES torneos(id_torneo),
    FOREIGN KEY (partida_id) REFERENCES partidas(id_partida)
);

-- =========
-- INSERTS
-- =========

INSERT INTO tipo_usuarios (nombre_tipo, descripcion_tipo, created_by, updated_by)
VALUES 
    ('Jugador', 'Participa activamente en el torneo', 'system', 'system'),
    ('Admin', 'Crea, coordina y supervisa actividades en el torneo', 'system', 'system'),
    ('Jugador Lider', 'Dirige la estrategia colectiva y coordinar la comunicación entre los jugadores', 'system', 'system'),
    ('Equipo técnico', 'Encargados de infraestructura de juegos garantizan una experiencia multijugador fluida', 'system', 'system'),
    ('Comentarista', 'Creadores de ambiente, narran y analizan las partidas', 'system', 'system');
    
INSERT INTO paises (nombre_pais, created_by, updated_by)
VALUES 
    ('Chile', 'system', 'system'),
    ('Venezuela', 'system', 'system'),
    ('China', 'system', 'system'),
    ('Brazil', 'system', 'system'),
    ('Perú', 'system', 'system');

INSERT INTO ciudades (nombre_ciudad, pais_id, created_by, updated_by)
VALUES 
    ('Santiago', 1, 'system', 'system'),
    ('Caracas', 2, 'system', 'system'),
    ('Temuco', 1, 'system', 'system'),
    ('Rio de janeiro', 4, 'system', 'system'),
    ('Lima', 5, 'system', 'system');
    
INSERT INTO usuarios (nombre_completo, email, username, ciudad_id, edad, tipo_usuario_id, created_by, updated_by)
VALUES 
    ('Lautaro Ezequiel Martínez', 'lautaro.martinez@email.com', 'lautarito13', 2, 22, 1, 'system', 'system'),
    ('Camila Belén Rojas', 'camila.rojas@email.com', 'camirojas', 2, 19, 3, 'system', 'system'),
    ('Mateo Nicolás Fernández', 'mateo.fernandez@email.com', 'mateo_nfc', 2, 24, 2, 'system', 'system'),
    ('Valentina Soledad Lagos', 'valentina.lagos@email.com', 'vale_lagos', 2, 21, 1, 'system', 'system'),
    ('Tomás Ignacio Paredes', 'tomas.paredes@email.com', 'tomasparedes', 2, 20, 3, 'system', 'system'),
    ('Julieta Milagros Domínguez', 'julieta.dominguez@email.com', 'julidom', 2, 23, 3, 'system', 'system'),
    ('Facundo Ariel Navarro', 'facundo.navarro@email.com', 'facundo_nav', 2, 18, 4, 'system', 'system'),
    ('Sofía Belén Espinosa', 'sofia.espinosa@email.com', 'sofieesp', 2, 25, 5, 'system', 'system');

INSERT INTO equipos (nombre_equipo, fecha_creacion, capitan_id, created_by, updated_by)
VALUES 
    ('Bandamax', '2024-01-01', 6, 'system', 'system'),
    ('LosLucianos', '2024-01-01', 5, 'system', 'system');

INSERT INTO equipo_usuarios (equipo_id, usuario_id, fecha_ingreso, created_by, updated_by)
VALUES 
    (1, 6, '2024-01-15', 'system', 'system'),
    (1, 1, '2024-01-15', 'system', 'system'),
    (1, 4, '2024-01-20', 'system', 'system'),
    (2, 5, '2024-02-10', 'system', 'system'),
    (2, 2, '2024-02-10', 'system', 'system'),
    (2, 3, '2024-02-15', 'system', 'system');

INSERT INTO torneos (nombre_torneo, juego, premio, fecha_inicio, fecha_fin, organizador_id, ciudad_id, created_by, updated_by)
VALUES 
    ('Torneo Apertura 2025', 'League of Legends', '$5,000 + Trofeo', '2025-03-10', '2025-04-20', 3, 1, 'system', 'system'),
    ('Copa de Verano', 'Valorant', '$3,000', '2025-01-15', '2025-02-28', 3, 4, 'system', 'system'),
    ('Liga Invierno', 'CS:GO', '$7,000', '2025-06-05', '2025-07-15', 7, 2, 'system', 'system');

INSERT INTO torneo_equipos (torneo_id, equipo_id, fecha_inscripcion, created_by, updated_by)
VALUES 
    (1, 1, '2025-02-20', 'system', 'system'),
    (1, 2, '2025-02-21', 'system', 'system'),
    (2, 1, '2024-12-15', 'system', 'system'),
    (2, 2, '2024-12-16', 'system', 'system'),
    (3, 1, '2025-05-10', 'system', 'system'),
    (3, 2, '2025-05-12', 'system', 'system');

INSERT INTO partidas (torneo_id, equipo_local_id, equipo_visitante_id, fecha_partida, ronda, resultado_local, resultado_visitante, duracion_minutos, ganador_id, created_by, updated_by)
VALUES 
    (1, 1, 2, '2025-03-15 18:00:00', 1, 2, 1, 45, 1, 'system', 'system'),
    (1, 2, 1, '2025-03-22 18:00:00', 2, 1, 2, 48, 1, 'system', 'system'),
    (1, 1, 2, '2025-03-29 19:00:00', 3, 2, 0, 42, 1, 'system', 'system'),
    (2, 2, 1, '2025-01-20 17:30:00', 1, 13, 11, 55, 2, 'system', 'system'),
    (2, 1, 2, '2025-01-27 18:00:00', 2, 9, 13, 52, 2, 'system', 'system'),
    (2, 2, 1, '2025-02-03 19:00:00', 3, 2, 1, 48, 2, 'system', 'system'),
    (3, 1, 2, '2025-06-10 20:00:00', 1, 16, 14, 60, 1, 'system', 'system'),
    (3, 2, 1, '2025-06-17 20:00:00', 2, 12, 16, 58, 1, 'system', 'system');

INSERT INTO sanciones (usuario_id, torneo_id, partida_id, motivo, fecha_sancion, dias_suspension, created_by, updated_by)
VALUES 
    (1, 1, 1, 'Conducta antideportiva - insultos al rival', '2025-03-16', 3, 'system', 'system'),
    (5, 2, 4, 'Llegada tarde sin justificación', '2025-01-21', 1, 'system', 'system'),
    (2, 1, 2, 'Uso de lenguaje ofensivo en chat global', '2025-03-23', 2, 'system', 'system'),
    (4, 3, 7, 'Abandono voluntario de la partida', '2025-06-11', 5, 'system', 'system');