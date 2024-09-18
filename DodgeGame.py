import pyglet
from pyglet.window import mouse
from player import Player
from score import ScoreLabel
import random
import math


class DodgeGame(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(DodgeGame, self).__init__(*args, **kwargs)

        # Jugador
        self.player = Player(self.width // 2, 20, self.width)
        self.collision_state = False

        # Objetos que caen
        self.falling_objects = []
        self.object_speed = 150
        self.spawn_interval = 10
        self.difficulty_increase_interval = 10
        self.time_since_difficulty_increase = 0

        # Puntuación (Número de vidas)
        self.lives = 3
        self.score_label = ScoreLabel(self.lives, self)

        # Estado del juego
        self.game_over = False

        # Manejar la entrada del teclado
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.fps_display = pyglet.window.FPSDisplay(self)

        # Configurar la sincronización vertical (VSync) para limitar la tasa de FPS
        pyglet.options['vsync'] = True

        # Cargar imágenes de las bolas
        self.blue_ball_image = pyglet.resource.image('blue_ball.png')
        self.green_ball_image = pyglet.resource.image('green_ball.png')

        # Configuración de la actualización del juego
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

        # Contador de bolas azules
        self.blue_ball_counter = 0

        # Temporizador de juego
        self.time_elapsed = 0
        self.time_label = pyglet.text.Label(
            text=f'{self.time_elapsed:.1f}s',
            font_name='Arial',
            font_size=18,
            x=10, y=self.height - 20,
            anchor_x='left', anchor_y='top',
            color=(255, 255, 255, 255)
        )

        # Mensaje de fin del juego
        self.game_over_label = pyglet.text.Label(
            text='JUEGO FINALIZADO',
            font_name='Arial',
            font_size=36,
            x=self.width // 2, y=self.height // 2,
            anchor_x='center', anchor_y='center',
            color=(255, 0, 0, 255),
            bold=True
        )
        self.game_over_label.visible = False

        self.replay_button = pyglet.text.Label(
            text='Reintentar',
            font_name='Arial',
            font_size=24,
            x=self.width // 2, y=self.height // 2 - 50,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255),
            bold=True
        )
        self.replay_button.visible = False

        self.main_menu_button = pyglet.text.Label(
            text='Menú Principal',
            font_name='Arial',
            font_size=24,
            x=self.width // 2, y=self.height // 2 - 100,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255),
            bold=True
        )
        self.main_menu_button.visible = False

    def spawn_object(self):
        if len(self.falling_objects) < 30:
            x = random.uniform(self.player.radius, self.width - self.player.radius)
            y = self.height + self.player.radius
            speed = self.object_speed + random.uniform(0, 50)
            object_radius = random.uniform(30, 50)
            if self.blue_ball_counter < 20:
                color = (0, 0, 255)  # Azul
                new_object = pyglet.sprite.Sprite(self.blue_ball_image, x=x, y=y)
                new_object.scale = object_radius / self.blue_ball_image.width
                self.blue_ball_counter += 1
            else:
                color = (0, 255, 0)  # Verde
                new_object = pyglet.sprite.Sprite(self.green_ball_image, x=x, y=y)
                new_object.scale = object_radius / self.green_ball_image.width
                self.blue_ball_counter = 0

            self.falling_objects.append({'sprite': new_object, 'speed': speed, 'radius': object_radius})
        else:
            recycled_object = self.falling_objects.pop(0)
            recycled_object['sprite'].x = random.uniform(self.player.radius, self.width - self.player.radius)
            recycled_object['sprite'].y = self.height + self.player.radius
            recycled_object['speed'] = self.object_speed + random.uniform(0, 50)
            recycled_object['radius'] = random.uniform(30, 50)
            self.falling_objects.append(recycled_object)

    def update(self, dt):
        if self.game_over:
            return

        self.time_elapsed += dt
        self.time_label.text = f'{self.time_elapsed:.1f}s'

        self.time_since_difficulty_increase += dt

        self.player.update(self.keys, self.game_over)

        if self.keys[pyglet.window.key.LEFT] or self.keys[pyglet.window.key.RIGHT]:
            self.collision_state = False

        for obj in self.falling_objects:
            obj['sprite'].y -= obj['speed'] * dt * 2
            if obj['sprite'].y < -obj['sprite'].height:
                self.falling_objects.remove(obj)

        if random.random() < 1 / self.spawn_interval:
            self.spawn_object()

        if self.time_since_difficulty_increase > self.difficulty_increase_interval:
            self.object_speed += 20
            self.spawn_interval *= 0.8
            self.time_since_difficulty_increase = 0

        for obj in self.falling_objects:
            if self.check_collision(self.player, obj, 0.8):
                self.falling_objects.remove(obj)
                if obj['sprite'].image == self.blue_ball_image:
                    self.lives -= 1
                else:
                    self.lives += 1
                self.score_label.update(self.lives)
                if self.lives <= 0:
                    self.game_over = True
                    self.game_over_label.visible = True
                    self.replay_button.visible = True
                    self.main_menu_button.visible = True
                break


    def check_collision(self, player, obj, adjustment_factor=0.02):
        # Ajuste para que la zona de colisión esté más centrada visualmente en el personaje
        adjusted_y = player.y - player.sprite.height / 4
        distance = math.sqrt((player.x - obj['sprite'].x)**2 + (adjusted_y - obj['sprite'].y)**2)
        return distance < (player.radius + obj['radius']) * adjustment_factor

    def on_draw(self):
        self.clear()
        self.player.draw()
        for obj in self.falling_objects:
            obj['sprite'].draw()
            self.score_label.draw()
            self.time_label.draw()
            if self.game_over:
                self.game_over_label.draw()
                self.replay_button.draw()
                self.main_menu_button.draw()
            self.fps_display.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over and button == mouse.LEFT:
            if self.replay_button.x - self.replay_button.content_width / 2 < x < self.replay_button.x + self.replay_button.content_width / 2 and \
               self.replay_button.y - self.replay_button.content_height / 2 < y < self.replay_button.y + self.replay_button.content_height / 2:
                self.restart_game()
            elif self.main_menu_button.x - self.main_menu_button.content_width / 2 < x < self.main_menu_button.x + self.main_menu_button.content_width / 2 and \
                 self.main_menu_button.y - self.main_menu_button.content_height / 2 < y < self.main_menu_button.y + self.main_menu_button.content_height / 2:
                self.return_to_main_menu()

    def restart_game(self):
        # Restablecer todas las configuraciones del juego
        self.lives = 3
        self.score_label.update(self.lives)
        self.time_elapsed = 0
        self.game_over = False
        self.game_over_label.visible = False
        self.replay_button.visible = False
        self.main_menu_button.visible = False
        self.falling_objects.clear()
        self.player.x = self.width // 2
        self.player.draw_idle_animation()

    def return_to_main_menu(self):
        self.close()
        import main
        main.iniciar_menu()

if __name__ == '__main__':
    game = DodgeGame()
    pyglet.app.run()