import requests
import json
import re
from more_itertools import unique_everseen

with open("urls.json", "r", encoding="utf-8") as fp:
    urls = json.load(fp)

# lots of regex to extract video ID from different types of YouTube links
def get_id(url):
    if "youtube" in url:
        if "attribution" in url:
            try:
                video_id = re.search("%3D(.*)\%26", url).group(1)
            except Exception:
                print(url)
                video_id = ""
        else:
            try:
                video_id = re.search("(\?|\&)(v|ci)=(.*)", url).group(3)
            except Exception:
                print(url)
                video_id = ""
    else:
        try:
            video_id = re.search("\.be\/(.*)", url).group(1)
        except Exception:
                print(url)
                video_id = ""
    return video_id

# get video IDs from URLs, then deduplicate
ids = list(map(get_id, urls))
ids = list(filter(lambda x: len(x) > 0, ids))
ids = list(unique_everseen(ids))

# access token can be acquired from https://developers.google.com/oauthplayground/
access_token = "YOUR_ACCESS_TOKEN"

# your YouTube playlist ID can be found in the playlist URL
playlist_id = "YOUR_PLAYLIST_ID"

# correct API path
path = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&access_token={access_token}".format(access_token=access_token)
headers = {'Content-Type': 'application/json'}

# finally insert the video into your playlist
for video_id in ids:
    payload = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "videoId": video_id,
                "kind": "youtube#video"
            }
        }
    }

    request = requests.post(path, data=json.dumps(payload), headers=headers)
    # for confirmation of success
    print(request.content)
