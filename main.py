import whisper
import shlex
import subprocess as sp
import tkinter as tk
from tkinter import filedialog
import os

def transcribe_video(input_file_path):
    model = whisper.load_model("small")
    output_audio_file = input_file_path.rsplit(".", 1)[0] + ".wav"
    subtitle_file_path = input_file_path.rsplit(".", 1)[0] + ".srt"

    # Extract audio from video
    cmd = f"ffmpeg -i \"{input_file_path}\" -vn -acodec pcm_s16le -ac 2 \"{output_audio_file}\""
    sp.check_call(shlex.split(cmd))

    # Transcribe audio
    result = model.transcribe(output_audio_file)

    # Create Subtitle File from Transcription
    def seconds_to_srt_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:06.3f}".format(int(hours), int(minutes), seconds)

    with open(subtitle_file_path, "w") as subtitle_file:
        for segment in result["segments"]:
            start_time = seconds_to_srt_time(segment["start"])
            end_time = seconds_to_srt_time(segment["end"])
            subtitle_file.write(f"{segment['id']}\n")
            subtitle_file.write(f"{start_time} --> {end_time}\n")
            subtitle_file.write(f"{segment['text']}\n\n")

    # Delete the .wav file after creating the .srt file
    os.remove(output_audio_file)

    print(f"Subtitle file created: '{subtitle_file_path}' generated successfully")

def select_video():
    file_paths = filedialog.askopenfilenames(
        title="Select Video Files",
        filetypes=(("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*"))
    )
    for file_path in file_paths:
        transcribe_video(file_path)

def create_gui():
    root = tk.Tk()
    root.title("Video Transcriber")

    btn_select_video = tk.Button(root, text="Select Video(s)", command=select_video)
    btn_select_video.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()