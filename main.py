import os
import asyncio
import discord
from discord.ext import commands
try:
    from TikTokLive import TikTokLiveClient  # type: ignore
except ImportError:  # pragma: no cover - provide a clear runtime error if missing
    TikTokLiveClient = None
    print("Warning: TikTokLive library not found. Install with 'pip install TikTokLive' to enable TikTok checks.")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TIKTOK_USER = os.getenv("TIKTOK_USER")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

avisou = False

async def verificar_live():
    global avisou

    await bot.wait_until_ready()

    while not bot.is_closed():
        if TikTokLiveClient is None:
            avisou = False
            print("TikTokLiveClient unavailable; skipping check.")
        else:
            client = TikTokLiveClient(unique_id=TIKTOK_USER)

            try:
                await client.connect()

                if not avisou:
                    canal = bot.get_channel(CHANNEL_ID)
                    await canal.send(
                        f"🔴 **LIVE ABERTA NO TIKTOK!**\n"
                        f"https://www.tiktok.com/@{TIKTOK_USER}/live"
                    )
                    avisou = True

                await client.disconnect()

            except Exception:
                avisou = False
                print("Não está em live.")

        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    bot.loop.create_task(verificar_live())

bot.run(DISCORD_TOKEN)