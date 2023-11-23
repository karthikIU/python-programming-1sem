import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression as lr
import statsmodels.api as sm
from sqlalchemy import create_engine, Table, Column, Integer, Float, MetaData
import os
from database_migration import upgrade_migrations
from iu_python_db import IuPythonDb


# In Python, class names should follow the CamelCase convention, 
# also known as CapWords or PascalCase.
        
# for convenient purpose placing all files in same/single project directory
# files are not organized 


# here we no need class for just converting csv to df
# csv to df==>not linked to db, so not written in db.py file
def convert_csv_to_df(csv_path):
    csv_path = os.path.join(csv_path)
    return pd.read_csv(csv_path)

# Usage
train_data_df = convert_csv_to_df("train.csv")
ideal_data_df = convert_csv_to_df("ideal.csv")
test_data_df = convert_csv_to_df("test.csv")

#upgrade all migrations that creates train_data, ideal_data tables
upgrade_migrations()

# initializing db_connection instance
db_connection = IuPythonDb('iu_python.db')

# calling method of db_connection with df & table name
db_connection.df_to_sql(train_data_df, 'train_data')

# calling method of db_connection with df & table name
db_connection.df_to_sql(ideal_data_df, 'train_data')





def predict_ideal_functions():
    try:
        
        # merging the ideal_df and train_df1 dataframes
        # to remove naming conflicts with ideal y1, y2, y3, y4 columns with train y1, y2, y3, y4 columns
        # added suffixes to columns in train
        train_ideal_merged_df = pd.merge( train_data_df , ideal_data_df , on ="x", suffixes=('_train',''))

        # Provide 'suffixes' as a tuple.
        # These suffixes are used to disambiguate columns with the same name in the original DataFrames train_df and ideal_df. 
        
        # When you merge DataFrames based on a common column (in your case, "x"), 
        # the common column used for the merge (i.e., "x") will not get the suffixes added
        # print(train_ideal_merged_df)
        # Create dataframes for deviations

        columns_to_exclude = ['x']

        selected_ideal_cols=[]
        selected_ideal_deviations_df=pd.DataFrame()

        # iterating on column names y1, y2, y3, y4
        for train_col in train_data_df.columns:
            deviation_df = pd.DataFrame()
            if train_col not in columns_to_exclude:
                # iterating on column names y1...y50 in ideal
                for ideal_col in ideal_data_df.columns:
                    if ideal_col not in columns_to_exclude:
                        # since suffixes used only for train df columns in merged df
                        # storing with same column names y1...y50 in deviation_df
                        deviation_df[ideal_col] = train_ideal_merged_df[f'{train_col}_train'] - train_ideal_merged_df[ideal_col]

                # here used square deviation & summed & later we use absolute deviation in 2nd criteria
                sum_values =  deviation_df.apply(lambda x: (x ** 2).sum())
               
                # since have same no of rows or length we can use sum or mean of deviations

                lowest_sum_index = sum_values.idxmin() # finds the index, index==coloumn name

                # storing the lowest sum column name in selected_ideal_cols
                selected_ideal_cols.append(lowest_sum_index)

                # storing the absolute deviation of (train - ideal_ to find largest deviation for criteria 2 
                selected_ideal_deviations_df[lowest_sum_index]=deviation_df[lowest_sum_index].abs()

        # in selected ideal cols names added x, we need x col for further usage
        selected_ideal_cols.insert(0, 'x') 
        selected_ideal_df = train_ideal_merged_df.loc[:, selected_ideal_cols]
        # print(selected_ideal_df)
        # calculating max/largest deviation of selected ideal  cols
        max_devs_of_selected_ideal=selected_ideal_deviations_df.max()
        # print(max_devs_of_selected_ideal)

        # returning selected ideal function dataframe & largest deviation of selected ideal cols
        return selected_ideal_df , max_devs_of_selected_ideal
    except Exception as e :
        print ("Error !  Message , {m}".format( m =str( e ) ) )


# after traindata & ideal data loaded to db, now test data must be loaded line-by-line
# dont use pd.read it converts to df, instead read line by line








selected_ideal_df, max_devs_of_selected_ideal =predict_ideal_functions()

# print(selected_ideal_df)  included x 
# print(max_devs_of_selected_ideal)

# merging the test_df and selected_ideal_df
test_selected_ideal_df=pd.merge(test_data_df, selected_ideal_df, on='x')

# print(test_selected_ideal_df)


# calculating the deviation of test & selected ideal
test_ideal_deviation_df=pd.DataFrame()
for selected_ideal in test_selected_ideal_df:
    # including the x & y columns in test_ideal_deviation_df since needed to insert in db
    if selected_ideal == 'x' or selected_ideal == 'y':
        test_ideal_deviation_df[selected_ideal]=test_selected_ideal_df[selected_ideal]
    else:
        test_ideal_deviation_df[selected_ideal] = (test_selected_ideal_df['y'] - test_selected_ideal_df[selected_ideal]).abs()

# adding delta_y column in test_ideal_deviation_df
# delta_y is the devaiton of (test- lowest ideal), lowest ideal=lowest deviation of selected ideals
test_ideal_deviation_df['delta_y'] = test_ideal_deviation_df.drop(columns=['x', 'y']).min(axis=1)

# Find the column name corresponding to the minimum deviation value
test_ideal_deviation_df['least_dev_col_name'] = test_ideal_deviation_df.drop(columns=['x', 'y']).idxmin(axis=1)

# adding threshold column with different threshold for different rows so that we can compare easily
test_ideal_deviation_df['threshold'] = test_ideal_deviation_df['least_dev_col_name'].apply(lambda col: max_devs_of_selected_ideal[col] * np.sqrt(2))
# Compare 'delta_y' with the thresholds and replace with 'pass' if not satisfied
condition = test_ideal_deviation_df['delta_y'] <= test_ideal_deviation_df['threshold']

# test_ideal_deviation_df.loc[condition, 'min_column'] = 'pass'
test_ideal_deviation_df['no_of_ideal_functions'] = np.where(condition, test_ideal_deviation_df['least_dev_col_name'], 'pass',)

# required cols to insert in db
desired_columns = ['x', 'y', 'delta_y', 'no_of_ideal_functions']
test_ideal_deviation_df = test_ideal_deviation_df[desired_columns]
print(test_ideal_deviation_df)



db_connection.df_to_sql(test_ideal_deviation_df, 'test_mapping')
# write except cases for Nan when calculating

