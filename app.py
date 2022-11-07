from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
import random 

model = load_model('Final LDA Model 16Oct2022')

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():

    from PIL import Image
    airport = Image.open('airport.jpg')
    american = Image.open('american.png')
    southwest = Image.open('southwest.png')
    delta = Image.open('delta.png')
    express = Image.open('express.png')
    alaska = Image.open('alaska.png')


    st.image(airport,use_column_width=False)

    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))

    st.sidebar.image(american)
    st.sidebar.image(southwest)
    st.sidebar.image(delta)
    st.sidebar.image(express)
    st.sidebar.image(alaska)
    st.title("Airline Delay Prediction App")

    if add_selectbox == 'Online':
        
        flight = st.number_input('Flight Number (Enter a value between 10 and 2000)', min_value=10, max_value=2000, value=10)
        airline = st.selectbox('Airline', ['CO', 'AA','AS','DL','WN','OO','DL','EV','XE','OH'])
        st.text('CO: North-Western Cargo International Airlines')
        st.text('AA: American Airlines')
        st.text('AS: Alaska Airlines')
        st.text('DL: Delta AirLines')
        st.text('WN: Southwest Airlines')
        st.text('OO: SkyWest Airlines')
        st.text('EV: ExpressJet Airlines')
        st.text('XE: Delux Public Charter LLC dba JSX Air')
        st.text('OH: PSA Airlines')

        dayofweek = st.number_input('Day of Week (1 is Monday and 7 is Sunday)', min_value=1, max_value=7, value=1)
        airportfrom = st.selectbox('Airport From', ['SFO','PHX','LAX','ANC','DEN','ONT','EWR','LIT','SAV','CHA'])
        st.text('SFO: San Francisco, CA ')
        st.text('PHX: Phoenix, AZ')
        st.text('LAX: Los Angeles, CA')
        st.text('ANC: Anchorage, AK')
        st.text('DEN: Denver, CO')
        st.text('ONT: Ontario, CA')
        st.text('EWR: Newark, NJ')
        st.text('LIT: Little Rock, AR')
        st.text('SAV: Savannah, GA')
        st.text('CHA: Chattanooga, TN')
        
        airportto = st.selectbox('Airport To', ['SFO','PHX','LAX','ANC','DEN','ONT','EWR','LIT','SAV','CHA'])
        time = st.number_input('Time Departed (Enter a value between 10 and 1440)', min_value=10, max_value=1440, value=10)
        st.text('For example, if the flight departed at 7pm, your input should be 420 (19th hour x 60 minutes)')
        length = st.number_input('Length of Flight', min_value=10, max_value=600, value=10)
        st.text('For example, if the flight lasted for 3 hours, your input should be 180 (3 x 60 minutes)')

        output=""
        hour = time//60
        hourfull = float(time/60)
        minutes = time - (hour * 60)
        lengthhour = float(length/60)

        input_dict = {'Airline' : airline, 'Flight' : flight, 'AirportFrom' : airportfrom, 'AirportTo' : airportto, 'DayOfWeek' : dayofweek,  'Time' : time, 'Length': length, 'Hour_full': hourfull , 'Hour': hour, 'Minutes': minutes, 'Length_hour': lengthhour}
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            if output == 1:
               st.success('The flight will get Delayed')
            elif output == 0:
               st.success('The flight will not get Delayed')


    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()
