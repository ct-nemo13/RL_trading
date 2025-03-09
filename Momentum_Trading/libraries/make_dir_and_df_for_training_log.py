# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 00:56:30 2023

@author: ritwi
"""

import pandas as pd
import os


def make_dir_and_df_for_training_log(policy, agents_per_policy):
   
    'Creating training_log directory and log data frames'
    
    'Creating the main log directory'
    if os.path.exists('training_logs') is False:
        os.mkdir('training_logs')
        print('The main "training-logs" directory is successfully created.')
    else:
        print('The "training-logs" directory already exists.')
    
    
    if os.path.exists('policies/' + policy) is False:
        print('There exists no Policy named ' + policy + '\nCreate the policy first')
    else:
        # creating log directory for each policy
        if os.path.exists('training_logs/policy_' + policy) is False:
            os.mkdir('training_logs/policy_' + policy)
            print('The log directory for Policy- ' + policy + ' is successfully created.')
        else:
            print('The "training-logs/policy_' + policy + '" directory already exists.')

        # creating data frame log for each agent
        for i in range (agents_per_policy): 
            # Checking if there existing any agent
            if os.path.exists('policies/' + policy + '/agent_' + str(i) + '/0') is False:
                print('No ' + str(i) + 'th agent exists for Policy- ' + policy + ' Create the agent first.')
            else:
                if os.path.exists('training_logs/policy_' + policy + '/agent_' + str(i)) is False:
                    columns = ['agent_name','itr_steps','rew_mean','rew_max','rew_min','entropy','entropy_coeff','policy_loss','vf_loss', 'lr']
                    df = pd.DataFrame(columns=columns)
                    df.to_csv('training_logs/policy_' + policy + '/agent_' + str(i), index=False)
                    print('The training log for Policy- ' + policy + ', Agent- '+ str(i) + ' is successfully created.')
                else:
                    print('The training log for Policy- ' + policy + ', Agent- '+ str(i) + ' already exits.')