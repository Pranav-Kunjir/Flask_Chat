import speech_recognition as sr
import wave
import math
from datetime import datetime

def get_audio_duration(wav_file_path):
    """Get the duration of the WAV file in seconds"""
    with wave.open(wav_file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration

def transcribe_wav(wav_file_path, chunk_duration=30):
    """
    Transcribe a WAV file with timestamps.
    
    Args:
        wav_file_path (str): Path to the WAV file
        chunk_duration (int): Duration in seconds for each chunk to process
                            (helpful for long files)
    """
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    try:
        # Get total audio duration
        total_duration = get_audio_duration(wav_file_path)
        print(f"Audio file duration: {total_duration:.2f} seconds")
        
        # Open the audio file
        with sr.AudioFile(wav_file_path) as audio_file:
            # Get the audio data
            print("Processing audio file...")
            
            # If the file is long, process it in chunks
            if total_duration > chunk_duration:
                chunks = math.ceil(total_duration / chunk_duration)
                print(f"File will be processed in {chunks} chunks")
                
                for i in range(chunks):
                    # Calculate offset and duration for each chunk
                    offset = i * chunk_duration
                    duration = min(chunk_duration, total_duration - offset)
                    
                    print(f"\nProcessing chunk {i+1}/{chunks} ({offset:.2f}s to {offset+duration:.2f}s)")
                    
                    # Get the audio data for this chunk
                    audio = recognizer.record(audio_file, duration=duration, offset=offset)
                    
                    try:
                        # Perform the transcription
                        text = recognizer.recognize_google(audio)
                        timestamp = f"{offset:.2f}s - {(offset+duration):.2f}s"
                        print(f"[{timestamp}] {text}")
                        
                    except sr.UnknownValueError:
                        print(f"[{offset:.2f}s - {(offset+duration):.2f}s] Could not understand audio")
                    except sr.RequestError as e:
                        print(f"Error with the speech recognition service: {e}")
            
            else:
                # For shorter files, process the whole file at once
                print("Processing entire file...")
                audio = recognizer.record(audio_file)
                
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"[0.00s - {total_duration:.2f}s] {text}")
                    
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")
                    
        print("\nTranscription complete!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Replace this with your WAV file path
    wav_file_path = "audio.wav"
    
    print("Starting transcription...")
    print(f"File: {wav_file_path}")
    
    # Create a timestamped log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"transcription_{timestamp}.txt"
    
    # Redirect output to both console and file
    import sys
    class Logger:
        def __init__(self, filename):
            self.terminal = sys.stdout
            self.log = open(filename, 'w', encoding='utf-8')
        
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
            
        def flush(self):
            self.terminal.flush()
            self.log.flush()
    
    # Set up logging
    sys.stdout = Logger(log_file)
    
    # Perform transcription
    transcribe_wav(wav_file_path)
    
    print(f"\nTranscription has been saved to: {log_file}")

if __name__ == "__main__":
    main()

