# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 23:08:23 2023

@author: ritwi
"""

import os
from ray.rllib.algorithms.ppo import PPOConfig
from main_Env import SingleStockLongOnly

from libraries.make_dir_for_policy import create_policy_dir


"Creating the agents"

'Selecting the policy'
policy = 'default_LSTM_v2'

'Numbers of agents'
agents_per_policy = 3

'Create Directories for the policy'
create_policy_dir(policy, agents_per_policy)


# Configuring one of the Agents: This agent use Defatlt settings from RayRLlib 
# Name: default

# Building agents utilizing the selected policy
for i in range (agents_per_policy):
    # Building the agent
    if os.path.exists('policies/' + policy + '/agent_' + str(i)) is False:
        print('No directory exists for\nPolicy: ' + policy + '\nAgent: ' + str(i) + 'th agent\nFirst create the directory.')        
    else:    
        # First checking if it is already created 
        if os.path.exists('policies/' + policy + '/agent_' + str(i) +'/0') is True:
            print('The following agent already exists \nPolicy- ' + policy + '\nAgent- ' + str(i) +'_0')
        else:
            # Ray configuration of the agent        
            config = (
                # The RL algorithm
                PPOConfig()                           
                # The gym Env
                .environment(SingleStockLongOnly,
                             env_config={'mode':'train',
                                         'test_agent_id': None,
                                         'data_dir':'data_dir/train_data',
                                         'episode_length_in_steps': 500,                      
                                         'look_back_window': 500}
                             )           
                # Numbers of rollout workers
                .rollouts(num_rollout_workers = 1)
                # Use "torch" for using pytorch or "tf" or "tf2" for Tensor Flow. "tf2" is not working for the time being.
                .framework("tf")
                .training(model =
                          {"use_lstm": True,
                           "max_seq_len": 200,
                           "lstm_cell_size": 256,
                           "fcnet_hiddens": [512, 512],
                           "fcnet_activation": "relu"
                           }
                          #lr_schedule =[[0, 0.01], [800000, 0.001], [1600000, 0.0005], [2000000, 0.0001], [2500000, 0.00005], [3000000, 0.00001]]
                          )
                # Numbers of evalution workers
                .evaluation(evaluation_num_workers=1)
            )
            agent = config.build()
            check_point = 'policies/' + policy + '/agent_' + str(i) +'/0'
            agent.save(check_point)
            print('The following agent is successfully created \nPolicy- ' + policy + '\nAgent- ' + str(i) +'_0')