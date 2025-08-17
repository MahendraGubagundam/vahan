import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

DB_FILE = "vahan.db"

# ================== Load Data ==================
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM vahan_data", conn, parse_dates=["date"])
    conn.close()

    # Normalize vehicle_category
    if "vehicle_category" in df.columns:
        df["vehicle_category"] = df["vehicle_category"].str.strip().str.upper()
        df["vehicle_category"] = df["vehicle_category"].replace({
            "TWO WHEELER": "2W",
            "THREE WHEELER": "3W",
            "FOUR WHEELER": "4W",
            "LIGHT MOTOR VEHICLE": "4W",
            "LIGHT GOODS VEHICLE": "4W",
            "OTHER": "OTHERS"
        })
    else:
        df["vehicle_category"] = "OTHERS"

    # Ensure manufacturer column exists
    if "manufacturer" not in df.columns and "maker_company" in df.columns:
        df["manufacturer"] = df["maker_company"]

    # Ensure state_name column exists
    if "state_name" not in df.columns:
        df["state_name"] = "Unknown"

    return df

# ================== Lottie Helper ==================
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
car_anim = load_lottie("https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json")
growth_anim = load_lottie("https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json")

df = load_data()

# Derive Year & Quarter
df["year"] = df["date"].dt.year
df["quarter"] = df["date"].dt.to_period("Q").astype(str)

# ================== Sidebar Filters ==================
st.sidebar.title("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "📅 Select Date Range", [df["date"].min(), df["date"].max()]
)

# Predefined full state list
full_states = [
    'Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
    'Chandigarh', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
    'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh',
    'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
    'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura',
    'The Dadra And Nagar Haveli And Daman And Diu', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]

# State filter
states = st.sidebar.multiselect(
    "🏛️ Select State(s)",
    full_states,
    default=full_states
)

# Manufacturer filter
manufacturers = st.sidebar.multiselect(
    "🏭 Select Manufacturer(s)",
    df["manufacturer"].unique(),
    default=df["manufacturer"].unique()
)

# Vehicle category filter
all_categories = ["2W", "3W", "4W", "OTHERS"]
categories = st.sidebar.multiselect(
    "🚘 Select Vehicle Category",
    all_categories,
    default=all_categories
)

# Animation speed control
anim_speed = st.sidebar.slider(
    "⏱️ Animation Speed (ms per frame)", min_value=200, max_value=2000, step=200, value=1000
)

# ================== Apply Filters ==================
mask = (
    df["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
) & (df["state_name"].isin(states)) \
  & (df["manufacturer"].isin(manufacturers)) \
  & (df["vehicle_category"].isin(categories))

filtered = df[mask]

# Sort
filtered = filtered.sort_values(by=["state_name", "manufacturer", "vehicle_category"])

# ================== KPIs ==================
st.markdown("## 📊 Key Metrics")
col1, col2 = st.columns([1, 3])

with col1:
    st_lottie(car_anim, height=120, key="car")

with col2:
    total_reg = int(filtered["registrations"].sum())
    yoy_growth = (
        filtered.groupby("year")["registrations"].sum().pct_change().iloc[-1] * 100
        if len(filtered["year"].unique()) > 1 else 0
    )
    qoq_growth = (
        filtered.groupby("quarter")["registrations"].sum().pct_change().iloc[-1] * 100
        if len(filtered["quarter"].unique()) > 1 else 0
    )

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("📌 Total Registrations", f"{total_reg:,}")
    kpi2.metric("📈 YoY Growth", f"{yoy_growth:.2f} %", delta=f"{yoy_growth:.2f}%")
    kpi3.metric("📊 QoQ Growth", f"{qoq_growth:.2f} %", delta=f"{qoq_growth:.2f}%")

# ================== Tabs ==================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 YoY Trends", "📊 QoQ Trends", "🏭 Manufacturers", "🚘 Categories", "📊 Raw Data"]
)

# --- YoY Growth ---
with tab1:
    st.subheader("📈 Animated Year-over-Year Growth by Category")
    yoy = filtered.groupby(["year", "vehicle_category"])["registrations"].sum().reset_index()
    years = yoy["year"].unique()
    full_index = pd.MultiIndex.from_product([years, all_categories], names=["year", "vehicle_category"])
    yoy = yoy.set_index(["year", "vehicle_category"]).reindex(full_index, fill_value=0).reset_index()

    fig = px.bar(
        yoy,
        x="year",
        y="registrations",
        color="vehicle_category",
        text="registrations",
        animation_frame="year",
        barmode="group",
        title="YoY Vehicle Registrations (2W, 3W, 4W, Others)",
    )
    if "updatemenus" in fig.layout and len(fig.layout.updatemenus) > 0:
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = anim_speed
    st.plotly_chart(fig, use_container_width=True)

# --- QoQ Growth ---
with tab2:
    st.subheader("📊 Smooth Quarter-over-Quarter Growth by Category")
    qoq = filtered.groupby(["quarter", "vehicle_category"])["registrations"].sum().reset_index()
    quarters = qoq["quarter"].unique()
    full_index = pd.MultiIndex.from_product([quarters, all_categories], names=["quarter", "vehicle_category"])
    qoq = qoq.set_index(["quarter", "vehicle_category"]).reindex(full_index, fill_value=0).reset_index()

    fig = px.line(
        qoq,
        x="quarter",
        y="registrations",
        color="vehicle_category",
        markers=True,
        title="QoQ Vehicle Registrations (2W, 3W, 4W, Others)"
    )
    fig.update_traces(line_shape="spline")
    st.plotly_chart(fig, use_container_width=True)

# --- Manufacturers ---
with tab3:
    st.subheader("🏭 Manufacturer Insights by Category")
    # Aggregate by manufacturer + vehicle_category within filtered states
    mf = filtered.groupby(["manufacturer", "vehicle_category"])["registrations"].sum().reset_index()
    manufacturers_unique = mf["manufacturer"].unique()
    full_index = pd.MultiIndex.from_product([manufacturers_unique, all_categories], names=["manufacturer", "vehicle_category"])
    mf = mf.set_index(["manufacturer", "vehicle_category"]).reindex(full_index, fill_value=0).reset_index()

    fig = px.bar(
        mf,
        x="registrations",
        y="manufacturer",
        color="vehicle_category",
        orientation="h",
        text="registrations",
        barmode="stack",
        title=f"Top Manufacturers by Registrations (Filtered States: {', '.join(states)})",
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Categories ---
with tab4:
    st.subheader("🚘 Vehicle Category Insights")
    vc = filtered.groupby("vehicle_category")["registrations"].sum().reindex(all_categories, fill_value=0).reset_index()
    fig = px.pie(vc, values="registrations", names="vehicle_category", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    st_lottie(growth_anim, height=200, key="growth")

# --- Raw Data ---
with tab5:
    st.markdown("### 📊 Raw Data")
    st.dataframe(filtered)
    st.download_button(
        "⬇️ Download CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        "filtered_data.csv",
        "text/csv",
    )
    st.markdown("### ✅ Investor-Friendly Insights")
    st.write("- Users see **clear animated YoY growth 📈** (2W, 3W, 4W, Others).")
    st.write("- Users see **smooth QoQ trend line 📊** with all categories.")
    st.write("- Manufacturer trends include **2W, 3W, 4W, Others** clearly.")
    st.write("- **Clean, interactive, attractive dashboard with state-wise sorting**.")
