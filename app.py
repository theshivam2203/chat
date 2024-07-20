import streamlit as st
import requests
import json

# FastAPI endpoint URL
FASTAPI_URL = "http://124.123.78.136:6000/qa"

# Set up the page configuration
st.set_page_config(
    page_title="Chatbot",
    page_icon="💬",
    layout="wide",
)

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    .chat-container {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .chat-message {
        font-size: 1.1em;
        margin: 5px 0;
    }
    .user-message {
        text-align: right;
        color: blue;
    }
    .bot-message {
        text-align: left;
        color: green;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Input
st.title("Medical Chatbot")
st.subheader("Ask me anything about health!")

query = st.text_input("Enter your query", "What is Malaria")

if st.button("Send"):
    payload = {"query": query, "category": "health"}
    try:
        response = requests.post(FASTAPI_URL, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Parse the response
        data = response.json()
        result = data.get("response", {}).get("result", "No result found.")

        # Display the conversation
        st.markdown(f"""
        <div class="chat-container">
            <div class="chat-message user-message">
                <strong>You:</strong> {query}
            </div>
            <div class="chat-message bot-message">
                <strong>Bot:</strong> {result}
            </div>
        </div>
        """, unsafe_allow_html=True)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"An error occurred: {req_err}")
