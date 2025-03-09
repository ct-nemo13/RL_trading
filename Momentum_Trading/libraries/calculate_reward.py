# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:46:57 2024

@author: ritwi
"""

import numpy as np


'Calculate Reward'
def calculate_reward(self):
    
    'Reward by the net worth groth. I have adapted it from  Gym Trading Environment'
    'Seems to be legit. However, I have to explore more.'
    self.reward = np.log(self.net_worth/self.old_net_worth)
    
    
    'Here I am addining the penalty for wrong action.'
    self.reward += self.penalty_for_wrong_action
    
    
    print('Reward at the step:', self.reward)
    
    
    

        