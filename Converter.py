from typing import Optional
from disnake.ext import commands
import disnake
import asyncio
import os
import pathlib
from yt_dlp import YoutubeDL


class Converter(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5)
    async def convertmp3(self, ctx, link: str, *, filename: Optional[str]) -> None:
        """Mengconvert video yang nantinya akan menjadi file mp3 (Audio)"""
        loop = asyncio.get_event_loop()
        message = await ctx.send("Converting...")
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                # !CHANGEME
                "outtmpl": f"D:/Project/python/boilerplate_daffa/media/TEMP-{ctx.author.id}.%(ext)s",
                "overwrite": True,
                "cookiefile": "cookies/youtube.com_cookies.txt",
                "ffmpeg_location": "ffmpeg/",
                "quiet": True,
                "ignoreerrors": True,
                "logtostderr": False,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = await loop.run_in_executor(None, ydl.extract_info, link, True)
                # ydl.download([link])

            if filename:
                title = filename
            else:
                title = info["title"]

            await ctx.send(
                file=disnake.File(
                    f"media/TEMP-{ctx.author.id}.mp3", filename=f"{title}.mp3"
                )
            )
        except:
            await ctx.send(f"Error")
        finally:
            pathlib.Path(f"media/TEMP-{ctx.author.id}.mp3").unlink(missing_ok=True)


def setup(client):
    client.add_cog(Converter(client))


