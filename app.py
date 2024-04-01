#録音→文字起こしをwhisperで実行
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment
import io
import pyperclip

# OpenAI APIキーの設定
import openai
from openai import OpenAI
client = OpenAI()

#secretからOPENAPIKEYを取り出す
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Copy&Paste", page_icon= "📎")

# オーディオレコーダーで録音
audio_bytes = audio_recorder(pause_threshold=60, text="",
    recording_color="#e8b62c", neutral_color="#6aa36f")

if audio_bytes:
    # BytesIOオブジェクトにデータを書き込む
    audio_io = io.BytesIO(audio_bytes)
    # BytesIOからAudioSegmentオブジェクトに変換
    audio_segment = AudioSegment.from_file(audio_io)
    # mp3ファイルとして保存
    audio_segment.export("recorded_audio.mp3", format="mp3")
    # st.success("Recording saved as recorded_audio.mp3.")
    audio_file = open("recorded_audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    st.text(transcription.text)
     # テキストをクリップボードにコピーするボタン
    if st.button("Copy Transcription"):
        pyperclip.copy(transcription.text)
        st.success("Transcription copied to clipboard!")
# else:
    # st.warning("No audio recorded.")
