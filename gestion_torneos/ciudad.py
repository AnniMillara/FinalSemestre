from conexion import Conexion
from pais import Pais

class Ciudad:
    def __init__(self, nombre_ciudad=None, pais_id=None):
        self.nombre_ciudad = nombre_ciudad
        self.pais_id = pais_id  # ← CAMBIADO: antes era "pais" (objeto), ahora es "pais_id" (entero)
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # 1. Verificar si el país existe
        if not Pais.existe(self.pais_id):
            print(f"\nEl país con ID {self.pais_id} no existe.")
            print("Primero debes crear el país.")
            cursor.close()
            conexion.close()
            return
        
        # 2. Verificar si la ciudad ya existe en ese país
        cursor.execute("""
            SELECT id_ciudad FROM ciudades 
            WHERE nombre_ciudad = %s AND pais_id = %s AND deleted = 0
        """, (self.nombre_ciudad, self.pais_id))
        
        if cursor.fetchone():
            print(f"\nLa ciudad '{self.nombre_ciudad}' ya existe en este país.")
            cursor.close()
            conexion.close()
            return
        
        # 3. Insertar nueva ciudad
        sql = """
            INSERT INTO ciudades (nombre_ciudad, pais_id, created_by)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (self.nombre_ciudad, self.pais_id, "system"))
        conexion.commit()
        
        # Obtener nombre del país para mensaje más informativo
        cursor.execute("SELECT nombre_pais FROM paises WHERE id_pais = %s", (self.pais_id,))
        nombre_pais = cursor.fetchone()[0]
        
        print(f"\nCiudad '{self.nombre_ciudad}' agregada correctamente en {nombre_pais}.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT c.id_ciudad, c.nombre_ciudad, p.nombre_pais
            FROM ciudades c
            JOIN paises p ON c.pais_id = p.id_pais
            WHERE c.deleted = 0
            ORDER BY p.nombre_pais, c.nombre_ciudad
        """
        cursor.execute(sql)
        ciudades = cursor.fetchall()
        
        print("\n===== CIUDADES =====")
        
        # Agrupar por país para mejor visualización
        pais_actual = None
        for ciudad in ciudades:
            if ciudad[2] != pais_actual:
                pais_actual = ciudad[2]
                print(f"\n📍 {pais_actual}:")
            print(f"   ID: {ciudad[0]} | {ciudad[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_por_pais(pais_id):
        """Lista ciudades de un país específico"""
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT id_ciudad, nombre_ciudad
            FROM ciudades
            WHERE pais_id = %s AND deleted = 0
            ORDER BY nombre_ciudad
        """
        cursor.execute(sql, (pais_id,))
        ciudades = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return ciudades
    
    @staticmethod
    def agregar():
        print("\n===== NUEVA CIUDAD =====")
        
        # Listar países disponibles primero
        Pais.listar_simple()
        
        try:
            pais_id = int(input("\nID del país: "))
        except ValueError:
            print("\nID inválido.")
            return
        
        # Verificar que el país existe
        if not Pais.existe(pais_id):
            print("\nEl país no existe.")
            return
        
        nombre = input("Nombre de la ciudad: ")
        
        nueva_ciudad = Ciudad(nombre, pais_id)
        nueva_ciudad.guardar()
    
    @staticmethod
    def eliminar():
        Ciudad.listar()
        
        try:
            id_ciudad = int(input("\nIngrese ID de la ciudad a eliminar: "))
        except ValueError:
            print("\nID inválido.")
            return
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si hay usuarios en esta ciudad
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ciudad_id = %s AND deleted = 0", (id_ciudad,))
        total_usuarios = cursor.fetchone()[0]
        
        if total_usuarios > 0:
            print(f"\nNo se puede eliminar la ciudad. Tiene {total_usuarios} usuarios asociados.")
            print("Primero reasigne o elimine los usuarios de esta ciudad.")
            cursor.close()
            conexion.close()
            return
        
        sql = "UPDATE ciudades SET deleted = 1 WHERE id_ciudad = %s"
        cursor.execute(sql, (id_ciudad,))
        conexion.commit()
        print("\nCiudad eliminada correctamente.")
        
        cursor.close()
        conexion.close()