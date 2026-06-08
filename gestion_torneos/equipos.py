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
        
        # Agregar al capitan como miembro del equipo
        sql_miembro = "INSERT INTO equipo_usuarios (equipo_id, usuario_id, fecha_ingreso, created_by) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_miembro, (self.id_equipo, self.capitan_id, self.fecha_creacion, "system"))
        conexion.commit()
        
        print(f"\nEquipo '{self.nombre_equipo}' agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    def agregar_miembro(self, usuario_id, fecha_ingreso):
        # Agrega un miembro al equipo
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si el usuario ya es miembro
        cursor.execute("SELECT id_equipo_usuario FROM equipo_usuarios WHERE equipo_id = %s AND usuario_id = %s AND deleted = 0", 
                    (self.id_equipo, usuario_id))
        if cursor.fetchone():
            print("\nEl usuario ya es miembro de este equipo.")
            cursor.close()
            conexion.close()
            return
        
        # Insertar miembro
        sql = "INSERT INTO equipo_usuarios (equipo_id, usuario_id, fecha_ingreso, created_by) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (self.id_equipo, usuario_id, fecha_ingreso, "system"))
        conexion.commit()
        
        print(f"\nUsuario agregado al equipo '{self.nombre_equipo}'.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        # Lista todos los equipos activos
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT e.id_equipo, e.nombre_equipo, e.fecha_creacion, u.nombre_completo
            FROM equipos e
            LEFT JOIN usuarios u ON e.capitan_id = u.id_usuario
            WHERE e.deleted = 0
        """
        cursor.execute(sql)
        equipos = cursor.fetchall()
        
        print("\n===== EQUIPOS =====")
        for e in equipos:
            print(f"ID: {e[0]} | Equipo: {e[1]} | Capitan: {e[3]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        # Interfaz para agregar un nuevo equipo
        print("\n===== NUEVO EQUIPO =====")
        
        print("\nUSUARIOS DISPONIBLES")
        Usuario.listar_simple()
        
        print("\nNOTA: El capitan debe ser tipo 'Jugador Lider'")
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
            SELECT u.id_usuario, u.nombre_completo, u.username, eu.fecha_ingreso, t.nombre_tipo
            FROM equipo_usuarios eu
            JOIN usuarios u ON eu.usuario_id = u.id_usuario
            JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE eu.equipo_id = %s AND eu.deleted = 0 AND u.deleted = 0
            ORDER BY eu.fecha_ingreso ASC
        """
        cursor.execute(sql, (id_equipo,))
        miembros = cursor.fetchall()
        
        print("\n===== MIEMBROS DEL EQUIPO =====")
        if len(miembros) == 0:
            print("No hay miembros en este equipo.")
        else:
            for m in miembros:
                print(f"ID: {m[0]} | {m[1]} | @{m[2]} | Tipo: {m[4]} | Ingreso: {m[3]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar_miembro():
        # Interfaz para agregar un miembro a un equipo
        print("\n===== AGREGAR MIEMBRO A EQUIPO =====")
        Equipo.listar()
        id_equipo = input("\nID del equipo: ")
        
        print("\nUSUARIOS DISPONIBLES")
        Usuario.listar_simple()
        usuario_id = input("ID del usuario a agregar: ")
        fecha_ingreso = input("Fecha de ingreso (AAAA-MM-DD): ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_equipo, nombre_equipo FROM equipos WHERE id_equipo = %s AND deleted = 0", (id_equipo,))
        equipo_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if equipo_data:
            equipo = Equipo(equipo_data[1], None, None)
            equipo.id_equipo = int(id_equipo)
            equipo.agregar_miembro(usuario_id, fecha_ingreso)
        else:
            print("\nEquipo no encontrado.")
    
    @staticmethod
    def eliminar():
        # Elimina logicamente un equipo
        Equipo.listar()
        id_equipo = input("\nIngrese ID del equipo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE equipos SET deleted = 1 WHERE id_equipo = %s"
        cursor.execute(sql, (id_equipo,))
        conexion.commit()
        print("\nEquipo eliminado correctamente.")
        
        cursor.close()
        conexion.close()