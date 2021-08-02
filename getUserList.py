#By Jakob Coughlan
#7/25/2021
import twitter
import requests
import shutil
import time
import os

apiKey = ''
apiKeySecret = ''
accessToken = ''
accessTokenSecret = ''

api = twitter.Api(consumer_key=apiKey,
                  consumer_secret=apiKeySecret,
                  access_token_key=accessToken,
                  access_token_secret=accessTokenSecret)
# Funimation, DisneyXD, kianamaiart
user = "Crunchyroll"
filepath = os.getcwd()+"\\pfp\\pfp"
print("Get follow list from:"+user)

print(time.ctime())
#time.sleep(450)

cursorIteration = 0
cursorMax = 1
u2List = api.GetFollowersPaged(screen_name = user, cursor = '1706435805575181265')
nextCursor = u2List[0]
print(nextCursor)
uList = u2List[2]
print(uList)

while (cursorIteration < cursorMax):

    for r in uList:

        username = getattr(r,'screen_name')
        link = getattr(r,'profile_image_url')
        link = link.replace('normal', '400x400')
        print("page:"+ str(cursorIteration)+ " " + username + " " + link)

        filename = filepath + "\\" + username + ".jpg"
        response = requests.get(link, stream=True)

        with open(filename, 'wb') as img:
            shutil.copyfileobj(response.raw, img)
            print ("Downloaded twitter avatar to", filename)
        del response

    print(nextCursor)
    cursorIteration =+ 1
    if nextCursor == 0:
        break


print("done")

