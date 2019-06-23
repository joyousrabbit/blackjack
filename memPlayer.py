# -*- coding: utf-8 -*-

from player import Player



class MemPlayer(Player):
    def __init__(self,game):
        Player.__init__(self)
        self.game = game
        
    def get_left_cards(self):
        seen_cards = []
        seen_cards += self.game.machine.used_cards
        seen_cards += self.game.dealer.cards
        for p in self.game.players:
            if p is not None:
                seen_cards += p.cards
        assert(len(seen_cards)+len(self.game.machine.cards)==self.game.machine.CARDS_NUM)
        
        cards_occurs = [(i,seen_cards.count(i)) for i in set(seen_cards)]
        #print(card_occur)
        pairs = self.game.machine.pairs
        left_occurs = {1:4*pairs,2:4*pairs,3:4*pairs,4:4*pairs,
                       5:4*pairs,6:4*pairs,7:4*pairs,8:4*pairs,
                       9:4*pairs,10:4*4*pairs}
        for card,occur in cards_occurs:
            left_occurs[card] -= occur
            
        #for key, value in init_occurs.items() :
        #    print (key, value)
        
        return left_occurs
    
    def cmd(self):
        left_cards = self.get_left_cards()
        my_cards = self.cards
        dealer_cards = self.game.dealer.cards
        
        cmd = self.get_full_probability(my_cards,dealer_cards,left_cards)
        
        return cmd
    
    def get_full_probability(self,my_cards,dealer_cards,left_cards):
        dealer_probability = self.get_dealer_probability(dealer_cards,1.0,left_cards)
        #for a,b in dealer_probability.items():
        #    print(a,b)
            
        '''
        left_cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4*self.game.machine.pairs
        cards_occurs = [(i,left_cards.count(i)) for i in set(left_cards)]
        left_cards = {}
        for c,o in cards_occurs:
            left_cards[c] = o
        dealer_probability = self.get_dealer_probability(dealer_cards,1.0,left_cards)
        for a,b in dealer_probability.items():
            print(a,b)
        '''
        
        #pass
        pass_prob = self.get_pass_probability(my_cards)
        pass_expect = self.get_expect(pass_prob,dealer_probability)
        print('pass_expert:',pass_expect)
        hit_expect = self.get_hit_expect(my_cards,left_cards,dealer_probability)
        print('hit_expert:',hit_expect)
        double_expect = -2
        if len(my_cards)==2:
            double_prob = self.get_double_probability(my_cards,left_cards)
            double_expect = self.get_expect(double_prob,dealer_probability)*2
            print('double_expert:',double_expect)
        
        if pass_expect>=hit_expect and pass_expect>=double_expect:
            return 'pass'
        elif hit_expect>=pass_expect and hit_expect>=double_expect:
            return 'hit'
        elif double_expect>=pass_expect and double_expect>=hit_expect:
            return 'double'
            
    def get_hit_expect(self,my_cards,left_cards,dealer_probs):
        cards_probs = self.get_cards_probs(left_cards)
        prob_chain = self.get_prob_chain(cards_probs,dealer_probs)
        values = self.game.get_values(my_cards)
        a = prob_chain[values[0]]
        if values[1]<=21:
            b = prob_chain[values[1]]
            if b[0]>a[0]:
                a = b
        if a[1]=='h':
            return a[0]
        else:
            return -1
        
    def get_prob_chain(self,cards_probs,dealer_probs):
        chain = {}
        for i in range(21,0,-1):
            pass_prob = self.get_pass_probability([i])
            pass_expert = self.get_expect(pass_prob,dealer_probs)
            hit_prob = self.get_hit_probability([i],cards_probs)
            hit_expert = 0
            for v,p in hit_prob.items():
                if v>0 and p>0:
                    hit_expert += chain[v][0]*p
                elif v==0:
                    hit_expert -= p
            if hit_expert>pass_expert:
                chain[i] = (hit_expert,'h')
            else:
                chain[i] = (pass_expert,'p')
            #print(i,chain[i])
        return chain
    
    def get_expect(self,player_probs,dealer_probs):
        expect = 0
        for p_c,p_p in player_probs.items():
            for d_c,d_p in dealer_probs.items():
                p = p_p*d_p
                if p_c==0:
                    expect -= p
                elif p_c<d_c:
                    expect -= p
                elif p_c>d_c:
                    expect += p
        return expect
    
    def get_hit_probability(self,cards,cards_probs):
        result_sum = {}
        for i in range(0,23):
            result_sum[i] = 0
        for card, prob in cards_probs:
            if prob>0:
                values = self.game.get_values(cards+[card])
                if values[1]<=21:
                    result_sum[values[1]] += prob
                elif values[0]<=21:
                    result_sum[values[0]] += prob
                else:
                    result_sum[0] += prob
        return result_sum
        
    def get_double_probability(self,cards,left_cards):
        cards_probs = self.get_cards_probs(left_cards)
        result_sum = {}
        for i in range(0,23):
            result_sum[i] = 0
        for card, prob in cards_probs:
            if prob>0:
                values = self.game.get_values(cards+[card])
                if values[1]<=21:
                    result_sum[values[1]] += prob
                elif values[0]<=21:
                    result_sum[values[0]] += prob
                else:
                    result_sum[0] += prob
        return result_sum
        
    def get_pass_probability(self,cards):
        values = self.game.get_values(cards)
        prob = {}
        for i in range(0,23):
            prob[i] = 0
        if cards==[1,10] or cards==[10,1]:
            prob[22] = 1
        elif values[1]<=21:
            prob[values[1]] = 1
        elif values[0]<=21:
            prob[values[0]] = 1
        elif values[0]>21:
            prob[0] = 1
        return prob
        
    def get_dealer_probability(self,dealer_cards,init_prob,left_cards):
        values = self.game.get_values(dealer_cards)
        if dealer_cards==[1,10] or dealer_cards==[10,1]:
            return {22:init_prob}
        elif 17<=values[1]<=21:
            return {values[1]:init_prob}
        elif 17<=values[0]<=21:
            return {values[0]:init_prob}
        elif values[0]>21:
            return {0:init_prob}
        else:
            cards_probs = self.get_cards_probs(left_cards)
            result_sum = {17:0,18:0,19:0,20:0,21:0,22:0,0:0}
            for card, prob in cards_probs:
                if prob>0:
                    new_left_cards = left_cards.copy()
                    new_left_cards[card] -= 1
                    result = self.get_dealer_probability(dealer_cards+[card],prob,new_left_cards)
                    for v,p in result.items():
                        result_sum[v] += p*init_prob
            return result_sum
        
    def get_cards_probs(self,cards):
        occurs = list(cards.values())
        s = 0
        for oc in occurs:
            s += oc
        assert(s>0)
        probs = []
        for card, occur in cards.items():
            probs.append((card, occur/s))
        return probs
        
    def get_name(self):
        return 'memPlayer'
    
if __name__ == "__main__":
    mem_player = MemPlayer(None)