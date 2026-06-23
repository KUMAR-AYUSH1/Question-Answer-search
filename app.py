import streamlit as st
import requests

st.set_page_config(page_title="Question Answer Search", page_icon="🔍")

st.title("🔍 Question Answer Search")

API_URL = "http://localhost:8000/ask"

def get_answer(question):
    try:
        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching..."):
            result = get_answer(question)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Answer Found")
            st.write(result.get("answer", "No answer available"))