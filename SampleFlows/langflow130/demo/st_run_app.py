import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Stock Research Assistant", layout="wide")

st.title("Stock Market Research Assistant")

# Embed Langflow chat component
chat_html = """
<script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.7/dist/build/static/js/bundle.min.js"></script>
<langflow-chat
    window_title="Market News"
    flow_id="09072bb7-b3fb-4650-8d36-f4d58794dd1b"
    host_url="http://localhost:7880">
</langflow-chat>
"""

# Display the chat interface
html(chat_html, height=800)

# Add some context
st.markdown("""
## How to use:
1. Type your stock research question in the chat
2. Get AI-powered insights and analysis
3. Ask follow-up questions for deeper understanding
""")
