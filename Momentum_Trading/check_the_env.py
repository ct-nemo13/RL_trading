# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 18:11:57 2023

@author: ritwi
"""
import gymnasium as gym
import time
import math
import matplotlib.pyplot as plt


'Registering the Gym Environment'
gym.register(id='SingleStockLongOnly', entry_point='main_Env:SingleStockLongOnly')


test_agent_id = 'random_agent'
episodes = 10


'Calling the Environment'
env = gym.make('SingleStockLongOnly',
               env_config={'mode':'test',
                           'test_agent_id': test_agent_id,
                           'data_dir':'data_dir/train_data',
                           'episode_length_in_steps': 10,                      
                           'look_back_window': 3,
                           'initial_fund_in_money': 500000,
                           'fee_percentage': 0.1,
                           'max_fee': 40,
                           'lowest_acceptabl_net_worth': 0.75,
                           'position_per_action_value': 0.5}
               )    

print('\nObservation Sample\n', env.observation_space)
print('\nObservation Sample\n', env.observation_space.sample())
print('\nAction Sample\n', env.action_space.sample())


'Play an Eplisode with a Random Agent'
reward_list = []
for episode in range(episodes):
    
    'Starting countdown to measure the time taken for one episode'
    start = time.time()
    done = False
    obs = env.reset()
    print('\nObservation after Reset:', obs)
    total_reward = 0
    score = 0
    while not done:
        'Taking an random action'
        random_action = env.action_space.sample()
        print('\nAction taken by the agent:',random_action)
        
        'Getting the observation, reward and done status from the environment'
        obs, reward, done, info = env.step(random_action)
        print('\nInfo:',info)
        print('\nReward at the step:', reward)
        print('\nObservation at the step:', obs)
        
        total_reward += reward
    
    reward_list.append((math.exp(total_reward)-1) * 100)
    end = time.time()
    print(f"Time taken for the episode: {(end-start)*10**3:.03f}ms")
    
    
'Plotting a Reward histogram'
plt.hist(reward_list, bins=30, color='blue', edgecolor='black')
'Adding labels and title'
plt.xlabel('% Reward')
plt.ylabel('Frequency')
plt.title('Reward Histogram')

'Save the histogram plot.'
file_path = 'test_logs/' + test_agent_id + '/Reward_in_Percentage_Histogram.jpeg'


plt.savefig(file_path, dpi=500)

'Display the plot'
plt.show()