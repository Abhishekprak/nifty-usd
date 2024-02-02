from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()


df = pd.read_csv("nifty_usd_signal.csv", parse_dates=['date'], dayfirst=True)


class InputData(BaseModel):
    date: str
    nifty_close: float
    nifty_open: float
    nifty_high: float
    nifty_low: float
    usd_close: float
    usd_open: float
    usd_high: float
    usd_low: float


@app.post("/update-data/")
async def update_data(data: InputData):
    global df

    def fill_columns(df, date, nifty_close, nifty_open, nifty_high, nifty_low, usd_close, usd_open, usd_high, usd_low):
        # Your existing function code goes here
        
       

        # Convert 'date' column in DataFrame to Timestamp if it's not already in that formatt
        # Assuming 'date' column contains date strings with a mix of date and time
        df['date'] = pd.to_datetime(df['date'])

        # Proper indentation of your existing code logic is essential.
        # Also, make sure you're using 'date' parameter instead of 'new_date'.
        df.sort_values('date', inplace=True)

        # Create a DataFrame with the provided data
        data_to_append = {
            'date': pd.to_datetime(date, format='%d-%m-%Y'),
            'nifty_close': nifty_close,
            'nifty_open': nifty_open,
            'nifty_high': nifty_high,
            'nifty_low': nifty_low,
            'usd_close': usd_close,
            'usd_open': usd_open,
            'usd_high': usd_high,
            'usd_low': usd_low,
            'nifty returns (%)': None,
            'usd/inr returns (%)': None,
            'nifty_mean': None,
            'usd/inr_mean': None,
            'nifty_std': None,
            'usd/inr_std': None,
            'normalised nifty': None,
            'normalised usd/inr': None,
            'signal': None
        }

        df.loc[len(df)] = data_to_append


        # Calculate 'percentage of nifty returns' and 'percentage of usd/inr returns'
        df['nifty returns (%)'] = df['nifty_close'].pct_change() * 100
        df['usd/inr returns (%)'] = df['usd_close'].pct_change() * 100

        # Calculate rolling means and standard deviations
        df['nifty_mean'] = df['nifty returns (%)'].rolling(window=21).mean()
        df['usd/inr_mean'] = df['usd/inr returns (%)'].rolling(window=21).mean()
        df['nifty_std'] = df['nifty returns (%)'].rolling(window=21).std()
        df['usd/inr_std'] = df['usd/inr returns (%)'].rolling(window=21).std()

        # Calculate 'normalised nifty data' and 'normalised usd/inr data'
        df['normalised nifty'] = df['nifty_mean'] / df['nifty_std']
        df['normalised usd/inr'] = df['usd/inr_mean'] / df['usd/inr_std']

        
        df['signal'] = np.where(df['normalised nifty'] > df['normalised usd/inr'], 'NIFTY', 'USD/INR')

        return df  # This line should be aligned with 'df.sort_values' line to be part of the function

    result_df = fill_columns(
        df,
        data.date,
        data.nifty_close,
        data.nifty_open,
        data.nifty_high,
        data.nifty_low,
        data.usd_close,
        data.usd_open,
        data.usd_high,
        data.usd_low
    )

    result_df.to_csv("nifty_usd_signal.csv", index=False)

    return {"message": "Data updated successfully"}
