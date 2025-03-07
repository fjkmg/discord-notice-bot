import io
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option, SlashCommandOptionType
import pprint


# main.pyで読み込ませるためのCogを継承したクラスを作成します。
class SubCog(commands.Cog):
    def __init__(self, bot):
        print("start sub init")
        self.bot = bot

    # comというコマンドグループを定義します
    com = SlashCommandGroup("com", "comコマンドのグループ")

    # comというコマンドグループにhelloコマンドを定義します
    @com.command(name="hello", description="挨拶するだけのコマンド")
    async def hello(
        self,
        ctx: discord.ApplicationContext,
        # name引数を受け取る様に設定します。
        name,
    ):
        # 引数の段階だと型がstr型かわかりにくいので注釈をつけてます
        name: str = name
        # 名前にさんづけしてこんにちはするだけの処理
        await ctx.response.send_message(f"{name}さん、こんにちは！")

    @com.command()
    async def status(self, ctx, member: discord.Member):
        await ctx.response.send_message(str(member.status))

    # サーバー内のメンバー一覧のcsvを書き出すコマンド
    @commands.slash_command()
    async def memberlist(self, ctx):
        csv_list = []
        members: list = ctx.guild.members
        role_names: list = [role.name for role in ctx.guild.roles]
        print(f"roles: {role_names}")
        print(f"number of guild member: {len(members)}")
        csv_list.append(
            [
                "joined_at",
                "id",
                "display_name",
                "name",
                "discriminator",
                "global_name",
                "nick",
                "bot",
                "mention",
                "display_avatar",
                "jump_url",
            ]
            + role_names
        )
        csv_list += [
            [
                m.joined_at.astimezone(ZoneInfo("Asia/Tokyo")).strftime(
                    "%Y/%m/%d %H:%M:%S"
                ),
                m.id,
                m.display_name,
                m.name,
                m.discriminator,
                m.global_name,
                m.nick,
                m.bot,
                m.mention,
                m.display_avatar,
                m.jump_url,
            ]
            + [
                role_name if role_name in {m_role.name for m_role in m.roles} else ""
                for role_name in role_names
            ]
            for m in members
        ]
        print(csv_list)

        # textファイルとして送信
        with io.StringIO() as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)
            file.seek(0)
            await ctx.response.send_message(file=discord.File(file, "memberlist.csv"))


# main.pyのload_extensionsのが実行する実際の関数を定義します
def setup(bot):
    bot.add_cog(SubCog(bot))  # add_cog関数にSubCogのインスタンスを渡します
