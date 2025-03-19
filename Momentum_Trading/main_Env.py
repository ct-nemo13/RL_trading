# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 02:09:05 2023

@author: ritwik
"""
import os
import gymnasium as gym
from gymnasium import spaces
import numpy as np


from libraries.update_observation import update_observation
from libraries.reset_all_parameters import reset_all_parameters
from libraries.execute_trading import  execute_trading
from libraries.task_1 import task_1
from libraries.task_2 import task_2
from libraries.calculate_reward import calculate_reward
from libraries.plt_action_histogram_and_save import plt_action_histogram_and_save
from libraries.candle_plot import candle_plot
from libraries.init_for_test_mode import init_for_test_mode
from libraries.penalty_for_wrong_action import penalty_for_wrong_action


'Defining the class of the environmentas gym.Env'
class SingleStockLongOnly(gym.Env):
    
    def __init__(self, env_config):

        'Enter the mode of the environment. There are 2 modes, train and test.'
        self.mode = env_config['mode']
        
        'Do the operations for test mode.'
        if ((self.mode=='test')):
            
            'Test Agent ID'
            self.test_agent_id = env_config['test_agent_id']
            
            '''
            Following function: 1. Create the main test logs dir, 2. Create test logs dir for the particular agent,
            3. Test episode count, 4. Initialize the action_list
            '''
            init_for_test_mode(self)


        'The directory where all the stocks data are kept'
        self.data_dir = env_config['data_dir']
        
        
        'Initializing the list of stocks.'
        self.list_of_stock = []
        
        
        'Extract the list of stocks. At each episode one random stock will beselected from the list during rset'       
        for filename in os.listdir(self.data_dir):
            'Extract the file names from the file list by spliting the extension.'
            name, extension = os.path.splitext(filename)
            'Append the file names.'
            self.list_of_stock.append(name)
            
        'Delete the file name, .ipynb_checkpoints that is coming from a residual file'
        if '.ipynb_checkpoints' in self.list_of_stock:
            self.list_of_stock.remove('.ipynb_checkpoints')
            
        print('\nList of Stocks:\n', self.list_of_stock)
        
        
        'Number of steps in one Episode'
        self.episode_length_in_steps = env_config['episode_length_in_steps']
        
        
        'How many time steps (in int) the agent looking back at every step.'
        self.look_back_window = env_config['look_back_window']
        
        
        'Initial fund in money'
        self.initial_fund_in_money = env_config['initial_fund_in_money']
        

        'Trading fee: Percentage fee and max fee'
        self.fee_percentage = env_config['fee_percentage']
        self.max_fee = env_config['max_fee']
        
        
        'Lowest acceptable net worth: The maimum allowed draw-down to stop the episode.'
        self.lowest_acceptabl_net_worth = self.initial_fund_in_money * env_config['lowest_acceptabl_net_worth']
        
        
        '''
        Action Space: Action space is discrete. The agent produce only +ve integers as actions.
        The Action is scalled in following way internally.
        Example: [0 to 10] is scalled [-5 to +5]
        
        Method: Position_per_action_value = percentage of fund will be used to buy or sell per unit int value in action
        Example: An action space [10 to -10].
                 If action value is 2, 20% of the cash balance will be used to buy stock.
                 If action value is -4, 40% of the stock holding will be sold.
        '''
        self.position_per_action_value = env_config['position_per_action_value']
        self.discrete_actions = int(((1/self.position_per_action_value) * 2) + 1)
        self.action_substractor = int((1/self.position_per_action_value))
        self.action_space = spaces.Discrete(self.discrete_actions)
        
        
        'Observation Space'
        
        'List of observation parameters'
        '''
        'Observations Parameters those will be changed'
        self.obs_params = ['PROC_5', 'PROC_21', 'PROC_55',       # Price Rate of Change
                           'PRMA_5','PRMA_21', 'PRMA_55',        # Price Relative to Moving Avarage
                           'VROC_5', 'VROC_21', 'VROC_55',       # Volume Rate of Change
                           'VRMA_5','VRMA_21', 'VRMA_55',        # Volume Relative to Moving Avarage
                           ]
        
        '''

        'Observations Parameters those will be changed: and have the window period t-n to t'
        self.obs_params_from_df_1 = ['open']
        
        'Observations Parameters those will be changed: and have the window period t-n-1 to t-1'
        self.obs_params_from_df_2 = ['high', 'low', 'close', 'volume']
        
        '''
        Observations Parameters those will not be changed: and have the window period t-n-1 to t-1'
        1. Normalized Money Reserve, 2. Normalized Stock Reserve, 3. Net Worth, 4. Fund Status, 5. Action Taken, 6. Reward
        '''
        self.fixed_obs_params = ['money_n', 'stock_n', 'net_worth_n', 'fund_status', 'reward']
        
        'All the Observation Parameters'
        self.all_obs_params = (self.obs_params_from_df_1 + 
                               self.obs_params_from_df_2 + 
                               self.fixed_obs_params)
        
        print('\nAll Observation Parameters:', self.all_obs_params)
        
        'Total Numbers of Observation Parameters'
        self.obs_param_numbers = len(self.all_obs_params)  
        
        'Define the Observation Space'
        self.observation_space = spaces.Box(low=-np.inf,
                                            high=np.inf,
                                            shape=(self.look_back_window, self.obs_param_numbers),
                                            dtype=np.float64)
           
        'Defining the empty observation array.'
        self.observation = np.empty((self.look_back_window, self.obs_param_numbers,),
                                    dtype=np.float64)
        
        
        
    def reset(self): 
        
        'Reseting time and all the parameters of the observation space'
        print('\nReseting the Env...')
        reset_all_parameters(self)
        print('\nThe Observation after the Reset:\n', self.observation)
        
        
        'Initialize the "done" status as False'
        self.done = False        
        print('\nDone Status after the reset:', self.done)
        
        
        'Do the operations for test mode.'
        if ((self.mode=='test')):

            'Increase the episode count by 1. The count is initialized to 0 in libraries (init_for_test_mode.py)'
            self.test_episode_count += 1
            print('The test episode count:', self.test_episode_count)
            
            'Adding the Execution Price in data frame in test mode for candle plotting.'
            self.df['execution_price'] = 0
            self.df['execution_price'] = self.df['execution_price'].astype(np.float64)
            
        
        print('\nThe reset is completed')
        return self.observation
    
        
    
    def step(self, action_from_agent):
        
        'Update the Action taken by the agent'
        self.action = action_from_agent - self.action_substractor
        print('\nThe action, applied to the env by the agent:', action_from_agent)
        print('\nThe actual action after scalling:', self.action)
        
        
        '''
        Penalty for wrong (unnecessary, uneffective) actions.
        1. If effective_money_reserve = 0 but agent = Buy
        2. Stock reserve = 0 but Action = Sell 
        
        The following Function: Impose a large panelty and end the episode by manking done status yes
        '''
        penalty_for_wrong_action(self)
        
        
        '''
        task_1: Update the following parameters
        1. Parameters that will be required for different calculations in later stages, i.e., update observation space and execute tradings
            1.1. 'high' and 'low' to derived Execution Price
            1.2. 'close' to derive the Net Worth
        2. All the parameters listed in self.obs_params_from_df_2, i.e., Obs Parameters having window period t-n-1 to t-1
        3. Calculation of Execution Price to be used in execute_trading(self)
        '''
        task_1(self)  
        
        
        ''' execute_trading: According to the action the update the following Parameters
        1. Money Reserve
        2. Stock Holdings
        '''
        execute_trading(self)
        
        
        ''' ***
        This is the instant when one time stamp just ends. At this instant all
        the parameter of the instant including the reward is available. However, the
        observation for next instant is not ready yet. But this instant is useful for 
        rendering.
        *** '''
        
        
        'Calculate the net worth after the trade is executed'
        self.old_net_worth = self.net_worth
        self.net_worth = self.money + (self.stock * self.close)


        'Calculate reward'
        calculate_reward(self)


        'Do the operations for test mode.'
        if ((self.mode=='test')):
            
            'Append the action list.'
            self.action_list.append(self.action)
            print('The appended action list:',self.action_list)
            
            
            '''
            calculate sharp ratio and other parameters
            '''
            
            'Update the Action and Execution Price in the data frame for candle stick plot.'
            self.df.at[self.time, 'action'] = self.action 
            self.df.at[self.time, 'execution_price'] = self.execution_price
        

        '''
        Episode stopping criteria.
        1. Wrong Action
        2. Time is up
        3. Net Worth is lower than Lowest Acceptable Net Worth
        '''
        if ((self.done == True) or (self.time>=self.end_time) or (self.net_worth <= self.lowest_acceptabl_net_worth)):
            self.done = True # Ending the episode
            print('\nThe net Worth at the end of the episode:', self.net_worth)
            print('\n The episode length was:', (self.present_index_in_int - self.start_time_index_in_int))
            
            'Do the operations for test mode.'
            if ((self.mode=='test')):
                
                'Plot and Save Action Histogram'
                plt_action_histogram_and_save(self)

                'Plot the Candle Stick diagram and save.'
                candle_plot(self)


        '''
        task_2: 
        1. advancing the time,
        2. update Open price
        '''
        task_2(self)
        

        'Updating the Observation'
        self.observation = update_observation(self)
        
        
        print('\nTime and done status at the end of the step:', self.time, self.done)
        print('The updated observation at the end of the step:\n', self.observation)
        
        info = {}

        info['Time'] = self.time
        print(info)
        
        
        return self.observation, self.reward, self.done, info
    
    
    
    def render(self, mode='human'):
        pass
    
    
    
    def close (self):
        pass