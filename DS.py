import asyncio
import logging
from translate import Translator

import pymorphy2
import discord
from discord.ext import commands

from config import DS_BOT_TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
morph = pymorphy2.MorphAnalyzer()
convert = {
    'nomn': 0,
    'gent': 1,
    'datv': 2,
    'accs': 3,
    'ablt': 4,
    'loct': 5,

}

language = 'ru'
translator = Translator(to_lang=language)


class RandomThings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send("""
        \n !#help_bot — для инструкций по работе команд бота
        \n !#set_lang — для смены языка (en-ru, ru-en, fr-ru и так далее)
        \n !#text — для ввода фразы для перевода
        """)

    @commands.command(name='set_lang')
    async def lang(self, ctx, lang):
        global language, translator
        language = lang.split('-')[1]
        translator = Translator(to_lang=language)
        await ctx.send(f'Переводить  на {language}')

    @commands.command(name='text')
    async def transl(self, ctx, *text):
        await ctx.send(translator.translate(' '.join(text)))


bot = commands.Bot(command_prefix='!#', intents=intents)

TOKEN = DS_BOT_TOKEN


async def main():
    await bot.add_cog(RandomThings(bot))
    await bot.start(TOKEN)


asyncio.run(main())
