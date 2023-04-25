# basic imports
import pandas as pd
import numpy as np

# Define a function to resample a time series data by a specified time period and aggregate by a measure
def resample_series(series, time_period='day', measure='revenue'):
    
    # Define a dictionary to convert time periods to the corresponding resample frequencies
    time_periods = {'day': 'D', 'week': 'W', 'month': 'M', 'year': 'Y'}
    
    # Define a dictionary to convert measure names to the corresponding column names in the series DataFrame
    measures = {'revenue': 'sales_revenue', 'gross': 'gross_profit', 'margin': 'profit_margin'}
    
    # Set the index of the DataFrame to the 'date' column and resample the data by the specified time period 
    # (e.g., 'D' for daily, 'W' for weekly, etc.), and aggregate the 'sales_revenue', 'gross_profit', or 'profit_margin'
    # column by summing the values within each time period
    series = series.set_index('date')[measures[measure]].resample(time_periods[time_period]).sum()
    
    # Convert the resampled series back to a DataFrame and reset the index to include the 'date' column
    series = pd.DataFrame(series).reset_index()
    
    return series


# Define a function to extract date features from a time series DataFrame
def create_date_features(timeseries_df):
    
    # Extract year, month, day, week of year, and weekday from the 'date' column using pandas datetime functions
    timeseries_df['year'] = timeseries_df['date'].dt.year
    timeseries_df['month'] = timeseries_df['date'].dt.month
    timeseries_df['day'] = timeseries_df['date'].dt.day
    timeseries_df['weekofyear'] = timeseries_df['date'].dt.isocalendar().week
    timeseries_df['weekday'] = timeseries_df['date'].dt.weekday + 1
    
    return timeseries_df


# Define a function to add lagged features to a time series DataFrame
def add_lagged_features(timeseries_df, num_lag):
    
    # Loop over a range of lags (from 1 to num_lag) and add columns to the DataFrame containing the values of the 
    # sales_revenue, gross_profit, or profit_margin column lagged by each specified amount
    for lag in range(1, num_lag+1):
        timeseries_df[f'lag_{lag}'] = timeseries_df.iloc[:,1].shift(lag)
        
    # Drop rows that contain NaN values (due to the lags shifting the values out of the DataFrame)
    timeseries_df = timeseries_df.iloc[num_lag: , :]
    
    return timeseries_df
