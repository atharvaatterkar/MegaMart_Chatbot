import streamlit as st
from .faq import faq_chain
from .sql import sql_chain
from .smalltalk import talk
from .router import router


st.set_page_config(page_title="MegaMart Bot", layout="centered")
st.title("🛍️ MegaMart Chatbot")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")



def ask(query):
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'small-talk':
        return talk(query)
    else:
        return f"Route {route} not implemented yet"



query = st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    if not api_key:
        response = "⚠️ Please enter your Groq API key in the sidebar."
    else:
        response = ask(query, api_key)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


