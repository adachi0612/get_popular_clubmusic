import logging
import os
import random
import traceback

import discord
from discord import app_commands
from dotenv import load_dotenv
from googleapiclient.discovery import build

# from youtube_search_experiment import Fetch_Youtube_Links

# ログ設定を追加
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv('YOUTUBE_DATA_APIKEY')

# デバッグ用：環境変数の確認
print(f"Discord Token exists: {bool(DISCORD_TOKEN)}")
print(f"YouTube API Key exists: {bool(YOUTUBE_API_KEY)}")

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

if not DISCORD_TOKEN:
    raise ValueError("Discord Bot Token is not set. Please set the DISCORD_BOT_TOKEN environment variable.")

# Message Content Intentを追加
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を読み取るために必要

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# 簡単なYouTube検索関数を追加（Fetch_Youtube_Linksの代替）
def search_youtube_video(query, max_results):
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video'
    )
    response = request.execute()
    links = []
    for item in response.get('items', []):
        video_id = item['id'].get('videoId')
        if video_id:
            links.append(f"https://www.youtube.com/watch?v={video_id}")

    random_link = random.choice(links) if links else None
    return random_link


@bot.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == bot.user:
        return

    # 手動でスラッシュコマンドをテスト（デバッグ用）
    if message.content.startswith('/search ') or message.content.startswith('/search　'):
        query = message.content[8:]  # '/search 'の後の部分を取得
        await message.channel.send(f"波菜だけ見てて!")

        link = search_youtube_video(query, max_results=1)
        if link:
            await message.channel.send(f"🔎 検索ワード: `{query}` で以下の動画が見つかりました! \n🎬 {link}")
        else:
            await message.channel.send("動画が見つかりませんでした。")

        # 手動でスラッシュコマンドをテスト（デバッグ用）
    if message.content.startswith('/random ') or message.content.startswith('/random　'):
        query = message.content[8:]  # '/random 'の後の部分を取得
        await message.channel.send(f"波菜だけ見てて!")

        link = search_youtube_video(query, max_results=50)
        if link:
            await message.channel.send(f"🔎 検索ワード: `{query}` で以下の動画が見つかりました! \n🎬 {link}")
        else:
            await message.channel.send("動画が見つかりませんでした。")

    # デバッグ用：メッセージを受信したことをログに出力
    print(f"Message received: {message.content} from {message.author}")

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    print(f"Bot is in {len(bot.guilds)} guilds")

    # ギルド情報を詳細表示
    for guild in bot.guilds:
        print(f"Guild: {guild.name} (ID: {guild.id})")

    try:
        # グローバルコマンドとして同期
        synced = await tree.sync()
        print(f"Synced {len(synced)} global command(s)")
        print(f"Commands: {[cmd.name for cmd in synced]}")

        # 各ギルドに対してもコマンドを同期（テスト用）
        for guild in bot.guilds:
            try:
                guild_synced = await tree.sync(guild=guild)
                print(f"Synced {len(guild_synced)} command(s) to guild {guild.name}")
            except Exception as guild_error:
                print(f"Failed to sync commands to guild {guild.name}: {guild_error}")

    except Exception as e:
        print(f"Failed to sync commands: {e}")
        print(traceback.format_exc())

# エラーハンドリングを追加
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in event {event}:")
    print(traceback.format_exc())

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"App command error: {error}")
    print(traceback.format_exc())
    if not interaction.response.is_done():
        await interaction.response.send_message("エラーが発生しました。", ephemeral=True)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)