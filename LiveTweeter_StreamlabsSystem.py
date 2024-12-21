#---------------------------------------
#    Import Libraries
#---------------------------------------
import json
import os
import time
import clr
import codecs
import sys, base64, zlib, collections


#---------------------------------------
#    [Required]    Script Information
#---------------------------------------
ScriptName = "LiveTweeter"
Website = "https://burnysc2.github.io" #Old
Description = "Tweet when going live"
Creator = "Burny & Brain & Patcha" # API v2.0
Version = "1.4.1" # API v2.0 (Login with API 1.1)

configFile = "settings.json"
settings = {
    "successfullyLoaded": False
}
tweetData = {}
scriptData = {
    "scriptEnabled": False,
    # for sending automatic tweets
    "timestampLiveSince": 0,
    "timestampOfflineSince": 0,
    "timestampTweetSent": 0, # info for periodic
    "twitterUsername": "",
    # for "tweet on game change"
    "lastGameChangeCheck": 0,
    "lastGameName": "",
    # for removing last tweet
    "lastTweetId": "",
    # for sending tweet URL in chat
    "messageInChatTimestamp": 0,
    "notificationsInChatRemaining": 0,
    "twitchMsg": "",
    "username" : "",
}


def Init():
    global settings, tweetData
    global TWITCH_CHANNEL_NAME # Workaround for BOT issue
    global TWITTER_CHANNEL_NAME # Workaround for Twitter Free API limits
    global eventTrigged, typeTrigged, timeTrigged, offTrigged

    path = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
        settings["successfullyLoaded"] = True
    except:
        return

    if "sliderNewTweetWaiting" not in settings:
        settings["sliderNewTweetWaiting"] = 0;
    eventTrigged = False
    typeTrigged = "normal"
    timeTrigged = time.time()

    # Workaround for BOT issue
    if "cbTwitchChannelName" in settings and settings["cbTwitchChannelName"] \
            and "txtTwitchChannelName" in settings and settings["txtTwitchChannelName"]:
        TWITCH_CHANNEL_NAME = settings["txtTwitchChannelName"]
    else:
        TWITCH_CHANNEL_NAME = Parent.GetChannelName()
        if not isinstance(TWITCH_CHANNEL_NAME, str):
            if "txtTwitchChannelName" in settings:
                TWITCH_CHANNEL_NAME = settings["txtTwitchChannelName"]
            else:
                TWITCH_CHANNEL_NAME = ""

    # Workaround for Twitter Free API limits
    TWITTER_CHANNEL_NAME = None

    tweetData = {
        "pathPython": settings["txtPathPython"].strip(),
        "pathScript": os.path.join(path, "TweetScript.py"),
        "pathScriptData": os.path.join(path, "scriptData", "scriptData.json"),
        "pathTweetMessage": os.path.join(path, "Tweet_Message.txt"),
        "pathTweetOnGameChange": os.path.join(path, "Tweet_OnGameChange.txt"),
        "pathTweetPeriodic": os.path.join(path, "Tweet_Periodic.txt"),
        "consumer_key": settings["txtConsumerKey"].strip(),
        "consumer_secret": settings["txtConsumerSecret"].strip(),
        "access_token": settings["txtAccessToken"].strip(),
        "access_token_secret": settings["txtAccessTokenSecret"].strip(),
    }

    # load normal tweet text
    if os.path.isfile(tweetData["pathTweetMessage"]):
        with codecs.open(tweetData["pathTweetMessage"], mode="r", encoding='utf-8-sig') as f:
            tweetData["normalTweetText"] = f.read().rstrip("\n")
    else:
        with codecs.open(tweetData["pathTweetMessage"], mode="w+", encoding='utf-8-sig') as f:
            f.write("I went live right now playing $game!\r\nTitle: $title\r\nMessage: $message\r\n\r\n$url")
        tweetData["normalTweetText"] = "I went live right now playing $game!\r\nTitle: $title\r\nMessage: $message\r\n\r\n$url"

    # load on game change tweet text
    if os.path.isfile(tweetData["pathTweetOnGameChange"]):
        with codecs.open(tweetData["pathTweetOnGameChange"], mode="r", encoding='utf-8-sig') as f:
            tweetData["onGameChangeTweetText"] = f.read().rstrip("\n")
    else:
        with codecs.open(tweetData["pathTweetOnGameChange"], mode="w+", encoding='utf-8-sig') as f:
            f.write("We switched to $game now!\r\nTitle: $title\r\n$url")
        tweetData["onGameChangeTweetText"] = "We switched to $game now!\r\nTitle: $title\r\n$url"

    # load periodic tweet text
    if os.path.isfile(tweetData["pathTweetPeriodic"]):
        with codecs.open(tweetData["pathTweetPeriodic"], mode="r", encoding='utf-8-sig') as f:
            tweetData["periodicTweetText"] = f.read().rstrip("\n")
    else:
        with codecs.open(tweetData["pathTweetPeriodic"], mode="w+", encoding='utf-8-sig') as f:
            f.write("We're still live! Come over and hang out with us.\r\nStill playing $game.\r\n$url")
        tweetData["periodicTweetText"] = "We're still live! Come over and hang out with us.\r\nStill playing $game.\r\n$url"

    # load settings so we don't send a new tweet while just restarting SLchatbot
    handleScriptData(execType="load")


#---------------------------------------
#    [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    Init()
    return

def ScriptToggled(state):
    global scriptData
    scriptData["scriptEnabled"] = state
    #Tells you if your script is enabled or not
    return

#---------------------------------------
#    [Required] Tick Function
#---------------------------------------
def Tick():
    global scriptData, settings, TWITTER_CHANNEL_NAME
    global eventTrigged, typeTrigged, timeTrigged, offTrigged

    if settings["successfullyLoaded"] and settings["cbTweetWhenGoingLive"]:
        # Workaround for Twitter Free API limits
        # getting twitter user name
        if TWITTER_CHANNEL_NAME is None:
            TWITTER_CHANNEL_NAME = getTwitterChannelInfo()
            handleScriptData(execType="save")

        if Parent.IsLive():

            # if planned tweet was waiting some time offline, but wasn't cancelled,
            # (aka: it didn't reach its time "to be intended as new stream" while offline)
            # its trigger time will be resetted, to restart waiting the "new tweet waiting option" seconds
            if eventTrigged and offTrigged:
                if settings["cbLoggingToScriptLogs"]:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Back live: will try to send new initial stream start tweet, after around " + str(settings["sliderNewTweetWaiting"]) + " seconds.")
                trigTweet(tweetType = typeTrigged)

            # sending tweet info to chat
            if settings["cbPostMsgMultipleTimes"]:
                if scriptData["notificationsInChatRemaining"] > 0 and time.time() - scriptData["messageInChatTimestamp"] > settings["sliderRTInterval"] * 60 and scriptData["twitchMsg"] != "":
                    scriptData["notificationsInChatRemaining"] -= 1
                    scriptData["messageInChatTimestamp"] = time.time()
                    # store "scriptData" variable to hard drive
                    handleScriptData(execType="save")
                    Parent.SendStreamMessage(scriptData["twitchMsg"])

            # trig automated tweet
            if time.time() - scriptData["timestampOfflineSince"] > settings["sliderNewTweetAfterBreak"] * 60:
                if settings["cbLoggingToScriptLogs"]:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Will try to send new initial stream start tweet, after around " + str(settings["sliderNewTweetWaiting"]) + " seconds.")
                trigTweet(tweetType = "normal")

            # trig tweet on game change, checks every 5 minutes
            if settings["cbSendNewTweetOnGameChange"] and time.time() - scriptData["lastGameChangeCheck"] > 5 * 60:
                scriptData["lastGameChangeCheck"] = time.time()
                jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/game/" + TWITCH_CHANNEL_NAME, {}))
                if jsonData["status"] == 200:
                    currentGameName = jsonData["response"]
                    if scriptData["lastGameName"] != currentGameName:
                        if settings["cbLoggingToScriptLogs"]:
                            Parent.Log("LiveTweeter", getCurrentDayTime() + " > Will try to send new tweet, after around " + str(settings["sliderNewTweetWaiting"]) + " seconds, game change detected from {} to {}.".format(scriptData["lastGameName"], currentGameName))
                        scriptData["lastGameName"] = currentGameName
                        trigTweet(tweetType = "gameChange")

            # trig periodic tweet
            if settings["cbPeriodicTweeting"] and time.time() - scriptData["timestampTweetSent"] > settings["sliderPeriodicTweetInterval"] * 60 :
                if settings["cbLoggingToScriptLogs"]:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Trying to send new periodic tweet, immediately.")
                sendTweet(tweetType = "periodic")

            # send planned tweet if "trigger time plus new tweet waiting" time was reached
            if eventTrigged and timeTrigged + settings["sliderNewTweetWaiting"] <= time.time():
                eventTrigged = False
                if settings["cbLoggingToScriptLogs"]:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Now trying sendind new tweet, after around " + str(settings["sliderNewTweetWaiting"]) + " seconds passed.")
                sendTweet(tweetType = typeTrigged)

            scriptData["timestampOfflineSince"] = time.time()
        else:

            scriptData["timestampLiveSince"] = time.time()
            scriptData["notificationsInChatRemaining"] = 0

            # cancel the old planned tweet if stream was offline enough "to be intended as new stream"
            if eventTrigged and timeTrigged + settings["sliderNewTweetAfterBreak"] * 60 <= time.time():
                if settings["cbLoggingToScriptLogs"]:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Offline for " + str(settings["sliderNewTweetWaiting"]) + " minutes already : when you'll be back live it will count as a new streaming.")
                eventTrigged = False

            # else, I mark the eventually planned tweet as being waiting while offline
            elif eventTrigged and not offTrigged:
                if settings["cbLoggingToScriptLogs"]:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Suddenly offline: will try to send a new initial stream start tweet when back live and after around " + str(settings["sliderNewTweetWaiting"]) + " additional seconds.")
                offTrigged = True

    return

def trigTweet(tweetType="normal"):
    global eventTrigged, typeTrigged, timeTrigged, offTrigged
    eventTrigged = True
    offTrigged = False
    typeTrigged = tweetType
    timeTrigged = time.time()
    return

def sendTweet(tweetType="normal"):
    global tweetData, scriptData, settings
    path = os.path.dirname(__file__)

    if settings["successfullyLoaded"]:
        if os.path.isfile(tweetData["pathTweetMessage"]):
            # load new content from text file before tweeting
            loadTweetTextFile(tweetType)

            # unicode and emojis supported
            with codecs.open(tweetData["pathTweetMessage"], mode="r", encoding='utf-8-sig') as f:
                tweetData["tweetText"] = f.read().rstrip("\n")

            if tweetData["tweetText"] == "Default Test Tweet":
                # dont tweet a default text
                Parent.Log("LiveTweeter", getCurrentDayTime() + "You left the default text in the text file - Tweet has not been sent.")
                return

            scriptData["timestampTweetSent"] = time.time()
            scriptData["timestampOfflineSince"] = time.time()

            if tweetType == "normal":
                tweetData["tweetText"] = tweetData["normalTweetText"]
            elif tweetType == "gameChange":
                tweetData["tweetText"] = tweetData["onGameChangeTweetText"]
                if tweetData["tweetText"] == "":
                    loadTweetTextFile("normal")
                    tweetData["tweetText"] = tweetData["normalTweetText"]
            elif tweetType == "periodic":
                tweetData["tweetText"] = tweetData["periodicTweetText"]
            else:
                # tweet type not detected
                Parent.Log("LiveTweeter", getCurrentDayTime() + "Tweet type hasn't been detected.")
                return


            # Replace $message with textfield 'Message for Tweet'
            tweetData["tweetText"] = tweetData["tweetText"].replace("$message", settings["txtTweetContent"])
            # Replace $url with the twitch channel - only available on twitch
            tweetData["tweetText"] = tweetData["tweetText"].replace("$url", "https://www.twitch.tv/" + TWITCH_CHANNEL_NAME)
            # Replace $preview with a preview image - only available on twitch
            tweetData["tweetText"] = tweetData["tweetText"].replace("$preview", "https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-{}x{}.jpg".format(TWITCH_CHANNEL_NAME, 1280, 720)) # TODO: change resolution
            # Replace $title with current set title - only available on twitch
            jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/title/" + TWITCH_CHANNEL_NAME, {}))
            if "$title" in tweetData["tweetText"]:
                if jsonData["status"] == 200:
                    tweetData["tweetText"] = tweetData["tweetText"].replace("$title", jsonData["response"])
                else:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + "Script was not able to replace $title with the stream title. Status code: {}".format(jsonData["status"]))

            # Replace $game with current set game - only available on twitch
            jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/game/" + TWITCH_CHANNEL_NAME, {}))
            if jsonData["status"] == 200:
                scriptData["lastGameName"] = jsonData["response"]
                tweetData["tweetText"] = tweetData["tweetText"].replace("$game", jsonData["response"])
            else:
                Parent.Log("LiveTweeter", getCurrentDayTime() + "Script was not able to replace $game with the game name. Status code: {}".format(jsonData["status"]))

            # Cutting exceeding text
            tweetData["tweetText"] = tweetData["tweetText"][:280]

            # send new tweet
            tweetData["action"] = "SendTweet"
            tweetData["url"] = "https://api.twitter.com/2/tweets" # API v2.0
            response = launchExternalScript(tweetData["pathPython"], tweetData["pathScript"], tweetData)
            if response["statusCode"] != 200 and response["statusCode"] != 201: # API v2.0
                # something went wrong, see bot script log
                return

            # if checkbox enabled to link tweet in chat:
            if settings["cbPostTweetInChat"] and tweetType == "normal":
                tweetUrl = "https://twitter.com/{}/status/{}".format(TWITTER_CHANNEL_NAME, response["data"]["id"]) # API v2.0
                string = settings["txtTweetLinkInChat"].replace("$tweetUrl", tweetUrl)
                scriptData["twitchMsg"] = string[:490]
                scriptData["messageInChatTimestamp"] = time.time()
                scriptData["notificationsInChatRemaining"] = settings["sliderRTAmount"]
                Parent.SendStreamMessage(string[:490])

            # store "scriptData" variable to hard drive
            handleScriptData(execType="save")
        else:
            pass

def launchExternalScript(pathPythonExe, pathExternalScript, data={}):
    global scriptData, settings

    if not os.path.isfile(pathPythonExe):
        Parent.Log("LiveTweeter", getCurrentDayTime() + "Please check your python path! Tweet has not been sent.")
        return {"statusCode": -1}

    # not really necessary but just in case
    if not os.path.isfile(pathExternalScript):
        Parent.Log("LiveTweeter", getCurrentDayTime() + "Something is wrong with the path to the external python script!")
        return {"statusCode": -1}

    if not all([len(data[x]) > 0 for x in ["consumer_key", "consumer_secret", "access_token", "access_token_secret"]]):
        Parent.Log("LiveTweeter", getCurrentDayTime() + "One of your 4 key fields is empty! Tweet has not been sent.")
        return {"statusCode": -1}

    encodedData = encodeBlueprint(data)
    encodedResponse = os.popen("cmd /C \"\"{}\" \"{}\" \"{}\"\"".format(pathPythonExe, pathExternalScript, encodedData)).read()
    response = decodeBlueprint(encodedResponse)

    # error message depends on tweet type: send tweet or remove tweet
    if data["action"] == "SendTweet":
        errorMessage = "trying to send the tweet"
    elif data["action"] == "RemoveTweet":
        errorMessage = "trying to remove the previous tweet sent by the script"


    if response["scriptStatus"] == "Success":
        if data["action"] == "SendTweet":
            scriptData["lastTweetId"] = response["data"]["id"] # API v2.0
            if settings["cbLoggingToScriptLogs"]:
                if TWITTER_CHANNEL_NAME:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Tweet was successfully sent for twitter account @{}".format(TWITTER_CHANNEL_NAME)) # API v2.0
                else:
                    Parent.Log("LiveTweeter", getCurrentDayTime() + " > Tweet was successfully sent") # API v2.0

    elif response["scriptStatus"] == "Error":
        if response["statusCode"] == 404:
            message = "Error while {}: The tweet does not seem to exist anymore.".format(errorMessage)
        elif response["statusCode"] == 401:
            message = "Error while {}: Please double check your keys (Consumer Key, Consumer Secret, Access Token, Access Token Secret.".format(errorMessage)
        elif response["statusCode"] == -2:
            message = "Error while {}: It seems your requests library was not correctly installed. Check your python path and click the button \"INSTALL PIP REQUESTS\" again.".format(errorMessage)
        elif response["statusCode"] == -3:
            message = "Error while {}: It seems your requests_oauthlib library was not correctly installed. Check your python path and click the button \"INSTALL PIP REQUESTS\" again.".format(errorMessage)
        elif response["statusCode"] == -4:
            message = "Error while {}: Some unknown error occured, error message: {}".format(errorMessage, response["statusText"])
        else:
            message = "Unknown error while {}: status code {}, status reason {}".format(errorMessage, response["statusCode"], response["statusText"]) # API v2.0
        Parent.Log("LiveTweeter", getCurrentDayTime() + "{}".format(message))

    return response

def handleScriptData(execType = "save"):
    global scriptData, tweetData
    pathScriptDataJson = tweetData["pathScriptData"]
    pathScriptDataFolder = os.path.dirname(pathScriptDataJson)
    if execType == "save":
        if not os.path.isdir(pathScriptDataFolder):
            os.makedirs(pathScriptDataFolder)
        with codecs.open(pathScriptDataJson, mode="w+", encoding='utf-8-sig') as f:
            json.dump(scriptData, f, indent=4)

    elif execType == "load":
        if os.path.isfile(pathScriptDataJson):
            with codecs.open(pathScriptDataJson, mode="r", encoding='utf-8-sig') as f:
                try:
                    scriptData = json.load(f)
                except:
                    pass

    # TODO: still need to implement (old note from v1.2.0)
    # removes the data files when stream is offline, e.g. info about when the last tweet was sent etc.
    elif execType == "remove":
        if os.path.isfile(pathScriptDataJson):
            os.remove(pathScriptDataJson)
            os.rmdir(pathScriptDataFolder)
    return

def loadTweetTextFile(textFile = "normal"):
    global tweetData

    if textFile == "normal":
        if os.path.isfile(tweetData["pathTweetMessage"]):
            with codecs.open(tweetData["pathTweetMessage"], mode="r", encoding='utf-8-sig') as f:
                tweetData["normalTweetText"] = f.read().rstrip("\n")

    elif textFile == "gameChange":
        if os.path.isfile(tweetData["pathTweetOnGameChange"]):
            with codecs.open(tweetData["pathTweetOnGameChange"], mode="r", encoding='utf-8-sig') as f:
                tweetData["periodicTweetText"] = f.read().rstrip("\n")

    elif textFile == "periodic":
        if os.path.isfile(tweetData["pathTweetPeriodic"]):
            with codecs.open(tweetData["pathTweetPeriodic"], mode="r", encoding='utf-8-sig') as f:
                tweetData["onGameChangeTweetText"] = f.read().rstrip("\n")


# Workaround for Twitter Free API limits
def getTwitterChannelInfo():
    global scriptData, settings, TWITTER_CHANNEL_NAME

    if "cbTwitterChannelName" in settings and settings["cbTwitterChannelName"] \
            and "txtTwitterChannelName" in settings and settings["txtTwitterChannelName"]:
        TWITTER_CHANNEL_NAME = settings["txtTwitterChannelName"]

    else:
        if "twitterUsername" not in scriptData or not scriptData["twitterUsername"]:
            tweetData["action"] = "GetInfo"
            tweetData["url"] = "https://api.twitter.com/2/users/me"
            response = launchExternalScript(tweetData["pathPython"], tweetData["pathScript"], tweetData)

            if response["statusCode"] != 200 and response["statusCode"] != 201 and not response["data"]["username"]:
                if "txtTwitterChannelName" in settings:
                    scriptData["twitterUsername"] = settings["txtTwitterChannelName"]
                else:
                    scriptData["twitterUsername"] = ""
            else:
                scriptData["twitterUsername"] = response["data"]["username"]

    return scriptData["twitterUsername"]


def decodeBlueprint(blueprintString):
    version_byte = blueprintString[0]
    decoded = base64.b64decode(blueprintString[1:])
    json_str = zlib.decompress(decoded).decode('utf-8')
    data = json.loads(json_str, object_pairs_hook=collections.OrderedDict)
    return data

def encodeBlueprint(data, level=6):
    json_str = json.dumps(data, ensure_ascii=False)
    encoded = zlib.compress(json_str.encode('utf-8'), level)
    blueprintString = base64.b64encode(encoded)
    return "0" + blueprintString

def getCurrentDayTime():
    now = time.localtime()
    return str(now.tm_hour).rjust(2, '0') + ":" + str(now.tm_min).rjust(2, '0') + ":" + str(now.tm_sec).rjust(2, '0')

#---------------------------------------
# BUTTONS
#---------------------------------------
def OpenTwitterApp():
    os.startfile("https://developer.twitter.com/en/portal/dashboard")

def btnInstallPipRequets():
    global settings
    if os.path.isfile(settings['txtPathPython']):
        os.system("cmd /k \"{}\" -m pip install requests==2.18.4 requests_oauthlib==1.3.1".format(settings['txtPathPython'])) # python 2.7 compatibility
    else:
        Parent.Log("LiveTweeter", getCurrentDayTime() + "Could not execute \"Install pip requests\". Please double check your entered python path.")

def btnOpenReadme():
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    if os.path.isfile(location):
        os.startfile(location)
    return

def btnOpenTweetMessageFile():
    global tweetData
    location = tweetData["pathTweetMessage"]
    if os.path.isfile(location):
        os.startfile(location)
    return

def btnOpenTweetOnGameChangeFile():
    global tweetData
    location = tweetData["pathTweetOnGameChange"]
    if os.path.isfile(location):
        os.startfile(location)
    return

def btnOpenTweetPeriodicFile():
    global tweetData
    location = tweetData["pathTweetPeriodic"]
    if os.path.isfile(location):
        os.startfile(location)
    return

def btnResetTwitterChannelName():
    global scriptData, TWITTER_CHANNEL_NAME
    scriptData["twitterUsername"] = ""
    TWITTER_CHANNEL_NAME = getTwitterChannelInfo()
    handleScriptData(execType="save")
    return

def btnSendTweet():
    if settings["successfullyLoaded"] and scriptData["scriptEnabled"]:
        if settings and "cbLoggingToScriptLogs" in settings and settings["cbLoggingToScriptLogs"]:
            Parent.Log("LiveTweeter", getCurrentDayTime() + " > Trying to send new manual requested tweet, immediately.")
        sendTweet()
    return
