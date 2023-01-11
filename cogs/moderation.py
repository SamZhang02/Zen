import discord
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.utils import get
 
class Moderation(commands.Cog, description="Moderation commands."):
    
    def __init__(self, client: commands.Bot):
        self.client = client
        
    def moderation_embed(self, ctx: commands.Context) -> discord.Embed:
        embed = discord.Embed(title="Zen | Moderation", color=ctx.author.color, timestamp=datetime.now())
        return embed

    async def cog_command_error(self, ctx: commands.Context, error: str):
        embed = self.moderation_embed(ctx)
        if isinstance(error, Exception):
            embed.description = str(error).capitalize()
            return await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation module has been loaded.")

    @commands.command(aliases=["clear", "clearm", "deletemessage", "deletem", "purge"])
    async def clearmessage(self, ctx: commands.Context, amount: int = 20, member: discord.Member = None):
        embed = self.moderation_embed(ctx)
        if member is None:
            await ctx.channel.purge(limit=amount+1)
            embed.description = f"Cleared `{amount}` messages in {ctx.channel.mention}!"
            await ctx.send(embed=embed, delete_after=15)
        else:
            await ctx.channel.purge(limit=amount+1, check=lambda x: x.author.id == member.id)
            embed.description = f"Cleared all messages sent by {member.mention} in {ctx.channel.mention} in the last {amount} messages!"
            await ctx.send(embed=embed, delete_after=15)

    @commands.command()
    async def warn(self, ctx: commands.Context, member: discord.Member, *, message: str):
        embed = self.moderation_embed(ctx)
        embed.title = "Zen | Warning"
        embed.add_field(name="Message", value=f"**{message}**")
        embed.set_footer(text=f"You have been warned by {ctx.author.name}", icon_url=ctx.author.avatar)
        await member.send(embed=embed)

    @commands.command()
    async def lockchannel(self, ctx: commands.Context):
        embed = self.moderation_embed(ctx)
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed.description = f"Locked {ctx.channel.mention}"
        await ctx.send(embed=embed)

    @commands.command()
    async def unlockchannel(self, ctx: commands.Context):
        embed = self.moderation_embed(ctx)
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed.description = f"Unlocked {ctx.channel.mention}"
        await ctx.send(embed=embed)

    @commands.command()
    async def rolesetup(self, ctx: commands.Context, channel: discord.TextChannel):

        study_role = get(ctx.author.guild.roles, name="Study")
        movie_role = get(ctx.author.guild.roles, name="Movie")
        game_role = get(ctx.author.guild.roles, name="Game")
        vibe_role = get(ctx.author.guild.roles, name="Vibe")
        karaoke_role = get(ctx.author.guild.roles, name="Karaoke")

        description = "React with the emoji corresponding to the role you\'d like.\n\n"
        description += f"💚 | <@&{study_role.id}> - Study sessions\n"
        description += f"💛 | <@&{movie_role.id}> - Movie nights\n"
        description += f"💙 | <@&{game_role.id}> - Gaming\n"
        description += f"💜 | <@&{vibe_role.id}> - Vibe with others\n"
        description += f"🤎 | <@&{karaoke_role.id}> - Karaoke nights\n"

        embed = discord.Embed(title="List of available roles", description=description, color=discord.Color.from_rgb(248, 175, 175))
        message: discord.Message = await channel.send(embed=embed)
        await message.add_reaction("💚")
        await message.add_reaction("💛")
        await message.add_reaction("💙")
        await message.add_reaction("💜")
        await message.add_reaction("🤎")

async def setup(client):
    await client.add_cog(Moderation(client))