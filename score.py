import pyglet

class ScoreLabel:
    def __init__(self, lives, window):
        self.label = pyglet.text.Label(f'Lives: {lives}',
                                       font_name='Arial',
                                       font_size=14,
                                       x=window.width - 80,
                                       y=window.height - 20,
                                       anchor_x='right',
                                       anchor_y='center')

    def update(self, lives):
        self.label.text = f'Lives: {lives}'

    def draw(self):
        self.label.draw()
