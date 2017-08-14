import json


class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()
        self.score = 0
        self.ships_left = self.ai_settings.ship_limit

    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

    def read_history_score(self):
        """读取历史最高分"""
        try:
            with open("game_data.json", "r") as game_file:
                self.high_score = int(json.load(game_file))
        except FileNotFoundError:
            self.high_score = 0
        except ValueError:
            self.high_score = 0

    def store_score(self):
        """存储最高分"""
        with open("game_data.json", "w") as game_file:
            json.dump(self.high_score, game_file)
