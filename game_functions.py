import sys
import pygame
import pygame.font
import random
from time import sleep

from bullet import Bullet
from invaders import Invaders


def set_bgscreen(ai_settings, screen):
    ai_settings.bg_image = pygame.image.load_extended('images/蓝天.jpg').convert()
    ai_settings.bg_image = pygame.transform.scale(ai_settings.bg_image,
                                                  (ai_settings.screen_width, ai_settings.screen_height))
    screen.blit(ai_settings.bg_image, (0, 0))


def check_events(ai_settings, screen, ship, bullets, play_button, stats, invaders, scoreboard, mouse_move, musics):
    """响应按键和鼠标事件"""
    if stats.game_active:
        check_mouse_move(mouse_move, ship)
    for event in pygame.event.get():
        # 退出窗口
        if event.type == pygame.QUIT:
            stats.store_score()
            sys.exit()

        # 响应键盘按下事件
        elif event.type == pygame.KEYDOWN:
            # 空格键发射子弹
            if event.key == pygame.K_SPACE:
                fire_bullet(ai_settings, screen, ship, bullets, musics)

            # 退出游戏
            elif event.key == pygame.K_DELETE:
                stats.store_score()
                sys.exit()
        # 响应按钮事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            fire_bullet(ai_settings, screen, ship, bullets, musics)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 检测鼠标是否点击在按钮内
            check_play_button(ai_settings, screen, ship, invaders, bullets, stats, play_button, mouse_x, mouse_y, scoreboard)


def check_play_button(ai_settings, screen, ship, invaders, bullets, stats, play_button, mouse_x, mouse_y, scoreboard):
    """在玩家单机Play按钮时开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(ai_settings, screen, ship, invaders, bullets, stats, play_button, scoreboard)


def update_screen(ai_settings, screen, stats, ship, invaders, bullets, play_button, scoreboard):
    """更新屏幕图像，并切换到新的屏幕"""
    screen.blit(ai_settings.bg_image, (0, 0))

    # 显示得分
    scoreboard.show_score()

    # 显示等级
    scoreboard.show_level()

    # 显示飞船生命数
    scoreboard.show_ships()

    # 如果游戏处于非活动状态，绘制play按钮

    if not stats.game_active:
        play_button.draw_button()

    # 重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    for invader in invaders:
        invader.blitme()

    pygame.display.update()


def update_bullets(bullets, invaders, ai_settings, screen, stats, musics):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    # 检查是否有子弹击中了外星人，如果是这样，就删除相应的子弹和外星人
    check_bullet_invader_collisions(ai_settings, screen, stats, invaders, bullets, musics)


def fire_bullet(ai_settings, screen, ship, bullets, musics):
    """如果已有子弹数小于限制，则发射子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        musics.fire_music.play()


def create_fleet(ai_settings, screen, invaders):
    """创建入侵者群"""
    all_num = 0
    y = 0
    while True:
        # 随机生成入侵者的出现位置
        positionx = []
        for i in range(0, random.randint(0, ai_settings.invader_everyline_num)):
            x = random.randint(0, ai_settings.screen_width - ai_settings.invader_width)
            flag = True
            for j in positionx:
                if j - (ai_settings.invader_width + ai_settings.invader_distancex) < x < j + (
                            ai_settings.invader_width + ai_settings.invader_distancex):
                    flag = False
            if flag:
                positionx.append(x)
                all_num += 1

        # 生成入侵者
        y -= (ai_settings.invader_height + ai_settings.invader_distancey)
        for centerx in positionx:
            invader = Invaders(ai_settings, screen)
            invader.x = centerx
            invader.rect.x = invader.x
            invader.rect.y = y
            invader.y = y
            invaders.add(invader)
        if all_num > ai_settings.invader_all_num:
            break


def check_edges(ai_settings, stats, ship, invaders, screen, scoreboard):
    """在入侵者超出屏幕后采取的措施"""
    for invader in invaders.copy():
        if invader.check_edges():
            # invaders.remove(invader)
            ship_hit(ai_settings, stats, ship, invaders, screen, scoreboard)


def update_invaders(ai_settings, stats, invaders, ship, screen, scoreboard):
    """更新入侵者群中所有入侵者"""
    check_edges(ai_settings, stats, ship, invaders, screen, scoreboard)
    invaders.update()

    # 检测飞船是否与入侵者碰撞
    if pygame.sprite.spritecollideany(ship, invaders):
        ship_hit(ai_settings, stats, ship, invaders, screen, scoreboard)


def check_bullet_invader_collisions(ai_settings, screen, stats, invaders, bullets, musics):
    """响应子弹和入侵者的碰撞"""
    # 删除发生碰撞的子弹和入侵者
    for invader in invaders.copy():
        if invader.is_live > 0:
            invader.boom()
        if 10 <= invader.is_live:
            invaders.remove(invader)
    collisions = pygame.sprite.groupcollide(bullets, invaders, True, False)
    if collisions:
        musics.boom.play()
        for i in collisions.values():
            stats.score += ai_settings.invader_points * len(i)
            for invader in i:
                invader.boom()
    check_high_score(stats)
    # 如果入侵者消灭完执行相关操作
    if len(invaders) == 0:
        start_new_level(ai_settings, screen, invaders)


def start_new_level(ai_settings, screen, invaders):
    ai_settings.increase_level()
    create_fleet(ai_settings, screen, invaders)


def ship_hit(ai_settings, stats, ship, invaders, screen, scoreboard):
    """响应入侵者撞到飞船"""
    # 飞船剩余生命数减1
    stats.ships_left -= 1

    # 飞船回到屏幕中央初始位置
    ship.center_ship()

    # 所有入侵者退出屏幕重新进入
    for invader in invaders.sprites():
        invader.y -= (ai_settings.screen_height + ai_settings.ship_height)

    # 刷新飞船生命数显示
    scoreboard.prep_ships()

    # 暂停
    sleep(0.2)

    if stats.ships_left < 0:
        # 游戏结束
        game_over(stats, screen)


def start_game(ai_settings, screen, ship, invaders, bullets, stats, play_button, scoreboard):
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 重置游戏难度
    ai_settings.initialize_settings()

    # 更新游戏生命数显示
    scoreboard.prep_ships()

    # 清空入侵者和子弹列表
    invaders.empty()
    bullets.empty()

    # 创建一群入侵者，并且让飞船居中
    ship.center_ship()
    create_fleet(ai_settings, screen, invaders)


def game_over(stats, screen):
    stats.game_active = False
    pygame.mouse.set_visible(True)


def check_high_score(stats):
    """检查当前得分是否超过最高风"""
    if stats.high_score < stats.score:
        stats.high_score = stats.score


def check_mouse_move(mouse_move, ship):
    present_x, present_y = pygame.mouse.get_pos()
    if present_x != mouse_move.x or present_y !=mouse_move.y:
        ship.rect.left = present_x
        ship.rect.top = present_y
    mouse_move.x, mouse_move.y = present_x, present_y
