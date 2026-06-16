# equipos.py
from conexion import Conexion
from usuarios import Usuario

class Equipo:
    def __init__(self, nombre_equipo=None, fecha_creacion=None, capitan_id=None):
        self.nombre_equipo = nombre_equipo
        self.fecha_creacion = fecha_creacion
        self.capitan_id = capitan_id
        self.id_equipo = None
    
    def guardar(self):
        # Metodo: INSERT en BD
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Estructura de control: valida campos vacios
        if not self.nombre_equipo or self.nombre_equipo.strip() == "":
            print("\nEl nombre del equipo no puede estar vacio.")
            cursor.close()
            conexion.close()
            return
        
        if not self.fecha_creacion:
            print("\nLa fecha de creacion no puede estar vacia.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: valida existencia y tipo del capitan
        sql = """
            SELECT u.id_usuario, t.nombre_tipo
            FROM usuarios u
            JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE u.id_usuario = %s AND u.deleted = 0
        """
        cursor.execute(sql, (self.capitan_id,))
        capitan = cursor.fetchone()
        
        if not capitan:
            print("\nEl capitan no existe.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: valida tipo "Jugador Lider"
        if capitan[1].lower() != "jugador lider":
            print(f"\nEl usuario es '{capitan[1]}', no es 'Jugador Lider'.")
            print("Solo los usuarios con tipo 'Jugador Lider' pueden ser capitanes.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: valida nombre unico
        sql = """SELECT id_equipo FROM equipos WHERE nombre_equipo = %s AND deleted = 0"""
        cursor.execute(sql, (self.nombre_equipo,))
        if cursor.fetchone():
            print(f"\nYa existe un equipo con el nombre '{self.nombre_equipo}'.")
            cursor.close()
            conexion.close()
            return
        
        # INSERT
        sql = """
            INSERT INTO equipos (nombre_equipo, fecha_creacion, capitan_id, created_by) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (self.nombre_equipo, self.fecha_creacion, self.capitan_id, "system"))
        conexion.commit()
        
        self.id_equipo = cursor.lastrowid
        
        # UPDATE: asigna capitan al equipo
        sql = """UPDATE usuarios SET equipo_id = %s WHERE id_usuario = %s"""
        cursor.execute(sql, (self.id_equipo, self.capitan_id))
        conexion.commit()
        
        print(f"\nEquipo '{self.nombre_equipo}' agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    def agregar_miembro(self, usuario_id):
        # Metodo: UPDATE equipo_id
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Estructura de control: verifica existencia del usuario
        sql = """SELECT equipo_id FROM usuarios WHERE id_usuario = %s AND deleted = 0"""
        cursor.execute(sql, (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print("\nEl usuario no existe.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: verifica que no tenga equipo
        if usuario[0] is not None:
            print("\nEl usuario ya pertenece a un equipo.")
            cursor.close()
            conexion.close()
            return
        
        # UPDATE
        sql = """UPDATE usuarios SET equipo_id = %s WHERE id_usuario = %s"""
        cursor.execute(sql, (self.id_equipo, usuario_id))
        conexion.commit()
        
        print(f"\nUsuario agregado al equipo '{self.nombre_equipo}'.")
        
        cursor.close()
        conexion.close()
    
    def eliminar_miembro(self, usuario_id):
        # Metodo: SET equipo_id = NULL
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Estructura de control: verifica pertenencia al equipo
        sql = """SELECT equipo_id FROM usuarios WHERE id_usuario = %s AND equipo_id = %s AND deleted = 0"""
        cursor.execute(sql, (usuario_id, self.id_equipo))
        if not cursor.fetchone():
            print("\nEl usuario no pertenece a este equipo.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: no permite eliminar capitan
        if int(usuario_id) == int(self.capitan_id):
            print("\nNo se puede eliminar al capitan del equipo.")
            cursor.close()
            conexion.close()
            return
        
        # UPDATE
        sql = """UPDATE usuarios SET equipo_id = NULL WHERE id_usuario = %s"""
        cursor.execute(sql, (usuario_id,))
        conexion.commit()
        
        print(f"\nUsuario eliminado del equipo '{self.nombre_equipo}'.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        # Metodo estatico: SELECT con subquery
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT e.id_equipo, e.nombre_equipo, e.fecha_creacion, u.nombre_completo,
                   (SELECT COUNT(*) FROM usuarios WHERE equipo_id = e.id_equipo AND deleted = 0) as total_miembros
            FROM equipos e
            LEFT JOIN usuarios u ON e.capitan_id = u.id_usuario
            WHERE e.deleted = 0
        """
        cursor.execute(sql)
        equipos = cursor.fetchall()
        
        print("\n===== EQUIPOS =====")
        # Bucle for: recorre resultados
        for e in equipos:
            capitan_nombre = e[3] if e[3] else "Sin capitan"
            print(f"ID: {e[0]} | Equipo: {e[1]} | Capitan: {capitan_nombre} | Miembros: {e[4]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        # Interfaz: input usuario
        print("\n===== NUEVO EQUIPO =====")
        
        print("\nUSUARIOS SIN EQUIPO (pueden ser capitanes)")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        sql = """SELECT id_usuario, nombre_completo, username FROM usuarios WHERE equipo_id IS NULL AND deleted = 0 AND tipo_usuario_id = 3"""
        cursor.execute(sql)
        usuarios_sin_equipo = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        # Bucle for: muestra usuarios disponibles
        for u in usuarios_sin_equipo:
            print(f"ID: {u[0]} | {u[1]} | @{u[2]}")
        
        print("\nNOTA: El capitan debe ser tipo 'Jugador Lider' y no tener equipo")
        
        capitan_id = int(input("\nID del capitan: "))
        nombre = input("Nombre del equipo: ")
        
        # Estructura de control: valida entrada
        if not nombre or nombre.strip() == "":
            print("\nEl nombre del equipo no puede estar vacio.")
            return
        
        fecha = input("Fecha creacion (AAAA-MM-DD): ")
        
        equipo = Equipo(nombre, fecha, capitan_id)
        equipo.guardar()
    
    @staticmethod
    def ver_miembros():
        # Metodo estatico: SELECT miembros por equipo
        Equipo.listar()
        
        id_equipo = int(input("\nIngrese ID del equipo: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # SELECT informacion del equipo
        sql = """SELECT nombre_equipo, capitan_id FROM equipos WHERE id_equipo = %s AND deleted = 0"""
        cursor.execute(sql, (id_equipo,))
        equipo_info = cursor.fetchone()
        
        if not equipo_info:
            print("\nEquipo no encontrado.")
            cursor.close()
            conexion.close()
            return
        
        capitan_id = equipo_info[1]
        
        # SELECT miembros
        sql = """
            SELECT u.id_usuario, u.nombre_completo, u.username, u.edad, t.nombre_tipo
            FROM usuarios u
            JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE u.equipo_id = %s AND u.deleted = 0
            ORDER BY u.id_usuario ASC
        """
        cursor.execute(sql, (id_equipo,))
        miembros = cursor.fetchall()
        
        print(f"\n===== MIEMBROS DEL EQUIPO: {equipo_info[0]} =====")
        
        # Bucle for: recorre miembros
        for m in miembros:
            capitan_texto = " (Capitan)" if m[0] == capitan_id else ""
            print(f"ID: {m[0]} | {m[1]} | @{m[2]} | Tipo: {m[4]}{capitan_texto}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar_miembro():
        # Interfaz: agregar miembro
        print("\n===== AGREGAR MIEMBRO A EQUIPO =====")
        Equipo.listar()
        
        id_equipo = int(input("\nID del equipo: "))
        
        print("\nUSUARIOS SIN EQUIPO")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        sql = """SELECT id_usuario, nombre_completo, username FROM usuarios WHERE equipo_id IS NULL AND deleted = 0"""
        cursor.execute(sql)
        usuarios_sin_equipo = cursor.fetchall()
        
        # Bucle for: muestra usuarios disponibles
        for u in usuarios_sin_equipo:
            print(f"ID: {u[0]} | {u[1]} | @{u[2]}")
        
        usuario_id = int(input("\nID del usuario a agregar: "))
        cursor.close()
        conexion.close()
        
        # SELECT equipo
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        sql = """SELECT id_equipo, nombre_equipo FROM equipos WHERE id_equipo = %s AND deleted = 0"""
        cursor.execute(sql, (id_equipo,))
        equipo_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        # Estructura de control: verifica existencia
        if equipo_data:
            equipo = Equipo(equipo_data[1], None, None)
            equipo.id_equipo = int(id_equipo)
            equipo.agregar_miembro(usuario_id)
        else:
            print("\nEquipo no encontrado.")
    
    @staticmethod
    def eliminar_miembro_ui():
        # Interfaz: eliminar miembro
        print("\n===== ELIMINAR MIEMBRO DE EQUIPO =====")
        Equipo.listar()
        
        id_equipo = int(input("\nID del equipo: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # SELECT miembros del equipo
        sql = """
            SELECT u.id_usuario, u.nombre_completo, u.username
            FROM usuarios u
            WHERE u.equipo_id = %s AND u.deleted = 0
        """
        cursor.execute(sql, (id_equipo,))
        miembros = cursor.fetchall()
        
        print("\nMIEMBROS DEL EQUIPO")
        # Bucle for: muestra miembros
        for m in miembros:
            print(f"ID: {m[0]} | {m[1]} | @{m[2]}")
        
        usuario_id = int(input("\nID del usuario a eliminar: "))
        cursor.close()
        conexion.close()
        
        # SELECT equipo
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        sql = """SELECT id_equipo, nombre_equipo, capitan_id FROM equipos WHERE id_equipo = %s AND deleted = 0"""
        cursor.execute(sql, (id_equipo,))
        equipo_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        # Estructura de control: verifica existencia
        if equipo_data:
            equipo = Equipo(equipo_data[1], None, equipo_data[2])
            equipo.id_equipo = int(id_equipo)
            equipo.eliminar_miembro(usuario_id)
        else:
            print("\nEquipo no encontrado.")
    
    @staticmethod
    def eliminar():
        # Interfaz: DELETE logico equipo
        Equipo.listar()
        
        id_equipo = int(input("\nIngrese ID del equipo: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # UPDATE: libera miembros
        sql = """UPDATE usuarios SET equipo_id = NULL WHERE equipo_id = %s"""
        cursor.execute(sql, (id_equipo,))
        
        # UPDATE logico equipo
        sql = """UPDATE equipos SET deleted = 1 WHERE id_equipo = %s"""
        cursor.execute(sql, (id_equipo,))
        conexion.commit()
        print("\nEquipo eliminado correctamente. Los miembros quedaron sin equipo.")
        
        cursor.close()
        conexion.close()