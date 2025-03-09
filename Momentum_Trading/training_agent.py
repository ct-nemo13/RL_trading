# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 16:00:26 2023

@author: ritwi
"""

from ray.rllib.algorithms.algorithm import Algorithm
import os
import pandas as pd
from  libraries.make_dir_and_df_for_training_log import  make_dir_and_df_for_training_log



# Training the Default Agent
policy = 'default_LSTM_v2'
agents_per_policy = 3

'The agents to be trained out of all'
agents = [0, 1, 2]
training_range = 200

'Create directories for training logs'
make_dir_and_df_for_training_log(policy,agents_per_policy)


for i in agents:
    if os.path.exists('policies/' + policy + '/agent_' + str(i) + '/0') is False:
        print('The following agent does not exist:\nPolicy- ' + policy + '\nAgent- ' + str(i))
    else:
        print('The training is getting started for the following agent:\nPolicy- ' + policy + '\nAgent- ' + str(i))
        print('Recalling the last trained agent')
        
        # Recall the last trained agent
        agent_name_list = os.listdir('policies/' + policy + '/agent_' + str(i))
        agent_name_list_in_int = [int(x) for x in agent_name_list]
        last_agent_num = max(agent_name_list_in_int)
        check_point = 'policies/' + policy + '/agent_' + str(i) + '/' + str(last_agent_num)
        print('The recalled Check Point: ' + check_point)
        agent = Algorithm.from_checkpoint(check_point)
        
        # Recall the log data frame
        print('Recalling the log dataframe')
        logs = pd.read_csv('training_logs/policy_' + policy + '/agent_' + str(i))
        print(logs)
        
        print('Starting the training loop')
        for j in range(last_agent_num, (last_agent_num + training_range)):
            'Train the agent'
            '*****************************************************************'
            'Need to figure how to change learning rate.'
            '******************************************************************'        
            result = agent.train()
            # Save the agent
            check_point_path_name = 'policies/' + policy + '/agent_' + str(i) + '/' + str(j+1)
            agent.save(check_point_path_name)
            
            # Capture the log parameters and record in the data frame    
            #print(pretty_print(result)) # It gives all the parameters regarding the training
            logs.at[j,'agent_name'] = str(int(j+1))
            logs.at[j,'itr_steps'] = result['num_env_steps_trained_this_iter'] * (j+1)
            logs.at[j,'rew_mean'] = result['episode_reward_mean']
            logs.at[j,'rew_max'] = result['episode_reward_max']
            logs.at[j,'rew_min'] = result['episode_reward_min']
            logs.at[j,'entropy'] = result['info']['learner']['default_policy']['learner_stats']['entropy']
            logs.at[j,'entropy_coeff'] = result['info']['learner']['default_policy']['learner_stats']['entropy_coeff']
            logs.at[j,'policy_loss'] = result['info']['learner']['default_policy']['learner_stats']['policy_loss']
            logs.at[j,'vf_loss'] = result['info']['learner']['default_policy']['learner_stats']['vf_loss']
            logs.at[j,'lr'] = result['info']['learner']['default_policy']['learner_stats']['cur_lr']
            
            print('The updated log\n')
            print(logs)
            
            print('Saving the log data frame...')
            logs.to_csv('training_logs/policy_' + policy + '/agent_' + str(i), index=False)
            print('The final log\n')
            print(logs)
        