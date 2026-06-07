import os
import asyncio
import discord
from discord.ext import commands
try:
    from TikTokLive import TikTokLiveClient  # type: ignore
except ImportError:  # pragma: no cover - provide a clear runtime error if missing
    TikTokLiveClient = None
    print("Warning: TikTokLive library not found. Install with 'pip install TikTokLive' to enable TikTok checks.")

TOKEN = os.getenv("DISCORD_TOKEN")
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
                task = asyncio.create_task(client.connect())
                await asyncio.sleep(8)
                if not task.done():
                    if not avisou:
                        canal = bot.get_channel(int(CHANNEL_ID))
                        if canal is not None:
                            await canal.send(
                                f"🔴 LIVE ABERTA NO TIKTOK!\n"
                                f"https://www.tiktok.com/@{TIKTOK_USER}/live"
                            )
                        avisou = True

                    task.cancel()
            except Exception as e:
                avisou = False
                print(f"Não está em live ou deu erro: {e}")
bot.run(TOKEN)