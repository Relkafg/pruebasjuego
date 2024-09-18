import pyglet
from pyglet.window import key, mouse
from DodgeGame import DodgeGame
from pantalla_carga import PantallaCarga
from ventana_inicial import VentanaInicial
from plataformas import Plataformas
from submenu import SubMenu

# Configuración de la actualización del juego
pyglet.clock.schedule_interval(lambda dt: None, 1 / 75.0)
# Definir la música de fondo globalmente
music_player = pyglet.media.Player()
music_loaded = False  # Variable global para rastrear el estado de la música

def iniciar_musica():
    global music_loaded
    if not music_loaded:
        music = pyglet.media.load('musica.mp3')
        music_player.queue(music)
        music_player.loop = True
        music_player.volume = 0.1  # Ajustar el volumen según lo desees
        music_player.play()
        music_loaded = True

def iniciar_menu():
    # Después de que la pantalla de carga se cierre, inicia la ventana inicial
    ventana_inicial = VentanaInicial(width=800, height=600, caption="Ventana Inicial")
    ventana_inicial.set_visible(True)
    pyglet.app.run()
    
    opcion_seleccionada = ventana_inicial.obtener_opcion_seleccionada()
    ventana_inicial.cerrar_ventana()

    if opcion_seleccionada == 'Esquivar':
        print("Ejecutando código para Opción 1")
        game = DodgeGame(width=800, height=600, caption="Dodge")
        game.set_visible(True)
        pyglet.app.run()

    elif opcion_seleccionada == 'Plataformas':
        print("Ejecutando código para Opción 2")
        op2 = Plataformas(width=800, height=600, caption="Plataformas")
        op2.set_visible(True)
        pyglet.app.run()

    elif opcion_seleccionada == 'Ajustes':
        print("Ejecutando código para Opción 3")
        submenu = SubMenu(800, 600, "Submenu", music_player)
        submenu.set_visible(True)
        pyglet.app.run()
        iniciar_menu()  # Vuelve al menú principal después de cerrar el SubMenu

    elif opcion_seleccionada == 'Salir':
        print("Saliendo de la aplicación")
        # Puedes agregar lógica adicional para salir de la aplicación



if __name__ == "__main__":
    iniciar_musica()
    # Inicia la pantalla de carga
    pantalla_carga = PantallaCarga(width=800, height=600, caption="Cargando...")
    pantalla_carga.set_visible(True)
    pyglet.app.run()
    pantalla_carga.cerrar_ventana()

    iniciar_menu()
