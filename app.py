"""
Streamlit Gemini Voice Bot - Web-based voice bot with real voice input and output

Uses audio-recorder-streamlit for browser microphone access
Uses gTTS for text-to-speech output
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import base64

# Configure page
st.set_page_config(
    page_title="Gemini Voice Bot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f3e5f5;
        margin-right: 20%;
    }
    .example-questions {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stAudio {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'last_audio' not in st.session_state:
    st.session_state.last_audio = None
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True
if 'last_response_audio' not in st.session_state:
    st.session_state.last_response_audio = None

# API Configuration
API_KEY = 'AIzaSyBpqgFYLuF_hUAPJWI8ZJKmqzjazPkCNoA'

# System prompt
SYSTEM_PROMPT = """You are having a friendly, casual conversation. Answer questions in a warm, authentic way as if you're chatting with a friend. 

When answering personal questions:
- Be conversational and natural, using contractions and everyday language
- Share thoughtful, specific responses rather than generic ones
- Show personality through your word choices and examples
- Keep responses brief (2-4 sentences) unless asked for more detail
- Be honest and relatable

For questions about life, growth, strengths, or experiences, give genuine, thoughtful answers that feel personal and real."""


def initialize_gemini():
    """Initialize Gemini API and create chat session"""
    try:
        genai.configure(api_key=API_KEY)

        # Create model without system_instruction (not supported in all versions)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Safety settings
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Generation config
        generation_config = genai.GenerationConfig(
            temperature=0.9,
            top_p=0.95,
            top_k=40,
            max_output_tokens=300,
        )

        # Start chat with system prompt as first message
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.safety_settings = safety_settings
        st.session_state.generation_config = generation_config
        st.session_state.system_prompt_sent = False

        return True
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        return False


def transcribe_audio(audio_bytes):
    """Convert audio bytes to text using speech recognition"""
    try:
        recognizer = sr.Recognizer()

        # Save audio bytes to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Load audio file
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Clean up temp file
        os.unlink(temp_audio_path)

        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition error: {e}")
        return None
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None


def get_bot_response(user_input):
    """Get response from Gemini"""
    try:
        response = st.session_state.chat_session.send_message(
            user_input,
            generation_config=st.session_state.generation_config,
            safety_settings=st.session_state.safety_settings
        )

        if not response.parts:
            return "I'm having trouble answering that right now. Could you rephrase your question?"

        return response.text
    except Exception as e:
        return f"Sorry, I had trouble processing that. Error: {str(e)}"


def text_to_speech(text):
    """Convert text to speech and return audio bytes"""
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang='en', slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            tts.save(temp_audio.name)
            temp_audio_path = temp_audio.name

        # Read audio file
        with open(temp_audio_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()

        # Clean up temp file
        os.unlink(temp_audio_path)

        return audio_bytes
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None


# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Gemini Voice Bot</h1>
    <p>Have a natural conversation with AI using voice or text</p>
</div>
""", unsafe_allow_html=True)

# Voice toggle
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    voice_toggle = st.checkbox("🔊 Enable Voice Output", value=st.session_state.voice_enabled)
    st.session_state.voice_enabled = voice_toggle

# Initialize Gemini if not already done
if st.session_state.chat_session is None:
    with st.spinner("Initializing AI..."):
        if initialize_gemini():
            st.success("✅ Bot ready to chat!")
        else:
            st.stop()

# Example questions
with st.expander("📝 Example Questions to Try", expanded=False):
    st.markdown("""
    <div class="example-questions">
        • What should I know about your life story in a few sentences?<br>
        • What's your #1 superpower?<br>
        • What are the top 3 areas you'd like to grow in?<br>
        • What misconception do your coworkers have about you?<br>
        • How do you push your boundaries and limits?<br>
        • What's your name?<br>
        • Tell me about yourself<br>
    </div>
    """, unsafe_allow_html=True)

# Chat interface
st.markdown("### 💬 Conversation")

# Display chat history
for message in st.session_state.chat_history:
    if message['role'] == 'user':
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Bot:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)

# Voice input section
st.markdown("### 🎤 Voice Input")
st.info("Click the microphone button below to record your message, then it will automatically transcribe and send!")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e74c3c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="3x",
    pause_threshold=2.0,
    sample_rate=41000
)

# Process audio if new recording
if audio_bytes and audio_bytes != st.session_state.last_audio:
    st.session_state.last_audio = audio_bytes

    with st.spinner("🎧 Transcribing audio..."):
        transcribed_text = transcribe_audio(audio_bytes)

    if transcribed_text:
        st.success(f"📝 You said: {transcribed_text}")

        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': transcribed_text
        })

        # Get bot response
        with st.spinner("🤔 Thinking..."):
            bot_response = get_bot_response(transcribed_text)

        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'bot',
            'content': bot_response
        })

        # Generate voice response if enabled
        if st.session_state.voice_enabled:
            with st.spinner("🔊 Generating voice response..."):
                st.session_state.last_response_audio = text_to_speech(bot_response)

        # Rerun to update display
        st.rerun()
    else:
        st.error("❌ Could not understand the audio. Please try again or use text input.")

# Play the latest bot response audio if available
if st.session_state.last_response_audio and st.session_state.voice_enabled:
    st.markdown("### 🔊 Bot Voice Response")
    st.audio(st.session_state.last_response_audio, format='audio/mp3', autoplay=True)
    st.caption("↑ Click play if audio doesn't start automatically")

# Divider
st.markdown("---")

# Text input section
st.markdown("### ⌨️ Text Input")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Your message:",
        key="user_input",
        placeholder="Type your message here...",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", type="primary", use_container_width=True)

# Process text input
if send_button and user_input:
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })

    # Get bot response
    with st.spinner("🤔 Thinking..."):
        bot_response = get_bot_response(user_input)

    # Add bot response to history
    st.session_state.chat_history.append({
        'role': 'bot',
        'content': bot_response
    })

    # Generate voice response if enabled
    if st.session_state.voice_enabled:
        with st.spinner("🔊 Generating voice response..."):
            st.session_state.last_response_audio = text_to_speech(bot_response)

    # Rerun to update display
    st.rerun()

# Clear chat button
if st.session_state.chat_history:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chat_session = None
            st.session_state.last_audio = None
            st.session_state.last_response_audio = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 14px;">
    <p>Powered by Gemini 2.5 Flash | Built with Streamlit</p>
    <p><em>🎤 Click the microphone to record • ⌨️ Or type your message below</em></p>
</div>
""", unsafe_allow_html=True)