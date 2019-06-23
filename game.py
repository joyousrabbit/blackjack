# -*- coding: utf-8 -*-

from machine import Machine

class Game():
    def __init__(self,max_players=6):
        self.machine = Machine()
        self.round = 0
        self.max_players = max_players
        print('Max players:',self.max_players)
        self.dealer = None
        self.players = [None]*self.max_players
        
    def set_dealer(self,dealer):
        self.dealer = dealer
        print('Dealer ready.')
    
    def set_player(self,place,player):
        self.players[place] = player
        print(player.get_name(),'sit in ',place)
        
    def remove_player(self,place):
        self.players[place] = None
    
    def play(self):
        print('\nRound',self.round,'after shuttle.')
        #coin on
        for i in range(self.max_players):
            if self.players[i] is not None:
                self.players[i].reset()
                self.players[i].set_coin()
        
        #check players has no card
        for i in range(self.max_players):
            if self.players[i] is not None:
                assert(len(self.players[i].cards)==0)
                
        #first card
        for i in range(self.max_players):
            if self.players[i] is not None and self.players[i].coin>0:
                a_card = self.machine.get_a_card()
                self.players[i].add_a_card(a_card)
        
        #dealer's first card
        a_card = self.machine.get_a_card()
        self.dealer.add_a_card(a_card)
        
        #second card
        for i in range(self.max_players):
            if self.players[i] is not None and self.players[i].coin>0:
                a_card = self.machine.get_a_card()
                self.players[i].add_a_card(a_card)
                
        self.show_cards()
        
        #play one by one
        for i in range(self.max_players):
            if self.players[i] is not None and self.players[i].coin>0:
                # stop blackjack!
                if 1 in self.players[i].cards and 10 in self.players[i].cards:
                    continue
                if self.players[i].is_doubled:
                    continue
                while True:
                    if not self.is_bust(self.players[i].cards):
                        cmd = self.players[i].cmd()
                        if cmd=='hit':
                            a_card = self.machine.get_a_card()
                            self.players[i].add_a_card(a_card)
                            self.show_cards()
                        elif cmd=='pass':
                            break
                        elif cmd=='double':
                            assert(len(self.players[i].cards)==2)
                            self.players[i].double_coin()
                            a_card = self.machine.get_a_card()
                            self.players[i].add_a_card(a_card)
                            self.show_cards()
                        else:
                            print(cmd)
                            assert(False)
                    else:
                        # player bust
                        self.recycle_player_cards(self.players[i])
                        self.players[i].money -= self.players[i].coin
                        self.dealer.money += self.players[i].coin
                        break
         
        # dealer
        has_survival = False
        for i in range(self.max_players):
            if self.players[i] is not None and len(self.players[i].cards)>0:
                has_survival = True
                break
        if has_survival:
            while True:
                if not self.is_bust(self.dealer.cards):
                    cmd = self.dealer.cmd()
                    if cmd=='hit':
                        a_card = self.machine.get_a_card()
                        self.dealer.add_a_card(a_card)
                        self.show_cards()
                    elif cmd=='pass':
                        break
                    else:
                        print(cmd)
                        assert(False)
                else:
                    # dealer bust
                    self.recycle_player_cards(self.dealer)
                    break
            # win-lose check between dealer and survivals
            self.win_lose()
        else:
            self.recycle_player_cards(self.dealer)
            
        # end round
        for i in range(self.max_players):
            if self.players[i] is not None:
                self.recycle_player_cards(self.players[i])
        self.recycle_player_cards(self.dealer)
        self.round += 1
        if self.round >=3:
            self.machine.shuttle()
            self.round = 0
                    
    def recycle_player_cards(self,player):
        cards = player.remove_cards()
        self.machine.recycle_cards(cards)
        
    def get_values(self,cards):
        value = 0
        for card in cards:
            value += card
        if 1 in cards:
            return [value,value+10]
        else:
            return [value,value]
        
    def get_final_value(self,cards):
        if len(cards)==0:
            return 0
        elif cards==[1,10] or cards==[10,1]:
            return 22
        else:
            values = self.get_values(cards)
            if values[1]>21:
                return values[0]
            else:
                return values[1]
            
    def is_bust(self,cards):
        values = self.get_values(cards)
        return values[0]>21
    
    def win_lose(self):
        dealer_value = self.get_final_value(self.dealer.cards) 
        for i in range(self.max_players):
            if self.players[i] is not None and len(self.players[i].cards)>0:
                player_value = self.get_final_value(self.players[i].cards)
                if player_value>dealer_value:
                    if player_value == 22:
                        coin = 1.5*self.players[i].coin
                    else:
                        coin = self.players[i].coin
                    self.players[i].money += coin
                    self.dealer.money -= coin
                elif player_value<dealer_value:
                    coin = self.players[i].coin
                    self.players[i].money -= coin
                    self.dealer.money += coin
        
    def show_cards(self):
        #return
        for i in range(self.max_players):
            if self.players[i] is not None:
                print(i,':','(%05d,%d)'%(self.players[i].money,self.players[i].coin),self.players[i].cards,'x2' if self.players[i].is_doubled else '')
            else:
                print(i,':','(*)','[]')
        print('D',': (%05d)'%(self.dealer.money),self.dealer.cards)
        print('cards left:',len(self.machine.cards))
            
        
if __name__ == "__main__":
    game = Game()
    