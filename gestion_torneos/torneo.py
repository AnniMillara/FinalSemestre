# torneo.py - corregido
from conexion import Conexion
from ciudad import Ciudad
from usuarios import Usuario
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
    
    def inscribir_equipo(self, equipo):
        if equipo not in self.equipos_inscritos:
            self.equipos_inscritos.append(equipo)
            return f"Equipo {equipo.nombre_equipo} inscrito en {self.nombre_torneo}"
        return "Equipo ya inscrito"
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
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
        
        if organizador[1].lower() != "admin":
            print(f"\nEl usuario {organizador[1]} no es 'Admin'.")
            print("Solo los usuarios con tipo 'Admin' pueden ser organizadores.")
            cursor.close()
            conexion.close()
            return
        
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
        Ciudad.listar()
        ciudad_id = input("\nID de la ciudad: ")
        
        print("\nORGANIZADORES (usuarios tipo Admin)")
        Usuario.listar_simple()
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
        fecha_inscripcion = input("Fecha de inscripcion (AAAA-MM-DD): ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_torneo_equipo FROM torneo_equipos WHERE torneo_id = %s AND equipo_id = %s AND deleted = 0", 
                    (id_torneo, id_equipo))
        
        if cursor.fetchone():
            print("\nEl equipo ya esta inscrito en este torneo.")
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
    
    @staticmethod
    def listar_partidas():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT p.id_partida, t.nombre_torneo, eq1.nombre_equipo, eq2.nombre_equipo, 
                   p.fecha_partida, p.ronda, p.resultado_local, p.resultado_visitante
            FROM partidas p
            JOIN torneos t ON p.torneo_id = t.id_torneo
            JOIN equipos eq1 ON p.equipo_local_id = eq1.id_equipo
            JOIN equipos eq2 ON p.equipo_visitante_id = eq2.id_equipo
            WHERE p.deleted = 0
        """
        cursor.execute(sql)
        partidas = cursor.fetchall()
        
        print("\n===== PARTIDAS =====")
        for p in partidas:
            print(f"ID: {p[0]} | Torneo: {p[1]} | {p[2]} vs {p[3]} | Ronda: {p[5]} | {p[6]}-{p[7]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar_partida():
        Torneo.listar()
        id_torneo = input("\nID del torneo: ")
        
        Equipo.listar()
        id_local = input("ID equipo local: ")
        id_visitante = input("ID equipo visitante: ")
        
        fecha = input("Fecha y hora (AAAA-MM-DD HH:MM:SS): ")
        ronda = input("Ronda: ")
        resultado_local = input("Resultado local: ")
        resultado_visitante = input("Resultado visitante: ")
        duracion = input("Duracion (minutos): ")
        
        ganador_id = input("ID del ganador (0 si no aplica): ")
        if ganador_id == "0":
            ganador_id = None
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            INSERT INTO partidas (torneo_id, equipo_local_id, equipo_visitante_id, fecha_partida, 
                                  ronda, resultado_local, resultado_visitante, duracion_minutos, ganador_id, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_torneo, id_local, id_visitante, fecha, ronda, resultado_local, resultado_visitante, duracion, ganador_id, "system"))
        conexion.commit()
        print("\nPartida agregada correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def actualizar_resultado():
        Torneo.listar_partidas()
        id_partida = input("\nID de la partida: ")
        
        nuevo_local = input("Nuevo resultado local: ")
        nuevo_visitante = input("Nuevo resultado visitante: ")
        ganador_id = input("ID del ganador: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE partidas SET resultado_local = %s, resultado_visitante = %s, ganador_id = %s WHERE id_partida = %s"
        cursor.execute(sql, (nuevo_local, nuevo_visitante, ganador_id, id_partida))
        conexion.commit()
        print("\nResultado actualizado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def eliminar_partida():
        Torneo.listar_partidas()
        id_partida = input("\nID de la partida: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE partidas SET deleted = 1 WHERE id_partida = %s"
        cursor.execute(sql, (id_partida,))
        conexion.commit()
        print("\nPartida eliminada correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_sanciones():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT s.id_sancion, u.nombre_completo, t.nombre_torneo, s.motivo, s.fecha_sancion, s.dias_suspension
            FROM sanciones s
            JOIN usuarios u ON s.usuario_id = u.id_usuario
            JOIN torneos t ON s.torneo_id = t.id_torneo
            WHERE s.deleted = 0
        """
        cursor.execute(sql)
        sanciones = cursor.fetchall()
        
        print("\n===== SANCIONES =====")
        for s in sanciones:
            print(f"ID: {s[0]} | Usuario: {s[1]} | Torneo: {s[2]} | Motivo: {s[3]} | Fecha: {s[4]} | Dias: {s[5]}")
        
        cursor.close()
        conexion.close()
    
    # torneo.py - metodo agregar_sancion sin fecha
    @staticmethod
    def agregar_sancion():
        Usuario.listar_simple()
        id_usuario = input("\nID del usuario: ")
        
        Torneo.listar()
        id_torneo = input("ID del torneo: ")
        
        Torneo.listar_partidas()
        id_partida = input("ID de la partida (0 si no aplica): ")
        if id_partida == "0":
            id_partida = None
        
        motivo = input("Motivo de la sancion: ")
        dias = input("Dias de suspension: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            INSERT INTO sanciones (usuario_id, torneo_id, partida_id, motivo, fecha_sancion, dias_suspension, created_by)
            VALUES (%s, %s, %s, %s, CURDATE(), %s, %s)
        """
        cursor.execute(sql, (id_usuario, id_torneo, id_partida, motivo, dias, "system"))
        conexion.commit()
        print("\nSancion agregada correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def eliminar_sancion():
        Torneo.listar_sanciones()
        id_sancion = input("\nID de la sancion: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE sanciones SET deleted = 1 WHERE id_sancion = %s"
        cursor.execute(sql, (id_sancion,))
        conexion.commit()
        print("\nSancion eliminada correctamente.")
        
        cursor.close()
        conexion.close()