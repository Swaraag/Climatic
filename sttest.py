import streamlit as st
import pandas as pd
st.write(""" # Polling""")
st.write("Below are some questions")

ccYears = st.slider("How many years will it take for Climate Change to be solved?", 0, 100)