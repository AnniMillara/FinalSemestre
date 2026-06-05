from conexion import Conexion
from ciudad import ciudad
from usuarios import usuario
from equipos import Equipo

class Torneo:
    torneos_disponibles = []
    
    def __init__(self, nombre_torneo=None, juego=None, premio=None, fecha_inicio=None, fecha_fin=None, organizador_id=None, ciudad_id=None):
        self.nombre_torneo = nombre_torneo
        self.juego = juego
        self.premio = premio
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.organizador_id = organizador_id
        self.ciudad_id = ciudad_id
        self.equipos_inscritos = []
        Torneo.torneos_disponibles.append(self)
    
    def inscribir_equipo(self, equipo):  # Método de instancia
        if equipo not in self.equipos_inscritos:
            self.equipos_inscritos.append(equipo)
            return f"Equipo {equipo.nombre_equipo} inscrito en {self.nombre_torneo}"
        return "Equipo ya inscrito"
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # validar organizador como Admin
        cursor.execute("""
            SELECT u.id_usuario, t.nombre_tipo
            FROM usuarios u
            JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE u.id_usuario = %s AND u.deleted = 0
        """, (self.organizador_id,))
        
        organizador = cursor.fetchone()
        
        if not organizador:
            print("\nEl organizador no existe.")
            cursor.close()
            conexion.close()
            return
        
        # Verificar que el tipo sea "Admin"
        if organizador[1].lower() != "admin":
            print(f"\nEl usuario {organizador[1]} no es 'Admin'.")
            print("Solo los usuarios con tipo 'Admin' pueden ser organizadores.")
            cursor.close()
            conexion.close()
            return
        
        # validar ciudad
        cursor.execute("SELECT id_ciudad FROM ciudades WHERE id_ciudad = %s AND deleted = 0", (self.ciudad_id,))
        if not cursor.fetchone():
            print("\nLa ciudad no existe. Primero debes crear la ciudad.")
            cursor.close()
            conexion.close()
            return
        
        sql = """
            INSERT INTO torneos (nombre_torneo, juego, premio, fecha_inicio, fecha_fin, organizador_id, ciudad_id, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (self.nombre_torneo, self.juego, self.premio, self.fecha_inicio, self.fecha_fin, self.organizador_id, self.ciudad_id, "system"))
        conexion.commit()
        print("\nTorneo agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT t.id_torneo, t.nombre_torneo, t.juego, t.premio, c.nombre_ciudad
            FROM torneos t
            LEFT JOIN ciudades c ON t.ciudad_id = c.id_ciudad
            WHERE t.deleted = 0
        """
        cursor.execute(sql)
        torneos = cursor.fetchall()
        
        print("\n\nTORNEOS\n")
        for t in torneos:
            ciudad_nombre = t[4] if t[4] else "Sin ciudad"
            print(f"ID: {t[0]} | Torneo: {t[1]} | Juego: {t[2]} | Ciudad: {ciudad_nombre}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        print("\n===== NUEVO TORNEO =====")
        
        print("\nCIUDADES DISPONIBLES")
        ciudad.listar()
        ciudad_id = input("\nID de la ciudad: ")
        
        print("\nORGANIZADORES (usuarios tipo Admin)")
        usuario.listar_simple()
        organizador_id = input("\nID del organizador: ")
        
        nombre = input("Nombre del torneo: ")
        juego = input("Juego: ")
        premio = input("Premio: ")
        fecha_ini = input("Fecha inicio (AAAA-MM-DD): ")
        fecha_fin = input("Fecha fin (AAAA-MM-DD): ")
        
        torneo = Torneo(nombre, juego, premio, fecha_ini, fecha_fin, organizador_id, ciudad_id)
        torneo.guardar()
    
    @staticmethod
    def buscar_por_juego():
        juego_buscar = input("\nIngrese el nombre del juego a buscar: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT t.id_torneo, t.nombre_torneo, t.juego, t.premio, c.nombre_ciudad
            FROM torneos t
            LEFT JOIN ciudades c ON t.ciudad_id = c.id_ciudad
            WHERE t.juego LIKE %s AND t.deleted = 0
        """
        cursor.execute(sql, ('%' + juego_buscar + '%',))
        resultados = cursor.fetchall()
        
        print("\n===== RESULTADOS =====")
        if len(resultados) == 0:
            print(f"No se encontraron torneos del juego '{juego_buscar}'.")
        else:
            for t in resultados:
                ciudad_nombre = t[4] if t[4] else "Sin ciudad"
                print(f"ID: {t[0]} | {t[1]} | {t[2]} | Premio: {t[3]} | Ciudad: {ciudad_nombre}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def inscribir_equipo():
        Torneo.listar()
        id_torneo = input("\nIngrese ID del torneo: ")
        
        Equipo.listar()
        id_equipo = input("Ingrese ID del equipo: ")
        fecha_inscripcion = input("Fecha de inscripción (AAAA-MM-DD): ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar que no esté ya inscrito
        cursor.execute("SELECT id_torneo_equipo FROM torneo_equipos WHERE torneo_id = %s AND equipo_id = %s AND deleted = 0", 
                    (id_torneo, id_equipo))
        
        if cursor.fetchone():
            print("\nError: El equipo ya está inscrito en este torneo.")
            cursor.close()
            conexion.close()
            return
        
        sql = """
            INSERT INTO torneo_equipos (torneo_id, equipo_id, fecha_inscripcion, created_by)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (id_torneo, id_equipo, fecha_inscripcion, "system"))
        conexion.commit()
        
        print(f"\nEquipo inscrito correctamente en el torneo.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def eliminar():
        Torneo.listar()
        id_torneo = input("\nIngrese ID del torneo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE torneos SET deleted = 1 WHERE id_torneo = %s"
        cursor.execute(sql, (id_torneo,))
        conexion.commit()
        print("\nTorneo eliminado correctamente.")
        
        cursor.close()
        conexion.close()