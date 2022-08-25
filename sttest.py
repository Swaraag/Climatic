import streamlit as st
import pandas as pd
st.write(""" # Polling Time!""")

questionText = st.write("Below are some questions we'd love for you to answer!")


ccYears = st.slider("How many years will it take for Climate Change to be solved?", 0, 100)
ccDeath = st.radio("Do you think Climate Change will be the end of humanity?", ("Yes", "No"))
if (ccDeath == "Yes"):
    ccDate = st.date_input("What's your best guess for the exact date we will die due to Climate Change?")
elif (ccDeath == "No"):
    ccDate = st.date_input("What's your best guess for the exact date we will stop Climate Change?")

csv_data = st.file_uploader("Upload any CSV files you would like to visualize", type='csv')
if csv_data is not None:
    df = pd.read_csv(csv_data)
    try:
        st.bar_chart(df)
    except:
        st.write("Uh oh! Something went wrong!")
    

if st.button("Submit"):

    completed = st.write("Thanks for filling out the questions!")
