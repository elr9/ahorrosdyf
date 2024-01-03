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

if st.button('El día de hoy ahorraremos:'):
    next_day = len(get_all_savings()) + 1
    if next_day <= 365 and available_amounts:
        amount_to_save = random.choice(list(available_amounts))
        available_amounts.remove(amount_to_save)
        save_day(next_day, amount_to_save)
        st.success(f'Ahorraremos: ${amount_to_save} y es el día: {next_day}')
    else:
        st.error("Todos los días se han asignado, ¡el año está completo!")

if st.button('Me equivoqué! Quita un día'):
    last_entry = supabase.table("ahorrosdyf").select("*").order("day", desc=True).limit(1).execute().data
    if last_entry:
        last_entry_id = last_entry[0]['id']
        supabase.table("ahorrosdyf").delete().eq('id', last_entry_id).execute()
        st.success('El último día se eliminó con éxito!')
    else:
        st.error('Nada que borrar.')

savings_data = get_all_savings()
if savings_data:
    df = pd.DataFrame(savings_data)[['day', 'amount']]
    df.columns = ['Día', 'Ahorro']  # Rename columns for display
    st.write("Así vamos:")
    html = df.to_html(index=False)
    st.markdown(html, unsafe_allow_html=True)

    # Calculate the total and display it
    total_saved = df['Ahorro'].sum()
    st.markdown(f"Llevamos ahorrado: **${total_saved:,}**")

