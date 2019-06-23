# -*- coding: utf-8 -*-

from game import Game
from dealer import Dealer
from randomPlayer import RandomPlayer
from modestPlayer import ModestPlayer
from nodoPlayer import NodoPlayer
from tablePlayer import TablePlayer

import sys
#sys.stdout = open("log.txt", "w")

if __name__ == "__main__":
    game = Game()
    
    dealer = Dealer()
    player_a = RandomPlayer()
    player_b = ModestPlayer()
    player_c = NodoPlayer()
    player_d = TablePlayer(dealer)
    
    game.set_dealer(dealer)
#    game.set_player(0,player_a)
#    game.set_player(1,player_b)
#    game.set_player(2,player_c)
    game.set_player(3,player_d)
    
    dealer.cards = [10,10]
    player_d.cards = [1,10]
    player_d.init_coin(1)
    
    game.win_lose()
