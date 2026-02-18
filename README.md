# Mashup Generator Assignment
**Roll Number:** 102317062  
**Program:** Mashup Generator (Python)

## Project Description
This project implements a command-line tool and a web service to create a "mashup" of audio from YouTube videos. It downloads multiple videos of a specified singer, extracts the audio, trims them to a specific duration, and merges them into a single MP3 file.

## Methodology
The assignment is solved in two parts:

### Part 1: CLI Script (102317062.py)
1.  **Input:** The script accepts command-line arguments: Singer Name, Number of Videos, Duration, and Output Filename.
2.  **Search:** Uses `yt-dlp` to search and retrieve YouTube video results for the given singer.
3.  **Download:** Uses `yt-dlp` to download the best available audio streams from YouTube.
4.  **Processing:** 
    * Iterates through downloaded audio files using `moviepy`.
    * Trims each audio file to the specified duration (e.g., 25 seconds).
    * Concatenates all trimmed clips into a single audio track.
5.  **Output:** Exports the final mashup as an MP3 file.

### Part 2: Web Service (app.py)
1.  **Framework:** Uses `Flask` to create a web interface.
2.  **User Interface:** A HTML form allows users to input parameters (Singer, Number of Videos, Duration, Email).
3.  **Backend Logic:** Reuses the logic from Part 1 to generate the mashup on the server.
4.  **Email Delivery:** 
    * The generated MP3 is compressed into a ZIP file.
    * Uses Python's `smtplib` to email the ZIP file to the user's provided email address using Gmail App Password authentication.

## How to Run
1.  **Install Prerequisites:**
    ```bash
    pip install yt-dlp moviepy flask
    ```
    (Ensure FFmpeg is installed and added to PATH).

2.  **Run CLI Script:**
    ```bash
    python 102317062.py "Singer Name" 15 25 output.mp3
    ```

3.  **Run Web App:**
    ```bash
    python app.py
    ```
    Access at: `http://127.0.0.1:5000`

## Libraries Used
* `yt-dlp`: For downloading YouTube content.
* `moviepy`: For audio processing (cutting and merging).
* `flask`: For the web server.
* `smtplib`: For sending emails.
* `zipfile`: For compressing output files.
