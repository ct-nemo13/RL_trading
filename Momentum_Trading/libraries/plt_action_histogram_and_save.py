# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:35:57 2024

@author: ritwi
"""

import matplotlib.pyplot as plt

def plt_action_histogram_and_save(self):
                
    'Plotting a basic histogram'
    plt.hist(self.action_list, bins=30, color='blue', edgecolor='black')
    'Adding labels and title'
    plt.xlabel('Action Values')
    plt.ylabel('Frequency')
    plt.title('Action Value Histogram')

    'Save the histogram plot.'
    file_path = self.dir + 'Action_Histogram.jpeg'


    plt.savefig(file_path, dpi=500)
    
    'Display the plot'
    plt.show()
