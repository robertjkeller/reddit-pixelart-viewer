from redditclient import RedditClient
from flask import Flask, redirect, render_template
from pathlib import Path

app = Flask(__name__)

class ImageCollection:
    def __init__(self) -> None:
        self.files = [f for f in Path('static/img').glob('*.gif')]
        self.current_index = 0
        self.file_count = len(self.files)

collection = ImageCollection()

@app.route('/')
def main():
    if collection.current_index == collection.file_count:
        collection.current_index = 0
        return render_template('end_screen.html')
    else:
        image = collection.files[collection.current_index]
        collection.current_index += 1
        return render_template('display_image.html', image=image)

@app.route('/start_fetch')
def loading():
    return render_template('loading.html')

@app.route('/fetch_new')
def fetch_new_images():
    client = RedditClient()
    client.run()
    collection.__init__()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
