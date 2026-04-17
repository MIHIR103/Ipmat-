import streamlit as st
import random

st.set_page_config(layout="wide")
st.title("🚀 IPMAT AI Prep Platform")

menu = st.sidebar.radio("Menu", ["Home", "Vocabulary", "RC", "RC Test 🔒", "Math Solver"])

if menu == "Home":
    st.write("Welcome to your AI IPMAT prep system!")

elif menu == "Vocabulary":
    words = [
        ("Aberration", "a departure from what is normal"),
        ("Capitulate", "to surrender"),
        ("Enigma", "something mysterious"),
        ("Ubiquitous", "present everywhere"),
        ("Pragmatic", "practical approach"),
        ("Alacrity", "eagerness"),
        ("Ephemeral", "short-lived"),
        ("Obfuscate", "to make unclear"),
        ("Tenacious", "persistent"),
        ("Zealous", "enthusiastic")
    ]

    st.subheader("📘 Daily Words")
    for w in random.sample(words, 5):
        st.write(f"**{w[0]}** - {w[1]}")

elif menu == "RC":
    st.subheader("📖 Daily RC")

    st.write("""
    Climate change is one of the most pressing issues of our time. Governments,
    organizations, and individuals must take responsibility...
    """)

    q = st.radio("Main idea?", ["Climate issue", "Sports", "Technology"])
    if st.button("Submit"):
        st.success("Answer submitted!")

elif menu == "RC Test 🔒":
    st.warning("🔒 Pay ₹10 to unlock (Demo Mode)")

    if st.button("I Paid"):
        st.success("Unlocked!")

elif menu == "Math Solver":
    st.subheader("➗ Solve Math")

    q = st.text_input("Enter question")

    if st.button("Solve"):
        st.write("Step-by-step solution will appear here (AI coming soon)")
