# Gemini Voice Bot 🤖

A conversational AI voice bot powered by Google's Gemini 2.5 Flash model, built with Streamlit.

## Features

- 🎤 **Voice Input**: Record your questions using browser microphone
- 🔊 **Voice Output**: Bot responds with natural speech
- 💬 **Text Chat**: Type messages as an alternative to voice
- 🤖 **AI-Powered**: Uses Gemini 2.5 Flash for intelligent responses
- 📱 **Mobile Friendly**: Works on all devices
- 🌐 **Web-Based**: No installation required, access via browser

## Live Demo

https://gemini-voice-bot-6ndn.onrender.com

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/gemini-voice-bot.git
cd gemini-voice-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open browser at `http://localhost:8501`

## Deployment to Render

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Quick Deploy

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Render auto-detects `render.yaml` and deploys

## Usage

1. **Enable Voice Output**: Check the "🔊 Enable Voice Output" box
2. **Ask a Question**: 
   - Click the microphone button and speak
   - Or type in the text input box
3. **Get Response**: Bot will respond with text and voice
4. **Continue Conversation**: Keep chatting naturally

## Example Questions

- What should I know about your life story?
- What's your #1 superpower?
- What are the top 3 areas you'd like to grow in?
- What misconception do your coworkers have about you?
- How do you push your boundaries and limits?

## Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Voice Input**: audio-recorder-streamlit, SpeechRecognition
- **Voice Output**: Google Text-to-Speech (gTTS)
- **Deployment**: Render

## Configuration

To use your own Gemini API key:

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Update `API_KEY` in `app.py` or use environment variables

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
