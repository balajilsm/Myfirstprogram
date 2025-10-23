import streamlit as st
import pandas as pd

# --- Page Title ---
st.title("🎉 My Second Streamlit App")
st.write("This app shows how to collect user inputs and display results interactively.")

# --- User Inputs ---
st.header("👤 Enter Your Details")

name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=120)
color = st.selectbox("Pick your favorite color:", ["Red", "Green", "Blue", "Yellow", "Purple"])

# --- Display Results ---
if st.button("Show My Info"):
    st.success(f"Hi **{name}**, you are **{age}** years old and your favorite color is **{color}** 🎨")

    # Add some conditional logic
    if age < 18:
        st.warning("⚠️ You are still a minor.")
    elif 18 <= age < 60:
        st.info("💪 You are an adult — keep learning and exploring!")
    else:
        st.success("🎯 You are wise and experienced!")

# --- CSV Upload Section ---
st.header("📂 Upload a CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Preview:")
    st.dataframe(df)

    st.subheader("📈 Summary Statistics:")
    st.write(df.describe())

# --- Footer ---
st.caption("Made with ❤️ using Streamlit")

if uploaded_file is not None:
    st.subheader("📈 Data Chart Example")
    column = st.selectbox("Select a numeric column to plot:", df.select_dtypes('number').columns)
    fig, ax = plt.subplots()
    ax.hist(df[column], bins=20)
    st.pyplot(fig)
