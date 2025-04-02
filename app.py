import streamlit as st
import requests

st.title("🤖 Chat with Mistral-7B (via Hugging Face)")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_TOKEN = st.secrets["HF_TOKEN"]

def query(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if user_input:
    full_prompt = "\n".join([f"User: {u}\nBot: {b}" for u, b in st.session_state.chat_history])
    full_prompt += f"\nUser: {user_input}\nBot:"

    output = query({
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    })

    response = output[0]["generated_text"].split("Bot:")[-1].strip()
    st.session_state.chat_history.append((user_input, response))
    st.markdown(f"**Bot:** {response}")
