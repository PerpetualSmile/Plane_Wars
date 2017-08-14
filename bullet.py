import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """对飞船发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 在（0,0）处创建一个表示子弹的矩形， 再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed
        self.load_image()
        self.index = 0

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        # 制造子弹尾部火焰的动态效果
        self.screen.blit(self.image[self.index % 2], self.rect)
        self.index += 1

    def load_image(self):
        self.image1 = pygame.image.load_extended('images/导弹1.png')
        self.image1 = pygame.transform.scale(self.image1, (self.ai_settings.bullet_width, self.ai_settings.bullet_height))
        self.image2 = pygame.image.load_extended('images/导弹2.png')
        self.image2 = pygame.transform.scale(self.image2,
                                             (self.ai_settings.bullet_width, self.ai_settings.bullet_height))
        self.image = []
        self.image.append(self.image1)
        self.image.append(self.image2)


