from pathlib import Path


class ImageCollection:
    def __init__(self) -> None:
        self.files = [f for f in Path("static/img").glob("*.gif")]
        self.current_index = 0
        self.file_count = len(self.files)
