# models.py
"""
Models used for GUI:
- Real summarization model (DistilBART) for Text Generator
- Simulated image classifier
"""

# import random
import time
from functools import wraps
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# ---------- DECORATORS ----------
def log_call(func): 
    @wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0].__class__.__name__
        print(f"[LOG] {cls}.{func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIME] {func.__name__} took {end-start:.3f}s")
        return result
    return wrapper

# ---------- BASE CLASS ----------
class AIModel:
    """Polymorphic base class for all AI models"""
    def __init__(self, model_name: str):
        self.model_name = model_name

    def run(self, input_data):
        """Must be overridden"""
        raise NotImplementedError("Subclass must implement run()")

    def info(self):
        return f"Base model: {self.model_name}"

# ---------- SUBCLASS: Text Generator (real summarization) ----------
try:
    from transformers import pipeline
except ImportError:
    pipeline = None
    print("[WARNING] Transformers not installed, summary model won't work.")

class HFTextGenerator(AIModel):
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        super().__init__(model_name)
        self._state = "ready"
        self._mode = "error"
        if pipeline is not None:
            try:
                print("Loading summarization model (DistilBART)...")
                self._pipe = pipeline("summarization", model=self.model_name)
                self._mode = "real"
            except Exception as e:
                print(f"[WARNING] Could not load summarization model: {e}")

    @log_call
    @timeit
    def run(self, prompt: str, max_length=100):
        if self._mode == "real":
            try:
                result = self._pipe(prompt, max_length=max_length, do_sample=False)
                return result[0]['summary_text']
            except Exception as e:
                return f"Error running model: {e}"
        else:
            return "Summary model could not be loaded."

    def info(self):
        if self._mode == "real":
            return f"Text Generator (Summarization) using {self.model_name}"
        else:
            return f"Text Generator (Summarization) not available, check connection"

# ---------- SUBCLASS: Image Classifier ----------
class HFImageClassifier(AIModel):
    def __init__(self, model_name="microsoft/resnet-18"):
        super().__init__(model_name)
        self._state = "ready"
        self._model = None
        self._processor = None
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # try to load ResNet-18
        try:
            print(f"Loading {self.model_name}...")
            self._processor = AutoImageProcessor.from_pretrained(model_name)
            self._model = AutoModelForImageClassification.from_pretrained(model_name)
            self._model.to(self._device)
            print(f"{self.model_name} loaded successfully on {self._device}.")
        except Exception as e:
            print(f"Failed to load {self.model_name}: {e}")
            self._model = None

    @log_call
    @timeit
    def run(self, image_path: str):
        if self._model is None:
            return "Image classification model could not be loaded."

        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self._processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self._device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self._model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                top5_prob, top5_idx = torch.topk(probs, 1)

            results = []
            for prob, idx in zip(top5_prob[0], top5_idx[0]):
                label = self._model.config.id2label[idx.item()]
                results.append({"label": label, "score": round(prob.item(), 3)})
            return results

        except Exception as e:
            return f"Failed to classify image: {e}"

    def info(self):
        if self._model is not None:
            return f"Image Classifier ({self.model_name}): real model for image classification."
        else:
            return f"Image Classifier ({self.model_name}): could not load model."