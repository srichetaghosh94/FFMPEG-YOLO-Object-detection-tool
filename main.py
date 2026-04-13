import tkinter as tk
from tkinter import ttk

from video_to_frames import VideoToFramesTab
from object_detection import ObjectDetectionTab


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Toolkit")
        self.root.geometry("700x400")

        self.create_tabs()

    def create_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        # Create frames for each tab
        video_tab_frame = ttk.Frame(notebook)
        object_tab_frame = ttk.Frame(notebook)

        notebook.add(video_tab_frame, text="Video to Frames (FFmpeg)")
        notebook.add(object_tab_frame, text="Object Detection")

        # Load each tab widget
        VideoToFramesTab(video_tab_frame)
        ObjectDetectionTab(object_tab_frame)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


 