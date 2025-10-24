# AgriNathi - Voice-Powered Agricultural Assistant

AgriNathi is an innovative voice-based farming assistant that allows farmers to ask agricultural questions in isiZulu and receive instant, comprehensive farming advice in their native language.

## 🌟 Features

- **Voice Recognition**: Speak naturally in isiZulu (Zulu language)
- **Real-time Translation**: Automatic Zulu ↔ English translation
- **Smart Farming Advice**: AI-powered agricultural guidance
- **Offline Capable**: Works with fallback responses when offline
- **Comprehensive Coverage**: Plant diseases, pest control, watering, fertilization, weather considerations
- **Modern Web Interface**: Responsive design with voice recording capabilities

## 🚀 Technology Stack

- **Backend**: Python Flask
- **Speech-to-Text**: OpenAI Whisper (Zulu language support)
- **Translation**: Google Translate API
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Storage**: Firebase (audio file storage)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## 📋 Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)
- Internet connection (for translation services)
- Microphone access (for voice input)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MelzaSibanda/AgriNathi.git
   cd AgriNathi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg** (Required for Whisper)
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH
   - Or use: `choco install ffmpeg` (Windows with Chocolatey)

5. **Set up Firebase** (Optional - for audio storage)
   - Create Firebase project
   - Download service account key as `firebase-service-account.json`
   - Enable Storage in Firebase console

## 🚀 Running the Application

1. **Start the Flask server**
   ```bash
   python app/__init__.py
   ```

2. **Open your browser**
   ```
   http://localhost:5000
   ```

3. **Navigate to Voice Assistant**
   - Click on "Voice Assistant" in the navigation
   - Allow microphone access when prompted
   - Click the microphone button and speak in isiZulu

## 🎯 Usage Examples

**Sample Questions in isiZulu:**
- "Ngizitshala nini utamatisi?" (When should I plant tomatoes?)
- "Izitshalo zami zinezifo" (My plants have diseases)
- "Ngidinga ukunisela" (I need to water)
- "Zinambuzane ezikhunjeni" (Pests on maize)
- "Yini umanyolo ofanele?" (What fertilizer is suitable?)

## 📁 Project Structure

```
AgriNathi/
├── app/
│   ├── __init__.py                 # Flask application factory
│   ├── services/
│   │   ├── voice_assistant_service.py    # Main voice processing logic
│   │   ├── farming_advice_service.py     # Agricultural knowledge base
│   │   ├── speech_service.py             # Google Cloud Speech (legacy)
│   │   └── translation_service.py        # Google Cloud Translate (legacy)
│   └── templates/
│       ├── index.html                    # Home page
│       ├── voice_recognition.html       # Voice assistant interface
│       ├── weather.html                 # Weather page
│       └── plant_scan.html              # Plant scanner page
├── data/
│   ├── Crop_recommendation.csv          # Crop data
│   └── pest_disease_info.json           # Pest and disease information
├── firebase_config.py                   # Firebase configuration
├── requirements.txt                     # Python dependencies
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for sensitive configuration:
```
SECRET_KEY=your-secret-key-here
GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
```

### Firebase Setup
1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Cloud Storage
3. Generate a service account key
4. Save as `firebase-service-account.json` in project root

## 🌐 API Endpoints

- `GET /` - Home page
- `GET /voice-recognition` - Voice assistant interface
- `POST /voice-query` - Process voice queries
- `GET /test-voice` - System health check

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for Whisper speech recognition
- Google for Translate and Text-to-Speech services
- Bootstrap team for the UI framework
- South African agricultural communities for inspiration

## 📞 Support

For questions or support, please open an issue on GitHub or contact the maintainers.

---

**Empowering farmers with voice-powered agricultural assistance in their native language.** 🌱🗣️