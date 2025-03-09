# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:45:38 2024

@author: ritwi
"""

'''
Task-2: 1. Advance the time
        2. Update parameters needed for different calculations other than obs parameters
        3. Update the Obs Parameters having window period t-n to t, listed in self.obs_params_from_df_1 
'''

def task_2(self):
    
    
    '''
    Advancing the time:
    self.present_index_in_int is the current time index in int value
    The present int index value is then advances by 1
    self.df.index[] gives the datetime index value
    '''  
    self.present_index_in_int += 1   
    self.time = self.df.index[(self.present_index_in_int)]
    
    
    param_list_1_excluding_obs_list = ['open']
    
    'Update parameters needed for different calculations other than obs parameters'
    for var in param_list_1_excluding_obs_list:
        setattr(self, var, self.df.loc[self.time, var])
    
    
    'Update the Variable Observations Parameters have window period t-n to t'
    for var in self.obs_params_from_df_1:
        if var not in param_list_1_excluding_obs_list:
            setattr(self, var, self.df.loc[self.time, var])