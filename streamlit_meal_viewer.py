import streamlit as st
from shared.supabase_client import get_supabase_client
import pandas as pd
from datetime import datetime
import csv
import io

# Set page configuration
st.set_page_config(
    page_title="Gordita's Dachshund Bites",
    layout="wide",
    page_icon="🌭"  # Dachshund-like emoji
)

# Custom CSS for header style and a cute heart-dog vibe
st.markdown("""
    <style>
    .main h1 {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #d45c5c;
        text-align: center;
    }
    .stApp {
        background-color: #fff8f0;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🐶 Made with Love for Gordita — Dachshund Bites & Nutrition 💕")

# Initialize Supabase client
supabase = get_supabase_client()

# --- Upload CSV ---
st.sidebar.header("📤 Upload Meals")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    file_content = uploaded_file.getvalue().decode("utf-8")
    reader = csv.DictReader(io.StringIO(file_content))

    HEADER_MAP = {
        "Date": "date",
        "Meal": "meal",
        "Time": "time",
        "Calories": "calories",
        "Fat (g)": "fat_g",
        "Saturated Fat": "saturated_fat",
        "Polyunsaturated Fat": "polyunsaturated_fat",
        "Monounsaturated Fat": "monounsaturated_fat",
        "Trans Fat": "trans_fat",
        "Cholesterol": "cholesterol",
        "Sodium (mg)": "sodium_mg",
        "Potassium": "potassium",
        "Carbohydrates (g)": "carbohydrates_g",
        "Fiber": "fiber",
        "Sugar": "sugar",
        "Protein (g)": "protein_g",
        "Vitamin A": "vitamin_a",
        "Vitamin C": "vitamin_c",
        "Calcium": "calcium",
        "Iron": "iron",
        "Note": "note"
    }

    inserted_count = 0
    skipped_count = 0

    for row in reader:
        record = {}
        for key, value in row.items():
            field = HEADER_MAP.get(key)
            if not field:
                continue
            if value in (None, "", "null"):
                record[field] = None
            elif field in ("date", "meal", "time", "note"):
                record[field] = value
            else:
                try:
                    record[field] = float(value)
                except ValueError:
                    record[field] = None

        # Check for duplicates by date + meal + time
        if record.get("date") and record.get("meal") and record.get("time"):
            existing = supabase.table("meals").select("id").eq("date", record["date"]).eq("meal", record["meal"]).eq("time", record["time"]).execute()
            if existing.data:
                skipped_count += 1
                continue
            supabase.table("meals").insert(record).execute()
            inserted_count += 1

    st.sidebar.success(f"✅ {inserted_count} new meals added. {skipped_count} duplicates skipped.")

# --- Fetch and Display Data ---
response = supabase.table("meals").select("*").order("date", desc=True).limit(100).execute()
data = response.data

if not data:
    st.warning("No meals found. Please upload data.")
else:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["calories"] = pd.to_numeric(df["calories"], errors="coerce")
    df["protein_g"] = pd.to_numeric(df["protein_g"], errors="coerce")

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    start_date = st.sidebar.date_input("Start Date", df["date"].min())
    end_date = st.sidebar.date_input("End Date", df["date"].max())
    meal_types = st.sidebar.multiselect("Meal Types", options=df["meal"].unique(), default=df["meal"].unique())

    filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) &
                     (df["date"] <= pd.to_datetime(end_date)) &
                     (df["meal"].isin(meal_types))]

    # Show filters summary
    st.markdown(f"Showing meals from **{start_date}** to **{end_date}** filtered by: {', '.join(meal_types)}")

    # Metrics
    total_calories = filtered_df["calories"].sum()
    avg_protein = filtered_df["protein_g"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Total Calories", f"{total_calories:.0f} kcal")
    col2.metric("Avg Protein", f"{avg_protein:.1f} g")

    # Chart: Calories Over Time
    chart_data = filtered_df.groupby("date")["calories"].sum().reset_index().sort_values("date")
    st.subheader("📈 Calories Over Time")
    st.line_chart(chart_data.set_index("date"))

    # Chart: Protein Over Time
    protein_data = filtered_df.groupby("date")["protein_g"].sum().reset_index().sort_values("date")
    st.subheader("🥩 Protein Over Time")
    st.line_chart(protein_data.set_index("date"))

    # Chart: Meal Type Breakdown
    meal_counts = filtered_df["meal"].value_counts()
    st.subheader("🍽️ Meal Type Breakdown")
    st.bar_chart(meal_counts)

    # Show Table
    st.dataframe(filtered_df.sort_values("date", ascending=False), use_container_width=True)
