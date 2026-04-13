'''import tkinter as tk
from tkinter import filedialog, messagebox
import requests

class ObjectDetectionTab:
    def __init__(self, parent):
        self.root = parent
        self.api_key = tk.StringVar()
        self.image_path = tk.StringVar()
        self.result_text = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        tk.Label(self.root, text="Image File:").grid(row=0, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.image_path, width=50).grid(row=0, column=1, **padding)
        tk.Button(self.root, text="Browse", command=self.browse_image).grid(row=0, column=2, **padding)

        tk.Label(self.root, text="YOLO API Key:").grid(row=1, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.api_key).grid(row=1, column=1, sticky="w", **padding)

        tk.Button(self.root, text="Detect Object", command=self.detect_object).grid(
            row=3, column=1, pady=20
        )
        tk.Label(self.root, textvariable=self.result_text, fg="blue", wraplength=500).grid(
            row=4, column=0, columnspan=3, **padding
        )



    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("All Image Files", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.tif *.gif"),]
        )
        if file_path:
            self.image_path.set(file_path)

    def detect_object(self):
        api_key = self.api_key.get()
        image_file = self.image_path.get()

        if not api_key or not image_file:
            messagebox.showerror("Error", "Please provide both API key and image file.")
            return

        #url = "https://api.api-ninjas.com/v1/objectdetection"
        url = "https://router.huggingface.co/hf-inference/models/facebook/detr-resnet-50"
        #headers = {"X-Api-Key": api_key}
        headers = {"Authorization": f"Bearer {api_key}"}
        print(url)

        try:
            print("In TRY")
            with open(image_file, "rb") as f:
                files = {"image": f}
                response = requests.post(url, headers=headers, files=files)

            response.raise_for_status()  
            data = response.json()
            print(f"Data: {data}")     

            if not data:
                self.result_text.set("No objects detected.")
            else:
                detected_objects = [obj["label"] for obj in data]
                self.result_text.set(f"Detected objects: {', '.join(detected_objects)}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Request failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))'''



import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import json
import os


class ObjectDetectionTab:
    def __init__(self, parent):
        self.root = parent

        self.image_paths = []
        self.selected_model = tk.StringVar(value="yolov8")

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Image selection
        tk.Label(self.root, text="Select Images:").grid(row=0, column=0, sticky="w", **padding)

        self.image_listbox = tk.Listbox(self.root, width=60, height=8)
        self.image_listbox.grid(row=1, column=0, columnspan=2, **padding)

        tk.Button(self.root, text="Browse Images", command=self.browse_images)\
            .grid(row=1, column=2, **padding)

        # Model dropdown
        tk.Label(self.root, text="Select Model:").grid(row=2, column=0, sticky="w", **padding)

        self.model_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.selected_model,
            values=["yolov5", "yolov8"],
            state="readonly"
        )
        self.model_dropdown.grid(row=2, column=1, sticky="w", **padding)

        # Predict button
        tk.Button(self.root, text="Predict", command=self.run_prediction)\
            .grid(row=3, column=1, pady=20)

    def browse_images(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )

        if files:
            self.image_paths = list(files)
            self.image_listbox.delete(0, tk.END)

            for f in self.image_paths:
                self.image_listbox.insert(tk.END, f)

    def run_prediction(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select images.")
            return

        model = self.selected_model.get()

        url = "http://127.0.0.1:8000/predict"

        try:
            files = []
            for path in self.image_paths:
                files.append(
                    ("files", (os.path.basename(path), open(path, "rb"), "image/jpeg"))
                )

            data = {
                "model": model
            }

            response = requests.post(url, files=files, data=data)

            if response.status_code != 200:
                messagebox.showerror("API Error", response.text)
                return

            result = response.json()

            # Save JSON
            save_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")]
            )

            if save_path:
                with open(save_path, "w") as f:
                    json.dump(result, f, indent=4)
                messagebox.showinfo("Success", "Predictions saved successfully!")

            for img_name, data in result.items():
                annotated_path = data["annotated_image"]

                messagebox.showinfo("Done", f"Annotated image saved at:\n{annotated_path}")



        except Exception as e:
            messagebox.showerror("Error", str(e))