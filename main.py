import os
import plistlib
import yt_dlp
from rich import print
from rich.prompt import Prompt

def parse_favorite_songs(xml_path, min_play_count=5):
    """Parse Apple Music XML and return only favorite songs with play count above threshold."""
    with open(xml_path, 'rb') as f:
        plist = plistlib.load(f)
    
    tracks = plist['Tracks']
    favorite_songs = []

    for track_id, track_info in tracks.items():
        name = track_info.get('Name')
        artist = track_info.get('Artist')
        play_count = track_info.get('Play Count', 0)

        if name and play_count >= min_play_count:
            if artist:
                favorite_songs.append(f"{name} {artist}")
            else:
                favorite_songs.append(name)
    
    return favorite_songs

def download_song_from_youtube(query, download_path):
    """Search and download the song from YouTube as an mp3."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"[cyan]Searching and downloading:[/] {query}")
            ydl.download([query])
        except Exception as e:
            print(f"[red]Failed to download {query}: {e}[/red]")

def main():
    xml_path = Prompt.ask("[bold green]Enter the path to your Apple Music XML file[/]")
    download_path = Prompt.ask("[bold green]Enter the path where you want to save MP3 files[/]")
    min_play_count = int(Prompt.ask("[bold green]Enter minimum Play Count to consider as favorite[/]", default="5"))

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    favorite_songs = parse_favorite_songs(xml_path, min_play_count)

    print(f"\n[bold yellow]Found {len(favorite_songs)} favorite songs. Starting download...[/bold yellow]\n")

    for song in favorite_songs:
        download_song_from_youtube(song, download_path)

    print("\n[bold green]All downloads finished![/bold green]")

if __name__ == '__main__':
    main()
