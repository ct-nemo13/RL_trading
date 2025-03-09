# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 22:48:51 2023

@author: ritwi
"""

import os

def create_policy_dir(policy, agents_per_policy):
    
    if os.path.exists('policies') is False:
        os.mkdir('policies')
        print('Directory for the Policies is created successfully')
    else:
        print('Directory for the Policies exists already.')
    
    
    if os.path.exists('policies/' + policy) is False:
        os.mkdir('policies/' + policy)
        print('Directory for the Policy- ' + policy + ' is created successfully')
    else:
        print('Directory for the Policy- ' + policy + ' already exists')
        
    # Next to create the directory for each agent which use the policy. It save each the version of the agent during training.
    for i in range (agents_per_policy):
        if os.path.exists('policies/' + policy + '/agent_' + str(i)) is False:
            os.mkdir('policies/' + policy + '/agent_' + str(i))
            print('The directory for the following agent is successfully created \nPolicy- ' + policy + '\nAgent- ' + str(i))
        else:
            print('The directory for the following agent already exists \nPolicy- ' + policy + '\nAgent- ' + str(i))  