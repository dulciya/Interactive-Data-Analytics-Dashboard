import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Universal Data Analytics App", layout="wide")
st.title("📊 Universal Interactive Data Analytics Dashboard")

# ==============================
# File Upload
# ==============================
uploaded_file = st.file_uploader("Upload Any CSV File", type=["csv"], key="main_uploader")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df.drop_duplicates(inplace=True)

    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())

    # =====================================
    # Auto-detect numeric columns
    # =====================================
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    all_columns = df.columns.tolist()

    if len(numeric_columns) == 0:
        st.error("❌ No numeric columns found in dataset.")
        st.stop()

    # =====================================
    # Sidebar Configuration
    # =====================================
    st.sidebar.header("⚙ Configure Analysis")

    date_column = st.sidebar.selectbox(
        "Select Date Column",
        ["None"] + all_columns,
        index=0
    )

    revenue_column = st.sidebar.selectbox(
        "Select Revenue/Numeric Column",
        numeric_columns
    )

    category_column = st.sidebar.selectbox(
        "Select Category Column (Optional)",
        ["None"] + all_columns
    )

    region_column = st.sidebar.selectbox(
        "Select Region Column (Optional)",
        ["None"] + all_columns
    )

    # =====================================
    # Date Processing + Date Filter
    # =====================================
    if date_column != "None":
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce", dayfirst=True)
        df = df.dropna(subset=[date_column])

        min_date = df[date_column].min()
        max_date = df[date_column].max()

        date_range = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date]
        )

        if len(date_range) == 2:
            df = df[
                (df[date_column] >= pd.to_datetime(date_range[0])) &
                (df[date_column] <= pd.to_datetime(date_range[1]))
            ]

        df["Month"] = df[date_column].dt.to_period("M").astype(str)

    # =====================================
    # KPIs
    # =====================================
    total_value = df[revenue_column].sum()
    avg_value = df[revenue_column].mean()
    total_records = df.shape[0]

    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Value", f"{total_value:,.2f}")
    col2.metric("Average Value", f"{avg_value:,.2f}")
    col3.metric("Total Records", total_records)

    # =====================================
    # Monthly Trend
    # =====================================
    if date_column != "None":
        st.subheader("📈 Monthly Trend")

        monthly_data = df.groupby("Month")[revenue_column].sum().reset_index()

        fig_line = px.line(
            monthly_data,
            x="Month",
            y=revenue_column,
            markers=True,
            title="Monthly Trend"
        )

        st.plotly_chart(fig_line, use_container_width=True)

    # =====================================
    # Category Chart + Top 10
    # =====================================
    if category_column != "None":
        st.subheader("📊 Category Distribution (Top 10)")

        category_data = (
            df.groupby(category_column)[revenue_column]
            .sum()
            .reset_index()
            .sort_values(by=revenue_column, ascending=False)
            .head(10)
        )

        fig_bar = px.bar(
            category_data,
            x=category_column,
            y=revenue_column,
            color=category_column,
            title="Top 10 Categories"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # =====================================
    # Region Pie Chart
    # =====================================
    if region_column != "None":
        st.subheader("🌍 Region Distribution")

        region_data = (
            df.groupby(region_column)[revenue_column]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            region_data,
            names=region_column,
            values=revenue_column,
            title="Revenue by Region"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # =====================================
    # Download Filtered Data
    # =====================================
    st.subheader("⬇ Download Filtered Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv",
    )

else:
    st.info("👆 Upload a CSV file to begin analysis.")
