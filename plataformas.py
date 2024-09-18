import pyglet
from pyglet.window import key
from pyglet import shapes

class Plataforma(pyglet.shapes.Rectangle):
    def __init__(self, x, y, width, height, batch=None):
        super().__init__(x, y, width, height, color=(0, 0, 0, 0), batch=batch)

class Plataformas(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Plataformas, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        
        self.plataformas = [
            Plataforma(0, 82, 200, 20, self.batch),   # Suelo imaginario
            Plataforma(310, 132, 300, 20, self.batch),
            Plataforma(390, 250, 120, 5, self.batch),
            Plataforma(648, 330, 152, 130, self.batch),  # Nueva plataforma
            Plataforma(595, 82, 20, 70, self.batch),  # Nueva plataforma
            Plataforma(0, 463, 203, 20, self.batch),  # Nueva plataforma
            Plataforma(648, 460, 152, 20, self.batch),  # Nueva plataforma
            Plataforma(615, 82, 100, 20, self.batch),  # Nueva plataforma
            Plataforma(0, 385, 203, 80, self.batch), # Nueva plataforma
            Plataforma(117, 267, 150, 20, self.batch),   # Nueva plataforma
            Plataforma(305, 385, 100, 10, self.batch),
            Plataforma(452, 438, 97, 20, self.batch)
        ]

        

        self.volver_button = pyglet.shapes.Rectangle(
            x=10,
            y=self.height - 50,
            width=100,
            height=40,
            color=(0, 255, 0)
        )

        self.volver_label = pyglet.text.Label(
            'Volver',
            font_name='Arial',
            font_size=18,
            x=self.volver_button.x + self.volver_button.width // 2,
            y=self.volver_button.y + self.volver_button.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 255)
            
        )

        self.player = shapes.Rectangle(120, 170, 20, 20, color=(50, 225, 30), batch=self.batch)
        self.player.dx = 0
        self.player.dy = 0
        
        self.gravity = -0.5
        self.jump_strength = 11

        self.fps_display = pyglet.window.FPSDisplay(self)
        
        self.vidas = 3
        self.etiqueta_vidas = pyglet.text.Label('Vidas: {}'.format(self.vidas),
                                                font_name='Arial',
                                                font_size=14,
                                                x=self.width - 100,
                                                y=self.height - 20,
                                                anchor_x='center',
                                                anchor_y='center',
                                                color=(50, 50, 50, 255),  # Color más oscuro
                                                bold=True)  # Texto en negrita
        
        self.juego_terminado = False
        self.etiqueta_reintentar = pyglet.text.Label('Presiona "R" para reintentar',
                                                     font_name='Arial',
                                                     font_size=20,
                                                     x=self.width // 2,
                                                     y=self.height // 2,
                                                     anchor_x='center',
                                                     anchor_y='center')
        
        
        self.keys = {}

        
        
        fondo_image = pyglet.image.load('fondo.png')
        self.fondo = pyglet.sprite.Sprite(fondo_image)

        self.fondo.scale_x = self.width / self.fondo.width
        self.fondo.scale_y = self.height / self.fondo.height
        
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        
    def on_draw(self):
        self.clear()
        
        self.fondo.draw()
        
        self.batch.draw()
        self.volver_label.draw()
        self.etiqueta_vidas.draw()
        if self.juego_terminado:
            self.etiqueta_reintentar.draw()
        self.fps_display.draw()

        
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.volver_button.x <= x <= self.volver_button.x + self.volver_button.width and \
           self.volver_button.y <= y <= self.volver_button.y + self.volver_button.height:
            self.return_to_main_menu()
            print("Volviendo a la pantalla anterior")
        
    def update(self, dt):
        if not self.juego_terminado:
            self.player.dx = 0
            if key.LEFT in self.keys:
                self.player.dx = -200 * dt
            if key.RIGHT in self.keys:
                self.player.dx = 200 * dt
            if key.SPACE in self.keys and any(self.is_on_platform(plataforma) for plataforma in self.plataformas):
                self.player.dy = self.jump_strength

            self.player.dy += self.gravity

            # Guardar la posición y del jugador antes de moverlo
            previous_y = self.player.y

            self.player.x += self.player.dx
            self.player.y += self.player.dy

            for plataforma in self.plataformas:
                if self.is_on_platform(plataforma):
                    if self.player.dy < 0:  # Jugador cayendo
                        self.player.y = plataforma.y + plataforma.height
                        self.player.dy = 0
                    elif self.player.dy > 0:  # Jugador saltando
                        self.player.y = previous_y
                        self.player.dy = 0
                    else:  # Jugador estático o moviéndose lateralmente en la plataforma
                        # Solo ajustar la posición lateral si el jugador no está sobre la plataforma
                        if not (key.LEFT in self.keys or key.RIGHT in self.keys):
                            if self.player.x + self.player.width > plataforma.x and self.player.x < plataforma.x + plataforma.width:
                                self.player.y = plataforma.y + plataforma.height
                                self.player.dy = 0
                                break
                        # Manejar colisiones laterales
                        if self.player.dx > 0:  # Movimiento hacia la derecha
                            self.player.x = plataforma.x - self.player.width
                        elif self.player.dx < 0:  # Movimiento hacia la izquierda
                            self.player.x = plataforma.x + plataforma.width
                    break


            if self.player.y < 0:
                self.vidas -= 1
                self.reset_player()
                self.etiqueta_vidas.text = 'Vidas: {}'.format(self.vidas)
                if self.vidas <= 0:
                    self.juego_terminado = True

    
    def is_on_platform(self, plataforma):
        return (self.player.x + self.player.width > plataforma.x and
                self.player.x < plataforma.x + plataforma.width and
                self.player.y <= plataforma.y + plataforma.height and
                self.player.y + self.player.height >= plataforma.y)
    
    def reset_player(self):
        self.player.x = 120
        self.player.y = 170
        self.player.dx = 0
        self.player.dy = 0
        
    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True
        if symbol == key.R and self.juego_terminado:
            self.vidas = 3
            self.etiqueta_vidas.text = 'Vidas: {}'.format(self.vidas)
            self.reset_player()
            self.juego_terminado = False
        
    def on_key_release(self, symbol, modifiers):
        self.keys.pop(symbol, None)

    def return_to_main_menu(self):
        self.close()
        import main
        main.iniciar_menu()
    
    

if __name__ == '__main__':
    window = Plataformas(800, 600, "Juego de Plataformas")
    pyglet.app.run()
