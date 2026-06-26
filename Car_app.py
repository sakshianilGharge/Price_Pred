import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os

st.title("Predict your Future Car Price")

# Load dataset
df = pd.read_csv("final_data.csv")

# DEBUG (remove later if everything works)
st.write(os.listdir())

# Load model ONCE (IMPORTANT FIX)
model = pickle.load(open("model.pkl", "rb"))

# Sidebar inputs
companies = sorted(df['company'].unique())
company = st.sidebar.selectbox("Select company", companies)

names = sorted(df[df['company'] == company]['name'].unique())
name = st.sidebar.selectbox("Select name", names)

year = st.sidebar.number_input(
    "Enter year",
    min_value=2000,
    max_value=2026,
    step=1
)

km_driven = st.sidebar.number_input(
    "Enter km driven",
    value=50000,
    min_value=1000,
    max_value=200000,
    step=5000
)

fuel_type = st.sidebar.selectbox("Select fuel type", ["Petrol", "Diesel"])

# Predict button
if st.sidebar.button("Predict Price"):

    st.write("Predicting for:")
    st.write("Company:", company)
    st.write("Name:", name)
    st.write("Year:", year)
    st.write("KM Driven:", km_driven)
    st.write("Fuel Type:", fuel_type)

    # Input dataframe
    columns = ['company', 'name', 'year', 'kms_driven', 'fuel_type']
    myinput = pd.DataFrame([[company, name, year, km_driven, fuel_type]],
                           columns=columns)

    # Prediction
    result = model.predict(myinput)

    # Output fix (correct indexing)
    if result[0] < 0:
        st.error("Sorry, inputs are wrong.")
    else:
        st.success("Predicted Price: ₹ " + str(round(result[0])))