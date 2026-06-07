import os
import asyncio
import importlib.util
import discord
from discord.ext import commands

load_dotenv = None
if importlib.util.find_spec("dotenv") is not None:
    load_dotenv = importlib.import_module("dotenv").load_dotenv

if load_dotenv is not None:
    load_dotenv(".env")

from TikTokLive import TikTokLiveClient

TOKEN = os.getenv("DISCORD_TOKEN")
print("CHANNEL_ID:", os.getenv("CHANNEL_ID"))
print("TIKTOK_USER:", os.getenv("TIKTOK_USER"))

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TIKTOK_USER = os.getenv("TIKTOK_USER")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

avisou = False


async def verificar_live():
    global avisou

    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            client = TikTokLiveClient(unique_id=TIKTOK_USER)

            esta_live = await client.is_live()

            if esta_live:
                if not avisou:
                    canal = bot.get_channel(CHANNEL_ID)

                    if canal:
                        await canal.send(
                            f"🔴 LIVE ABERTA NO TIKTOK!\n"
                            f"https://www.tiktok.com/@{TIKTOK_USER}/live"
                        )

                    avisou = True
            else:
                avisou = False
                print("Não está em live.")

        except Exception as e:
            avisou = False
            print(f"Erro ao verificar live: {e}")

        await asyncio.sleep(60)


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

    if not hasattr(bot, "live_task"):
        bot.live_task = asyncio.create_task(verificar_live())


bot.run(TOKEN)