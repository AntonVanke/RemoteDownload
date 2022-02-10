import os

import requests
from flask import Flask, request, Response, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/download/<path:file_url>')
def download(file_url):
    if request.method == 'GET':
        file_size = ''
        file_name = ''

        def send_file():
            nonlocal file_size, file_name
            with requests.get(file_url, stream=True) as res:
                file_size = res.headers.get('Content-length')
                if res.headers.get('Content-disposition'):
                    file_name = res.headers.get('Content-disposition').split('; ')[1].replace('filename=', '')
                else:
                    file_name = os.path.basename(file_url.split("?")[0])
                for content in res.iter_content(chunk_size=40960):
                    yield content

        response = Response(send_file(), content_type='application/octet-stream')
        if file_size:
            response.headers["Content-disposition"] = file_size
        response.headers["Content-disposition"] = 'attachment; filename=%s' % file_name
        return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
