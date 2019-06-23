# -*- coding: utf-8 -*-

from player import Player
import random

class RandomPlayer(Player):
    def cmd(self):
        return random.choice(['hit','pass'])
    
    def get_name(self):
        return 'randomPlayer'