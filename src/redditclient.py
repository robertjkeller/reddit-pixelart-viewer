from io import BytesIO
from pathlib import Path

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
        self.folder_path = 'static/img'
        self.read_only_client = self._get_read_only_client()
        self.image_urls = []

    def _get_read_only_client(self):
        read_only_client = praw.Reddit(
            client_id=self.client_id, client_secret=self.client_secret, user_agent=self.user_agent
        )
        return read_only_client

    def _get_top_posts_of_week(self, subreddit_name=SUBREDDIT_NAME):
        subreddit = self.read_only_client.subreddit(subreddit_name)
        return [p for p in subreddit.top(time_filter="week")]

    def _get_image_urls(self):
        urls = [p.url for p in self._get_top_posts_of_week()]
        self.image_urls = [u for u in urls if ".gif" in u]

    def _prepare_target_folder(self):
        folder = Path(self.folder_path)
        [f.unlink() for f in folder.glob("*") if f.is_file()]

    def _save_images(self):
        self._prepare_target_folder()

        for url in self.image_urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            if img.size[0] == img.size[1]:
                i = len([f for f in Path(self.folder_path).glob('*.gif')])
                new_sequence = [f.resize(SCREEN_SIZE) for f in ImageSequence.Iterator(img)]
                outfile = f"{self.folder_path}/{i}.gif"
                new_sequence[0].save(
                    outfile, format="gif", save_all=True, append_images=new_sequence[1:]
                )

    def run(self):
        self._get_image_urls()
        self._save_images()


if __name__ == '__main__':
    client = RedditClient()
    client.run()