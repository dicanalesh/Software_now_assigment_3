# gui_components.py
"""
GUI functional that recieve inputs, outputs (randoms), OOPs utilized, and description of models:
- Modular, with encapsulation and mixins.
- Dinamic output y section for info y OOP.
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import Image, ImageTk
from typing import Optional
from models import HFTextGenerator, HFImageClassifier
import os

class LoggerMixin:
    def log(self, msg: str):
        print(f"[GUI LOG] {msg}")

class UIHelperMixin:
    def center_window(self, width=900, height=600):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - width)//2
        y = (self.winfo_screenheight() - height)//2
        self.geometry(f"{width}x{height}+{x}+{y}")

class AppGUI(tk.Tk, LoggerMixin, UIHelperMixin):
    def __init__(self):
        super().__init__()
        self.title("AI OOP Tkinter App - Simulation")
        self.center_window(1000, 650)

        # simulated models
        self._text_model = HFTextGenerator()
        self._image_model = HFImageClassifier()
        self._selected_image_path: Optional[str] = None

        self._build_ui()

    def _build_ui(self):
        # Top controls
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)

        ttk.Label(top, text="Input type:").pack(side="left")
        self._input_type = tk.StringVar(value="Text")
        ttk.Combobox(top, textvariable=self._input_type, values=["Text", "Image"], state="readonly", width=12).pack(side="left", padx=6)

        ttk.Label(top, text="Model:").pack(side="left", padx=(10,0))
        self._model_choice = tk.StringVar(value="Text Generator")
        ttk.Combobox(top, textvariable=self._model_choice, values=["Text Generator", "Image Classifier"], state="readonly", width=20).pack(side="left", padx=6)

        ttk.Button(top, text="Run", command=self._on_run).pack(side="right")
        ttk.Button(top, text="Choose file", command=self._on_choose_file).pack(side="right", padx=6)

        # Main body
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=10, pady=6)

        left = ttk.Frame(body)
        left.pack(side="left", fill="both", expand=True)

        right = ttk.Frame(body, width=360)
        right.pack(side="right", fill="y")

        # Left: input
        self._input_label = ttk.Label(left, text="Text Input:")
        self._input_label.pack(anchor="w")
        self._text_input = scrolledtext.ScrolledText(left, height=12)
        self._text_input.pack(fill="both", expand=False)

        self._image_preview = ttk.Label(left)
        self._image_preview.pack(fill="both", expand=True, pady=8)
        self._image_preview.image = None

        # Right: output, info, OOP
        ttk.Label(right, text="Output:").pack(anchor="w")
        self._output_box = scrolledtext.ScrolledText(right, height=10)
        self._output_box.pack(fill="x")

        ttk.Label(right, text="Model info:").pack(anchor="w")
        self._model_info = tk.Text(right, height=6, wrap="word")
        self._model_info.pack(fill="x")
        self._update_model_info()

        ttk.Label(right, text="OOP used (brief):").pack(anchor="w")
        self._oop_text = tk.Text(right, height=10, wrap="word")
        self._oop_text.pack(fill="both", expand=True)
        self._update_oop_text()

    # ---------- Helpers ----------
    def _on_choose_file(self):
        if self._input_type.get() == "Image":
            path = filedialog.askopenfilename(title="Select image", filetypes=[("Images","*.png *.jpg *.jpeg *.bmp")])
            if path:
                self._selected_image_path = path
                self._display_image(path)
                self.log(f"Selected image: {os.path.basename(path)}")

    def _display_image(self, path):
        img = Image.open(path)
        img.thumbnail((500,500))
        tkimg = ImageTk.PhotoImage(img)
        self._image_preview.configure(image=tkimg)
        self._image_preview.image = tkimg

    def _update_model_info(self):
        text = self._text_model.info() + "\n\n" + self._image_model.info()
        self._model_info.delete("1.0", "end")
        self._model_info.insert("1.0", text)

    def _update_oop_text(self):
        s = (
            "OOP aplicado:\n"
            "- Multiple inheritance: mixins in GUI\n"
            "- Decorators: log_call, timeit in models\n"
            "- Encapsulation: private atributes  _state y _pipe\n"
            "- Polimorfism y overriding: AIModel.run() es overrited\n"
            "- Modularity: models.py separated from GUI\n"
        )
        self._oop_text.delete("1.0", "end")
        self._oop_text.insert("1.0", s)

    # ---------- Run models ----------
    def _on_run(self):
        choice = self._model_choice.get()
        itype = self._input_type.get()
        self._output_box.delete("1.0","end")

        if choice == "Text Generator":
            prompt = self._text_input.get("1.0","end").strip() or "Texto por defecto"
            res = self._text_model.run(prompt)
            self._output_box.insert("1.0", res)
        elif choice == "Image Classifier":
            if not self._selected_image_path:
                self._output_box.insert("1.0","Selecciona una imagen primero")
                return
            results = self._image_model.run(self._selected_image_path)
            lines = [f"{r['label']} ({r['score']})" for r in results]
            self._output_box.insert("1.0", "\n".join(lines))
