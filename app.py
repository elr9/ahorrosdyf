import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# Function to generate savings amounts
def generate_savings():
    amounts = list(range(1, 366))
    random.shuffle(amounts)
    return amounts

# Initialize session state for amounts and current day
if 'amounts' not in st.session_state or not st.session_state.amounts:
    st.session_state.amounts = generate_savings()

if 'current_day' not in st.session_state:
    st.session_state.current_day = 1

# Load the custom component
def load_component():
    component = components.html(open("my_component.html").read(), height=100)
    return component

# Display the custom component and interact with it
data_from_storage = load_component()

# Update local session state with data from LocalStorage if it exists
if data_from_storage:
    st.session_state.amounts, st.session_state.current_day = data_from_storage

# App title
st.title('Daily Savings App')

# Button to generate amount for the next day
if st.button('Save for Next Day'):
    if st.session_state.current_day <= 365:
        st.session_state.current_day += 1
        # Save the updated state to LocalStorage via the custom component
        components.html(f"""
            <script>
            window.parent.postMessage({{
                type: 'streamlit:saveData',
                value: [{st.session_state.amounts}, {st.session_state.current_day}]
            }}, '*');
            </script>
        """, height=0)
    else:
        st.warning('You have completed the savings for the year!')

# Display the amount for the current day
if st.session_state.current_day <= 365:
    st.write(f'Day {st.session_state.current_day}: Save ${st.session_state.amounts[st.session_state.current_day - 1]}')
else:
    st.write('No more savings days left this year.')

# Creating a table to display the savings plan
data = {'Day': list(range(1, st.session_state.current_day + 1)),
        'Amount to Save': st.session_state.amounts[:st.session_state.current_day]}

df = pd.DataFrame(data)

# Display the table in the app
st.table(df)
