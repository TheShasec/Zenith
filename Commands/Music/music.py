import yt_dlp  
import discord
# YT-DLP configuration options
YTDLP_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# FFmpeg audio options
FFMPEG_OPTIONS = {
    'options': '-vn'
}

# Create YouTube downloader instance
ytdlp = yt_dlp.YoutubeDL(YTDLP_OPTIONS)

# Class to handle audio source using YTDL
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        try:
            # Download or stream video info
            data = await loop.run_in_executor(
                None,
                lambda: ytdlp.extract_info(url, download=not stream)
            )

            # If the URL is a playlist, get the first entry
            if 'entries' in data:
                data = data['entries'][0]

            filename = data['url'] if stream else ytdlp.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

        except Exception as e:
            print(f"[YTDL Error] {e}")
            return None