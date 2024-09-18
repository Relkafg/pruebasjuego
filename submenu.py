import pyglet
from pyglet.window import key, mouse
from pyglet.shapes import Rectangle
from pyglet.text import Label

class SubMenu(pyglet.window.Window):
    def __init__(self, width, height, caption, music_player, *args, **kwargs):
        super().__init__(width=width, height=height, caption=caption, *args, **kwargs)
        self.music_player = music_player

        # Barra de volumen
        self.volume_bar = Rectangle(self.width // 2 - 100, self.height // 2 - 50, 200, 40, color=(0, 120, 255))
        self.dragging = False  # Estado de arrastre

        # Sincronizar la posición inicial de la barra de volumen con el volumen global
        self.volume_bar.width = music_player.volume * 200

        # Botón de volver al menú principal
        self.return_button = Rectangle(self.width // 2 - 50, self.height // 4, 100, 40, color=(0, 255, 0))
        self.return_label = Label('Volver', font_size=16, x=self.width // 2, y=self.height // 4 + 20, anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()

        # Dibujar la barra de volumen
        self.volume_bar.draw()

        # Dibujar el botón de volver
        self.return_button.draw()
        self.return_label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if (self.volume_bar.x <= x <= self.volume_bar.x + self.volume_bar.width and
                self.volume_bar.y <= y <= self.volume_bar.y + self.volume_bar.height):
                self.dragging = True  # Iniciar arrastre
            elif (self.return_button.x <= x <= self.return_button.x + self.return_button.width and
                  self.return_button.y <= y <= self.return_button.y + self.return_button.height):
                # Cerrar la ventana del SubMenu
                self.close()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = False  # Terminar arrastre

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            new_width = x - self.volume_bar.x
            if 0 <= new_width <= 200:  # Asegurar que el ancho esté dentro del rango
                self.volume_bar.width = new_width  # Actualizar ancho de la barra de volumen
                self.update_volume(new_width)

    def update_volume(self, new_width):
        # Convertir el ancho de la barra a un valor de volumen entre 0.0 y 1.0
        volume = new_width / 200
        self.music_player.volume = volume
        print(f"Volume updated to: {volume}")  # Para depuración

if __name__ == "__main__":
    # Crear el player y cargar un archivo de música
    music_player = pyglet.media.Player()
    source = pyglet.media.load('your_music_file.mp3')  # Cambia a tu archivo de música
    music_player.queue(source)
    music_player.play()

    # Crear y mostrar el SubMenu
    submenu = SubMenu(800, 600, "Submenu", music_player=music_player)
    pyglet.app.run()
