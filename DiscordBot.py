from imageai.Classification.Custom import CustomImageClassification
import requests
import shutil
import os
import json
import discord

from discord.ext import commands

#client = discord.Client()
filepath = os.getcwd()
jsonLocation = filepath + "\\BotConfig.json"
whitelistLocation = filepath + "\\Whitelist.json"

detector = CustomImageClassification()
detector.setModelTypeAsInceptionV3()

detector.setModelPath(filepath + "\\Anime3\\models\\model_ex-073_acc-0.996815.h5")
detector.setJsonPath(filepath+ "\\Anime3\\json\\model_class.json")
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
client = commands.Bot(intents = intents, command_prefix=['-'])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global aggresion
    if message.author == client.user:
        return

    await client.process_commands(message)


    if not(message.content.startswith('-check')) and \
            not(aggresion == "0") and \
            not onWhitelist(message.author) and \
            (checkForAnimePFP(message.author)):
        if(aggresion == "1"):
            await message.channel.send("BANNED")
        if(aggresion == "2"):
            await message.channel.send("Kicked :3")
            await message.author.kick(reason = "Anime PFP")
        if(aggresion == "3"):
            await message.channel.send("BANNED")
            await message.author.ban(reason="Anime PFP")


    #if message.content.startswith('$hello'):
        #await message.channel.send('Hello!')

@client.command(pass_context=True)
async def check(ctx,*users):

    #all I feel is pain, so much PAIN
    t = ""
    for r in users:
        t = t + str(r) + " "
    t = t[:-1]
    print("COMPLETED:"+t)
    if(users):
        for user in users:
            for guild in client.guilds:
                for member in guild.members:
                    print(t)
                    print(user)
                    print(member.name)
                    if(str(member.name) == str(user)) or (str(member) == str(user)) or (t == str(member.name) or (t == str(member))):
                        print("FOUND")
                        if(checkForAnimePFP(member)):
                            await ctx.send(member.name + " appears to have an anime profile picture. \n\nthey should fix that.")
                        else:
                            await ctx.send(member.name + " does not appear to have an Anime Profile Picture")
                        return
            await ctx.send("could not find "+"".join(users))
            return

    if(checkForAnimePFP(ctx.message.author)):
        await ctx.send("you appear to have an anime profile picture. \n\nyou should fix that.")
    else:
        await ctx.send("you do not appear to have an Anime Profile Picture")

@client.command(pass_context = True)
async def analyze(ctx, link):

    #tries to download a picture from the internet, if it can't it responds no image found and returns
    try:
        response = requests.get(link, stream=True)
        filename = filepath +"\\analyze.jpg"

        with open(filename, 'wb') as img:
            shutil.copyfileobj(response.raw, img)
            print ("Downloaded image:", filename)
    except:
        await ctx.send("No image found")
        return
    del response

    predictions, probabilities = detector.classifyImage(filename, result_count = 2)

    #stupid formating garbage
    words ="Analysis"
    num = True
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction , " : " , eachProbability)
        if num:
            words = words + "\n**"+ str(eachPrediction) + "** : " + str(eachProbability)[:3] + "%"
            num = not num
        else:
            words = words + "\n"+ str(eachPrediction) + " : " + str(eachProbability)[:3] + "%"

    await ctx.send(words)

@client.command(pass_context=True)
async def aggression(ctx, number):
    global aggresion

    if number == aggresion:
        await ctx.send(number + " is the current aggression level")
        return
    elif number == "0":
        aggresion = number
        await ctx.send("aggression set to: 0\n Anti-Anime-Automata will ignore all profile pictures")
    elif number == "1":
        aggresion = number
        await ctx.send("aggression set to: 1\n Anti-Anime-Automata will reply with snyde comments")
    elif number == "2":
        aggresion = number
        await ctx.send("aggression set to: 2\n Anti-Anime-Automata will kick all offenders")
    elif number == "3":
        aggresion = number
        await ctx.send("aggression set to: 3\n Anti-Anime-Automata will BAN all offenders")
    else:
        await ctx.send("Not a valid input. Try a number from 0 to 3")
    saveConfig()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vigilence lvl " + number))
    return

@client.command(pass_context=True)
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
async def whitelist(ctx, user):
    for guild in client.guilds:
        for member in guild.members:
            print(member)
    return

@client.command(pass_context=True)
async def unwhitelist(ctx, user):
    pass

@client.command(pass_context=True)
async def whitelistlist(ctx):
    global whitelistusers
    listof = ""
    for x in whitelistusers:
        listof = listof + x + "\n"

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

    filename = filepath +"\\test.jpg"

    with open(filename, 'wb') as img:
        shutil.copyfileobj(response.raw, img)
        print ("Downloaded Discord pfp to:", filename)
    del response

    predictions, probabilities = detector.classifyImage(filename, result_count = 2)

    print("results for:" + testUser.name)
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction , " : " , eachProbability)
        if(eachPrediction == "anime" and eachProbability > 60):
            return True
    return False

def onWhitelist(testUser):
    if not enableWhitelist:
        return False

    global whitelistusers
    print ("checking on whitelist")
    for x in whitelistusers:
        if x == testUser:
            return True
    return False


client.run('')