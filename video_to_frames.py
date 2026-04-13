import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os


class VideoToFramesTab:
    def __init__(self, parent):
        self.root = parent

        self.video_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.frame_rate = tk.StringVar(value="1")
        self.image_format = tk.StringVar(value="png")
        self.start_number = tk.StringVar(value="0")

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Video selection
        tk.Label(self.root, text="Video File:").grid(row=0, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.video_path, width=50).grid(row=0, column=1, **padding)
        tk.Button(self.root, text="Browse", command=self.browse_video).grid(row=0, column=2, **padding)

        # Output folder
        tk.Label(self.root, text="Output Folder:").grid(row=1, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.output_folder, width=50).grid(row=1, column=1, **padding)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2, **padding)

        # Frame rate
        tk.Label(self.root, text="Frame Rate (fps):").grid(row=2, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.frame_rate).grid(row=2, column=1, sticky="w", **padding)

        # Image format
        tk.Label(self.root, text="Image Format:").grid(row=3, column=0, sticky="w", **padding)

        self.format_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.image_format,
            values=["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
            state="readonly"  # prevents manual typing
        )
        self.format_dropdown.grid(row=3, column=1, sticky="w", **padding)
        self.format_dropdown.current(0)  # default to first option

        # Start number
        tk.Label(self.root, text="Start Number:").grid(row=4, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.start_number).grid(row=4, column=1, sticky="w", **padding)

        # Convert button
        tk.Button(self.root, text="Convert to Frames", command=self.convert).grid(
            row=6, column=1, pady=20
        )

    def browse_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if file_path:
            self.video_path.set(file_path)

    def browse_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder.set(folder_path)

            
    def check_ffmpeg(self):
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def convert(self):
        video = self.video_path.get()
        output = self.output_folder.get()

        if not video or not output:
            messagebox.showerror("Error", "Please select both video and output folder.")
            return

        if not self.check_ffmpeg():
            messagebox.showerror("Error", "FFmpeg not found. Install it and add to PATH.")
            return

        try:
            fps = float(self.frame_rate.get())
        except ValueError:
            messagebox.showerror("Error", "Frame rate must be a number.")
            return

        start_num = self.start_number.get()
        if not start_num.isdigit():
            messagebox.showerror("Error", "Start number must be an integer.")
            return

        fmt = self.image_format.get()

        output_pattern = os.path.join(output, f"frame_%05d.{fmt}")

        command = [
            "ffmpeg",
            "-y",
            "-i", video,
            "-vf", f"fps={fps}",
            "-start_number", start_num,
            output_pattern
        ]

        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Frames extracted successfully!")

        except subprocess.CalledProcessError:
            messagebox.showerror("FFmpeg Error", "Failed to extract frames.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
