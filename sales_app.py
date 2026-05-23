import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    np.random.seed(42)
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=500, freq="D"),
        "Product": np.random.choice(["Laptop", "Phone", "Tablet", "Watch", "Earbuds"], 500),
        "Region": np.random.choice(["North", "South", "East", "West"], 500),
        "Sales": np.random.randint(100, 5000, 500),
        "Units": np.random.randint(1, 50, 500),
        "Customer_Age": np.random.randint(18, 65, 500),
    }
    df = pd.DataFrame(data)
    df["Month"] = df["Date"].dt.strftime("%B")
    df["Profit"] = df["Sales"] * np.random.uniform(0.2, 0.4, 500)
    return df

df = load_data()

# Header
st.title("📊 Sales Data Dashboard")
st.markdown("Interactive analysis of sales performance across products and regions.")
st.divider()

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
selected_product = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Filter data
filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Product"].isin(selected_product))
]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("📦 Total Units", f"{filtered_df['Units'].sum():,}")
col3.metric("💵 Avg Sale", f"${filtered_df['Sales'].mean():,.0f}")
col4.metric("📈 Total Profit", f"${filtered_df['Profit'].sum():,.0f}")

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product")
    product_sales = filtered_df.groupby("Product")["Sales"].sum().reset_index()
    fig = px.bar(product_sales, x="Sales", y="Product", orientation="h",
                 color="Sales", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    fig = px.pie(region_sales, values="Sales", names="Region",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Sales Trend")
    filtered_df["MonthNum"] = filtered_df["Date"].dt.month
    monthly_sales = filtered_df.groupby("MonthNum")["Sales"].sum().reset_index()
    fig = px.line(monthly_sales, x="MonthNum", y="Sales",
                  markers=True, color_discrete_sequence=["green"])
    fig.update_xaxes(title="Month")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales vs Profit")
    fig = px.scatter(filtered_df, x="Sales", y="Profit",
                     color="Product", opacity=0.6)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Raw data
st.subheader("📋 Raw Data")
st.dataframe(filtered_df.head(50), use_container_width=True)
st.caption(f"Showing 50 of {len(filtered_df)} records")
