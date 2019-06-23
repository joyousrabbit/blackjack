# -*- coding: utf-8 -*-

class Player():
    def __init__(self):
        self.cards = []
        self.money = 0
        self.reset()
        
    def reset(self):
        self.is_doubled = False
        self.coin = 0
        
    def set_coin(self,coin=1):
        self.coin = coin
        
    def double_coin(self):
        self.coin *= 2
        self.is_doubled = True
        
    def add_a_card(self,card):
        self.cards.append(card)
        
    def remove_cards(self):
        cards = self.cards
        self.cards = []
        return cards
    
    def get_values(self):
        value = 0
        for card in self.cards:
            value += card
        if 1 in self.cards:
            return [value,value+10]
        else:
            return [value,value]
    
    def cmd(self):
        return None
    
    def get_name(self):
        return None