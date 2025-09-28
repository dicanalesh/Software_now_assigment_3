# models.py
"""
Models used for GUI:
- Real summarization model (DistilBART) for Text Generator
- Simulated image classifier
"""

import random
import time
from functools import wraps

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

# ---------- SUBCLASS: Image Classifier (simulated) ----------
class HFImageClassifier(AIModel):
    def __init__(self, model_name="simulated-image-model"):
        super().__init__(model_name)
        self._state = "ready"

    @log_call
    @timeit
    def run(self, image_path_or_bytes):
        classes = ["cat", "dog", "tree", "car", "flower", "building", "person", "airplane"]
        results = [{"label": random.choice(classes), "score": round(random.random(), 3)} for _ in range(3)]
        return results

    def info(self):
        return f"Image Classifier ({self.model_name}): classify images with random categories and scores."
