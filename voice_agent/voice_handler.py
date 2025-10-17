# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
from datetime import datetime


class VoiceHandler:
    """
    Handles voice input and speech recognition
    Converts spoken words to text for Oracle Samuel
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.last_transcription = None
        self.transcription_history = []
    
    def check_microphone_available(self):
        """Check if microphone is available"""
        try:
            with sr.Microphone() as source:
                return True, "Microphone detected"
        except Exception as e:
            return False, f"Microphone not found: {str(e)}"
    
    def listen_and_transcribe(self, duration=5, language='en-US'):
        """
        Listen to microphone and transcribe speech to text
        
        Args:
            duration: Maximum listening duration in seconds
            language: Language code for recognition
            
        Returns:
            tuple: (success: bool, transcription: str or error message)
        """
        try:
            # Initialize microphone
            with sr.Microphone() as source:
                print("🎤 Oracle Samuel is listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                
                print("🔄 Processing speech...")
                
                # Recognize speech using Google Speech Recognition
                try:
                    transcription = self.recognizer.recognize_google(audio, language=language)
                    
                    self.last_transcription = transcription
                    self.transcription_history.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'text': transcription
                    })
                    
                    print(f"✅ Transcribed: {transcription}")
                    return True, transcription
                    
                except sr.UnknownValueError:
                    return False, "Could not understand audio. Please speak clearly."
                except sr.RequestError as e:
                    return False, f"Speech recognition service error: {str(e)}"
                    
        except Exception as e:
            return False, f"Microphone error: {str(e)}"
    
    def transcribe_from_file(self, audio_file_path, language='en-US'):
        """Transcribe speech from an audio file"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                transcription = self.recognizer.recognize_google(audio, language=language)
                
                self.last_transcription = transcription
                return True, transcription
                
        except Exception as e:
            return False, f"File transcription error: {str(e)}"
    
    def get_transcription_history(self, limit=10):
        """Get recent transcription history"""
        return self.transcription_history[-limit:]
    
    def clear_history(self):
        """Clear transcription history"""
        self.transcription_history = []
        self.last_transcription = None

