import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json

import streamlit as st

# Add CSS for customizing the background color
def set_background(color):
    """
    Sets the background color of the current page.
    
    Parameters:
        color (str): The color to set as the background.
                     It can be specified using color names (e.g., 'red', 'blue')
                     or hexadecimal codes (e.g., '#ff0000', '#0000ff').
    """
    hex_color = f"#{color}"
    html_code = f"""
        <style>
        .reportview-container {{
            background-color: {hex_color};
        }}
        </style>
        """
    st.markdown(html_code, unsafe_allow_html=True)

# Set the background color
set_background("lightblue")


st.title("Banglore House Price Predictor")

with open('banglore_home_prices_model.pickle', 'rb') as f:
    lr_clf= pickle.load(f)

with open("columns.json", "r") as f:
    columns_data = json.load(f)
data_columns=columns_data['data_columns']
#print(data_columns)

priority_column = "other"
if priority_column in data_columns:
    data_columns.remove(priority_column)
    data_columns.insert(3, priority_column)

def predict_price(location,sqft,bath,bhk):
    
    loc_index=data_columns.index(location.lower())
    fet=np.zeros(len(data_columns))
    fet[0]=sqft
    fet[1]=bath
    fet[2]=bhk
    
    if (loc_index>=0):
        fet[loc_index]=1
    return lr_clf.predict([fet])[0]

location=st.selectbox(
"Enter the location",data_columns[3:],index=None,placeholder="Choose the location"
    )
area=st.number_input("Enter the Area Size" , value=None , placeholder="Area(in Sq-ft)",step=1 )
bathrooms=st.number_input("Enter the no of Bathrooms",value=None,placeholder="Bathrooms",step=1)
bedrooms=st.number_input("Enter the no of Bedrooms",value=None,placeholder="Bedrooms",step=1)

if st.button("Predict Price"):
    predicted_price=round(predict_price(location,area,bathrooms,bedrooms),2)
    st.subheader(f"{predicted_price} Lakhs")


