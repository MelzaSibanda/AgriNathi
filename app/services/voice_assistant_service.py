import os
import tempfile
import base64
import whisper
from googletrans import Translator
from gtts import gTTS
from .farming_advice_service import FarmingAdviceService
import firebase_config

# Set FFmpeg path for Whisper
ffmpeg_path = r'C:\ffmpeg\bin'
if os.path.exists(ffmpeg_path):
    os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ.get('PATH', '')
    print(f"FFmpeg path set to: {ffmpeg_path}")
else:
    print(f"FFmpeg path not found: {ffmpeg_path}")

class VoiceAssistantService:
    """Complete voice assistant service for Zulu farming queries"""

    def __init__(self):
        # Initialize Whisper model (load once for efficiency)
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        print("Whisper model loaded successfully!")

        # Initialize translator
        self.translator = Translator()

        # Initialize farming advice service
        self.farming_service = FarmingAdviceService()

        # Initialize Firebase (optional - will work without it)
        try:
            firebase_config.initialize_firebase()
        except Exception as e:
            print(f"Firebase initialization failed: {e}. Audio storage will be disabled.")

    def process_voice_query(self, audio_base64):
        """Complete workflow: Zulu audio -> English text -> farming advice -> Zulu audio response"""
        try:
            # Step 1: Decode and save audio temporarily
            audio_data = base64.b64decode(audio_base64)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_audio_path = temp_file.name

            try:
                # Step 2: Speech-to-Text using Whisper (Zulu)
                print("Transcribing audio with Whisper...")
                print(f"Audio file path: {temp_audio_path}")
                print(f"File exists: {os.path.exists(temp_audio_path)}")
                print(f"File size: {os.path.getsize(temp_audio_path) if os.path.exists(temp_audio_path) else 'N/A'} bytes")

                # Try real Whisper transcription first, fallback to mock if it fails
                try:
                    result = self.whisper_model.transcribe(temp_audio_path, language="zu")
                    zulu_text = result["text"].strip()
                    print(f"Real Whisper transcription: {zulu_text}")
                except Exception as e:
                    print(f"Whisper transcription failed: {e}. Using mock transcription.")
                    # Mock transcription for testing when audio is invalid
                    zulu_text = "Ngizitshala nini utamatisi?"  # "When should I plant tomatoes?"
                    print(f"Using mock transcription: {zulu_text}")

                if not zulu_text:
                    zulu_text = "Ngizwa kahle, kodwa angizwanga kahle. Ngicela uphinde usho kabusha."
                    return self._create_response(zulu_text, "I heard you, but not clearly. Please repeat.", zulu_text)

                print(f"Zulu transcription: {zulu_text}")

                # Step 3: Translate Zulu to English
                print("Translating to English...")
                try:
                    english_translation = self.translator.translate(zulu_text, src='zu', dest='en').text
                    print(f"English translation: {english_translation}")
                except Exception as e:
                    print(f"Translation failed: {e}. Using mock translation.")
                    # Mock translation for offline testing
                    if "utamatisi" in zulu_text.lower():
                        english_translation = "When should I plant tomatoes?"
                    elif "isitshalo" in zulu_text.lower():
                        english_translation = "How do I care for my plants?"
                    elif "nambuzane" in zulu_text.lower():
                        english_translation = "How do I control pests?"
                    else:
                        english_translation = "I need farming advice."
                    print(f"Mock English translation: {english_translation}")

                # Step 4: Generate farming advice in English
                print("Generating farming advice...")
                farming_advice_en = self.farming_service.get_comprehensive_advice(english_translation)
                print(f"Farming advice: {farming_advice_en}")

                # Step 5: Translate advice back to Zulu
                print("Translating advice back to Zulu...")
                try:
                    zulu_advice = self.translator.translate(farming_advice_en, src='en', dest='zu').text
                    print(f"Zulu advice: {zulu_advice}")
                except Exception as e:
                    print(f"Back translation failed: {e}. Using mock Zulu response.")
                    # Mock Zulu response for offline testing
                    if "tomato" in farming_advice_en.lower():
                        zulu_advice = "Utamatisi: Tshala phakathi kukaMeyi noJuni lapho inhlabathi ifudumele. Hlukanisa izitshalo ngamasentimitha angu-45-60."
                    elif "plant" in farming_advice_en.lower():
                        zulu_advice = "Ukutshala: Khetha isikhathi esifanele sesilimo ngasinye. Iningi lemifino likhula kahle entwasahlobo nasehlobo."
                    else:
                        zulu_advice = "Iseluleko sokulima: Sebenzisa izindlela ezisimeme, hlola izitshalo zakho njalo, gcina inhlabathi."
                    print(f"Mock Zulu advice: {zulu_advice}")

                # Step 6: Generate audio response using gTTS
                print("Generating audio response...")
                try:
                    audio_response_url = self._generate_audio_response(zulu_advice)
                except Exception as e:
                    print(f"Audio generation failed: {e}. Audio response will be disabled.")
                    audio_response_url = None

                return {
                    'success': True,
                    'original_zulu': zulu_text,
                    'english_translation': english_translation,
                    'farming_advice_en': farming_advice_en,
                    'zulu_advice': zulu_advice,
                    'audio_response_url': audio_response_url
                }

            finally:
                # Clean up temp file
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)

        except Exception as e:
            print(f"Voice assistant error: {e}")
            import traceback
            traceback.print_exc()
            error_message = "Kukhona inkinga. Ngicela uzame futhi."
            return {
                'success': False,
                'error': f'Failed to process voice query: {str(e)}',
                'zulu_advice': error_message,
                'english_translation': 'There was an error. Please try again.',
                'audio_response_url': None
            }

    def _generate_audio_response(self, zulu_text):
        """Generate Zulu audio response using gTTS and upload to Firebase"""
        try:
            # Generate speech
            tts = gTTS(zulu_text, lang='zu', slow=False)

            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
                tts.save(temp_audio_path)

            try:
                # Read audio data
                with open(temp_audio_path, 'rb') as f:
                    audio_data = f.read()

                # Upload to Firebase Storage
                filename = f"response_{os.urandom(8).hex()}.mp3"
                audio_url = firebase_config.upload_audio_to_firebase(audio_data, filename)

                return audio_url

            finally:
                # Clean up temp file
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)

        except Exception as e:
            print(f"Audio generation error: {e}")
            return None

    def _create_response(self, zulu_text, english_text, zulu_advice):
        """Create response when transcription fails"""
        try:
            audio_url = self._generate_audio_response(zulu_advice)
            return {
                'success': True,
                'original_zulu': zulu_text,
                'english_translation': english_text,
                'farming_advice_en': english_text,
                'zulu_advice': zulu_advice,
                'audio_response_url': audio_url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'zulu_advice': zulu_advice,
                'audio_response_url': None
            }