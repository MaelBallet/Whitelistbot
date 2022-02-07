# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WHITELIST_ROLE_NAME = "Whitelisted"


bot = commands.Bot(command_prefix='!!', intents=discord.Intents.all())
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(pass_context=True)
@commands.has_role("Admin") # This must be exactly the name of the appropriate role
async def whitelist(ctx):
    channel = bot.get_channel(482465586925010944)
    messages = await ctx.channel.history(limit=1000).flatten()
    names_list = set()
    Already_whitelisted_list = set()
    word = '20 invites'
    for msg in messages:
        if word in msg.content:
            if msg.mentions:
                names_list.add(msg.mentions[0])

    with open("whitelisted.txt", "a") as file:
        for name in names_list:
            if str(name) not in open('whitelisted.txt').read():
                file.write(f'{name}\n')
                var = discord.utils.get(ctx.guild.roles, name = WHITELIST_ROLE_NAME)
                await name.add_roles(var)
            else:
                Already_whitelisted_list.add(name)

        for whitelisted in Already_whitelisted_list:
            names_list.remove(whitelisted)

    if names_list:
        await channel.send(' '.join(name.mention for name in names_list) + ' added to Whitelist') 
    else:
        await channel.send('No one added to Whitelist')

@bot.command(pass_context=True)
@commands.has_role("Admin") # This must be exactly the name of the appropriate role
async def whitelist_remove(ctx, member: discord.Member):
    channel = bot.get_channel(482465586925010944)
    Deleted = False
    with open("whitelisted.txt", "r") as f:
        lines = f.readlines()
    with open("whitelisted.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != str(member):
                f.write(line)
            else:
                Deleted = True
                var = discord.utils.get(ctx.guild.roles, name = WHITELIST_ROLE_NAME)
                await member.remove_roles(var)
                await channel.send(member.mention + ' deleted from Whitelist')
    if not Deleted:
        await channel.send('User not found in the Whitelist')

@bot.command(pass_context=True)
@commands.has_role("Admin") # This must be exactly the name of the appropriate role
async def whitelist_add(ctx, member: discord.Member):
    channel = bot.get_channel(482465586925010944)

    with open("whitelisted.txt", "a") as f:
        if str(member) not in open('whitelisted.txt').read():
            f.write(f'{str(member)}\n')
            var = discord.utils.get(ctx.guild.roles, name = WHITELIST_ROLE_NAME)
            await member.add_roles(var)
            await channel.send(member.mention + ' added to the Whitelist')
        else:
            await channel.send(member.mention + ' already in the Whitelist')

@commands.Cog.listener()
async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    """A global error handler cog."""

    if isinstance(error, commands.CommandNotFound):
        return  # Return because we don't want to show an error for every command not found
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        message = "Something about your input was wrong, please check your input and try again!"
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.send(message, delete_after=5)
    await ctx.message.delete(delay=5)

@bot.command(pass_context=True)
async def help(ctx):
    channel = bot.get_channel(482465586925010944)
    embed = discord.Embed(
        color = discord.Color.red()
    )
    embed.set_author(name='Help')
    embed.add_field(name='!!whitelist', value = 'Whitelist all users with 20 or more invites', inline=False)
    embed.add_field(name='!!whitelist_remove @user', value = 'Remove specified user from Whitelist', inline=False)
    embed.add_field(name='!!whitelist_add @user', value = 'Add specified user to Whitelist', inline=False)
    await channel.send(embed=embed)


bot.run(TOKEN)