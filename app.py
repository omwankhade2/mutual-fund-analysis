import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Mutual Funds Performance Analysis",
    page_icon="📊",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #12355b;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666666;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.10);
    text-align: center;
}

.card h2 {
    color: #12355b;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("mutual_funds_ind (1).csv")

    # Remove unwanted spaces from column names
    df.columns = df.columns.str.strip()

    # Convert return columns into numeric
    for col in ['return_1yr', 'return_3yr', 'return_5yr']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


df = load_data()


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.markdown(
    '<div class="title">📊 Mutual Funds Performance Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze Mutual Fund Returns, Risk Types, Categories and AMC Performance</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("🔍 Dashboard Filters")


# Category
categories = ["All"] + sorted(
    df['category'].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)


# Risk Type
risk_types = ["All"] + sorted(
    df['risk_type'].dropna().unique().tolist()
)

selected_risk = st.sidebar.selectbox(
    "Select Risk Type",
    risk_types
)


# AMC
amcs = ["All"] + sorted(
    df['AMC_name'].dropna().unique().tolist()
)

selected_amc = st.sidebar.selectbox(
    "Select AMC Name",
    amcs
)


# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------

filtered_df = df.copy()


if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df['category'] == selected_category
    ]


if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df['risk_type'] == selected_risk
    ]


if selected_amc != "All":
    filtered_df = filtered_df[
        filtered_df['AMC_name'] == selected_amc
    ]


# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

st.subheader("📌 Performance Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="card">
        <h2>{len(filtered_df)}</h2>
        <p>Mutual Funds</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    avg_1yr = filtered_df['return_1yr'].mean()

    st.markdown(
        f"""
        <div class="card">
        <h2>{avg_1yr:.2f}%</h2>
        <p>Average 1 Year Return</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    avg_3yr = filtered_df['return_3yr'].mean()

    st.markdown(
        f"""
        <div class="card">
        <h2>{avg_3yr:.2f}%</h2>
        <p>Average 3 Year Return</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    avg_5yr = filtered_df['return_5yr'].mean()

    st.markdown(
        f"""
        <div class="card">
        <h2>{avg_5yr:.2f}%</h2>
        <p>Average 5 Year Return</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")


# -------------------------------------------------
# RETURN ANALYSIS
# -------------------------------------------------

st.subheader("📈 Return Analysis")


col1, col2 = st.columns(2)


# Category vs Return
with col1:

    category_return = (
        filtered_df
        .groupby('category')['return_5yr']
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    category_return.plot(
        kind='bar',
        ax=ax
    )

    ax.set_title("Category vs Average 5 Year Return")
    ax.set_xlabel("Category")
    ax.set_ylabel("Average 5 Year Return")

    plt.xticks(rotation=90)

    st.pyplot(fig)


# Risk Type vs Return
with col2:

    risk_return = (
        filtered_df
        .groupby('risk_type')['return_5yr']
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    risk_return.plot(
        kind='bar',
        ax=ax
    )

    ax.set_title("Risk Type vs Average 5 Year Return")
    ax.set_xlabel("Risk Type")
    ax.set_ylabel("Average 5 Year Return")

    plt.xticks(rotation=45)

    st.pyplot(fig)


# -------------------------------------------------
# AMC ANALYSIS
# -------------------------------------------------

st.subheader("🏢 AMC Performance")


amc_return = (
    filtered_df
    .groupby('AMC_name')['return_3yr']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)


fig, ax = plt.subplots(figsize=(12, 5))

amc_return.plot(
    kind='bar',
    ax=ax
)

ax.set_title("Top 10 AMC by Average 3 Year Return")
ax.set_xlabel("AMC Name")
ax.set_ylabel("Average 3 Year Return")

plt.xticks(rotation=90)

st.pyplot(fig)


# -------------------------------------------------
# TOP 10 MUTUAL FUNDS
# -------------------------------------------------

st.subheader("🏆 Top 10 Mutual Funds")


top10 = (
    filtered_df
    .groupby('MutualFund_Name')['return_5yr']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)


fig, ax = plt.subplots(figsize=(12, 6))

top10.sort_values().plot(
    kind='barh',
    ax=ax
)

ax.set_title("Top 10 Mutual Funds Based on 5 Year Return")
ax.set_xlabel("Average 5 Year Return")
ax.set_ylabel("Mutual Fund Name")

st.pyplot(fig)


# -------------------------------------------------
# RETURN COMPARISON
# -------------------------------------------------

st.subheader("📊 Mutual Fund Return Comparison")


dashboard = (
    filtered_df
    .groupby('MutualFund_Name')[
        ['return_1yr', 'return_3yr', 'return_5yr']
    ]
    .mean()
)


st.dataframe(
    dashboard.sort_values(
        'return_5yr',
        ascending=False
    ),
    use_container_width=True
)


# -------------------------------------------------
# RAW DATA
# -------------------------------------------------

with st.expander("📋 View Complete Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")

st.markdown(
    "<center>Mutual Funds Performance Analysis | Python + Pandas + Streamlit</center>",
    unsafe_allow_html=True
)
