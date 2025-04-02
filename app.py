import streamlit as st

import google.generativeai as genai
from google.generativeai import types
import re

genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel('models/gemini-2.0-flash')
st.title("🎥 Video Search with Multimodal RAG")
yturl = st.text_input("Enter the youtube URL:")
query = st.text_input("Enter the query:")
if st.button("Search"):
    prompt = f"Given the URL of the youtube video: {yturl}, and the query: {query}, find the best timestamp. Return the Video ID and start timestamp in the following format if required, along with your answer to the query: Video ID: [Video ID], Start Timestamp: [Timestamp]"
    response = model.generate_content(prompt)
    with st.spinner("Searching the video..."):
        st.subheader("LLM Response")
        st.write(response.text)

        # Regular expressions to find video ID and timestamp
        video_id_match = re.search(r"video ID:\s*([a-zA-Z0-9_-]+)", response.text, re.IGNORECASE)
        timestamp_match = re.search(r"start timestamp:\s*(\d+)", response.text, re.IGNORECASE)
        video_id = video_id_match.group(1) if video_id_match else None
        start_timestamp = int(timestamp_match.group(1)) if timestamp_match else None
        if(video_id_match is None or timestamp_match is None):
            st.error("Could not find video ID or start timestamp in the response.")
        else:
            # Construct the embed URL with start time
            youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?start={start_timestamp}&autoplay=0"
            st.write(youtube_embed_url)
            # Embed the video
            st.components.v1.iframe(youtube_embed_url, width=700, height=400)
        
