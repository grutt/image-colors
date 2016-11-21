from flask import Flask, request, abort
import os
import subprocess
import urllib.request


app = Flask(__name__)


@app.route('/')
def index():
    return 'Visit /api/num_colors?src=SOMEURL.'


@app.route('/api/num_colors', methods=['GET'])
def numColors():
    img = request.args.get('src')
    if img is None or img == "":
        abort(500)
    else:
        try:
            filename = img.split('/')[-1]
            local = "imgs/"+filename
            urllib.request.urlretrieve(img, local)
            colors = subprocess.run(["identify", "-format", "%k", local],
                                    stdout=subprocess.PIPE)
#            os.remove(local)
            if(colors.returncode == 0):
                return colors.stdout
            else:
                abort(500)
        except:
            abort(500)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
