import sys
import base64
import requests # pip install requests==2.18.4
from requests_oauthlib import OAuth1 # pip install requests_oauthlib==1.3.1
import zlib, json
import collections
import os

path = os.path.dirname(__file__)

def decodeBlueprint(blueprintString):
    version_byte = blueprintString[0]
    decoded = base64.b64decode(blueprintString[1:])
    # json_str = zlib.decompress(decoded) # python 2 version
    json_str = zlib.decompress(decoded).decode('utf-8') # python 2 and 3 version
    data = json.loads(json_str, object_pairs_hook=collections.OrderedDict)
    return data

def encodeBlueprint(data, level=6):
    json_str = json.dumps(data, ensure_ascii=False)
    encoded = zlib.compress(json_str.encode('utf-8'), level)
    blueprintString = base64.b64encode(encoded)
    return "0" + blueprintString


if __name__ == "__main__":
    # read arguments from commandline
    encodedTweetData = "".join(sys.argv[1:])
    tweetData = decodeBlueprint(encodedTweetData)


    # API v2.0 updates made only for SendTweet and RemoveTweet action
    # Login as for API v1.1 still works
    auth = OAuth1(
        tweetData["consumer_key"].strip(),
        tweetData["consumer_secret"].strip(),
        tweetData["access_token"].strip(),
        tweetData["access_token_secret"].strip())

    # API v2.0 (with Free API you can pratically do only these 3 actions)
    if tweetData["action"] == "SendTweet":
        # i.e.: https://api.twitter.com/2/tweets
        r = requests.post(tweetData["url"], auth=auth, json={"text": tweetData["tweetText"]})
    elif tweetData["action"] == "RemoveTweet":
        # i.e.: https://api.twitter.com/2/tweets/ + tweet_id
        r = requests.delete(tweetData["url"], auth=auth)
    elif tweetData["action"] == "GetInfo":
        # i.e.: https://api.twitter.com/2/users/me
        r = requests.get(tweetData["url"], auth=auth)

    try:
        if r.status_code == 200 or r.status_code == 201: # API v2.0
            response = r.json()
            response["scriptStatus"] = "Success"
            response["statusCode"] = r.status_code
            response["statusText"] = r.reason # API v2.0
            print(encodeBlueprint(response))
        else:
            response = {
                "scriptStatus": "Error",
                "statusCode": r.status_code,
                "statusText": r.reason, # API v2.0
            }
            print(encodeBlueprint(response))
    except Exception as e:
        response = {
                "scriptStatus": "Error",
                "statusCode": -4,
                "statusText": e,
            }
        # with open(os.path.join(path, "tempTweetScriptOutput.json"), mode="w") as f:
        #     json.dump(response, f, indent=4)
        print(encodeBlueprint(response))

    sys.exit(0)

