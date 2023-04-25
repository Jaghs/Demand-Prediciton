# basic imports
import pandas as pd
import numpy as np

def column_select_revenue(df, column, category_list):
    # create an empty list to store dataframes
    df_list = []
    
    # loop through each category in the category list
    for category in category_list:
        # filter the dataframe to include only rows with the current category
        cur = df[df[column] == category]
        # resample the data to a monthly frequency and sum the sales revenue
        cur = cur.resample('M', on='date').sum().reset_index()
        # add a new column with the current category name
        cur[column] = category
        # append the resampled dataframe to the list of dataframes
        df_list.append(cur)
    
    # concatenate the list of dataframes into a single dataframe
    category_df = pd.concat(df_list).reset_index(drop=True)
    
    # create a line plot of sales revenue over time, with a separate line for each category
    ax = sns.lineplot(data=category_df, x="date", y="sales_revenue", hue=f"{column}")
    
    # set the y-axis format to plain notation (i.e., no scientific notation)
    ax.ticklabel_format(style='plain', axis='y')
    
    # return the concatenated dataframe
    return category_df