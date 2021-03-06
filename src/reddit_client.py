from io import BytesIO
from pathlib import Path
import itertools

import praw
import requests
from PIL import Image, ImageSequence

from config import UserConfigs
from constants import SCREEN_SIZE, SUBREDDIT_NAME

configs = UserConfigs()


class RedditClient:
    def __init__(self) -> None:
        self.client_id = configs.client_id
        self.client_secret = configs.client_secret
        self.user_agent = configs.user_agent
        self.folder_path = "static/img"
        self.read_only_client = self._get_read_only_client()
        self.image_urls = []
        self.rotation = configs.rotation

    def _get_read_only_client(self):
        read_only_client = praw.Reddit(
            client_id=self.client_id, client_secret=self.client_secret, user_agent=self.user_agent
        )
        return read_only_client

    def _get_top_posts_of_week(self, subreddit_name=SUBREDDIT_NAME):
        subreddit = self.read_only_client.subreddit(subreddit_name)
        return [p for p in subreddit.top(time_filter="year")]

    def _get_image_urls(self):
        urls = [p.url for p in self._get_top_posts_of_week()]
        self.image_urls = [u for u in urls if u[-4:] == ".gif"]

    def _prepare_target_folder(self):
        folder = Path(self.folder_path)
        [f.unlink() for f in folder.glob("*") if f.is_file()]

    def _save_images(self):
        self._prepare_target_folder()

        for url in self.image_urls:
            response = requests.get(url)
            with Image.open(BytesIO(response.content)) as img:

                if abs(img.size[0] - img.size[1]) <= 10:
                    i = len([f for f in Path(self.folder_path).glob("*.gif")])

                    frames = (f.resize(SCREEN_SIZE).rotate(self.rotation) for f in ImageSequence.Iterator(img))
                    frame1 = next(frames)

                    outfile = f"{self.folder_path}/{i}.gif"
                    frame1.save(
                        outfile, format="gif", save_all=True, loop=0, append_images=(frames)
                    )

    def run(self):
        self._get_image_urls()
        self._save_images()


if __name__ == "__main__":
    client = RedditClient()
    client.run()
