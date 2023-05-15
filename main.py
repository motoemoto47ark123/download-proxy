import os
from flask import Flask, send_from_directory, Response, request
from urllib.parse import urlparse
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    if filename.endswith('.css'):
        return send_from_directory('public', filename, mimetype='text/css')
    elif filename.endswith('.js'):
        return send_from_directory('public', filename, mimetype='text/javascript')
    else:
        return send_from_directory('public', filename)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return "Download URL is empty!", 400

    # Parse the URL to get the filename
    filename = urlparse(url).path.split('/')[-1]

    try:
        # Stream the file directly from the source URL to the client using curl
        cmd = f"curl --fail --silent {url}"
        headers = {
            'Content-Disposition': f"attachment; filename={filename}"
        }
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return Response(iter(lambda: p.stdout.read(1024), b''), headers=headers)

    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during the download
        return f"Error downloading file: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
