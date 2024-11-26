from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip
import openai
from pathlib import Path
import os
import json

class AudioVideoGenerator:
    def __init__(self, config_path='config/config.json'):
        # Load API keys from configuration
        with open(config_path) as config_file:
            config = json.load(config_file)
        
        # Initialize OpenAI client with the API key from config
        self.client = openai.OpenAI(api_key=config.get('openai_api_key'))

    def split_text(self, text, max_length=4096):
        chunks = []
        while len(text) > max_length:
            split_index = text.rfind(' ', 0, max_length)
            if split_index == -1:  # No space found, hard split
                split_index = max_length
            chunks.append(text[:split_index])
            text = text[split_index:].strip()
        chunks.append(text)
        return chunks

    def text_to_speech(self, text_chunks, model="tts-1-hd", voice="alloy"):
        audio_files = []
        Path('logs').mkdir(parents=True, exist_ok=True)
        for i, chunk in enumerate(text_chunks):
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=chunk
            )
            audio_file_path = f"logs/speech_chunk_{i}.mp3"
            with open(audio_file_path, 'wb') as f:
                f.write(response.content)
            audio_files.append(audio_file_path)
        return audio_files

    def concatenate_audio(self, audio_files, output_path):
        combined = AudioSegment.empty()
        for file in audio_files:
            combined += AudioSegment.from_file(file)
        combined.export(output_path, format="mp3")
        return output_path

    def generate_final_video(self, image_path, output_audio_path, output_video_path):
        audio_clip = AudioFileClip(output_audio_path)
        image_clip = ImageClip(image_path)
        video_clip = image_clip.set_audio(audio_clip)
        video_clip = video_clip.set_duration(audio_clip.duration)
        video_clip = video_clip.set_fps(30)
        video_clip.write_videofile(output_video_path, codec='libx264', threads=4)

    def get_audio_files(self, dialogue, role):
        chunks = self.split_text(dialogue)
        if role == 'teacher':
            audio_files = self.text_to_speech(chunks, model="tts-1-hd", voice="nova")
        else:
            audio_files = self.text_to_speech(chunks, model="tts-1-hd", voice="echo")
        return audio_files

    def generate_speech(self, overall_narrative, output_path):
        ind = 0
        combined = AudioSegment.empty()
        while ind < len(overall_narrative['teacher']):
            dialogue = self.get_audio_files(overall_narrative['teacher'][ind], 'teacher') 
            for file in dialogue:
                combined += AudioSegment.from_file(file)
            if ind < len(overall_narrative['student']):
                dialogue = self.get_audio_files(overall_narrative['student'][ind], 'student') 
                for file in dialogue:
                    combined += AudioSegment.from_file(file)
            ind+=1
        combined.export(output_path, format="mp3")

    def get_av(self, overall_narrative, format, output):
        image_path = "assets/student_teacher.jpg"
        output_audio_path = os.path.join(output, "final_speech.mp3") 
        output_video_path = output_path=os.path.join(output, "final_video_clip.mp4") 
        # Ensure output directory exists
        Path(output).mkdir(parents=True, exist_ok=True)
        print('generating audio & concatenating audio')
        self.generate_speech(overall_narrative, output_audio_path)
        if format == "video":
            self.generate_final_video(image_path,output_audio_path,output_video_path)