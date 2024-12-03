import discord
from discord.ext import commands
import os

# docker-composeから渡された環境変数の設定
TOKEN = os.getenv("TOKEN")
GUILDS = [int(v) for v in os.getenv("GUILDS").split(",")]
# intentsの設定（エラーが出るまで基本defaultで良いです）
intents = discord.Intents.default()

# debug_guildsは公開BOTの場合は必要ないです
bot = commands.Bot(
    # debug_guilds=GUILDS,
    intents=intents
)


# botが動いてるか確認するだけのヤツ
@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


# cogsディレクトリにあるsub.pyを読み込む処理です
bot.load_extensions(
    "cogs.sub",
    # "cogs.hoge", # 複数読み込む場合は並べてかけます
    store=False,  # cog読み込み中にエラーが起きた時に止まる様に設定しています。
)
# botの起動
bot.run(TOKEN)
