from flask import Flask, jsonify, redirect
from datetime import datetime, timedelta

import requests

CACHE_DURATION = timedelta(hours=1)

cache = {}

app = Flask(__name__)

def get_url(gif_id):
    current_time = datetime.now()

    if gif_id in cache:
        cached_data, timestamp = cache[gif_id]
        if current_time - timestamp < CACHE_DURATION:
            print("Returning cached video URL")
            return cached_data

    res = requests.get("https://tenor.com/view/"+gif_id)
    res = res.text.split("\n")
    res = [i for i in res if "{\"appConfig" in i]
    res = res[0]
    res = '{"appConfig"' + res.split('{"appConfig"')[1]
    res = res.split('{"url":"')
    del res[0]
    del res[len(res)-1]
    res = [i.split('"',1)[0] for i in res]
    res = [i.encode().decode("unicode_escape") for i in res]
    res = [i for i in res if any([i.endswith(end) for end in [".mp4"]])]

    print(res)

    res = res[0]
    res = "https://media.tenor.com/"+res.split(".com/",1)[1].split("-")[0] + "-xFMAAAPo/" + res[::-1].split("/",1)[0][::-1]

    res = res.replace("AAAP1", "AAAPo") # quality setting i guess

    cache[gif_id] = (res, current_time)

    return res

@app.route('/<gif_id>', methods=['GET'])
def get_gif_url(gif_id):

        url = get_url(gif_id)
        return redirect(url)

if __name__ == '__main__':
    app.run(debug=False, port=2053)
