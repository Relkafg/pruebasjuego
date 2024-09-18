import pyglet

class Player:
    def __init__(self, x, y, window_width):
        self.x = x
        self.y = y
        self.window_width = window_width
        self.radius = 25  # Ajusta este valor según el tamaño de tu sprite

        # Cargar imágenes de animación para correr hacia la derecha
        self.run_right_images = [
            pyglet.resource.image(f'Warrior_Run_{i}.png') for i in range(1, 9)
        ]
        for image in self.run_right_images:
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2

        # Crear la animación para correr hacia la derecha
        self.run_right_animation = pyglet.image.Animation.from_image_sequence(
            self.run_right_images, duration=0.1, loop=True
        )

        # Crear la animación para correr hacia la izquierda invirtiendo las imágenes
        self.run_left_images = [image.get_transform(flip_x=True) for image in self.run_right_images]
        self.run_left_animation = pyglet.image.Animation.from_image_sequence(
            self.run_left_images, duration=0.1, loop=True
        )

        # Cargar imágenes de animación para estar quieto (idle)
        self.idle_images = [
            pyglet.resource.image(f'Warrior_Idle_{i}.png') for i in range(1, 7)
        ]
        for image in self.idle_images:
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2

        # Crear la animación para estar quieto (idle)
        self.idle_animation = pyglet.image.Animation.from_image_sequence(
            self.idle_images, duration=0.1, loop=True
        )

        # Crear un sprite inicial para el jugador
        self.sprite = pyglet.sprite.Sprite(self.idle_animation, x=self.x, y=self.y)

    def update(self, keys, game_over):
        if not game_over:
            moving_left = keys[pyglet.window.key.LEFT]
            moving_right = keys[pyglet.window.key.RIGHT]

            if moving_left:
                self.sprite.image = self.run_left_animation
                self.x -= 8
            elif moving_right:
                self.sprite.image = self.run_right_animation
                self.x += 8
            else:
                self.sprite.image = self.idle_animation

            # Asegurar que el jugador no salga de la pantalla
            self.x = max(self.radius, min(self.window_width - self.radius, self.x))

            # Actualizar la posición del sprite
            self.sprite.x = self.x
            self.sprite.y = self.y

    def draw_idle_animation(self):
        self.sprite.image = self.idle_animation

    def draw(self):
        self.sprite.draw()


