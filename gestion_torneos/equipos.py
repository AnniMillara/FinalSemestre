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
        # Guarda un nuevo equipo en la base de datos
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Validar que el capitan existe y es de tipo "Jugador Lider"
        cursor.execute("""
            SELECT u.id_usuario, t.nombre_tipo
            FROM usuarios u
            JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE u.id_usuario = %s AND u.deleted = 0
        """, (self.capitan_id,))
        
        capitan = cursor.fetchone()
        
        if not capitan:
            print("\nEl capitan no existe.")
            cursor.close()
            conexion.close()
            return
        
        if capitan[1].lower() != "jugador lider":
            print(f"\nEl usuario es '{capitan[1]}', no es 'Jugador Lider'.")
            print("Solo los usuarios con tipo 'Jugador Lider' pueden ser capitanes.")
            cursor.close()
            conexion.close()
            return
        
        # Validar que el nombre del equipo no exista
        cursor.execute("SELECT id_equipo FROM equipos WHERE nombre_equipo = %s AND deleted = 0", (self.nombre_equipo,))
        if cursor.fetchone():
            print(f"\nYa existe un equipo con el nombre '{self.nombre_equipo}'.")
            cursor.close()
            conexion.close()
            return
        
        # Insertar equipo
        sql = """
            INSERT INTO equipos (nombre_equipo, fecha_creacion, capitan_id, created_by) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (self.nombre_equipo, self.fecha_creacion, self.capitan_id, "system"))
        conexion.commit()
        
        self.id_equipo = cursor.lastrowid
        
        # Asignar el capitan al equipo (actualizar su equipo_id)
        cursor.execute("UPDATE usuarios SET equipo_id = %s WHERE id_usuario = %s", (self.id_equipo, self.capitan_id))
        conexion.commit()
        
        print(f"\nEquipo '{self.nombre_equipo}' agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    def agregar_miembro(self, usuario_id):
        # Agrega un miembro al equipo (actualiza su equipo_id)
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si el usuario ya pertenece a otro equipo
        cursor.execute("SELECT equipo_id FROM usuarios WHERE id_usuario = %s AND deleted = 0", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print("\nEl usuario no existe.")
            cursor.close()
            conexion.close()
            return
        
        if usuario[0] is not None:
            print("\nEl usuario ya pertenece a un equipo.")
            cursor.close()
            conexion.close()
            return
        
        # Asignar usuario al equipo
        cursor.execute("UPDATE usuarios SET equipo_id = %s WHERE id_usuario = %s", (self.id_equipo, usuario_id))
        conexion.commit()
        
        print(f"\nUsuario agregado al equipo '{self.nombre_equipo}'.")
        
        cursor.close()
        conexion.close()
    
    def eliminar_miembro(self, usuario_id):
        # Elimina un miembro del equipo (quita su equipo_id)
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar que el usuario esté en este equipo
        cursor.execute("SELECT equipo_id FROM usuarios WHERE id_usuario = %s AND equipo_id = %s AND deleted = 0", 
                      (usuario_id, self.id_equipo))
        if not cursor.fetchone():
            print("\nEl usuario no pertenece a este equipo.")
            cursor.close()
            conexion.close()
            return
        
        # No se puede eliminar al capitan
        if int(usuario_id) == int(self.capitan_id):
            print("\nNo se puede eliminar al capitan del equipo.")
            cursor.close()
            conexion.close()
            return
        
        # Quitar la asignacion del equipo
        cursor.execute("UPDATE usuarios SET equipo_id = NULL WHERE id_usuario = %s", (usuario_id,))
        conexion.commit()
        
        print(f"\nUsuario eliminado del equipo '{self.nombre_equipo}'.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        # Lista todos los equipos activos
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
        for e in equipos:
            print(f"ID: {e[0]} | Equipo: {e[1]} | Capitan: {e[3]} | Miembros: {e[4]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        # Interfaz para agregar un nuevo equipo
        print("\n===== NUEVO EQUIPO =====")
        
        # Mostrar solo usuarios que NO tienen equipo
        print("\nUSUARIOS SIN EQUIPO (pueden ser capitanes)")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre_completo, username FROM usuarios WHERE equipo_id IS NULL AND deleted = 0 AND tipo_usuario_id = 3")
        usuarios_sin_equipo = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        for u in usuarios_sin_equipo:
            print(f"ID: {u[0]} | {u[1]} | @{u[2]}")
        
        print("\nNOTA: El capitan debe ser tipo 'Jugador Lider' y no tener equipo")
        capitan_id = input("\nID del capitan: ")
        nombre = input("Nombre del equipo: ")
        fecha = input("Fecha creacion (AAAA-MM-DD): ")
        
        equipo = Equipo(nombre, fecha, capitan_id)
        equipo.guardar()
    
    @staticmethod
    def ver_miembros():
        # Muestra los miembros de un equipo
        Equipo.listar()
        id_equipo = input("\nIngrese ID del equipo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT u.id_usuario, u.nombre_completo, u.username, u.edad, t.nombre_tipo
            FROM usuarios u
            JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE u.equipo_id = %s AND u.deleted = 0
            ORDER BY u.id_usuario ASC
        """
        cursor.execute(sql, (id_equipo,))
        miembros = cursor.fetchall()
        
        print("\n===== MIEMBROS DEL EQUIPO =====")
        if len(miembros) == 0:
            print("No hay miembros en este equipo.")
        else:
            for m in miembros:
                capitan_texto = " (Capitan)" if m[0] == int(id_equipo) else ""
                print(f"ID: {m[0]} | {m[1]} | @{m[2]} | Tipo: {m[4]}{capitan_texto}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar_miembro():
        # Interfaz para agregar un miembro a un equipo
        print("\n===== AGREGAR MIEMBRO A EQUIPO =====")
        Equipo.listar()
        id_equipo = input("\nID del equipo: ")
        
        # Mostrar solo usuarios que NO tienen equipo
        print("\nUSUARIOS SIN EQUIPO")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre_completo, username FROM usuarios WHERE equipo_id IS NULL AND deleted = 0")
        usuarios_sin_equipo = cursor.fetchall()
        
        for u in usuarios_sin_equipo:
            print(f"ID: {u[0]} | {u[1]} | @{u[2]}")
        
        usuario_id = input("ID del usuario a agregar: ")
        cursor.close()
        conexion.close()
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_equipo, nombre_equipo FROM equipos WHERE id_equipo = %s AND deleted = 0", (id_equipo,))
        equipo_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if equipo_data:
            equipo = Equipo(equipo_data[1], None, None)
            equipo.id_equipo = int(id_equipo)
            equipo.agregar_miembro(usuario_id)
        else:
            print("\nEquipo no encontrado.")
    
    @staticmethod
    def eliminar_miembro_ui():
        # Interfaz para eliminar un miembro de un equipo
        print("\n===== ELIMINAR MIEMBRO DE EQUIPO =====")
        Equipo.listar()
        id_equipo = input("\nID del equipo: ")
        
        # Mostrar miembros del equipo
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.id_usuario, u.nombre_completo, u.username
            FROM usuarios u
            WHERE u.equipo_id = %s AND u.deleted = 0
        """, (id_equipo,))
        miembros = cursor.fetchall()
        
        print("\nMIEMBROS DEL EQUIPO")
        for m in miembros:
            print(f"ID: {m[0]} | {m[1]} | @{m[2]}")
        
        usuario_id = input("\nID del usuario a eliminar: ")
        cursor.close()
        conexion.close()
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_equipo, nombre_equipo, capitan_id FROM equipos WHERE id_equipo = %s AND deleted = 0", (id_equipo,))
        equipo_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if equipo_data:
            equipo = Equipo(equipo_data[1], None, equipo_data[2])
            equipo.id_equipo = int(id_equipo)
            equipo.eliminar_miembro(usuario_id)
        else:
            print("\nEquipo no encontrado.")
    
    @staticmethod
    def eliminar():
        # Elimina logicamente un equipo (primero libera a sus miembros)
        Equipo.listar()
        id_equipo = input("\nIngrese ID del equipo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Liberar a todos los miembros del equipo
        cursor.execute("UPDATE usuarios SET equipo_id = NULL WHERE equipo_id = %s", (id_equipo,))
        
        # Eliminar logicamente el equipo
        sql = "UPDATE equipos SET deleted = 1 WHERE id_equipo = %s"
        cursor.execute(sql, (id_equipo,))
        conexion.commit()
        print("\nEquipo eliminado correctamente. Los miembros quedaron sin equipo.")
        
        cursor.close()
        conexion.close()