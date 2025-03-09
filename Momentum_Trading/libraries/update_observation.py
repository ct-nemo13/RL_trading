# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:35:05 2024

@author: ritwi
"""
import numpy as np

def update_observation(self):
    
    '''
    Calculation of the following Parameters:
    1. Normalized Money Reserve, self.money_n
    2. Normalized Stock Reserve, self.stock_n
    3. Normalized Net Worth, self.net_worth_n
    4. Fund Status, self.fund_status
    '''
    
    'Calculation of Normalized Money Reserve, self.money_n'
    self.money_n = self.money/self.initial_fund_in_money
    print('\nThe Normalized Money Reserve:', self.money_n)
    
    'Calculation of Normalized Stock Reserve, self.stock_n'
    stock_value_in_money = self.stock*self.close
    self.stock_n = stock_value_in_money/self.initial_fund_in_money
    print('\nThe Normalized Stock Reserve:', self.stock_n)
    
    'Calculation of normalized Net Worth'
    self.net_worth_n = self.money_n + self.stock_n
    print('\nThe Normalized Net Worth:', self.net_worth_n)
    
    
    'Calculation of Fund Status'
    self.effective_money_reserve = (self.money - self.max_fee)
    self.effective_money_reserve -= (self.effective_money_reserve % self.high)
    print('\nThe Money Reserve:', self.money)
    print('\nThe Effective Money Reserve:', self.effective_money_reserve)
    print('\nThe Stock Reserve in Numbers:', self.stock)
    
    if (self.effective_money_reserve < self.high):
        self.fund_status = 0
        print('\nThere is no Money Reserve so Fund_Status is:', self.fund_status)
        
    elif (self.stock == 0):
        self.fund_status = 1
        print('\nThere is no Stock Reserve so Fund_Status is:', self.fund_status)
        
    else:
        self.fund_status = 2
        print('\nBoth Money and Stock Reserve Exists, so Fund_Status is:', self.fund_status)
        

    'Get the Updated Current State'
    current_state = np.array([[getattr(self, var) for var in self.all_obs_params]])
     

    'Concating the current state with the Observation'
    self.observation = np.concatenate((self.observation, current_state), axis=0)
    
    
    '''
    Discarding first row the observation array after concating the current state
    to keep the size constant.
    '''
    self.observation = np.delete(self.observation, 0, 0)
    
    
    return(self.observation)