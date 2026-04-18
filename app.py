import streamlit as st
import requests
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
}
h1 {
    color: #00ffe5;
    text-align: center;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.1);
    box-shadow: 0 0 15px rgba(0,255,255,0.5);
    margin-bottom: 20px;
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 IPMAT AI PREP PRO</h1>", unsafe_allow_html=True)

# ---------- HUGGING FACE API ----------
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

def hf_query(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    try:
        return response.json()[0]["generated_text"]
    except:
        return "⚠️ Model loading... please try again in a few seconds."

# ---------- MENU ----------
menu = st.radio(
    "",
    ["🏠 Home", "📘 Vocabulary", "📖 RC Generator", "🔒 RC Test", "➗ Math Solver", "🤖 AI Mentor"]
)

# ---------- HOME ----------
if menu == "🏠 Home":
    st.markdown('<div class="card">Welcome to your premium AI-powered IPMAT prep platform 💎</div>', unsafe_allow_html=True)

# ---------- VOCAB ----------
elif menu == "📘 Vocabulary":
    st.markdown('<div class="card"><h3>📘 Daily 10 Words</h3></div>', unsafe_allow_html=True)

    words = [
        ("Aberration","deviation"),
        ("Capitulate","surrender"),
        ("Enigma","mystery"),
        ("Ubiquitous","present everywhere"),
        ("Pragmatic","practical"),
        ("Ephemeral","short-lived"),
        ("Tenacious","persistent"),
        ("Zealous","enthusiastic"),
        ("Obfuscate","confuse"),
        ("Alacrity","eagerness")
    ]

    for word, meaning in words:
        st.write(f"**{word}** - {meaning}")

# ---------- RC ----------
elif menu == "📖 RC Generator":
    st.markdown('<div class="card"><h3>📖 AI RC Generator</h3></div>', unsafe_allow_html=True)

    topic = st.text_input("Enter Topic (e.g. Economy, Climate)")

    if st.button("Generate RC"):
        prompt = f"""
        Write a high-quality IPMAT level reading comprehension passage.

        Requirements:
        - 3 paragraphs
        - Each paragraph 6-8 lines
        - Formal tone
        - Topic: {topic}
        """
        st.write(hf_query(prompt))

# ---------- PAYMENT ----------
elif menu == "🔒 RC Test":
    st.markdown('<div class="card"><h3>🔒 Premium RC Test</h3></div>', unsafe_allow_html=True)

    st.write("💳 Pay ₹10 to unlock")
    st.markdown("[👉 Pay Now](https://rzp.io/l/demo)")

    if st.button("I Paid"):
        st.success("Unlocked (Demo)")

# ---------- MATH ----------
elif menu == "➗ Math Solver":
    st.markdown('<div class="card"><h3>➗ AI Math Solver</h3></div>', unsafe_allow_html=True)

    question = st.text_input("Enter math problem")

    if st.button("Solve"):
        prompt = f"Solve this step by step clearly:\n{question}"
        st.write(hf_query(prompt))

    st.subheader("📷 Upload Image")
    file = st.file_uploader("Upload math image", type=["png", "jpg", "jpeg"])

    if file:
        img = Image.open(file)
        st.image(img)

# ---------- AI ----------
elif menu == "🤖 AI Mentor":
    st.markdown('<div class="card"><h3>🤖 AI Mentor</h3></div>', unsafe_allow_html=True)

    user_q = st.text_input("Ask your doubt")

    if st.button("Ask AI"):
        prompt = f"You are an expert tutor. Explain clearly with examples:\n{user_q}"
        st.write(hf_query(prompt))
