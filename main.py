import discord
from decouple import config
from discord.ext import commands

from fonctions import *

client = commands.Bot(command_prefix='!')

big_list = [all_colles_dict(i) for i in range(1, 14)]
big_dico = dict(zip(list(range(1, 14)), big_list))


@client.event
async def on_ready():
    print('Connected as {}'.format(client.user))


@client.command()
async def ds(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/800044073158574093/927653423229329448/unknown.png")


@client.command()
async def c(ctx, *arg):
    """Affiche les deux prochaines colles du groupe choisi, vous pourrez ainsi réviser votre cours dans les
    meilleures conditions :)"""
    if not arg[0].isdigit() or int(arg[0]) > 13:
        await ctx.send(r"¯\_(ツ)_/¯")
        return
    group = int(arg[0])

    embed = discord.Embed(
        title=f"Prochaines colles",
        color=discord.Color.random())
    embed.set_footer(text=f"Groupe {group}")

    colles = find_next_two_colles(big_dico[group])
    for colle in colles:
        matiere, jour, heure, prof, salle, next_week = colle["matiere"], colle["day"], colle["start_hour"], colle[
            "name"], colle["room"], colle["next_week"]
        embed.add_field(
            name=matiere + (" | semaine prochaine" if next_week else ""),
            value=f"{jour[0].upper() + jour[1:]} {heure} en {salle} avec {prof}",
            inline=False)
    await ctx.send(embed=embed)


client.run(config("TOKEN"))
