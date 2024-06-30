import cv2
from moviepy.editor import VideoFileClip
import whisper
import PyPDF2
from pydub import AudioSegment

# Function to extract audio from video
def video_to_audio(video_path, output_audio_path):
    # Load the video file using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Get the audio stream from the video using moviepy
    clip = VideoFileClip(video_path)
    audio = clip.audio

    # Save the audio to a new file
    audio.write_audiofile(output_audio_path)

    # Release the OpenCV video capture
    cap.release()

# Function to convert video to mp4

def video_to_mp4(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

# Function to convert audio to wav
def audio_to_wav(input_file, output_file):
    sound = AudioSegment.from_file(input_file)
    sound.export(output_file, format="wav")

# Function to convert audio to text    
def audio_to_text(audio_path):
    if audio_path.endswith('.wav'):
        wav_file = audio_path
    else:
        audio_to_wav(audio_path, "temp.wav")
        wav_file = "temp.wav"
    model = whisper.load_model("base")
    result = model.transcribe(wav_file)
    return result["text"]  
   
# Function to convert video to text
def video_to_text(video_path):
    if video_path.endswith('.mp4'):
        video_to_audio(video_path, "temp.wav")
    else:
        video_to_mp4(video_path, "temp.mp4")
        video_to_audio("temp.mp4", "temp.wav")
    text = audio_to_text("temp.wav")
    return text

# Function to convert pdf to text
def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text



# Main code

print('''Choose the option:  
      1. Video to Text
      2. Audio to Text
      3. PDF to Text
      4. Exit
      ''')
while True:
    option = int(input("Enter the option: "))
    if option == 1:
        vid=input("Enter the video path: ")
        text=video_to_text(vid)
        output_file = f"{vid}_output.txt"
        with open(output_file, 'w') as file:
            file.write(text)
        print("Text written to", output_file)
    elif option == 2:
        audio=input("Enter the audio path: ")
        text=audio_to_text(audio)
        output_file = f"{audio}_output.txt"
        with open(output_file, 'w') as file:
            file.write(text)
        print("Text written to", output_file)
    elif option == 3:
        pdf_path=input("Enter the pdf path: ")
        text = pdf_to_text(pdf_path)
        output_file = f"{pdf_path}_output.txt"
        with open(output_file, 'w') as file:
            file.write(text)
        print("Text written to", output_file)
    elif option == 4:
        break
    else:
        print("Invalid Option")

