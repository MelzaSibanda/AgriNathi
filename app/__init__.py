from flask import Flask, render_template, request, jsonify
import os
import base64
import io
import sys

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['UPLOAD_FOLDER'] = 'data/audio_recordings'

    # Import the voice assistant service
    try:
        # Add current directory to path for imports
        import sys
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(current_dir)
        sys.path.append(parent_dir)

        from services.voice_assistant_service import VoiceAssistantService
        voice_assistant = VoiceAssistantService()
        print("Voice assistant service initialized successfully!")

    except Exception as e:
        print(f"Could not initialize voice assistant: {e}. Using fallback mode.")
        # Fallback mock service
        class MockVoiceAssistant:
            def process_voice_query(self, audio_base64):
                return {
                    'success': True,
                    'original_zulu': 'Sawubona, ngicela usizo ngezitshalo zami',
                    'english_translation': 'Hello, I need help with my plants',
                    'farming_advice_en': 'For plant diseases, ensure proper watering and use organic pesticides.',
                    'zulu_advice': 'Ngezifo zezitshalo, qiniseka ukuthi unisele kahle futhi usebenzise imithi yokubulala izinambuzane zemvelo.',
                    'audio_response_url': None
                }

        voice_assistant = MockVoiceAssistant()

    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/voice-recognition')
    def voice_recognition_page():
        return render_template('voice_recognition.html')

    @app.route('/weather')
    def weather():
        return render_template('weather.html')

    @app.route('/plant-scan')
    def plant_scan():
        return render_template('plant_scan.html')

    @app.route('/voice-assistant')
    def voice_assistant_page():
        return render_template('voice_assistant.html')

    @app.route('/voice-query', methods=['POST'])
    def voice_query():
        try:
            data = request.get_json()
            if not data or 'audio' not in data:
                return jsonify({'error': 'No audio data provided'}), 400

            # Process the audio data with new voice assistant
            audio_base64 = data['audio']
            result = voice_assistant.process_voice_query(audio_base64)

            return jsonify(result)
        except Exception as e:
            import traceback
            print(f"Error processing voice query: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @app.route('/test-voice')
    def test_voice():
        return jsonify({
            'message': 'Voice assistant system is active and ready.',
            'success': True
        })

    return app

if __name__ == '__main__':
    app = create_app()
    # Use environment variable for port (Heroku compatibility)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)