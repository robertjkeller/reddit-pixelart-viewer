from image_collection import ImageCollection
from reddit_client import RedditClient
from flask import Flask, redirect, render_template

app = Flask(__name__)

collection = ImageCollection()


@app.route("/")
def main():
    if collection.current_index == collection.file_count:
        collection.current_index = 0
        return render_template("end_screen.html")
    else:
        image = collection.files[collection.current_index]
        collection.current_index += 1
        return render_template("display_image.html", image=image)


@app.route("/start_fetch")
def loading():
    return render_template("loading.html")


@app.route("/fetch_new")
def fetch_new_images():
    client = RedditClient()
    client.run()
    collection.__init__()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
