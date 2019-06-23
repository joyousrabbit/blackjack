# -*- coding: utf-8 -*-

from player import Player

class TablePlayer(Player):
    def __init__(self,dealer):
        Player.__init__(self)
        self.dealer = dealer
        self.init_table()
        
    def cmd(self):
        dealer_card = self.dealer.cards
        assert(len(dealer_card)==1)
        dealer_card_ind = 9 if dealer_card[0]==1 else (dealer_card[0]-2)
        values = self.get_values()
        if values[0]==values[1]: # no 1
            ind = values[0]
        else: #1
            ind = 'a'+str(values[0]-1)
            if ind not in self.table.keys():
                ind = values[0]
        if str(ind).startswith('a'):
            cmd = self.table[ind][dealer_card_ind]
        else:
            if ind>=18:
                return 'pass'
            elif ind<=8:
                return 'hit'
            else:
                cmd = self.table[str(ind)][dealer_card_ind]
        
        if cmd=='h':
            return 'hit'
        elif cmd=='s':
            return 'pass'
        elif cmd=='d':
            return 'hit'
        elif cmd=='ds':
            return 'pass'
        else:
            print(cmd)
            assert(False)
                
    def init_table(self):
        table = {}
        table['9'] = ['h','d','d','d','d','h','h','h','h','h']
        table['10'] = ['d','d','d','d','d','d','d','d','h','h']
        table['11'] = ['d','d','d','d','d','d','d','d','d','h']
        table['12'] = ['h','h','s','s','s','h','h','h','h','h']
        table['13'] = ['s','s','s','s','s','h','h','h','h','h']
        table['14'] = ['s','s','s','s','s','h','h','h','h','h']
        table['15'] = ['s','s','s','s','s','h','h','h','h','h']
        table['16'] = ['s','s','s','s','s','h','h','h','h','h']
        table['17'] = ['s','s','s','s','s','s','s','s','s','s']
        table['a2'] = ['h','h','h','d','d','h','h','h','h','h']
        table['a3'] = ['h','h','h','d','d','h','h','h','h','h']
        table['a4'] = ['h','h','d','d','d','h','h','h','h','h']
        table['a5'] = ['h','h','d','d','d','h','h','h','h','h']
        table['a6'] = ['h','d','d','d','d','h','h','h','h','h']
        table['a7'] = ['s','ds','ds','ds','ds','s','s','h','h','h']
        table['a8'] = ['s','s','s','s','s','s','s','s','s','s']
        table['a9'] = ['s','s','s','s','s','s','s','s','s','s']
        self.table = table
        
    def get_name(self):
        return 'tablePlayer'

if __name__ == "__main__":
    tablePlayer = TablePlayer(None)
            