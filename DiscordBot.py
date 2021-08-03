from imageai.Classification.Custom import CustomImageClassification
import discord
import requests
import shutil
import os

client = discord.Client()
filepath = os.getcwd()

detector = CustomImageClassification()
detector.setModelTypeAsInceptionV3()

detector.setModelPath(filepath + "\\Anime3\\models\\model_ex-073_acc-0.996815.h5")
detector.setJsonPath(filepath+ "\\Anime3\\json\\model_class.json")

@client.event
async def on_ready():
    detector.loadModel(num_objects=2)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.author.avatar_url)
    link = message.author.avatar_url

    response = requests.get(link, stream=True)

    filename = filepath +"test.jpg"

    with open(filename, 'wb') as img:
        shutil.copyfileobj(response.raw, img)
        print ("Downloaded Discord pfp to:", filename)
    del response

    predictions, probabilities = detector.classifyImage(filepath, result_count=2)

    #if message.content.startswith('$hello'):
        #await message.channel.send('Hello!')

client.run('')