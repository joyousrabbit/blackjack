# -*- coding: utf-8 -*-
import random

class Machine():
    def __init__(self,pairs=6):
        self.pairs = pairs
        self.cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4*pairs
        self.CARDS_NUM = len(self.cards)
        print(len(self.cards),'cards')
        self.used_cards = []
        self.shuttle()
        
    def shuttle(self):
        self.cards = self.cards+self.used_cards
        self.used_cards = []
        assert(len(self.cards)==self.CARDS_NUM)
        random.shuffle(self.cards)
        print('cards washed',len(self.cards),'cards')
        
    def get_a_card(self):
        return self.cards.pop(0)
    
    def recycle_cards(self,cards):
        self.used_cards += cards
        
        
if __name__ == "__main__":
    machine = Machine()
    machine.get_a_card()


