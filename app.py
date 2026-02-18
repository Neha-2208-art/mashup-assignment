from flask import Flask, request, render_template
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yt_dlp
from moviepy import AudioFileClip, concatenate_audioclips

app = Flask(__name__)

# ===================================
# FUNCTION: CREATE MASHUP
# ===================================
def create_mashup(artist, total_videos, clip_duration, output_file):

    if not os.path.exists("temp_audio"):
        os.makedirs("temp_audio")

    search_query = f"ytsearch{total_videos}:{artist} songs"

    ydl_options = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio/%(id)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([search_query])
    except Exception as e:
        print("Download Error:", e)
        return False

    clips = []
    files = [f for f in os.listdir("temp_audio") if f.endswith(".mp3")]
    files = files[:total_videos]

    for file in files:
        path = os.path.join("temp_audio", file)
        try:
            audio = AudioFileClip(path)
            short_clip = audio.subclipped(0, min(clip_duration, audio.duration))
            clips.append(short_clip)
        except:
            pass

    if not clips:
        return False

    try:
        final_audio = concatenate_audioclips(clips)
        final_audio.write_audiofile(output_file, codec="libmp3lame")
        final_audio.close()
        for clip in clips:
            clip.close()
    except:
        return False

    # Cleanup
    for f in os.listdir("temp_audio"):
        os.remove(os.path.join("temp_audio", f))
    os.rmdir("temp_audio")

    return True


# ===================================
# FUNCTION: SEND EMAIL
# ===================================
def send_email(receiver_email, file_name):

    sender_email = "nehagarg0996@gmail.com"       
    sender_password = "abcd efgh ijkl mnop"        
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Mashup File - Neha 102317062"

    with open(file_name, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file_name}')
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email Error:", e)
        return False


# ===================================
# ROUTES
# ===================================
@app.route('/')
def home():
    return '''
    <h2>Mashup Generator - Neha (102317062)</h2>
    <form method="POST" action="/create">
        Singer Name:<br>
        <input type="text" name="artist" required><br><br>
        
        Number of Videos (>10):<br>
        <input type="number" name="count" min="11" required><br><br>
        
        Duration in seconds (>20):<br>
        <input type="number" name="duration" min="21" required><br><br>
        
        Email:<br>
        <input type="email" name="email" required><br><br>
        
        <input type="submit" value="Generate Mashup">
    </form>
    '''


@app.route('/create', methods=['POST'])
def process():

    artist = request.form['artist']
    count = int(request.form['count'])
    duration = int(request.form['duration'])
    email = request.form['email']

    if count <= 10 or duration <= 20:
        return "<h3>Error: Videos must be >10 and Duration must be >20 seconds.</h3>"

    mp3_file = "mashup_output.mp3"
    zip_file = "mashup_output.zip"

    success = create_mashup(artist, count, duration, mp3_file)

    if not success:
        return "<h3>Error while creating mashup.</h3>"

    with zipfile.ZipFile(zip_file, 'w') as z:
        z.write(mp3_file)

    email_sent = send_email(email, zip_file)

    if email_sent:
        return f"<h3>Success! Mashup sent to {email}</h3>"
    else:
        return "<h3>Mashup created but Email failed.</h3>"


if __name__ == "__main__":
    app.run(debug=True)
