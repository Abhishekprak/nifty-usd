import streamlit as st
import requests
import pandas as pd


st.title('NIFTY USD ROTATION')

def bat():
    df = pd.read_csv("nifty_usd_signal.csv")
    th = ["date","nifty_open","nifty_close","usd_open","usd_close","signal"]
    df1 = df[th]
    st.dataframe(df1.tail(5))
    

date = st.date_input("Enter date here (DD-MM-YYYY):")
nifty_close = st.number_input("Enter nifty_close value:")
nifty_open = st.number_input("Enter nifty_open value:")
nifty_high = st.number_input("Enter nifty_high value:")
nifty_low = st.number_input("Enter nifty_low value:")

usd_close = st.number_input("Enter usd_close value:")
usd_open = st.number_input("Enter usd_open value:")
usd_high = st.number_input("Enter usd_high value:")
usd_low = st.number_input("Enter usd_low value:")


if st.button('Submit'):
    # Validate input values
    if not all([date, nifty_close, nifty_open, nifty_high, nifty_low, usd_close, usd_open, usd_high, usd_low]):
        st.error("Please fill in all the fields.")
    else:
        try:
            # Convert inputs to appropriate types
            date = date.strftime("%d-%m-%Y")
            nifty_close = float(nifty_close)
            nifty_open = float(nifty_open)
            nifty_high = float(nifty_high)
            nifty_low = float(nifty_low)
            usd_close = float(usd_close)
            usd_open = float(usd_open)
            usd_high = float(usd_high)
            usd_low = float(usd_low)

            # Prepare input data for API request
            input_data = {
                "date": date,
                "nifty_close": nifty_close,
                "nifty_open": nifty_open,
                "nifty_high": nifty_high,
                "nifty_low": nifty_low,
                "usd_close": usd_close,
                "usd_open": usd_open,
                "usd_high": usd_high,
                "usd_low": usd_low
            }

            # Make a POST request to FastAPI endpoint
            response = requests.post("http://127.0.0.1:8000/update-data/", json=input_data)

            if response.status_code == 200:
                st.success("Data updated successfully!")
                bat()
            else:
                st.error("Error occurred while updating data.")
        except ValueError:
            st.error("Invalid input. Please enter valid numeric values.")
