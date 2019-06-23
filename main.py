# -*- coding: utf-8 -*-

from game import Game
from dealer import Dealer
from randomPlayer import RandomPlayer
from modestPlayer import ModestPlayer
from nodoPlayer import NodoPlayer
from tablePlayer import TablePlayer
from doublePlayer import DoublePlayer
from memPlayer import MemPlayer

import sys
sys.stdout = open("log.txt", "w")

if __name__ == "__main__":
    game = Game()
    
    dealer = Dealer()
    random_player = RandomPlayer()
    modest_player = ModestPlayer()
    nodo_player = NodoPlayer()
    table_player = TablePlayer(dealer)
    double_player = DoublePlayer(dealer)
    mem_player = MemPlayer(game)
    
    game.set_dealer(dealer)
    game.set_player(0,random_player)
    game.set_player(1,modest_player)
    game.set_player(2,nodo_player)
    game.set_player(3,table_player)
    game.set_player(4,double_player)
    game.set_player(5,mem_player)
    
    for i in range(100):
        game.play()
        
    for i in range(game.max_players):
        if game.players[i] is not None:
            print(i,game.players[i].get_name(),game.players[i].money)
            
    print('D',game.dealer.money)
