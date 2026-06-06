# main.py
import os
from ciudad import Ciudad
from tipoUsuario import TipoUsuario
from usuarios import Usuario
from equipos import Equipo
from torneo import Torneo
from pais import Pais

def limpiar_consola():
    os.system('cls')

go = True
while go:
    print("\n\nSISTEMA DE GESTION DE TORNEOS\n")
    
    print("\n   --- PAISES ---")
    print("   1. Listar paises")
    print("   2. Agregar pais")
    print("   3. Eliminar pais")
    
    print("\n   --- CIUDADES ---")
    print("   4. Listar ciudades")
    print("   5. Agregar ciudad")
    print("   6. Eliminar ciudad")
    
    print("\n   --- TIPOS DE USUARIO ---")
    print("   7. Listar tipos de usuario")
    print("   8. Agregar tipo de usuario")
    print("   9. Validar tipo de usuario")
    print("   10. Eliminar tipo de usuario")
    
    print("\n   --- USUARIOS ---")
    print("   11. Listar usuarios")
    print("   12. Listar usuarios (vista simple)")
    print("   13. Agregar usuario")
    print("   14. Actualizar email de usuario")
    print("   15. Cambiar ciudad de usuario")
    print("   16. Cambiar tipo de usuario")
    print("   17. Validar edad de usuario")
    print("   18. Eliminar usuario")
    
    print("\n   --- EQUIPOS ---")
    print("   19. Listar equipos")
    print("   20. Agregar equipo")
    print("   21. Ver miembros de un equipo")
    print("   22. Agregar miembro a equipo")
    print("   23. Eliminar equipo")
    
    print("\n   --- TORNEOS ---")
    print("   24. Listar torneos")
    print("   25. Agregar torneo")
    print("   26. Buscar torneo por juego")
    print("   27. Inscribir equipo en torneo")
    print("   28. Eliminar torneo")
    
    print("\n   --- PARTIDAS ---")
    print("   29. Listar partidas")
    print("   30. Agregar partida")
    print("   31. Actualizar resultado de partida")
    print("   32. Eliminar partida")
    
    print("\n   --- SANCIONES ---")
    print("   33. Listar sanciones")
    print("   34. Agregar sancion")
    print("   35. Eliminar sancion")
    
    print("\n  0. Salir\n")
    
    elect = int(input("\nSeleccione una opcion: "))
    
    if elect == 1:
        limpiar_consola()
        Pais.listar()
    
    elif elect == 2:
        limpiar_consola()
        Pais.agregar()
    
    elif elect == 3:
        limpiar_consola()
        Pais.eliminar()
    
    elif elect == 4:
        limpiar_consola()
        Ciudad.listar()
    
    elif elect == 5:
        limpiar_consola()
        Ciudad.agregar()
    
    elif elect == 6:
        limpiar_consola()
        Ciudad.eliminar()
    
    elif elect == 7:
        limpiar_consola()
        TipoUsuario.listar()
    
    elif elect == 8:
        limpiar_consola()
        TipoUsuario.agregar()
    
    elif elect == 9:
        limpiar_consola()
        TipoUsuario.validar()
    
    elif elect == 10:
        limpiar_consola()
        TipoUsuario.eliminar()
    
    elif elect == 11:
        limpiar_consola()
        Usuario.listar()
    
    elif elect == 12:
        limpiar_consola()
        Usuario.listar_simple()
    
    elif elect == 13:
        limpiar_consola()
        Usuario.agregar()
    
    elif elect == 14:
        limpiar_consola()
        Usuario.actualizar()
    
    elif elect == 15:
        limpiar_consola()
        Usuario.cambiar_ciudad()
    
    elif elect == 16:
        limpiar_consola()
        Usuario.cambiar_tipo()
    
    elif elect == 17:
        limpiar_consola()
        Usuario.validar_edad()
    
    elif elect == 18:
        limpiar_consola()
        Usuario.eliminar()
    
    elif elect == 19:
        limpiar_consola()
        Equipo.listar()
    
    elif elect == 20:
        limpiar_consola()
        Equipo.agregar()
    
    elif elect == 21:
        limpiar_consola()
        Equipo.ver_miembros()
    
    elif elect == 22:
        limpiar_consola()
        Equipo.agregar_miembro()
    
    elif elect == 23:
        limpiar_consola()
        Equipo.eliminar()
    
    elif elect == 24:
        limpiar_consola()
        Torneo.listar()
    
    elif elect == 25:
        limpiar_consola()
        Torneo.agregar()
    
    elif elect == 26:
        limpiar_consola()
        Torneo.buscar_por_juego()
    
    elif elect == 27:
        limpiar_consola()
        Torneo.inscribir_equipo()
    
    elif elect == 28:
        limpiar_consola()
        Torneo.eliminar()
    
    elif elect == 29:
        limpiar_consola()
        Torneo.listar_partidas()
    
    elif elect == 30:
        limpiar_consola()
        Torneo.agregar_partida()
    
    elif elect == 31:
        limpiar_consola()
        Torneo.actualizar_resultado()
    
    elif elect == 32:
        limpiar_consola()
        Torneo.eliminar_partida()
    
    elif elect == 33:
        limpiar_consola()
        Torneo.listar_sanciones()
    
    elif elect == 34:
        limpiar_consola()
        Torneo.agregar_sancion()
    
    elif elect == 35:
        limpiar_consola()
        Torneo.eliminar_sancion()
    
    elif elect == 0:
        limpiar_consola()
        print("\nok bye...")
        go = False
    else:
        print("\nPor favor seleccionar elemento valido...")