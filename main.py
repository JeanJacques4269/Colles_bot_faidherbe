import asyncio
import random
import discord
from decouple import config
from discord.ext import commands, tasks

from fonctions import *

client = commands.Bot(command_prefix='!')

# big_list = [all_colles_dict(i) for i in range(1, 14)]
# big_dico = dict(zip(list(range(1, 14)), big_list))

concours_time = datetime(2022, month=4, day=19, hour=8, tzinfo=pytz.timezone("Europe/Paris"))


@client.event
async def on_ready():
    print('Connected as {}'.format(client.user))


@client.command()
async def ds(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/800044073158574093/927653423229329448/unknown.png")


#
# @client.command()
# async def c(ctx, *arg):
#     """Affiche les deux prochaines colles du groupe choisi, vous pourrez ainsi réviser votre cours dans les
#     meilleures conditions :)"""
#     if not arg[0].isdigit() or int(arg[0]) > 13:
#         await ctx.send(r"¯\_(ツ)_/¯")
#         return
#     group = int(arg[0])
#
#     embed = discord.Embed(
#         title=f"Prochaines colles",
#         color=discord.Color.random())
#     embed.set_footer(text=f"Groupe {group}")
#
#     colles = find_next_two_colles(big_dico[group])
#     for colle in colles:
#         matiere, jour, heure, prof, salle, next_week = colle["matiere"], colle["day"], colle["start_hour"], colle[
#             "name"], colle["room"], colle["next_week"]
#         embed.add_field(
#             name=matiere + (" | semaine prochaine" if next_week else ""),
#             value=f"{jour[0].upper() + jour[1:]} {heure} en {salle} avec {prof}",
#             inline=False)
#     await ctx.send(embed=embed)

async def reminder():
    await client.wait_until_ready()
    while not client.is_closed():
        if is_time_between(time(20, 0), time(20, 1)):
            for guild in client.guilds:
                for channel in guild.text_channels:
                    if channel.name == "khôlles":
                        chan = channel
                        await chan.send(
                            "https://media.discordapp.net/attachments/709480777494298669/965299698925723708/unknown.png")
                        exit(0)
        await asyncio.sleep(10)


client.loop.create_task(reminder())
client.run(config("TOKEN"))
