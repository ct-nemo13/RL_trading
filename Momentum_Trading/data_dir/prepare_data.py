# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 04:01:12 2023

@author: ritwik
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

'Step 1: Define the Input and Output directories'
base_dir = "stock_data_raw"
training_dir = "train_data"
testing_dir = "test_data"

'Step 2:Create training and testing directories if not exist'
os.makedirs(training_dir, exist_ok=True)
os.makedirs(testing_dir, exist_ok=True)


'''
Step 3: Defining the size of the data that will be extracted from the main 
data for training and testing.
Here I am extracting last 3 months' data.
21 trading days in a month. 6.5 hours in a trading day. 12 steps in an hour.
'''
train_and_test_data_size_in_step = 3*21*6.5*12


'Step 4: Loop through CSV files in the base directory'
for file_name in os.listdir(base_dir):
    
    'Step 5: Check if the files are .csv files.'
    if file_name.endswith(".csv"):
        
        'Step 6: Read the CSV file into a DataFrame'
        file_path = os.path.join(base_dir, file_name)
        df = pd.read_csv(file_path)
        
        'Step 7: Extract last 3 month data from the data frame'
        total_steps = len(df)
        start_index = int(total_steps - train_and_test_data_size_in_step)
        end_index = int(total_steps)
        df = df.iloc[start_index:end_index]
        
        'Step 8: Split the extracted data into training and testing data sets'
        train_df, test_df = train_test_split(df, test_size=0.3, shuffle=False)
        
        'Step 9: Update the name. Remove "_5minute" from the file name.'
        updated_file_name = file_name.replace("_5minute", "")
        
        'Step 10: Save the train and test data frames'
        train_file_path = os.path.join(training_dir, updated_file_name)
        test_file_path = os.path.join(testing_dir, updated_file_name)
        train_df.to_csv(train_file_path, index=False)
        test_df.to_csv(test_file_path, index=False)

        print(f"\nProcessed {file_name}, \nCreated {updated_file_name} at location \n{train_file_path}\nand\n{test_file_path}")


