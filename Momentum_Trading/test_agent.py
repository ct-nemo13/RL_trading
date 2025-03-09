# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 00:51:47 2024

@author: ritwi
"""


import os
from ray.rllib.algorithms.algorithm import Algorithm
import gymnasium as gym
import time
import numpy as np
import matplotlib.pyplot as plt
import math

'Number Episode'
episodes = 200

'Selecting the policy'
policy = 'default_LSTM_v2'

'The agent to be trained.'
agents_to_test = 2

'Version of the agent.'
version = str(147)

'Test Agent ID'
test_agent_id = policy + '_' +str(agents_to_test) + '_' + version


'Calling the Environment'
env = gym.make('SingleStockLongOnly',
               env_config={'mode':'test',
                           'test_agent_id': test_agent_id,
                           'data_dir':'data_dir/test_data',
                           'episode_length_in_steps': 500,                      
                           'look_back_window': 500}
               )  

print('Get the Env')

'Recalling agents and play one episode'
i = agents_to_test
   
# First checking if it is already created 
if os.path.exists('policies/' + policy + '/agent_' + str(i) +'/0') is False:
    print('There exists no agent for \nPolicy- ' + policy + '\nAgent- ' + str(i) +'_0')
else:
    check_point = 'policies/' + policy + '/agent_' + str(i) +'/' + version
    restored_agent = Algorithm.from_checkpoint(check_point)
    

    
'Play an Eplisode with the restored agent'

reward_list = []

for episode in range(episodes):
    
    'Starting countdown to measure the time taken for one episode'
    start = time.time()
    done = False
    obs = env.reset()
    total_reward = 0
    
    state = [np.zeros([256], np.float32) for _ in range(2)]
    prev_a = 0
    prev_r = 0.0
    
    while not done:
        
        'Taking an random action'
        action, state_out, _ = restored_agent.compute_single_action(obs, state, prev_action = prev_a, prev_reward = prev_r)
        state = state_out
        
        #print('Action taken by the agent:',action)
        
        'Getting the observation, reward and done status from the environment'
        obs, reward, done, info = env.step(action)
        #print('Reward at the step:', reward)
        
        prev_a = action
        prev_r = reward
        
        total_reward += reward
    
    reward_list.append(((math.exp(total_reward))-1) * 100)
    end = time.time()
    print(f"Time taken for the episode: {(end-start)*10**3:.03f}ms")
    
'Plotting a basic histogram'
plt.hist(reward_list, bins=30, color='blue', edgecolor='black')
'Adding labels and title'
plt.xlabel('Reward')
plt.ylabel('Frequency')
plt.title('Reward Histogram')

'Save the histogram plot.'
file_path = 'test_logs/' + test_agent_id + '/Reward_Histogram.jpeg'


plt.savefig(file_path, dpi=500)

'Display the plot'
plt.show()
