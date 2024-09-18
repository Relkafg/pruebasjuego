import pyglet
from pyglet.window import key

class PantallaCarga(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cargar_recursos()

    def cargar_recursos(self):
        imagen = pyglet.image.load('fondo_pantallacarga.png')

        # Escalar la imagen para que ocupe toda la pantalla
        self.imagen = pyglet.sprite.Sprite(imagen)
        self.imagen.scale_x = self.width / self.imagen.width
        self.imagen.scale_y = self.height / self.imagen.height

        # Centrar la imagen
        self.imagen.x = (self.width - self.imagen.width) // 2
        self.imagen.y = (self.height - self.imagen.height) // 2

    def on_draw(self):
        self.clear()
        self.imagen.draw()  # Dibuja la imagen de fondo

        # Etiqueta para la primera línea de texto en negrita
        pyglet.text.Label("PRESIONA ENTER", font_size=36, x=self.width // 2, y=self.height // 2 + 50,
                          anchor_x='center', anchor_y='center', bold=True).draw()

        # Etiqueta para la segunda línea de texto en negrita
        pyglet.text.Label("PARA CONTINUAR", font_size=36, x=self.width // 2, y=self.height // 2 - 50,
                          anchor_x='center', anchor_y='center', bold=True).draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            # Lógica para continuar después de cargar
            self.close()

    def cerrar_ventana(self):
        self.close()

