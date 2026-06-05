import os
from ciudad import ciudad
from tipoUsuario import tipoUsuario
from usuarios import usuario
from equipos import Equipo
from torneo import Torneo

def limpiar_consola():
    os.system('cls')

# BUCLE WHILE
go = True
while go:
    print("\n\nSISTEMA DE GESTION DE TORNEOS\n")
    
    print("\n   --- CIUDADES ---")
    print("   1. Listar ciudades")
    print("   2. Agregar ciudad")
    print("   3. Eliminar ciudad")
    
    print("\n   --- TIPOS DE USUARIO ---")
    print("   4. Listar tipos de usuario")
    print("   5. Agregar tipo de usuario")
    print("   6. Validar tipo de usuario")
    print("   7. Eliminar tipo de usuario")
    
    print("\n   --- USUARIOS ---")
    print("   8. Listar usuarios")
    print("   9. Listar usuarios (vista simple)")
    print("   10. Agregar usuario")
    print("   11. Actualizar email de usuario")
    print("   12. Cambiar ciudad de usuario")
    print("   13. Cambiar tipo de usuario")
    print("   14. Validar edad de usuario")
    print("   15. Eliminar usuario")
    
    print("\n   --- EQUIPOS ---")
    print("   16. Listar equipos")
    print("   17. Agregar equipo")
    print("   18. Ver miembros de un equipo")
    print("   19. Agregar miembro a equipo")
    print("   20. Eliminar equipo")
    
    print("\n   --- TORNEOS ---")
    print("   21. Listar torneos")
    print("   22. Agregar torneo")
    print("   23. Buscar torneo por juego")
    print("   24. Inscribir equipo en torneo")
    print("   25. Eliminar torneo")
    
    print("\n  0. Salir\n")
    
    elect = int(input("\nSeleccione una opción: "))
    
    # ========== CIUDADES ==========
    if elect == 1:
        limpiar_consola()
        ciudad.listar()
    
    elif elect == 2:
        limpiar_consola()
        ciudad.agregar()
    
    elif elect == 3:
        limpiar_consola()
        ciudad.eliminar()
    
    # ========== TIPOS DE USUARIO ==========
    elif elect == 4:
        limpiar_consola()
        tipoUsuario.listar()
    
    elif elect == 5:
        limpiar_consola()
        tipoUsuario.agregar()
    
    elif elect == 6:
        limpiar_consola()
        tipoUsuario.validar()
    
    elif elect == 7:
        limpiar_consola()
        tipoUsuario.eliminar()
    
    # ========== USUARIOS ==========
    elif elect == 8:
        limpiar_consola()
        usuario.listar()
    
    elif elect == 9:
        limpiar_consola()
        usuario.listar_simple()
    
    elif elect == 10:
        limpiar_consola()
        usuario.agregar()
    
    elif elect == 11:
        limpiar_consola()
        usuario.actualizar()
    
    elif elect == 12:
        limpiar_consola()
        usuario.cambiar_ciudad()
    
    elif elect == 13:
        limpiar_consola()
        usuario.cambiar_tipo()
    
    elif elect == 14:
        limpiar_consola()
        usuario.validar_edad()
    
    elif elect == 15:
        limpiar_consola()
        usuario.eliminar()
    
    # ========== EQUIPOS ==========
    elif elect == 16:
        limpiar_consola()
        Equipo.listar()
    
    elif elect == 17:
        limpiar_consola()
        Equipo.agregar()
    
    elif elect == 18:
        limpiar_consola()
        Equipo.ver_miembros()
    
    elif elect == 19:
        limpiar_consola()
        Equipo.agregar_miembro()
    
    elif elect == 20:
        limpiar_consola()
        Equipo.eliminar()
    
    # ========== TORNEOS ==========
    elif elect == 21:
        limpiar_consola()
        Torneo.listar()
    
    elif elect == 22:
        limpiar_consola()
        Torneo.agregar()
    
    elif elect == 23:
        limpiar_consola()
        Torneo.buscar_por_juego()
    
    elif elect == 24:
        limpiar_consola()
        Torneo.inscribir_equipo()
    
    elif elect == 25:
        limpiar_consola()
        Torneo.eliminar()
    
    elif elect == 0:
        limpiar_consola()
        print("\nok bye...")
        go = False
    else:
        print("\nPor favor seleccionar elemento válido...")