import datetime as dt
import typing as t
import os
import discord
from discord.ext import commands
from lyrics_extractor import SongLyrics
from youtube_dl import YoutubeDL
from dotenv import load_dotenv

load_dotenv()


# apikey = API_KEY
# try:
#     chart = musixmatch.ws.track.chart.get(country='it', apikey=apikey)
# except musixmatch.api.Error as e:
#     pass


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        self.is_loop = False
        # 2d array containing [song, channel]
        self.music_queue = []  # initializing the queue
        self.YDL_OPTIONS = {'format': 'bestaudio', 'nonplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.vc = None
        self.LYRICS_URL = "https://sridurgayadav-chart-lyrics-v1.p.rapidapi.com/apiv1.asmx/SearchLyricDirect"
        self.m_url = ""
        self.curr_title = ""

        # searching the item on youtube

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            if self.is_loop is False:
                #  get the first url
                self.m_url = self.music_queue[0][0]['source']
                self.curr_title = self.music_queue[0][0]['title']
                # remove the first element from the queue that is currently being played
                self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(
                # executable="vanilla-musicbot/ffmpeg.exe",
                source=self.m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        elif len(self.music_queue) == 0 and self.is_loop is True:
            self.is_playing = True
            self.vc.play(discord.FFmpegPCMAudio(
                # executable="vanilla-musicbot/ffmpeg.exe",
                source=self.m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            # print(type(self.m_url))
        else:
            self.is_playing = False

        # different conditions (inf loop) checking

    async def play_music(self, ctx):

        if len(self.music_queue) > 0 and self.is_loop is False:
            self.is_playing = True
            self.m_url = self.music_queue[0][0]['source']
            self.curr_title = self.music_queue[0][0]['title']
            # the queue of songs contains a sub-queue(array) of len 2, containing the obj and the voice channel

            # trying to connect the bot to channel is the bot is not already connected to the voice channel
            # trying to call the bot to the specific voice channel (currently where users are)
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

            # if the bot fails to connect to the respective vc
            if self.vc is None:
                await ctx.send("The bot could not connect to the voice channel")
                return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(
                # executable="vanilla-musicbot/ffmpeg.exe",
                source=self.m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            # print(type(self.m_url))
        else:
            self.is_playing = False

    def is_present(self, ctx):
        if ctx.author.voice is None:
            return True
        else:
            return False

    @commands.command(name="remove", aliases=["rem"], help="Removes the song added in the queue")
    # async def remove(self, ctx, *args):
    #     if args != "":
    #         position = args
    #         self.music_queue.pop(position-1)
    #         await ctx.send("Song has been removed")
    #     else:
    #         # await ctx.send("Please enter the position of the song you want to remove from the queue")
    #         self.music_queue.pop()
    async def remove(self, ctx, position: t.Optional[int]):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            position = position or len(self.music_queue)
            self.music_queue.pop(position - 1)
            await ctx.send("Track at position {} is removed".format(position))

    @commands.command(name="current", aliases=["curr"], help="Gets the current title of the song that is playing")
    async def current(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the vice channel to use these commands")
        else:
            if self.curr_title == "":
                await ctx.send("There are no tracks playing at the moment")
            else:
                await ctx.send("Currently Playing: " + self.curr_title)

    @commands.command(name="lyrics", help="Gets the lyrics of the song")
    async def lyrics(self, ctx, name: t.Optional[str]):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            name = name or self.curr_title
            print(name)
            extract_lyrics = SongLyrics(os.getenv("LYRICS_API_KEY"), os.getenv("GCS_ENGINE_ID"))
            res = extract_lyrics.get_lyrics(self.curr_title)
            embed = discord.Embed(
                title=res['title'],
                description=res['lyrics'],
                color=ctx.author.color,
                timestamp=dt.datetime.utcnow()
            )
            embed.set_author(name=ctx.author)
            await ctx.send(embed=embed)

    @commands.command(name="loop", aliases=["l"], help="The bot loops the current music playing")
    async def loop(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            self.is_loop = True
            await ctx.send("Looping the current song.")

    @commands.command(name="loop_off", aliases=["lo"], help="Closes the current playing song in loop")
    async def loop_off(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            self.is_loop = False
            await ctx.send("Looping disabled")

    @commands.command(name="join", aliases=["j"], help="The bot joins the voice channel")
    async def join(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                self.vc = await voice_channel.connect()
            else:
                await self.vc.move_to(voice_channel)

    #  commands - play, pause, resume, skip, disconnect
    @commands.command(name="play", aliases=["p"], help="Plays a selected song from the youtube")
    async def play(self, ctx, *args):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            query = " ".join(args)

            voice_channel = ctx.author.voice.channel

            if voice_channel is None:
                # you need to be connected so that the  bot knows where to go
                await ctx.send("Connect to a voice channel yar kaisa horay")
            elif self.is_paused and len(args) == 0:
                self.vc.resume()
            else:
                song = self.search_yt(query)
                if type(song) is type(True):
                    await ctx.send(
                        "Could not get the song. Incorrect format try another keyword. This could be due to playlist or a livestream format")
                else:
                    await ctx.send(song['title'])
                    self.music_queue.append([song, voice_channel])

                    if self.is_playing is False:
                        await self.play_music(ctx)

    @commands.command(name="pause", aliases=["ps"], help="Pauses the current song being played")
    async def pause(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            # if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            # elif self.is_paused:
            #     self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            if self.is_paused:
                self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            if self.vc is not None and self.vc:
                self.vc.stop()

                # try to play the next song if the queue is not empty
                await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            retval = "Songs in the queue are:" + "\n"
            for i in range(0, len(self.music_queue)):
                # retval +=  self.music_queue[i][0]['title'] + "\n"
                retval += "{}) {}".format((i + 1), self.music_queue[i][0]['title']) + "\n"
            if len(self.music_queue) != 0:
                await ctx.send(retval)
            else:
                await ctx.send("No music in queue. Queue is empty")

    @commands.command(name="clear", aliases=["c"], help="stop the music and clears the queue")
    async def clear(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            if self.vc is not None and self.is_playing:
                self.vc.stop()
            self.music_queue = []
            await ctx.send("Music queue cleared")

    @commands.command(name="stop", aliases=["st"], help="stop the music and clears the queue")
    async def stop(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            if self.vc is not None and self.is_playing:
                self.vc.stop()
            self.music_queue = []

    @commands.command(name="disconnect", aliases=["dc", "leave", "d"], help="Kick the bot from voice channel")
    async def dc(self, ctx):
        if self.is_present(ctx) is True:
            await ctx.send("You're not connected to the voice channel to use these commands")
        else:
            self.is_playing = False
            self.is_paused = False
            await self.vc.disconnect()


async def setup(bot):
    await bot.add_cog(music(bot))
