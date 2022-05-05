import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def describe_columns(df):
    '''Get for each columns: the type, the number and the frequence of NaN and the number of unique values

            Parameters:
                    df (DataFrame): A DataFrame

            Returns:
                    desc_df (DataFrame): A DataFrame with described columns
    '''
    desc_df = {'Type':[],
              'NaN count':[],
              'NaN frequency':[],
              'Number of unique values':[]}
    for col in df.columns:
        desc_df['Type'].append(df[col].dtype)
        desc_df['NaN count'].append(pd.isnull(df[col]).sum())
        desc_df['NaN frequency'].append(pd.isnull(df[col]).mean())
        desc_df['Number of unique values'].append(len(df[col].unique()))
    return pd.DataFrame(desc_df, index=df.columns)

def move_column(df, column_name, column_place):
    '''Get for each columns: the type, the number and the frequence of NaN and the number of unique values

            Parameters:
                    df (DataFrame): A DataFrame
                    column_name (str): The name of the column that will be moved
                    column_place (int): The new position of the column

            Returns:
                    df (DataFrame): A DataFrame with rearranged columns
    '''
    mvd_column = df.pop(column_name)
    df.insert(column_place, column_name, mvd_column)
    return df

def prop_nan(df):
    '''Returns the proportion of NaN values in a DataFrame'''
    return (df.isna()).sum().sum()/df.size

def nan_map(df, figsize=(20,10), save=False, filename='nan_location'):
    '''Plot the NaN location with heatmap

            Parameters:
                    df (DataFrame): A DataFrame
                    figsize (tuple): Tuple representing the figure size
                    save (bool): save the plot if True
                    filename ('str'): Name of the file if save=True
    '''
    plt.figure(figsize=figsize)
    sns.heatmap(df.isna())
    if save:
        plt.savefig(filename)
