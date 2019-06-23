# -*- coding: utf-8 -*-

from player import Player

class NodoPlayer(Player):
    def cmd(self):
        return 'pass'
    
    def get_name(self):
        return 'nodoPlayer'