import yt_dlp

def download_audio(url, output="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output

def download_video_segment(url, start, end, output):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output,
        'download_sections': {'*': [{'start_time': start, 'end_time': end}]},
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
