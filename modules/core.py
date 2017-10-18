#########################################
############# Core Commands #############
#########################################

from extra.config import *
from discord.ext import commands
from collections import Counter
from utils import checks, formats, db
from utils.paginator import HelpPaginator, CannotPaginate
from collections import OrderedDict, deque, Counter

#from .utils import checks, db

import utils.checks
import utils.db
import logging
import discord
import asyncio
import datetime
import traceback
import copy
import unicodedata
import inspect
import psutil
import os, datetime

log = logging.getLogger(__name__)

#########################################

class Core:
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(rest_is_raw = True, hidden = True, aliases = ['say'])
    async def echo(self, ctx, *, content):
        if ctx.author.id == bot_owner:
            await ctx.send(content)
            await ctx.message.delete()
        else:
            raise commands.NotOwner()

### Invite Bot Link Command ###
    @commands.command(no_pm = True, hidden = True, aliases = ['inv'])
    async def invite(self, ctx):
        embed = discord.Embed(title = f"**Invite {self.bot.user.name} to your server!**", description = f"You want to invite **Noëlla** to your server?\nThen you can use this link to invite him!\n\n[Click here to invite **{self.bot.user.name}**](https://discordapp.com/oauth2/authorize?client_id=357852849029513216&scope=bot&permissions=527952983)\n[Click here to join **{self.bot.user.name}'s** Dev Discord]({dev_discord})", color = embed_color)
        embed.set_thumbnail(url = self.bot.user.avatar_url)
        await ctx.send(embed = embed)

### Character Information Checker ###
    @commands.command(no_pm = True, hidden = True, aliases = ['char'])
    async def charinfo(self, ctx, *, characters: str):
        if len(characters) > 25:
            return await ctx.send(f'Too many characters ({len(characters)}/25)')

        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'

        await ctx.send('\n'.join(map(to_string, characters)))

### About This Bot Command ###
    @commands.command()
    async def about(self, ctx):
        """Tells you information about the bot itself."""
        cmd = r'git show -s HEAD~3..HEAD --format="[{}](https://github.com/exunious/Noella-Bot/commit/%H) %s (%cr)"'
        if os.name == 'posix':
            cmd = cmd.format(r'\`%h\`')
        else:
            cmd = cmd.format(r'`%h`')

        revision = os.popen(cmd).read().strip()
        embed = discord.Embed(description='⠀\n**Latest Changes**\n' + revision + '\n⠀')
        embed.set_thumbnail(url = self.bot.user.avatar_url)
        embed.title = 'Official Bot Server Invite'
        embed.url = dev_discord
        embed.colour = embed_color

        owner = self.bot.get_user(bot_owner)
        embed.set_author(name=str(owner), icon_url=owner.avatar_url)

        # statistics
        total_members = sum(1 for _ in self.bot.get_all_members())
        total_online = len({m.id for m in self.bot.get_all_members() if m.status is discord.Status.online})
        total_unique = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        embed.add_field(name='Members in Guilds', value=f'Total Users: **{total_members}**\nTotal Unique: **{total_unique}**\nTotal Online: **{total_online}**')
        embed.add_field(name='Channels in Guilds', value=f'Total Channels: **{text + voice}**\nText Channels: **{text}**\nVoice Channels: **{voice}**')

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')


        embed.add_field(name='Active in Guilds', value = len(self.bot.guilds))
        #embed.add_field(name='Commands Run', value=sum(self.bot.command_stats.values()))
        embed.add_field(name='Uptime', value=(self.getuptime()))
        embed.set_footer(text='writen in discord.py', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Core(bot))
