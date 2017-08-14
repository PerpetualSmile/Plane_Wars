import pygame
from pygame.sprite import Sprite
import random


class Invaders(Sprite):
    """表示单个入侵者的类"""

    def __init__(self, ai_settings, screen):
        """初始化入侵者，并设置起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.is_live = 0

        # 加载入侵者图像，并设置其rect属性
        self.image = pygame.image.load_extended('images/f35(1).png')
        self.image = pygame.transform.scale(self.image, (ai_settings.invader_width, ai_settings.invader_height))
        self.rect = self.image.get_rect()

        # 设置每个入侵者出现位置
        self.rect.x = float(self.rect.width)
        self.rect.y = float(0)

        # 存储入侵者的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 制造动态效果图
        self.index = 0
        self.image2 = pygame.image.load_extended('images/f35(2).png')
        self.image2 = pygame.transform.scale(self.image2, (ai_settings.ship_width, ai_settings.ship_height))
        self.image3 = pygame.image.load_extended('images/f35(3).png')
        self.image3 = pygame.transform.scale(self.image3, (ai_settings.ship_width, ai_settings.ship_height))
        self.image_list = []
        self.image_list.append(self.image)
        self.image_list.append(self.image2)
        self.image_list.append(self.image3)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image_list[self.index % 2], self.rect)
        self.index += 1

    def update(self):
        """移动入侵者"""
        self.y += self.ai_settings.invader_speed
        self.rect.y = self.y


    def check_edges(self):
        """检测入侵者是否超出屏幕"""
        screen_rect = self.screen.get_rect()
        if self.rect.top >= screen_rect.bottom:
            return True
        elif self.rect.left >= screen_rect.right:
            return True
        elif self.rect.right <= screen_rect.left:
            return True
        return False

    def boom(self):
        self.image_list[0] = self.image3
        self.image_list[1] = self.image3
        self.is_live += 1
