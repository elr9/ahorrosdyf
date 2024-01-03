import streamlit as st
from supabase import create_client
import pandas as pd
import random

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

available_amounts = set(range(1, 366))

def save_day(day, amount):
    date = f"2024-{(day - 1) // 30 + 1:02d}-{(day - 1) % 30 + 1:02d}"
    supabase.table("ahorrosdyf").insert({"day": date, "amount": amount}).execute()

def get_all_savings():
    return supabase.table("ahorrosdyf").select("*").order("day").execute().data

st.title('Daily Savings Tracker')

if st.button('Save for Next Day'):
    next_day = len(get_all_savings()) + 1
    if next_day <= 365 and available_amounts:
        amount_to_save = available_amounts.pop()
        save_day(next_day, amount_to_save)
        st.success(f'Saved ${amount_to_save} for Day {next_day}')
    else:
        st.error("All days have been assigned or the year is complete!")

savings_data = get_all_savings()
if savings_data:
    df = pd.DataFrame(savings_data)
    st.write("Your Savings Plan:")
    st.table(df)
