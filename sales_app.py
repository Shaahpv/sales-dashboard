import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# Generate data
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
    product_sales = filtered_df.groupby("Product")["Sales"].sum().sort_values()
    fig, ax = plt.subplots()
    ax.barh(product_sales.index, product_sales.values, color="steelblue")
    ax.set_xlabel("Sales ($)")
    st.pyplot(fig)

with col2:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby("Region")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.pie(region_sales.values, labels=region_sales.index, autopct="%1.1f%%",
           colors=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"])
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_df.groupby(filtered_df["Date"].dt.month)["Sales"].sum()
    fig, ax = plt.subplots()
    ax.plot(monthly_sales.index, monthly_sales.values, marker="o", color="green", linewidth=2)
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    st.pyplot(fig)

with col2:
    st.subheader("Sales vs Profit")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df["Sales"], filtered_df["Profit"], alpha=0.5, color="purple")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Profit ($)")
    st.pyplot(fig)

st.divider()

# Raw data
st.subheader("📋 Raw Data")
st.dataframe(filtered_df.head(50), use_container_width=True)
st.caption(f"Showing 50 of {len(filtered_df)} records")
