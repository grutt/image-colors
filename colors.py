from flask import Flask, request, abort, jsonify
import os
import subprocess
import urllib.request
import boto3

client = boto3.client('dynamodb')

app = Flask(__name__)

OUT_DIR = "imgs/"


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def abort_with_message(message):
    response = jsonify({'message': message})
    response.status_code = 500
    return response


@app.route('/')
def index():
    return 'Visit /api/num_colors?src=SOMEURL.'


@app.route('/api/num_colors', methods=['GET'])
def numColors():
    img = request.args.get('src')
    if img is None or img == "":
        return bad_request("image is required")
    else:
        try:
            cached = client.get_item(TableName='cached_imgs',
                                     Key={'url': {'S': 'http://hello.com'}})
            return int(cached['Item']['colors']['N'])
        except:
            pass

        try:
            filename = img.split('/')[-1]
            local = OUT_DIR+filename
            urllib.request.urlretrieve(img, local)
        except:
            return abort_with_message("bad image")

        try:
            colors = subprocess.run(["/usr/bin/identify", "-format",
                                    "%k", local],
                                    stdout=subprocess.PIPE)
            os.remove(local)
            if(colors.returncode == 0):
                return colors.stdout
            else:
                return abort_with_message("img failed")
        except:
            return abort_with_message("general failure")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
