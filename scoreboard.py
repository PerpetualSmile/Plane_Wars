import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分等信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 显示图像
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为图像"""
        score_str = "Score: " + "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.prep_score()
        self.prep_high_score()
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def prep_high_score(self):
        """将最高得分渲染为图像"""
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def show_level(self):
        """显示当前游戏等级"""
        self.level_image = self.font.render("Level: "+str(self.ai_settings.level), True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        self.screen.blit(self.level_image, self.level_rect)

    def prep_ships(self):
        self.ships = Group()

        # 控制显示生命的图像大小
        x, y = self.ai_settings.ship_width, self.ai_settings.ship_height
        self.ai_settings.ship_width = 50
        self.ai_settings.ship_height = 60

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
        self.ai_settings.ship_width, self.ai_settings.ship_height = x, y

    def show_ships(self):
        """显示剩余多少飞船"""
        self.ships.draw(self.screen)