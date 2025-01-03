import re
import flask
import function

app = flask.Flask(__name__)

@app.route('/<param>', methods=['GET'])
def BiliAnalysis(param):
    bv_match = re.search(r'BV[a-zA-Z0-9]{10}', param)
    if bv_match:
        BV = bv_match.group(0)  # 提取到的 BV 号
        if len(BV) == 12 and BV.startswith('BV') and BV[2:].isalnum():
            p = flask.request.args.get('p', 1)
            try:
                p = int(p)
            except ValueError:
                p = 1
            videoUrl = function.BiliAnalysis(BV, p)["url"]
            videoUrl = function.ChangeBiliCDN(videoUrl)
            return flask.redirect(videoUrl)
        else:
            return flask.jsonify({'error': 'Invalid BV number'})
    else:
        return flask.jsonify({'error': 'No BV number found'})

@app.route('/', methods=['GET'])
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BV Analysis</title>
    </head>
    <body>
        <h1>BV Analysis</h1>
        <form action="/submit" method="get">
            <label for="bvid">BVID:</label>
            <input type="text" id="bvid" name="bvid" required>
            <label for="p">Page Number:</label>
            <input type="number" id="p" name="p">
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

@app.route('/submit', methods=['GET'])
def submit():
    bvid = flask.request.args.get('bvid')
    return flask.redirect(f'/{bvid}?p={flask.request.args.get("p", 1)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)