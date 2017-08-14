import pygame


class Musics:
    """用于控制背景音乐的类"""

    def __init__(self):
        self.fire_music = pygame.mixer.Sound("music/导弹发射.wav")
        self.fire_music.set_volume(0.3)

        self.boom = pygame.mixer.Sound("music/boom.wav")
        self.boom.set_volume(0.2)

        self.bgmusic = pygame.mixer.Sound("music/bg.wav")
        self.bgmusic.set_volume(0.3)


