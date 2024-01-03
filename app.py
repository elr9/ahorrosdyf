import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

def save_day(day, amount):
    data = {"day": day, "amount": amount}
    # Insert the data for the given day
    supabase.table("ahorrosdyf").insert(data).execute()

def get_all_savings():
    # Fetch all savings data
    data = supabase.table("ahorrosdyf").select("*").order("day", True).execute()
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
