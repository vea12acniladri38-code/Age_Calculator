from datetime import date
from dateutil.relativedelta import relativedelta
from google import genai
import streamlit as st
import random

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Age Calculator",
    page_icon="🎂",
    layout="centered"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#667eea,#764ba2);
}

h1,h2,h3,p,label{
color:white;
}

div[data-testid="stMetric"]{
background:rgba(255,255,255,0.15);
padding:15px;
border-radius:15px;
text-align:center;
}

.block-container{
padding-top:2rem;
}

.footer{
text-align:center;
color:white;
font-size:14px;
margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI ---------------- #

api_key = st.secrets["GOOGLE_API_KEY"]

client = genai.Client(api_key=api_key)

# ---------------- TITLE ---------------- #

st.title("🎂 AI Age Calculator")
st.write("Find your age and receive AI-powered motivation!")

# ---------------- QUOTES ---------------- #

quotes = [
    "🌟 Believe in yourself.",
    "🚀 Every day is a new opportunity.",
    "💪 Consistency beats talent.",
    "🎯 Stay focused on your goals.",
    "🔥 Success starts with discipline.",
    "🌈 Dream big and work hard.",
    "✨ Great things take time.",
    "🏆 Never stop learning."
]

st.info(random.choice(quotes))

# ---------------- INPUT ---------------- #

birth_date = st.date_input(
    "📅 Select Your Birth Date",
    min_value=date(1900,1,1),
    max_value=date.today()
)

# ---------------- BUTTON ---------------- #

if st.button("🚀 Calculate Age & Get Motivation"):

    with st.spinner("🤖 AI is preparing your motivation..."):

        today = date.today()

        diff = relativedelta(today, birth_date)

        years = diff.years
        months = diff.months
        days = diff.days

        st.balloons()

        st.success("🎉 Age Calculated Successfully!")

        col1,col2,col3 = st.columns(3)

        col1.metric("🎂 Years", years)
        col2.metric("📅 Months", months)
        col3.metric("📆 Days", days)

        # ---------------- LIFE PERCENTAGE ---------------- #

        st.divider()

        st.subheader("🌍 Life Journey")

        life_expectancy = 80

        life_percentage = (years / life_expectancy) * 100

        if life_percentage > 100:
            life_percentage = 100

        st.progress(life_percentage/100)

        st.metric(
            "Life Completed",
            f"{life_percentage:.1f}%"
        )

        st.metric(
            "Approx. Remaining",
            f"{100-life_percentage:.1f}%"
        )

        if life_percentage < 25:
            st.success("🌱 You're just getting started. Learn as much as possible!")

        elif life_percentage < 50:
            st.info("🚀 Build your career, develop new skills, and chase your dreams!")

        elif life_percentage < 75:
            st.warning("⭐ Keep growing and inspire those around you!")

        else:
            st.error("❤️ Every day is precious. Live fully and cherish each moment!")

        # ---------------- AI PROMPT ---------------- #

        prompt = f"""
You are a friendly AI life coach.

The user is:

Age: {years} years
Months: {months}
Days: {days}

Write an inspiring motivational message.

Rules:

- Maximum 180 words.
- Be positive.
- Mention their age.
- Give career advice.
- Give health advice.
- Give one inspiring quote.
- End with one action they should take today.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        st.divider()

        st.subheader("🤖 Your AI Motivation")

        st.markdown(
            f"""
<div style="
background:orange;
padding:20px;
border-radius:15px;
color:black;
font-size:18px;
line-height:1.7;
">

{response.text}

</div>
""",
            unsafe_allow_html=True
        )

st.markdown(
"""
<div class="footer">

❤️ Made with Streamlit + Gemini AI

</div>
""",
unsafe_allow_html=True
)
