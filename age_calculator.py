from datetime import date
import streamlit as st
from google import genai

st.markdown("""
<style>
.stApp {
    background-color: Coral;
}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets["GOOGLE_API_KEY"]

client = genai.Client(api_key=api_key)

st.title("Age Calculator With Motivation Tips")

year = st.number_input("Enter Birth Year:", min_value=1900, max_value=2100, step=1)
month = st.number_input("Enter Birth Month:", min_value=1, max_value=12, step=1)
day = st.number_input("Enter Birth Day:", min_value=1, max_value=31, step=1)

if st.button("Calculate Age & Get Motivation"):
   with st.spinner("Loading your motivation"):

    birth_date = date(int(year), int(month), int(day))
    today = date.today()

    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    st.success(f"Your age is {age} years")

    prompt = f"""
    Act like a AI Motivator and analyse the age & comment less than 200 words regarding what motivation should take in year is{year} and month {month}, and day is {day} age is {age}. "

    Give me motivational advice in less than 200 words.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    st.subheader("Motivation")
    st.write(response.text)