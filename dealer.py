# -*- coding: utf-8 -*-

from player import Player

class Dealer(Player):
    def __init__(self):
        Player.__init__(self)
        self.coin = None
        
    def cmd(self):
        values = self.get_values()
        if 17<=values[1]<=21 or 17<=values[0]<=21:
            return 'pass'
        else:
            return 'hit'
        
        