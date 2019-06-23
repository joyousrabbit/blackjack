# -*- coding: utf-8 -*-

from player import Player
import random

class ModestPlayer(Player):
    def cmd(self):
        values = self.get_values()
        if 17<=values[1]<=21 or 17<=values[0]<=21:
            return 'pass'
        elif values[0]+10>21:
            return 'pass'
        else:
            return 'hit'

    def get_name(self):
        return 'modestPlayer'
