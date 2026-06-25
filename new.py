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

# Uncomment for debugging if needed
# st.write(df.dtypes)
# st.write(df.head())

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("🏠 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Overview",
        "Location Analytics",
        "Property Analytics",
        "Investment Insights",
        "Property Explorer"
    ]
)

# ---------------------------
# OVERVIEW PAGE
# ---------------------------
if page == "Overview":

    st.title("🏠 Real Estate Investment Advisor")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Properties", f"{len(df):,}")

    with col2:
        st.metric(
            "Avg Price (Lakhs)",
            round(df["Price_in_Lakhs"].mean(), 2)
        )

    with col3:
        st.metric(
            "Avg Size (SqFt)",
            round(df["Size_in_SqFt"].mean(), 0)
        )

    with col4:
        st.metric(
            "Cities Covered",
            df["City"].nunique()
        )

    st.divider()

    fig1 = px.histogram(
        df,
        x="Price_in_Lakhs",
        title="Property Price Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(
        df,
        names="Property_Type",
        title="Property Type Share"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# LOCATION ANALYTICS
# ---------------------------
elif page == "Location Analytics":

    st.title("📍 Location Analytics")

    state_price = (
        df.groupby("State")["Price_in_Lakhs"]
        .mean()
        .reset_index()
        .sort_values("Price_in_Lakhs", ascending=False)
    )

    fig = px.bar(
        state_price,
        x="State",
        y="Price_in_Lakhs",
        title="Average Price by State"
    )

    st.plotly_chart(fig, use_container_width=True)

    city_price = (
        df.groupby("City")["Price_in_Lakhs"]
        .mean()
        .reset_index()
        .sort_values("Price_in_Lakhs", ascending=False)
        .head(10)
    )

    fig = px.bar(
        city_price,
        x="City",
        y="Price_in_Lakhs",
        title="Top 10 Expensive Cities"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# PROPERTY ANALYTICS
# ---------------------------
elif page == "Property Analytics":

    st.title("🏘️ Property Analytics")

    fig = px.box(
        df,
        x="Property_Type",
        y="Price_in_Lakhs",
        title="Property Type vs Price"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        df,
        x="BHK",
        y="Price_in_Lakhs",
        title="BHK vs Price"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# INVESTMENT INSIGHTS
# ---------------------------
elif page == "Investment Insights":

    st.title("📊 Investment Insights")

    most_expensive_state = (
        df.groupby("State")["Price_in_Lakhs"]
        .mean()
        .idxmax()
    )

    most_expensive_city = (
        df.groupby("City")["Price_in_Lakhs"]
        .mean()
        .idxmax()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"🏆 Most Expensive State: {most_expensive_state}"
        )

    with col2:
        st.success(
            f"🏆 Most Expensive City: {most_expensive_city}"
        )

# ---------------------------
# PROPERTY EXPLORER
# ---------------------------
elif page == "Property Explorer":

    st.title("🔍 Property Explorer")

    state = st.selectbox(
        "Select State",
        ["All"] + sorted(df["State"].dropna().unique().tolist())
    )

    if state != "All":
        filtered = df[df["State"] == state]
    else:
        filtered = df.copy()

    st.dataframe(filtered)

    csv = filtered.to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="filtered_properties.csv",
        mime="text/csv"
    )
