import streamlit as st

if 'my_button' not in st.session_state:
    st.session_state.my_button = True
    # Streamlit will raise an Exception on trying to set the state of button

st.button('Submit', key='my_button')