from conexion import Conexion

class tipoUsuario:
    # Define los roles que pueden tener los usuarios en el sistema
    tipos_disponibles = []  # Atributo de clase
    
    def __init__(self, nombre_tipo, descripcion_tipo):
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
        tipoUsuario.tipos_disponibles.append(self)
    
    def mostrar_info(self):  # Método de instancia
        return f"Rol: {self.nombre_tipo}\nDescripción: {self.descripcion_tipo}"
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = %s", (self.nombre_tipo,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nError: El tipo '{self.nombre_tipo}' ya existe.")
            cursor.close()
            conexion.close()
            return
        
        sql = "INSERT INTO tipo_usuarios (nombre_tipo, descripcion_tipo, created_by) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.nombre_tipo, self.descripcion_tipo, "system"))
        conexion.commit()
        print("\nTipo de usuario agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @classmethod
    def buscar_tipo_por_nombre(cls, nombre):  # Método de clase
        # Busca un tipo de usuario por su nombre
        for tipo in cls.tipos_disponibles:
            if tipo.nombre_tipo.lower() == nombre.lower():
                return tipo
        return None
    
    @staticmethod
    def validar_nombre_tipo(nombre):  # Método estático
        # Valida si el nombre del tipo es correcto
        nombres_validos = ["jugador", "admin", "jugador lider", "equipo tecnico", "comentarista"]
        return nombre.lower() in nombres_validos
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_tipo_usuario, nombre_tipo, descripcion_tipo FROM tipo_usuarios WHERE deleted = 0"
        cursor.execute(sql)
        tipos = cursor.fetchall()
        
        print("\n===== TIPOS DE USUARIO =====")
        for tipo in tipos:
            print(f"ID: {tipo[0]} | Tipo: {tipo[1]} | Descripción: {tipo[2]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        print("\n===== NUEVO TIPO DE USUARIO =====")
        nombre = input("Nombre del tipo: ")
        desc = input("Descripción: ")
        tipo = tipoUsuario(nombre, desc)
        tipo.guardar()
    
    @staticmethod
    def validar():
        nombre = input("Ingrese tipo a validar: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = %s AND deleted = 0", (nombre,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nEl tipo '{nombre}' existe.")
        else:
            print(f"\nEl tipo '{nombre}' no existe.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def eliminar():
        tipoUsuario.listar()
        id_tipo = input("\nIngrese ID del tipo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE tipo_usuarios SET deleted = 1 WHERE id_tipo_usuario = %s"
        cursor.execute(sql, (id_tipo,))
        conexion.commit()
        print("\nTipo de usuario eliminado correctamente.")
        
        cursor.close()
        conexion.close()