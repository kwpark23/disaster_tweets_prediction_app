from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
import random 

model = load_model('Final Model 11Nov2022')

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():

    from PIL import Image
    forestfire = Image.open('forestfire.jpg')
    flooding = Image.open('flooding.jpg')
    damaged = Image.open('damaged.jpg')
    shooting = Image.open('shooting.jpg')
    ambulance = Image.open('ambulance.jpg')
    tornado = Image.open('tornado.jpg')


    st.image(forestfire,use_column_width=False)

    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))

    st.sidebar.image(flooding)
    st.sidebar.image(damaged)
    st.sidebar.image(shooting)
    st.sidebar.image(ambulance)
    st.sidebar.image(tornado)
    st.title("Disaster Tweet Prediction App")

    if add_selectbox == 'Online':
        
        tweet = st.text_input("Enter your Tweet: ","Your tweet here")
        keyword = st.text_input("Enter your keyword: ","Your keyword here, if you don't have one, delete these texts")
        location = st.text_input("Enter your Location: ","Location here, if you don't have one, delete these texts")


        output=""
        
        input_dict = {'text' : tweet, 'keyword':keyword, 'location':location}
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            if output == 1:
               st.success('This is a disaster tweet')
            elif output == 0:
               st.success('This is not a disaster tweet')


    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()
