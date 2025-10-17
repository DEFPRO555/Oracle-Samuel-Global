# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

from gtts import gTTS
import os
import tempfile
from datetime import datetime
import base64


class TTSManager:
    """
    Text-to-Speech Manager for Oracle Samuel
    Gives the AI a voice - The Market Prophet persona
    """
    
    def __init__(self):
        self.voice_history = []
        self.default_language = 'en'
        self.default_accent = 'com'  # .com = US accent, .co.uk = UK accent
    
    def speak(self, text, language='en', slow=False, save_file=None):
        """
        Convert text to speech and return audio file path
        
        Args:
            text: Text to convert to speech
            language: Language code ('en', 'es', 'fr', etc.)
            slow: Speak slowly if True
            save_file: Optional path to save audio file
            
        Returns:
            tuple: (success: bool, audio_file_path or error message)
        """
        try:
            # Add Oracle Samuel personality prefix
            prophet_text = self._add_prophet_personality(text)
            
            # Create text-to-speech object
            tts = gTTS(text=prophet_text, lang=language, slow=slow)
            
            # Save to file
            if save_file is None:
                # Create temporary file
                temp_dir = tempfile.gettempdir()
                save_file = os.path.join(temp_dir, f'oracle_samuel_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp3')
            
            tts.save(save_file)
            
            # Log to history
            self.voice_history.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'text': text,
                'file': save_file
            })
            
            print(f"🗣️ Oracle Samuel speaks: {save_file}")
            return True, save_file
            
        except Exception as e:
            return False, f"TTS error: {str(e)}"
    
    def _add_prophet_personality(self, text):
        """Add Oracle Samuel's prophetic personality to responses"""
        # Don't add prefix if text already starts with specific patterns
        skip_prefixes = ['based on', 'the', 'according to', 'in', 'for', 'your', 'this']
        
        if any(text.lower().startswith(prefix) for prefix in skip_prefixes):
            return text
        
        # Add subtle personality without being too verbose
        return text
    
    def speak_greeting(self):
        """Speak Oracle Samuel's greeting"""
        greeting = ("Greetings. I am Oracle Samuel, The Real Estate Market Prophet. "
                   "I analyze property data with precision and foresight. "
                   "How may I illuminate the market for you today?")
        return self.speak(greeting)
    
    def speak_analysis_result(self, analysis_text):
        """Speak analysis result with prophet tone"""
        intro = "Based on my analysis, "
        full_text = intro + analysis_text
        return self.speak(full_text)
    
    def speak_prediction(self, prediction_text):
        """Speak price prediction with confidence"""
        intro = "My forecast reveals: "
        full_text = intro + prediction_text
        return self.speak(full_text)
    
    def create_audio_bytes(self, text, language='en'):
        """Create audio and return as bytes for Streamlit audio player"""
        try:
            success, audio_file = self.speak(text, language=language)
            
            if success:
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                
                # Clean up temporary file
                try:
                    os.remove(audio_file)
                except:
                    pass
                
                return True, audio_bytes
            else:
                return False, audio_file  # Error message
                
        except Exception as e:
            return False, f"Audio creation error: {str(e)}"
    
    def get_voice_history(self, limit=10):
        """Get recent voice generation history"""
        return self.voice_history[-limit:]
    
    def clear_history(self):
        """Clear voice history"""
        self.voice_history = []

