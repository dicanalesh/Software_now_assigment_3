# gui_components.py
import tkinter as tk
from tkinter import ttk, scrolledtext

from models import HFTextGenerator, HFImageClassifier

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI OOP Tkinter App - Primera versión")
        self.geometry("600x400")

        # instancias de modelos (simulados)
        self.text_model = HFTextGenerator("simulado-text")
        self.image_model = HFImageClassifier("simulado-image")

        # Widgets básicos
        ttk.Label(self, text="Input:").pack()
        self.input_box = scrolledtext.ScrolledText(self, height=5)
        self.input_box.pack(fill="x")

        self.run_text_btn = ttk.Button(self, text="Run Text Model", command=self.run_text)
        self.run_text_btn.pack(pady=5)

        self.run_image_btn = ttk.Button(self, text="Run Image Model", command=self.run_image)
        self.run_image_btn.pack(pady=5)

        ttk.Label(self, text="Output:").pack()
        self.output_box = scrolledtext.ScrolledText(self, height=8)
        self.output_box.pack(fill="both", expand=True)

    def run_text(self):
        prompt = self.input_box.get("1.0", "end").strip()
        result = self.text_model.run(prompt)
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)

    def run_image(self):
        result = self.image_model.run(None)
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)
