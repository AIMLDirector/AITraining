import streamlit as st

st.header("Hello, Streamlit!")
user_input = st.chat_input("Type your message...")

if user_input:
    st.write(f"You entered: {user_input}")




with st.sidebar:
    col1, col2 = st.columns(2)

    with col1:
        temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1, help="Higher = more creative, Lower = more deterministic")

        context_size = st.slider("Context Size", min_value=512, max_value=8192, value=2048, step=512, help="Maximum context window size")

    with col2:
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=4096, value=500, step=10, help="Maximum tokens to generate")

        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.05, help="Nucleus sampling parameter")

    st.write(f"Temperature: {temp}, Context Size: {context_size}, Max Tokens: {max_tokens}, Top P: {top_p}")    