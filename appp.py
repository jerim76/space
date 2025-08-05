```python
import streamlit as st
from datetime import datetime
import re
import base64
import pandas as pd

# Custom CSS with local fallback for background image
background_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="  # Placeholder tiny transparent image
st.markdown(f"""
<style>
    :root {{
        --primary: #26A69A;
        --accent: #FF6F61;
        --light: #e6f3f5;
        --dark: #2c3e50;
        --deep-blue: #1E3A8A;
    }}
    .stApp {{
        background-color: var(--light);
        background-image: url('{background_image}');
        font-family: 'Arial', sans-serif;
        color: var(--dark);
        min-height: 100vh;
        width: 100%;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    h1, h2, h3, h4 {{
        color: var(--deep-blue) !important;
    }}
    h1 {{ font-size: 2.2rem; }}
    h2 {{ font-size: 1.8rem; }}
    h3 {{ font-size: 1.4rem; }}
    h4 {{ font-size: 1.2rem; }}
    .service-card, .testimonial-card, .event-card, .partnership-card, .blog-card, .tracker-card, .volunteer-card, .founder-card {{
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }}
    .primary-btn {{
        background: var(--primary);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        font-size: 0.9rem;
    }}
    .stButton > button {{
        background: var(--primary);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }}
    .st-expander {{
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background: #f9f9f9;
        margin-bottom: 0.5rem;
    }}
    .footer {{
        text-align: center;
        padding: 1rem;
        background: #e8f4f8;
        border-top: 1px solid #ddd;
        margin-top: 1rem;
    }}
    @media (max-width: 768px) {{
        h1 {{ font-size: 1.6rem; }}
        h2 {{ font-size: 1.4rem; }}
        h3 {{ font-size: 1.2rem; }}
        h4 {{ font-size: 1.0rem; }}
    }}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="SafeSpace Organisation",
    page_icon="🧠",
    layout="wide",
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "outreach_form_data" not in st.session_state:
    st.session_state.outreach_form_data = {"name": "", "email": "", "phone": "", "experience": "", "role": "Any"}
if "partnership_form_data" not in st.session_state:
    st.session_state.partnership_form_data = {"name": "", "organization": "", "email": "", "phone": "", "type": "Partner"}
if "counseling_form_data" not in st.session_state:
    st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}

# Function to create download link
def get_download_link(file_content, file_name):
    b64 = base64.b64encode(file_content.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="primary-btn" style="display: block; text-align: center; margin-top: 0.5rem;">Download</a>'
    return href

# Function to export mood history
def export_mood_history():
    df = pd.DataFrame(st.session_state.mood_history, columns=["Date", "Mood", "Note"])
    df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x)
    csv = df.to_csv(index=False)
    return csv

# Chatbot knowledge base
knowledge_base = [
    {"question": r"what is safespace organisation\??", "answer": "SafeSpace Organisation is a non-profit providing mental health care since 2023."},
    {"question": r"what services do you offer\??", "answer": "We offer counseling and therapy services. Register at the Services section."},
    {"question": r"how can i contact you\??", "answer": "Contact us at +254 781 095 919 or info@safespaceorganisation.org."},
    {"question": r"what are your hours\??", "answer": "Mon-Fri 9 AM-5 PM, Sat 10 AM-2 PM."},
    {"question": r"how much does it cost\??", "answer": "Fees range from KSh 500-2,000 per session."},
    {"question": r"who are the founders\??", "answer": "Founded by Jerim Owino and Hamdi Roble."},
    {"question": r"what events are coming up\??", "answer": "Check the Events section for upcoming workshops."},
    {"question": r"how can i volunteer\??", "answer": "Register via the Volunteer form."},
    {"question": r"what is the crisis line\??", "answer": "Call +254 781 095 919 (8 AM-7 PM EAT)."},
    {"question": r"how can i partner with you\??", "answer": "Register through the Partnership form."},
    {"default": "I’m sorry, I didn’t understand. Ask about services, contact, hours, costs, founders, events, volunteering, crisis support, or partnerships. Time: 01:22 AM EAT, August 06, 2025."}
]

# Function to get chatbot response
def get_chatbot_response(query):
    query = query.lower()
    for entry in knowledge_base:
        if "question" in entry and re.search(entry["question"], query):
            return entry["answer"]
    return knowledge_base[-1]["default"]

# HEADER
st.markdown("""
<div style='text-align: center; padding: 0.8rem; background: var(--primary); color: white;'>
    <h1>SafeSpace Organisation</h1>
    <p>Empowering Minds Since 2023</p>
</div>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("<div id='hero'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 0.8rem; background: var(--primary); color: white;'>
    <h1>Healing Minds</h1>
    <p>SafeSpace offers confidential counseling for all.</p>
    <div style='display: flex; justify-content: center; gap: 0.5rem;'>
        <a href='#about' class='primary-btn'>About Us</a>
        <a href='#services' class='primary-btn'>Services</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ABOUT SECTION
st.markdown("<div id='about'></div>", unsafe_allow_html=True)
st.markdown("## About SafeSpace Organisation")
st.markdown("""
<div class='service-card'>
    <p>SafeSpace, founded in 2023, provides mental health care with 15 professionals across multiple regions.</p>
    <a href='#services' class='primary-btn'>Learn More</a>
</div>
""", unsafe_allow_html=True)

# SERVICES SECTION
st.markdown("<div id='services'></div>", unsafe_allow_html=True)
st.markdown("## Our Services")
services = [
    {"title": "Individual Counseling", "desc": "Personalized therapy sessions."},
    {"title": "Group Therapy", "desc": "Supportive group sessions."},
    {"title": "Online Counseling", "desc": "Virtual therapy options."}
]
for service in services:
    st.markdown(f"""
    <div class='service-card'>
        <h3>{service['title']}</h3>
        <p>{service['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
with st.form("counseling_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submit = st.form_submit_button("Register")
    if submit and all([name, email, phone]):
        st.session_state.counseling_form_data = {"name": name, "email": email, "phone": phone, "type": "Online"}
        st.success(f"Thank you, {name}! Registered at 01:22 AM EAT, August 06, 2025. Contact at {email}.")
        st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}

# TESTIMONIALS SECTION
st.markdown("<div id='testimonials'></div>", unsafe_allow_html=True)
st.markdown("## Testimonials")
st.markdown("""
<div class='testimonial-card'>
    <p><em>'Great support!'</em> - Jane K.</p>
</div>
""", unsafe_allow_html=True)

# EVENTS SECTION
st.markdown("<div id='events'></div>", unsafe_allow_html=True)
st.markdown("## Upcoming Events")
st.markdown("""
<div class='event-card'>
    <h4>Stress Management Workshop</h4>
    <p>August 10, 2025, Nairobi.</p>
</div>
""", unsafe_allow_html=True)

# PARTNERSHIPS SECTION
st.markdown("<div id='partnerships'></div>", unsafe_allow_html=True)
st.markdown("## Partnerships")
st.markdown("""
<div class='partnership-card'>
    <h4>Kenyatta National Hospital</h4>
    <p>Referrals since 2024.</p>
</div>
""", unsafe_allow_html=True)
with st.form("partnership_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submit = st.form_submit_button("Register")
    if submit and all([name, email, phone]):
        st.session_state.partnership_form_data = {"name": name, "email": email, "phone": phone, "type": "Partner"}
        st.success(f"Thank you, {name}! Registered at 01:22 AM EAT, August 06, 2025. Contact at {email}.")
        st.session_state.partnership_form_data = {"name": "", "email": "", "phone": "", "type": "Partner"}

# BLOG SECTION
st.markdown("<div id='blog'></div>", unsafe_allow_html=True)
st.markdown("## Blog")
st.markdown("""
<div class='blog-card'>
    <h4>Coping with Stress</h4>
    <p>July 20, 2025 - Tips by Dr. Amina.</p>
</div>
""", unsafe_allow_html=True)

# TRACKER SECTION
st.markdown("<div id='tracker'></div>", unsafe_allow_html=True)
st.markdown("## Mood Tracker")
mood = st.slider("Mood (1-5)", 1, 5, 3)
note = st.text_input("Note")
if st.button("Log"):
    st.session_state.mood_history.append({"Date": datetime.now(), "Mood": mood, "Note": note})
    st.success(f"Logged at 01:22 AM EAT, August 06, 2025!")
for entry in st.session_state.mood_history[-5:]:
    st.write(f"- {entry['Date'].strftime('%Y-%m-%d %H:%M')}: Mood {entry['Mood']}/5 {entry['Note']}")
if st.button("Export"):
    csv = export_mood_history()
    st.markdown(get_download_link(csv, "mood_history.csv"), unsafe_allow_html=True)

# VOLUNTEER SECTION
st.markdown("<div id='volunteer'></div>", unsafe_allow_html=True)
st.markdown("## Volunteer")
st.markdown("""
<div class='volunteer-card'>
    <h4>Outreach Support</h4>
    <p>2-4 hr campaigns.</p>
</div>
""", unsafe_allow_html=True)
with st.form("volunteer_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submit = st.form_submit_button("Register")
    if submit and all([name, email, phone]):
        st.session_state.outreach_form_data = {"name": name, "email": email, "phone": phone, "role": "Any"}
        st.success(f"Thank you, {name}! Registered at 01:22 AM EAT, August 06, 2025. Contact at {email}.")
        st.session_state.outreach_form_data = {"name": "", "email": "", "phone": "", "role": "Any"}

# CONTACT SECTION
st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
st.markdown("## Contact")
st.markdown("""
<div class='service-card'>
    <p>Greenhouse Plaza, Nairobi. Call +254 781 095 919 or email info@safespaceorganisation.org.</p>
</div>
""", unsafe_allow_html=True)

# CHATBOT (Simplified as static text)
st.markdown("## Chat with Us")
for message in st.session_state.chat_history:
    st.write(f"**{'You' if message[0] == 'user' else 'Bot'}:** {message[1]}")
query = st.text_input("Ask a question")
if st.button("Send"):
    response = get_chatbot_response(query)
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("bot", response))
    st.experimental_rerun()

# FOOTER
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>© 2023-2025 SafeSpace Organisation</p>
</div>
""", unsafe_allow_html=True)
```

### Additional Deployment Steps
- **Create `requirements.txt`**: Include `streamlit` and `pandas` to ensure dependencies are installed.
  ```
  streamlit>=1.22.0
  pandas>=1.5.0
  ```
- **Test Locally**: Run `streamlit run app.py` to verify functionality before deploying.
- **Deploy on Streamlit Community Cloud**: Upload the `app.py` and `requirements.txt` to a GitHub repository, then connect it to Streamlit Community Cloud.

This version should deploy successfully by avoiding common pitfalls while preserving the app's core functionality.
