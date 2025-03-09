# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:21:19 2024

@author: ritwi
"""

def penalty_for_wrong_action(self):
    
    '''
    Penalty for wrong (unnecessary, uneffective) actions.
    1. If effective_money_reserve = 0 but agent = Buy
    2. Stock reserve = 0 but Action = Sell 
    
    The following Function: Impose a large panelty and end the episode by manking done status yes
    '''
    
    self.penalty_for_wrong_action = 0
    
    'Wrong Buy Action.'
    if ((self.effective_money_reserve <= 0) and (self.action > 0)):
        self.done = True
        print('\nMoney Reserve', self.money)
        print('\nEffective Money Reserve', self.effective_money_reserve)
        print('\nAction:', self.action) 
        print('\nFund_Status:', self.fund_status)           
        print('\nEpisode is terminating due to wrong Buy Action')
        self.penalty_for_wrong_action = -10
        print('\nPenalty for Wrong Action:', self.penalty_for_wrong_action)
        
    
    'Wrong Sell Action.'
    if ((self.stock <= 0) and (self.action < 0)):
        self.done = True
        print('\nStock Holdings', self.stock)
        print('\nAction:', self.action) 
        print('\nFund_Status:', self.fund_status) 
        print('\nEpisode is terminating due to wrong Sell Action')
        self.penalty_for_wrong_action = -10
        print('\nPenalty for Wrong Action:', self.penalty_for_wrong_action)