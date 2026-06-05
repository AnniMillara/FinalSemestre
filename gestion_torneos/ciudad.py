from conexion import Conexion

class ciudad:
    def __init__(self, nombre_ciudad = None, pais = None):
        self.nombre_ciudad = nombre_ciudad
        self.pais = pais
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # 1. Verificar si la ciudad ya existe
        cursor.execute("SELECT id_ciudad FROM ciudades WHERE nombre_ciudad = %s", (self.nombre_ciudad,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nError: La ciudad '{self.nombre_ciudad}' ya está registrada.")
            cursor.close()
            conexion.close()
            return  # Termina el método sin insertar
            
        # 2. Si no existe, proceder con la inserción
        sql = """
            INSERT INTO ciudades (nombre_ciudad, pais_id, created_by)
            VALUES (%s, %s, %s)
        """
        
        cursor.execute(sql, (self.nombre_ciudad, self.pais, "system"))
        conexion.commit()
        print("\nCiudad agregada correctamente.")
        
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
        """
        cursor.execute(sql)
        ciudades = cursor.fetchall()
        
        print("\n===== CIUDADES =====")
        for ciudad in ciudades:
            print(f"ID: {ciudad[0]} | Ciudad: {ciudad[1]} | País: {ciudad[2]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        print("\n===== NUEVA CIUDAD =====")
        nombre = input("Nombre de la ciudad: ")
        print("\nPAISES DISPONIBLES:")
        print("ID 1: Chile")
        print("ID 2: Venezuela")
        print("ID 3: China")
        print("ID 4: Brazil")
        print("ID 5: Perú")
        pais_id = input("ID del país: ")
        nueva_ciudad = ciudad(nombre, pais_id)
        nueva_ciudad.guardar()
    
    @staticmethod
    def eliminar():
        ciudad.listar()
        id_ciudad = input("\nIngrese ID de la ciudad: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE ciudades SET deleted = 1 WHERE id_ciudad = %s"
        cursor.execute(sql, (id_ciudad,))
        conexion.commit()
        print("\nCiudad eliminada correctamente.")
        
        cursor.close()
        conexion.close()