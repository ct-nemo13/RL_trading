# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:59:34 2024

@author: ritwi
"""
import os


def init_for_test_mode(self):
        
    'First making folders for saving test reports'
    if os.path.exists('test_logs') is False:
        os.mkdir('test_logs')
        print('The main "test_logs" directory is successfully created.')
    else:
        pass
        print('The "test_logs" directory already exists.')
        
    'Create test log dir for the test agent.'
    if os.path.exists('test_logs/' + self.test_agent_id) is False:
        os.mkdir('test_logs/' + self.test_agent_id)

    'Get the test log directory path.'
    self.dir = 'test_logs/' + str(self.test_agent_id) + '/'

    'Initializing the test episode.'
    self.test_episode_count = 0
    
    'Initializing the action list. Here all the taken actions will be stored.'
    self.action_list = []
