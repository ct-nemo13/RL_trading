# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:39:14 2024

@author: ritwi
"""


import pandas as pd
import random
from libraries.update_observation import update_observation

'Reset function. It reset the stated at the begining of each episode'    
def reset_all_parameters(self):
    
    'Select a stock randomly from the stock list'
    self.selected_stock = random.choice(self.list_of_stock)    
    print('\nThe ramdomly selected stock for the episode:', self.selected_stock)
    
    
    'Retrive the data frame from the data dir'
    df = pd.read_csv(self.data_dir + '/' + self.selected_stock + '.csv', index_col=0)
    df.index = pd.to_datetime(df.index) # Ensuring the index is in datetime format
    self.df = df
    print('\nThe dataframe containing historical data of the selected stock:\n', self.df)
    
    
    'End time of the episode'
    end_time_int_index_lower_bound = self.look_back_window + self.episode_length_in_steps + 1
    end_time_int_index_upper_bound = len(self.df)-1
    self.end_time_int_index = random.randint(end_time_int_index_lower_bound, end_time_int_index_upper_bound)
    self.end_time = self.df.index[self.end_time_int_index] # Index value of the last row of the data frame
    print('\nThe episode end time:', self.end_time)
    
    
    'Reseting the Current Time'
    present_time_int_index = self.end_time_int_index - self.episode_length_in_steps + 1
    self.start_time_index_in_int = present_time_int_index
    self.time = self.df.index[present_time_int_index]
    print('\nThe start time at the reset:', self.time)
    
    'Present index value in int'
    self.present_index_in_int = self.df.index.get_loc(self.time)
    
    
    '''
    The starting and ending int index to fill the observation space at reser:
    (t-n to t). for parameters listed in self.obs_params_from_df_1 (check init in main_Env). Example: 'open'
    (t-n-1 to t-1) (substract by 1) for for parameters listed in self.obs_params_from_df_2 (check init in main_Env). Example: 'close'
    '''
    starting_int_index = present_time_int_index - self.look_back_window + 1
    print('\nInt index of the df from where observation starts at reset:', starting_int_index)
    
    ending_int_index = present_time_int_index
    print('\nInt index of the df where observation end at reset:', ending_int_index)
    
    
    '''
    The following list contains the parameters required to update for various calculations.
    1. 'high' is required for calculating self.effective_money_reserve in update_observation(self)
    2. 'close' is required for calculating stock_value_in_money in update_observation(self)
    '''
    param_list_2_excluding_obs_list = ['high', 'close']
    
    
    
    'Resetting the observation array and parameters needed for different calculations.'
    for i in range(starting_int_index, (ending_int_index+1)):
        
        'Resetting the Variable Observations Parameters Have window period t-n to t'
        for var in self.obs_params_from_df_1:
            setattr(self, var, self.df.loc[self.df.index[i], var])
        
        
        'parameters needed for different calculations other than obs parameters'
        for var in param_list_2_excluding_obs_list:
            setattr(self, var, self.df.loc[self.df.index[i-1], var])
        
        
        'Resetting the Variable Observations Parameters Have window period t-n-1 to t-1'
        for var in self.obs_params_from_df_2:
            if var not in param_list_2_excluding_obs_list:
                setattr(self, var, self.df.loc[self.df.index[i-1], var])
        
        
        '''
        Resetting Fixed Parameters: having window period t-n-1 to t-1
        1. Not in Observation Space but needed for calculations. Example: self.money
        2. Observation Parameters. Example: self.reward, self.action(action may be discarded from observation space)
        '''
        self.money = self.initial_fund_in_money
        self.net_worth = self.initial_fund_in_money   
        self.stock = int(0)
        self.action = int(0)
        self.reward = int(0)
        
        
        'Updating the observation space'
        self.observation = update_observation(self)
        
    
    'Do the operations for test mode.'
    if ((self.mode=='test')):
        
        'Add two column to plot buy and sell arrows.'
        self.df['execution_price'] = 0
        self.df['action'] = 0