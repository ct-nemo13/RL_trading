# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:44:51 2024

@author: ritwi
"""

import random

'''
task_1: Update the following parameters
1. Parameters that will be required for different calculations in later stages, i.e., update observation space and execute tradings
    1.1. 'high' and 'low' to derived Execution Price
    1.2. 'close' to derive the Net Worth
2. All the parameters listed in self.obs_params_from_df_2, i.e., Obs Parameters having window period t-n-1 to t-1
'''

def task_1(self):
    
    '''
    The following list contains the parameters required for various calculations
    1. 'high' and 'low' is required for calculating Executation Price, 
        self.effective_money_reserve in update_observation(self)
        
    2. 'close' is required for calculating Net Worth,
        stock_value_in_money in update_observation(self)
    '''
    param_list_2_excluding_obs_list = ['high', 'low', 'close']
    
    'Update parameters needed for different calculations other than obs parameters'
    for var in param_list_2_excluding_obs_list:
        setattr(self, var, self.df.loc[self.time, var])
    
    
    'Update the Variable Observations Parameters have window period t-n-1 to t-1'
    for var in self.obs_params_from_df_2:
        if var not in param_list_2_excluding_obs_list:
            setattr(self, var, self.df.loc[self.time, var])
    
    
    'Calculate the Execution Price'
    self.execution_price = random.uniform(self.low, self.high)
    print('\nThe execution price:', self.execution_price)