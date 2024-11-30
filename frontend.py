'''
Author: Aayan Ahmad Khan

Date: 25.11.2024

INFO: An SAAS Website that Create Obisidian notes from youtube videos in insant using YScript. Its a youtube caption extracter which utilises AI to
create beautiful Obisian notes ina fabolous speed.
'''
#Location: C:\Users\amna_\OneDrive\Desktop\Streamlit_web

import streamlit as st
import time
import yt_dlp
from transformers import pipeline


def download_audio(youtube_url, output_path="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best', 
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',  
            'preferredcodec': 'mp3',  
            'preferredquality': '192',  
        }],
        'outtmpl': output_path, 
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def transcribe_audio(audio_file_path):
    transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large")
    transcription = transcriber(audio_file_path)
    return transcription['text']

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']


def main(youtube_url):
    download_audio(youtube_url, "downloaded_audio.mp3")
    transcribed_text = transcribe_audio("downloaded_audio.mp3")
    summary = summarize_text(transcribed_text)
    st.write(summary)

st.set_page_config(page_title="Kranki.ai", page_icon="🌐", layout="centered")

st.title("Welcome to Kranki.ai 👋🏻")
st.caption("Create Obsidian notes from YouTube videos instantly using Kranki.ai. It's a YouTube caption extractor which utilizes AI to create beautiful Obsidian notes at fabulous speed. ⚡")
st.divider()


get_vid = st.text_input("YouTube Link 🔗")

try:
    if st.button("✨ Generate Note"):
        if get_vid: 
            st.video(get_vid)  
            with st.spinner('✨ Generating Note...'):
                time.sleep(10) 
                main(get_vid) 
            st.success("Done! 🎉")
        else:
            st.error("Please enter a valid YouTube link!")

except:
   st.error("Invalid input. Please enter a valid YouTube URL. Or The Ai didn't run")