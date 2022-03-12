from imageai.Classification.Custom import CustomImageClassification
from discord.utils import get
from pathlib import Path
import requests
import shutil
import json
import discord

from discord.ext import commands

filepath = Path()
jsonLocation = filepath / "BotConfig.json"
whitelistLocation = filepath / "Whitelist.json"
keyLocation = filepath / "key.txt"

detector = CustomImageClassification()
detector.setModelTypeAsInceptionV3()

detector.setModelPath(filepath / "model_ex-073_acc-0.996815.h5")
detector.setJsonPath(filepath / "model_class.json")
detector.loadModel(num_objects=2)

config = json.load(open(jsonLocation))
aggresion = config['Agression']
channelLogging = config['Channel Logging']
channelLoggingChannel = config['Channel Logging Channel']
saveBans = config['Save Bans to Disk']
savedBansLocation = config['Saved Bans Location']
enableWhitelist = config['Enable Whitelist']

whitelistusers = json.load(open(whitelistLocation))

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix=['-'])


@client.event
async def on_ready():
    global aggresion
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Vigilence lvl " + aggresion))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global aggresion

    if message.author == client.user:
        return

    await client.process_commands(message)

    if not (message.content.startswith('-check')) and \
            not (aggresion == "0") and \
            not onWhitelist(message.author) and \
            (checkForAnimePFP(message.author)):
        if aggresion == "1":
            await message.channel.send("BANNED")
        if aggresion == "2":
            print(message.channel)
            if message.channel != "anime-quarantine":
                await message.channel.send(str(message.author) + " has been quarantined")
                role = get(message.guild.roles, name="Anime PFP")
                await message.author.add_roles(role)
        if aggresion == "3":
            await message.channel.send("Kicked :3")
            await message.author.kick(reason="Anime PFP")
        if aggresion == "4":
            await message.channel.send(str(message.author) + ": BANNED")
            await message.author.ban(reason="Anime PFP")


@client.command(pass_context=True)
async def check(ctx, *users):
    # all I feel is pain, so much PAIN
    # combines all arguments into a single thing to search
    # solves the issue of searching for a user with a space in the name
    t = ""
    for r in users:
        t = t + str(r) + " "
    t = t[:-1]
    print("COMPLETED:" + t)

    # this checks if what was enter was an @. when someone puts an @ it sends it to this method as
    # <@!xxxxxxxxxxxxxxxxxx> so it detects when a search has the starting
    # <@! and ends with >. Is this the worse way to do it? probably. an issue with the commands is
    # you cannot overload methods. So I must live in jank
    if t[:3] == "<@!" and t[-1] == ">":
        t = t[3:-1]
        print(t)
    if users:
        for user in users:
            for guild in client.guilds:
                for member in guild.members:
                    if str(member.name) != str(user) and str(member) != str(user) and t != str(
                            member.name) and t != str(member) and t != str(member.id) and t != str(
                            member.nick):
                        continue
                    # print(t)
                    # print(user)
                    # print(member.name)
                    # print(member.id)
                    print("FOUND")
                    if checkForAnimePFP(member):
                        await ctx.send(
                            member.name + " appears to have an anime profile picture. \n\nthey should fix that.")
                    else:
                        await ctx.send(member.name + " does not appear to have an Anime Profile Picture")
                    return
            await ctx.send("could not find " + "".join(users))
            return

    if checkForAnimePFP(ctx.message.author):
        await ctx.send("you appear to have an anime profile picture. \n\nyou should fix that.")
    else:
        await ctx.send("you do not appear to have an Anime Profile Picture")
        for role in ctx.guild.roles:
            if role.name == "Anime PFP":
                role = get(ctx.message.guild.roles, name='Anime PFP')
                await ctx.message.author.remove_roles(role)


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def bancheck(ctx, *users):
    # all I feel is pain, so much PAIN
    # combines all arguments into a single thing to search
    # solves the issue of searching for a user with a space in the name
    t = ""
    for r in users:
        t = t + str(r) + " "
    t = t[:-1]
    print("COMPLETED:" + t)

    # this checks if what was enter was an @. when someone puts an @ it sends it
    # to this method as <@!xxxxxxxxxxxxxxxxxx> so it detects when a search has the starting
    # <@! and ends with >. Is this the worse way to do it? probably. an issue with the commands
    # is you cannot overload methods. So I must live in jank
    if t[:3] == "<@!" and t[-1] == ">":
        t = t[3:-1]
        print(t)
    if users:
        for user in users:
            for guild in client.guilds:
                for member in guild.members:
                    if str(member.name) != str(user) and str(member) != str(user) and t != str(
                            member.name) and t != str(member) and t != str(member.id) and t != str(
                            member.nick):
                        continue
                    # print(t)
                    # print(user)
                    # print(member.name)
                    # print(member.id)
                    print("FOUND")
                    if checkForAnimePFP(member):
                        await ctx.send(
                            member.name + " appears to have an anime profile picture. and will be banned.")
                        await ctx.guild.ban(member, reason="Anime PFP")
                    else:
                        await ctx.send(
                            member.name + " does not appear to have an Anime Profile Picture and will bot be banned")
                    return
            await ctx.send("could not find " + "".join(users))
            return

    if checkForAnimePFP(ctx.message.author):
        await ctx.send("you appear to have an anime profile picture. \n\nyou should fix that.")
    else:
        await ctx.send("you do not appear to have an Anime Profile Picture")


@client.command(pass_context=True)
async def checkall(ctx):
    for guild in client.guilds:
        for member in guild.members:
            if checkForAnimePFP(member):
                await ctx.send(member.name + " has an Anime Profile Picture")

    return


@client.command(pass_context=True)
async def analyze(ctx, *link):
    words = "Analysis of"

    if ctx.message.attachments:
        aLink = ctx.message.attachments[0].url
        words = words + " attachment"
    else:
        aLink = link[0]
        words = words + " URL"
    # tries to download a picture from the internet, if it can't it responds no image found and returns
    try:
        response = requests.get(aLink, stream=True)
        filename = filepath / "analyze.jpg"

        with open(filename, 'wb') as img:
            shutil.copyfileobj(response.raw, img)
            print("Downloaded image:", filename)
    except:
        await ctx.send("No image found")
        return
    del response

    predictions, probabilities = detector.classifyImage(filename, result_count=2)

    # stupid formating garbage

    num = True
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction, " : ", eachProbability)
        eachProbability = eachProbability / 100
        if num:
            words = words + f"\n**{eachPrediction}**: {eachProbability:.2%}"
            num = not num
        else:
            words = words + f"\n{eachPrediction}: {eachProbability:.2%}"

    await ctx.send(words)


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def aggression(ctx, number):
    global aggresion

    if number == aggresion:
        await ctx.send(number + " is the current aggression level")
        return
    elif number == "0":
        aggresion = number
        await ctx.send("aggression set to: " + number + "\nAnti-Anime-Automata will ignore all profile pictures")
    elif number == "1":
        aggresion = number
        await ctx.send("aggression set to: " + number + "\nAnti-Anime-Automata will reply with snyde comments")
    elif number == "2":
        aggresion = number
        await ctx.send("aggression set to: " + number + "\nAnti-Anime-Automata will quarantine all offenders")
    elif number == "3":
        aggresion = number
        await ctx.send("aggression set to: " + number + "\nAnti-Anime-Automata will kick all offenders")
    elif number == "4":
        aggresion = number
        await ctx.send("aggression set to: " + number + "\nAnti-Anime-Automata will BAN all offenders")
    else:
        await ctx.send("Not a valid input. Try a number from 0 to 4")
        return
    saveConfig()
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Vigilence lvl " + number))
    return


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def enablewhitelist(ctx, value):
    global enableWhitelist
    if value == "True":
        await ctx.send("Whitelist: enabled")
        enableWhitelist = True
        saveConfig()
    elif value == "False":
        await ctx.send("Whitelist: disabled")
        enableWhitelist = False
        saveConfig()
    else:
        await ctx.send("not a valid input. Enter 'True' or 'False'")
    print(config['Enable Whitelist'])


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def whitelist(ctx, *users):
    global whitelistusers
    t = ""
    for r in users:
        t = t + str(r) + " "
    t = t[:-1]
    # print("COMPLETED:"+t)

    # this checks if what was enter was an @. when someone puts an @ it sends it to this method as
    # <@!xxxxxxxxxxxxxxxxxx> so it detects when a search has the starting <@! and ends with >. Is this the worse way
    # to do it? probably. an issue with the commands is you cannot overload methods. So I must live in jank
    if t[:3] == "<@!" and t[-1] == ">":
        t = t[3:-1]
        print(t)
    if users:
        for user in users:
            for guild in client.guilds:
                for member in guild.members:
                    if (str(member.name) == str(user)) or (str(member) == str(user)) or (
                            t == str(member.name) or (t == str(member)) or t == str(member.id)):
                        for x in whitelistusers:
                            if x == member.id:
                                await ctx.send(member.name + " is already whitelisted")
                                return
                        whitelistusers.append(member.id)
                        print(member.name + "(" + str(member.id) + ") has been added to the whitelist")
                        await ctx.send(member.name + " has been added to the whitelist")
                        with open(whitelistLocation, 'w') as outfile:
                            json.dump(whitelistusers, outfile)
                        return
    await ctx.send("Could not find user to add to whitelist")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unwhitelist(ctx, *users):
    global whitelistusers
    t = ""
    for r in users:
        t = t + str(r) + " "
    t = t[:-1]
    # print("COMPLETED:"+t)

    # this checks if what was enter was an @. when someone puts an @ it sends it to this method as
    # <@!xxxxxxxxxxxxxxxxxx> so it detects when a search has the starting <@! and ends with >. Is this the worse way
    # to do it? probably. an issue with the commands is you cannot overload methods. So I must live in jank
    if t[:3] == "<@!" and t[-1] == ">":
        t = t[3:-1]
        print(t)
    if users:
        for user in users:
            for guild in client.guilds:
                for member in guild.members:
                    if (str(member.name) == str(user)) or (str(member) == str(user)) or (
                            t == str(member.name) or (t == str(member)) or t == str(member.id)):
                        for x in whitelistusers:
                            if (x == member.id):
                                whitelistusers.remove(x)
                                await ctx.send(member.name + " has been removed from the whitelist")
                                print(member.name + "(" + str(member.id) + ") has been removed from the whitelist")
                                with open(whitelistLocation, 'w') as outfile:
                                    json.dump(whitelistusers, outfile)
                                return
                        await ctx.send(member.name + " is not on the whitelist")
                        return
    await ctx.send("Could not find user to remove from whitelist")


@client.command(pass_context=True)
async def whitelistlist(ctx):
    global whitelistusers
    listof = "**Whitelist**\n"
    for x in whitelistusers:
        listof = listof + str(client.get_user(x).name) + "\n"

    await ctx.send(listof)
    return


def saveConfig():
    global aggresion
    global channelLogging
    global channelLoggingChannel
    global saveBans
    global savedBansLocation
    global enableWhitelist
    config['Agression'] = aggresion
    config['Channel Logging'] = channelLogging
    config['Channel Logging Channel'] = channelLoggingChannel
    config['Save Bans to Disk'] = saveBans
    config['Saved Bans Location'] = savedBansLocation
    config['Enable Whitelist'] = enableWhitelist

    with open(jsonLocation, 'w') as outfile:
        json.dump(config, outfile)
    print("saved json")


def checkForAnimePFP(testUser):
    print(testUser)
    print(testUser.avatar_url)
    link = testUser.avatar_url

    response = requests.get(link, stream=True)

    filename = filepath / "test.jpg"

    with open(filename, 'wb') as img:
        shutil.copyfileobj(response.raw, img)
        print("Downloaded Discord pfp to:", filename)
    del response

    predictions, probabilities = detector.classifyImage(filename, result_count=2)

    print("results for:" + testUser.name)
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction, " : ", eachProbability)
        if eachPrediction == "anime" and eachProbability > 60:
            return True
    return False


def onWhitelist(testUser):
    if not enableWhitelist:
        return False

    global whitelistusers
    for x in whitelistusers:
        if x == testUser.id:
            print(testUser.name + " is on the whitelist")
            return True
    return False


with open(keyLocation) as k:
    key = k.readline()
client.run(str(key))
