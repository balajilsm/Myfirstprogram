import streamlit as st

# Title for your web app
st.title("👋 My First Streamlit App")

# Create a text input box
name = st.text_input("Enter your name:")

# Create a button
if st.button("Submit"):
    # When the button is clicked, show this message
    st.success(f"Hello, {name}! Welcome to Streamlit 🎉")
