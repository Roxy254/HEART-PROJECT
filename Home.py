

import streamlit as st


def home():
# CSS styles for custom colors and image layout
st.markdown("""
<style>
    /* Center header with teal color */
    .header {
        text-align: center;
        color: #008080;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 0.1em;
    }
    /* Subtitle under header */
    .subheader {
        text-align: center;
        color: #004d4d;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-top: 0;
        margin-bottom: 2em;
        font-size: 20px;
        font-style: italic;
    }
    /* Image styling */
    .banner-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 90%;
        max-width: 900px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 0.5em;
    }
    /* Verse styling */
    .verse {
        text-align: center;
        color: #006666;
        font-family: 'Georgia', serif;
        font-size: 18px;
        font-weight: 500;
        margin-top: 0;
        margin-bottom: 3em;
    }
</style>
""", unsafe_allow_html=True)

# Header text
st.markdown('<h1 class="header">💖 Welcome to the H.E.A.R.T. Project App</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Use the sidebar to navigate through different pages.</p>', unsafe_allow_html=True)

# Image banner
st.image(
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80",
    use_column_width=False,
    output_format="auto",
    clamp=True,
    caption=""
)

# Verse below the image that captures the H.E.A.R.T message
st.markdown('''
<p class="verse">
    “I have loved you with an everlasting love; <br>
    therefore I have continued my faithfulness to you.” <br>
    — Jeremiah 31:3 (NIV)
</p>
''', unsafe_allow_html=True)
