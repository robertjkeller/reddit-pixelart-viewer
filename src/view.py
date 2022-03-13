import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence
from constants import GIF_DELAY
from config import UserConfigs

class ImageCollection:
    def __init__(self, configs) -> None:
        self.files = [f for f in Path(configs.folder_path).glob('*.gif')]
        self.current_index = 0
        self.file_count = len(self.files)


class ImageLabel(tk.Label):
    def load(self, file):
        self.file = file
        self.loc = 0
        animated_image = Image.open(file)
        self.frames = [ImageTk.PhotoImage(image=f) for f in ImageSequence.Iterator(animated_image)]

        self.delay = GIF_DELAY

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def play():
    configs = UserConfigs()

    def next_image():
        if collection.current_index < (collection.file_count - 1):
            collection.current_index += 1
        else:
            collection.current_index = 0
        label.load(file = collection.files[collection.current_index])
    
    root = tk.Tk()
    # Uncomment below for full-screen.
    # root.wm_overrideredirect(True)

    collection = ImageCollection(configs)
    label = ImageLabel(root)
    label.pack()
    label.bind('<Button-1>', lambda e: next_image())
    label.load(file=collection.files[collection.current_index])

    root.mainloop()