import streamlit as st
from supabase import create_client, Client
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

def save_day(day, amount):
    # Assuming 'day' is a number from 1 to 365
    date = f"2024-{(day - 1) // 30 + 1:02}-{(day - 1) % 30 + 1:02}"  # Simplified month-day calculation
    data = {"day": date, "amount": amount}
    supabase.table("ahorrosdyf").insert(data).execute()
    next_day = len(get_all_savings()) + 1
    amount_to_save = get_unique_amount()
    save_day(next_day, amount_to_save)

def get_unique_amount():
    if len(used_amounts) < 365:
        amount = random.randint(1, 365)
        while amount in used_amounts:
            amount = random.randint(1, 365)
        used_amounts.add(amount)
        return amount
    else:
        raise Exception("No more unique amounts available.")

@st.cache_data(ttl=600)
def get_all_savings():
    # Fetch all savings data
    data = supabase.table("ahorrosdyf").select("*").order("day").execute()
    return data.data if data.data else []

# Your Streamlit app logic here
st.title('Daily Savings Tracker')

# Button to save amount for the next day
next_day = len(get_all_savings()) + 1  # Assuming days are sequential and start from 1
amount_to_save = st.number_input(f'Enter the amount to save for Day {next_day}', min_value=1, max_value=365, value=1)

if st.button(f'Save for Day {next_day}'):
    save_day(next_day, amount_to_save)
    st.success(f'Saved ${amount_to_save} for Day {next_day}')

# Display the table of savings
savings_data = get_all_savings()
if savings_data:
    df = pd.DataFrame(savings_data)
    st.write("Your Savings Plan:")
    st.table(df[['day', 'amount']])
else:
    st.write("No savings data found.")
