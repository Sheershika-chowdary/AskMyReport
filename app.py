import streamlit as st
import pandas as pd
import openai

# Set your OpenAI key here or use environment variables
openai.api_key = "your_openai_api_key"

st.title("AskMyReport")
st.subheader("Rephrase. Simplify. Ask. All from your report.")

# 1. File Upload
uploaded_file = st.file_uploader("Upload your analysis (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded successfully!")
        st.write("**Preview:**", df.head())

        # 2. Get user summary (optional)
        user_summary = st.text_area("Paste your written analysis (optional)", "")

        # 3. Choose tone
        tone = st.selectbox("Choose your tone", ["Formal", "Bullet Points", "Casual"])

        # 4. Generate rephrased summary
        if st.button("Rephrase with AI"):
            prompt = f"Rephrase the following analysis in a {tone.lower()} tone:\n\n{user_summary}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_output = response.choices[0].message.content
            st.markdown("### AI Rephrased Summary")
            st.write(ai_output)

        # 5. Q&A
        question = st.text_input("Ask something about your report")
        if st.button("Ask AI"):
            combined = user_summary + "\n\nData:\n" + df.to_string()
            q_prompt = f"Based on this report, answer: {question}\n\n{combined}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": q_prompt}]
            )
            st.markdown("### AI Response")
            st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
