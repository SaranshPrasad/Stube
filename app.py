from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './downloads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        try:
            yt = YouTube(url)
            video_info = {
                'title': yt.title,
                'thumbnail': yt.thumbnail_url,
                'embed_url': f"https://www.youtube.com/embed/{yt.video_id}",
                'streams': yt.streams
            }
            return render_template('index.html', video_info=video_info)
        except Exception as e:
            return render_template('error.html', error=str(e))

@app.route('/download_video', methods=['POST'])
def download_video():
    if request.method == 'POST':
        url = request.form['url']
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            file = "video.mp4"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file)
            video.download(app.config['UPLOAD_FOLDER'], filename=file)
            if os.path.exists(filepath):
                return redirect(url_for('download_complete', filename=file))
            else:
                error_message = f"File '{file}' not found at path '{filepath}'."
                return render_template('error.html', error=error_message)
        except Exception as e:
            return render_template('error.html', error=str(e))

@app.route('/download_audio', methods=['POST'])
def download_audio():
    if request.method == 'POST':
        url = request.form['url']
        try:
            yt = YouTube(url)
            audio = yt.streams.filter(only_audio=True).first()
            title = yt.title
            title = "audio"
            filename = f"{title}.mp4"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.download(app.config['UPLOAD_FOLDER'])
            if os.path.exists(filepath):
                return redirect(url_for('download_complete', filename=filename))
            else:
                error_message = f"File '{filename}' not found at path '{filepath}'."
                return render_template('error.html', error=error_message)
        except Exception as e:
            return render_template('error.html', error=str(e))

@app.route('/download_complete/<filename>')
def download_complete(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        error_message = f"File '{filename}' not found at path '{filepath}'."
        return render_template('error.html', error=error_message)

