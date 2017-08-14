import pygame


class Settings:
    """存储所有设置"""

    def __init__(self):
        """初始化游戏的设置"""
        # 更改设置还需要改初始化函数initialize_setting

        # 屏幕的设置
        self.screen_width = 1200
        self.screen_height = 1000
        self.bg_color = (150, 174, 184)

        # 飞船设置
        self.ship_speed = float(5)
        self.ship_width = 110
        self.ship_height = 130
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = float(3)
        self.bullet_width = 30
        self.bullet_height = 80
        self.bullet_color = 0, 0, 0
        self.bullets_allowed = 8

        # 入侵者设置
        self.invader_width = 110
        self.invader_height = 130
        self.invader_speed = 1.2
        self.default_invader_speed = 1.2

        # 难度控制
        self.level = 1
        self.invader_everyline_num = 2   # 每行最多出现的入侵者个数
        self.invader_all_num = 100  # 入侵者的总数
        self.invader_distancex = 10  # 入侵者在x方向的间距
        self.invader_distancey = 20  # 入侵者在y方向的间距
        self.speedup_scale = 1.1  # 游戏难度提升的速度

        # 每个入侵者的分数
        self.invader_points = 50

    def initialize_settings(self):
        """初始化随着游戏进行而变化的值"""
        self.invader_speed = self.default_invader_speed
        self.bullet_speed = float(3)
        self.ship_speed = float(5)
        self.level = 1
        self.invader_everyline_num = 2
        self.invader_all_num = 10
        self.invader_points = 50

    def increase_level(self):
        """提高游戏难度"""
        self.level += 1

        # 游戏等级达到3之后每行的最大飞机数增加
        if self.level >= 5:
            if self.level <= 7:
                self.invader_everyline_num += 1

            # 加快速度
        self.invader_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        # 飞机总数目增加
        self.invader_all_num *= self.speedup_scale

        # 击落分数增加
        self.invader_points += 50