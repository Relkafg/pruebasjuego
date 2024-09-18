import pyglet
import webbrowser
from pyglet.window import key


class VentanaInicial(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opciones = ["Esquivar", "Plataformas", "Demo", "Ajustes", "Salir"]

        # Etiquetas para las opciones en el centro
        self.etiquetas = [pyglet.text.Label(opcion, font_size=24, x=self.width // 4 * (i + 1), y=self.height // 2,
                                            anchor_x='center', anchor_y='center') for i, opcion in
                          enumerate(self.opciones[:-2])]

        # Etiqueta para "Ajustes" en la esquina inferior izquierda
        self.etiqueta_ajustes = pyglet.text.Label(self.opciones[-2], font_size=24, x=20, y=20,
                                                  anchor_x='left', anchor_y='bottom')

        # Etiqueta para "Salir" en la esquina inferior derecha
        self.etiqueta_salir = pyglet.text.Label(self.opciones[-1], font_size=24, x=self.width - 20, y=20,
                                                anchor_x='right', anchor_y='bottom')

        self.opcion_seleccionada = None
        self.cargar_recursos()

    def cargar_recursos(self):
        # Fondo
        self.fondo = pyglet.image.load('fondo_pantallaseleccion.png')
        self.fondo_sprite = pyglet.sprite.Sprite(self.fondo)

        # Escalar la imagen de fondo para ajustarse a la pantalla
        self.fondo_sprite.scale_x = self.width / self.fondo.width
        self.fondo_sprite.scale_y = self.height / self.fondo.height

        # Título
        self.titulo = pyglet.text.Label("My videogame ❤️", font_size=36, bold=True,
                                        x=self.width // 2, y=self.height - 50, anchor_x='center', anchor_y='center')

        # Imagen (GIF)
        animation = pyglet.image.load_animation('blizcan.gif')
        self.imagen = pyglet.sprite.Sprite(animation)
        self.imagen.x = (self.width - self.imagen.width) // 2
        self.imagen.y = (self.titulo.y - self.imagen.height) - 10

        # Velocidad de desplazamiento
        self.velocidad_x = 5

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        self.fondo_sprite.draw()

        # Dibujar otros elementos
        self.titulo.draw()
        self.imagen.draw()
        for etiqueta in self.etiquetas:
            etiqueta.draw()
        self.etiqueta_ajustes.draw()
        self.etiqueta_salir.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.seleccionar_opcion()

    def on_mouse_press(self, x, y, button, modifiers):
        self.seleccionar_opcion(x, y)

    def seleccionar_opcion(self, x=None, y=None):
        for i, etiqueta in enumerate(self.etiquetas):
            if etiqueta.x - etiqueta.content_width // 2 <= x <= etiqueta.x + etiqueta.content_width // 2 \
                    and etiqueta.y - etiqueta.content_height // 2 <= y <= etiqueta.y + etiqueta.content_height // 2:
                self.opcion_seleccionada = self.opciones[i]

                if self.opcion_seleccionada == "Demo":
                    ruta_html = 'file:///D:/2ºDAM/PaginaWebJuego/prueba.html'
                    print(f"Intentando abrir: {ruta_html}")
                    webbrowser.open(ruta_html)

                print(f"Seleccionaste: {self.opcion_seleccionada}")

                self.close()
                return
        if self.etiqueta_ajustes.x <= x <= self.etiqueta_ajustes.x + self.etiqueta_ajustes.content_width \
                and self.etiqueta_ajustes.y <= y <= self.etiqueta_ajustes.y + self.etiqueta_ajustes.content_height:
            self.opcion_seleccionada = "Ajustes"
            print("Seleccionaste: Ajustes")
            self.close()
        elif self.etiqueta_salir.x - self.etiqueta_salir.content_width <= x <= self.etiqueta_salir.x \
                and self.etiqueta_salir.y <= y <= self.etiqueta_salir.y + self.etiqueta_salir.content_height:
            self.opcion_seleccionada = "Salir"
            print("Seleccionaste: Salir")
            self.close()
        for i, etiqueta in enumerate(self.etiquetas):
            if etiqueta.x - etiqueta.content_width // 2 <= x <= etiqueta.x + etiqueta.content_width // 2 \
                    and etiqueta.y - etiqueta.content_height // 2 <= y <= etiqueta.y + etiqueta.content_height // 2:
                self.opcion_seleccionada = self.opciones[i]

                if self.opcion_seleccionada == "Demo Pagina":
                    webbrowser.open(
                        'file:///ruta/a/tu/demo/index.html')  # Cambia esta ruta a la ruta de tu archivo HTML local

                print(f"Seleccionaste: {self.opcion_seleccionada}")
                self.close()
                return

    def obtener_opcion_seleccionada(self):
        return self.opcion_seleccionada

    def cerrar_ventana(self):
        self.close()


if __name__ == "__main__":
    ventana_inicial = VentanaInicial(width=800, height=600, caption="Ventana Inicial")
    pyglet.app.run()
