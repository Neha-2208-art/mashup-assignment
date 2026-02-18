import sys
import os
import yt_dlp
from moviepy import AudioFileClip, concatenate_audioclips


def generate_mashup(artist, total_videos, clip_duration, final_output):

    if not os.path.exists("temp_audio"):
        os.makedirs("temp_audio")

    search_url = f"https://www.youtube.com/results?search_query={artist.replace(' ', '+')}+songs"

    ydl_options = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio/%(id)s.%(ext)s',
        'quiet': False,
        'noplaylist': True,
        'extract_flat': True
    }

    print("\nFetching video links...\n")

    video_urls = []

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(search_url, download=False)
        if 'entries' in info:
            for entry in info['entries'][:total_videos]:
                video_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")

    if not video_urls:
        print("No videos found.")
        return

    print("\nDownloading audio files...\n")

    download_options = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio/%(id)s.%(ext)s',
        'quiet': False,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with yt_dlp.YoutubeDL(download_options) as ydl:
        for url in video_urls:
            try:
                ydl.download([url])
            except:
                continue

    print("\nProcessing and trimming clips...\n")

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
        print("No audio clips processed.")
        return

    print("\nMerging clips...\n")

    final_audio = concatenate_audioclips(clips)
    final_audio.write_audiofile(final_output, codec="libmp3lame")

    final_audio.close()
    for clip in clips:
        clip.close()

    for f in os.listdir("temp_audio"):
        os.remove(os.path.join("temp_audio", f))
    os.rmdir("temp_audio")

    print(f"\nMashup Created Successfully: {final_output}\n")


def main():

    if len(sys.argv) != 5:
        print("Usage: python 102317062.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        number = int(sys.argv[2])
        duration = int(sys.argv[3])
    except:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output = sys.argv[4]

    if number <= 10:
        print("Error: Number of videos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: Duration must be greater than 20 seconds.")
        sys.exit(1)

    if not output.endswith(".mp3"):
        output += ".mp3"

    generate_mashup(singer, number, duration, output)


if __name__ == "__main__":
    main()
