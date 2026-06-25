import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Real Estate Investment Advisor",
    page_icon="🏠",
    layout="wide"
)

@st.cache_data
def load_data():
# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("housing_cleaned.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    numeric_cols = [
        "Price_in_Lakhs",
        "Size_in_SqFt",
        "BHK",
        "Price_per_SqFt"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# Debug (remove later)
st.write(df.dtypes)
