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

st.set_page_config(page_title="My Smart Streamlit App", page_icon="🤖")

# -----------------------------
# Simple "AI" logic (rule-based)
# -----------------------------
def generate_profile(name: str, age: int, color: str):
    name = (name or "Friend").strip()
    # Age buckets
    if age < 18:
        stage = "Explorer"
        stage_trait = "curiosity"
        stage_tip = "experiment with many skills — coding, design, and writing."
    elif age < 30:
        stage = "Trailblazer"
        stage_trait = "energy"
        stage_tip = "build projects and share them — momentum is your friend."
    elif age < 45:
        stage = "Strategist"
        stage_trait = "focus"
        stage_tip = "prioritize high-leverage tasks and say no to the rest."
    elif age < 60:
        stage = "Mentor"
        stage_trait = "experience"
        stage_tip = "teach others — it multiplies your own impact."
    else:
        stage = "Sage"
        stage_trait = "wisdom"
        stage_tip = "simplify systems and document your playbooks."

    # Color vibes
    color = (color or "").lower()
    vibes = {
        "red": ("Bold", "You act fast and lead from the front."),
        "green": ("Balanced", "You value stability, growth, and steady progress."),
        "blue": ("Analytical", "You think clearly and communicate with calm logic."),
        "yellow": ("Optimistic", "You bring energy and positivity to teams."),
        "purple": ("Creative", "You connect dots and craft original ideas."),
    }
    vibe_title, vibe_desc = vibes.get(color, ("Adaptive", "You flex to what the moment needs."))

    # Little “signature”
    lucky_number = (sum(ord(c) for c in name) + age) % 9 + 1
    motto = {
        "Bold": "Decide. Act. Iterate.",
        "Balanced": "Grow a little every day.",
        "Analytical": "Measure twice, build once.",
        "Optimistic": "Light the room you enter.",
        "Creative": "Make things that make waves.",
        "Adaptive": "Flow around obstacles."
    }[vibe_title]

    profile = {
        "title": f"{stage} • {vibe_title}",
        "summary": f"{name}, you combine {stage_trait} with a {vibe_title.lower()} style.",
        "vibe_desc": vibe_desc,
        "tip": f"Tip: {stage_tip}",
        "lucky_number": lucky_number,
        "motto": motto
    }
    return profile

# -----------------------------
# UI
# -----------------------------
st.title("🤖 Mini AI Profile")
st.caption("Enter your details and get a playful personality profile.")

with st.container():
    st.subheader("👤 Your Inputs")
    col1, col2, col3 = st.columns([2,1,2])
    with col1:
        name = st.text_input("Name", value="")
    with col2:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
    with col3:
        color = st.selectbox("Favorite color", ["Red", "Green", "Blue", "Yellow", "Purple"])

    if st.button("Generate My Profile ✨", use_container_width=True):
        profile = generate_profile(name, int(age), color)
        st.balloons()
        st.success("Profile created!")

        st.subheader("🧠 Your Personality Snapshot")
        st.markdown(f"### **{profile['title']}**")
        st.write(profile["summary"])
        st.info(profile["vibe_desc"])
        st.markdown(f"**{profile['tip']}**")
        st.metric("🎲 Lucky Number", profile["lucky_number"])
        st.code(profile["motto"], language="text")

# Optional: keep your CSV demo from earlier
st.divider()
st.subheader("📂 (Optional) Upload a CSV to Preview Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    st.caption("Tip: Try adding charts next!")

st.caption("Built with ❤️ in Streamlit — no external AI services needed.")
