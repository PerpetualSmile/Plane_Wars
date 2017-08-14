import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ship_speed = ai_settings.ship_speed

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load_extended('images/歼20(1).png')
        self.image = pygame.transform.scale(self.image, (ai_settings.ship_width, ai_settings.ship_height))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom


        # 动态化飞船尾气
        self.index = 0
        self.image2 = pygame.image.load_extended('images/歼20(2).png')
        self.image2 = pygame.transform.scale(self.image2, (ai_settings.ship_width, ai_settings.ship_height))
        self.image_list = []
        self.image_list.append(self.image)
        self.image_list.append(self.image2)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image_list[self.index % 2], self.rect)
        self.index += 1

    def update(self):
        """根据键盘输入实时更新飞船状态"""
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ship_speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > self.screen_rect.top:
            self.rect.centery -= self.ship_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += self.ship_speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > self.screen_rect.left:
            self.rect.centerx -= self.ship_speed

    def center_ship(self):
        """让飞船回到屏幕底部初始位置"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom