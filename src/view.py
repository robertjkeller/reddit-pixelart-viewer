import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from constants import GIF_DELAY


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


def play(file):
    root = tk.Tk()
    root.wm_overrideredirect(True)
    label = ImageLabel(root)
    label.pack()
    label.load(file=file)

    root.mainloop()