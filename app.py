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

def save_day(day, amount):
    date = f"2024-{(day - 1) // 30 + 1:02d}-{(day - 1) % 30 + 1:02d}"
    supabase.table("ahorrosdyf").insert({"day": date, "amount": amount}).execute()

def get_all_savings():
    return supabase.table("ahorrosdyf").select("*").order("day").execute().data

# Initialize available amounts
all_amounts = set(range(1, 366))
used_amounts = {x['amount'] for x in get_all_savings()}
available_amounts = all_amounts - used_amounts

st.title('Ahorros Súper Poderosos de Diego y Fer')

if st.button('Dame la cantidad a ahorrar'):
    next_day = len(get_all_savings()) + 1
    if next_day <= 365 and available_amounts:
        amount_to_save = random.choice(list(available_amounts))
        available_amounts.remove(amount_to_save)
        save_day(next_day, amount_to_save)
        st.success(f'Ahorraremos ${amount_to_save} el día: {next_day}')
    else:
        st.error("Todos los días se han asignado, ¡el año está completo!")

savings_data = get_all_savings()
if savings_data:
    df = pd.DataFrame(savings_data)[['day', 'amount']]
    st.write("Así va el plan:")
    st.table(df)
