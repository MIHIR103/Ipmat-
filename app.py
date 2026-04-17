import streamlit as st
import time
from PIL import Image
import openai
import razorpay

# ---------- PAGE CONFIG & UI ANIMATIONS ----------
st.set_page_config(page_title="IPMAT AI Prep", layout="wide", page_icon="🚀")

st.markdown('''
<style>
    /* Fade-in animation for the main container */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        animation: fadeIn 0.8s ease-in-out;
    }
    /* Stylish Title */
    .title-text {
        text-align: center;
        background: linear-gradient(90deg, #4b6cb7, #182848);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
    }
    /* Hover effects on buttons */
    .stButton>button {
        transition: all 0.3s ease;
        border-radius: 8px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }
</style>
''', unsafe_allow_html=True)

st.markdown("<div class='title-text'>🚀 IPMAT AI Prep</div>", unsafe_allow_html=True)

# ---------- SIDEBAR & CREDENTIALS ----------
st.sidebar.title("Navigation & Settings")
menu = st.sidebar.radio("Choose Section", ["Home", "Vocabulary", "RC", "RC Test 🔒", "Math Solver", "AI Mentor"])

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 API Settings")
st.sidebar.caption("Required for AI generation and Real Payments")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
razorpay_key_id = st.sidebar.text_input("Razorpay Key ID", type="password")
razorpay_key_secret = st.sidebar.text_input("Razorpay Key Secret", type="password")

# ---------- HOME ----------
if menu == "Home":
    st.write("### Welcome to the Premium IPMAT Prep Platform")
    st.write("Navigate through the sidebar to access Vocabulary, Reading Comprehension, Math Solvers, and your personal AI Mentor.")
    st.info("💡 **Tip:** Add your API keys in the sidebar to unlock the full power of this app!")

# ---------- VOCAB ----------
elif menu == "Vocabulary":
    st.subheader("📘 Daily 10 Words")
    words = [
        ("Aberration", "deviation from norm"), ("Capitulate", "to surrender"),
        ("Enigma", "mystery"), ("Ubiquitous", "present everywhere"),
        ("Pragmatic", "practical"), ("Ephemeral", "short-lived"),
        ("Tenacious", "persistent"), ("Zealous", "enthusiastic"),
        ("Obfuscate", "to confuse"), ("Alacrity", "eagerness")
    ]
    
    col1, col2 = st.columns(2)
    for i, w in enumerate(words):
        if i % 2 == 0:
            col1.success(f"**{w[0]}**: {w[1]}")
        else:
            col2.info(f"**{w[0]}**: {w[1]}")

# ---------- RC ----------
elif menu == "RC":
    st.subheader("📖 RC Practice (IPMAT Level)")

    # AI RC Generation
    st.write("### ✨ Want fresh content?")
    if st.button("Generate AI RC Passage"):
        if openai_api_key:
            with st.spinner("Generating an IPMAT-level passage..."):
                try:
                    client = openai.OpenAI(api_key=openai_api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Write a 3-paragraph Reading Comprehension passage suitable for the IPMAT exam, followed by one multiple-choice question with 4 options, and clearly state the correct answer at the end."}]
                    )
                    st.success("Generated Successfully!")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"OpenAI Error: {e}")
        else:
            st.warning("Please provide your OpenAI API Key in the sidebar to generate new RCs.")
            
    st.markdown("---")
    st.write("### 📚 Static Practice")
    start = st.button("⏱ Start RC Timer")
    if start:
        timer_placeholder = st.empty()
        for seconds in range(60, 0, -1):
            timer_placeholder.write(f"⏱ **Time remaining:** {seconds} sec")
            time.sleep(1)
        timer_placeholder.write("⏱ **Time's up!**")

    st.write('''
    **Paragraph 1:** Economic inequality has been a persistent issue across both developed and developing nations. While economic growth often increases national income, it does not always ensure equitable distribution.
    
    **Paragraph 2:** Governments attempt to correct this imbalance through policies such as progressive taxation, subsidies, and welfare programs. However, these interventions sometimes create inefficiencies.
    
    **Paragraph 3:** Therefore, achieving a balance between economic efficiency and social equity remains a major challenge for policymakers worldwide.
    ''')

    ans = st.radio("Main idea?", ["Inequality problem", "Sports growth", "Technology boom"])
    if st.button("Submit Answer"):
        if ans == "Inequality problem":
            st.success("Correct ✅")
            st.balloons()
        else:
            st.error("Wrong ❌")

# ---------- RC TEST (RAZORPAY) ----------
elif menu == "RC Test 🔒":
    st.subheader("🔒 Premium RC Test")
    st.write("Unlock the advanced IPMAT mock test by paying ₹10.")

    if st.button("💳 Generate Razorpay Payment Link"):
        if razorpay_key_id and razorpay_key_secret:
            try:
                client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
                data = {
                    "amount": 1000,  # amount in paise (1000 paise = 10 INR)
                    "currency": "INR",
                    "description": "Unlock Premium RC Test",
                    "customer": {
                        "name": "IPMAT Student",
                        "email": "student@example.com"
                    },
                    "notify": {"sms": False, "email": False},
                    "reminder_enable": False
                }
                # Create payment link
                payment_link = client.payment_link.create(data)
                
                st.success("Payment Link Generated Successfully!")
                st.markdown(f"### [🔗 Click Here to Pay ₹10 via Razorpay]({payment_link['short_url']})")
                st.info("Once the payment is completed, the real tests will unlock here.")
                
            except Exception as e:
                st.error(f"Razorpay Error: Verify your keys. Error details: {e}")
        else:
            st.warning("⚠️ Please provide your Razorpay Key ID and Secret in the sidebar.")

# ---------- MATH ----------
elif menu == "Math Solver":
    st.subheader("➗ Math Solver")
    q = st.text_input("Enter your math question:")
    
    if st.button("Solve with AI"):
        if openai_api_key and q:
            with st.spinner("Calculating step-by-step solution..."):
                try:
                    client = openai.OpenAI(api_key=openai_api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "You are a helpful math tutor. Provide a step-by-step solution."},
                                  {"role": "user", "content": q}]
                    )
                    st.success("Solution:")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
        elif not openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API Key in the sidebar.")
        else:
            st.warning("Please enter a question.")

    st.markdown("---")
    st.subheader("📷 Upload Question Image")
    file = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="Uploaded Image", use_container_width=True)

# ---------- AI MENTOR ----------
elif menu == "AI Mentor":
    st.subheader("🤖 Chat with Your AI Mentor")
    
    # Setup Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask your IPMAT doubt here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if openai_api_key:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    client = openai.OpenAI(api_key=openai_api_key)
                    for response in client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "You are an expert IPMAT prep mentor. Be encouraging, precise, and helpful."}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                        stream=True,
                    ):
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Error: {e}")
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.warning("⚠️ Please provide your OpenAI API Key in the sidebar to talk to the mentor.")
