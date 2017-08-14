import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from mouse_move import MouseMove
from musics import Musics


def run_game():
    # 初始化游戏并且创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien_Invasion")
    gf.set_bgscreen(ai_settings, screen)

    # 创建按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个存储子弹的编组
    bullets = Group()

    # 创建入侵者
    invaders = Group()
    gf.create_fleet(ai_settings, screen, invaders)

    # 创建一个用于存储游戏统计数据的实例
    stats = GameStats(ai_settings)
    stats.read_history_score()
    scoreboard = Scoreboard(ai_settings, screen, stats)

    # 显示生命数
    scoreboard.show_ships()

    # 创建鼠标移动类
    x, y =pygame.mouse.get_pos()
    mouse_move = MouseMove(x, y)

    # 创建背景音乐类
    musics = Musics()
    musics.bgmusic.play(-1, 0)

    # 开始游戏主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets, play_button, stats, invaders, scoreboard, mouse_move, musics)

        if stats.game_active:
            gf.update_bullets(bullets, invaders, ai_settings, screen, stats, musics)
            ship.update()
            gf.update_invaders(ai_settings, stats, invaders, ship, screen, scoreboard)

        # 每次循环时重绘屏幕 让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, stats, ship, invaders, bullets, play_button, scoreboard)


run_game()
