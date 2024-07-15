import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os
import tempfile
import re
import patch_pytube

# Apply the pytube patch
patch_pytube.patch_pytube()

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def download_audio_from_youtube(video_url, output_path='output.mp3'):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)
        
        # Get the audio stream with the highest quality
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        # Download the audio file
        st.info("Downloading audio...")
        audio_file = audio_stream.download(filename='temp_audio')

        # Convert the downloaded file to mp3
        st.info("Converting to mp3...")
        audio = AudioSegment.from_file(audio_file)
        audio.export(output_path, format='mp3')

        # Remove the temporary audio file
        os.remove(audio_file)

        return output_path, yt.title

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

st.title("YouTube to MP3 Downloader")

video_url = st.text_input("Enter the YouTube video URL:")
output_filename = st.text_input("Enter the output filename (default is the video title):")

if st.button("Download MP3"):
    if video_url:
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = os.path.join(tmpdirname, 'output.mp3')
            result, video_title = download_audio_from_youtube(video_url, output_path)
            if result:
                if not output_filename:
                    output_filename = sanitize_filename(f"{video_title}.mp3")
                else:
                    output_filename = sanitize_filename(output_filename)
                st.success(f"Audio downloaded and saved as {output_filename}")
                with open(result, "rb") as file:
                    st.download_button(
                        label="Download MP3",
                        data=file,
                        file_name=output_filename,
                        mime='audio/mpeg'
                    )
            else:
                st.error("Failed to download audio.")
    else:
        st.warning("Please enter a valid YouTube URL.")
