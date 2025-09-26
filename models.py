# models.py
"""
Versión simulada de los modelos usando OOP avanzado:
- This code has the GUI almost finilished with inputs and outputs in the GUI
- The GUI call fake models from models.py to observe the interfase
- I added decorators of time and log because the assigment asks for it.
"""

import time
from functools import wraps
import random

# ---------- DECORADTS ----------
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
    """Clase base polimórfica para todos los modelos"""
    def __init__(self, model_name: str):
        self.model_name = model_name

    def run(self, input_data):
        """Debe sobrescribirse"""
        raise NotImplementedError("Subclase debe implementar run()")

    def info(self):
        return f"Modelo base: {self.model_name}"

# ---------- SUBCLASS: Text Generator ----------
class HFTextGenerator(AIModel):
    def __init__(self, model_name="simulated-text-model"):
        super().__init__(model_name)
        self._state = "ready"  # encapsulation: private atribute

    @log_call
    @timeit
    def run(self, prompt: str, max_length=60):
        # simulación de salida
        words = ["AI", "Tkinter", "Python", "OOP", "model", "simulation"]
        text = " ".join(random.choices(words, k=min(max_length, 15)))
        return f"[Simulated by {self.model_name}] {text}"

    def info(self):
        return f"Text Generator ({self.model_name}): generate simulated text."

# ---------- SUBCLASE: Image Classifier ----------
class HFImageClassifier(AIModel):
    def __init__(self, model_name="simulated-image-model"):
        super().__init__(model_name)
        self._state = "ready"

    @log_call
    @timeit
    def run(self, image_path_or_bytes):
        # simulación de clasificación de imagen
        classes = ["cat", "dog", "tree", "car", "flower","building", "person","airplane"]
        results = [{"label": random.choice(classes), "score": round(random.random(), 3)} for _ in range(3)]
        return results

    def info(self):
        return f"Image Classifier ({self.model_name}): clasify images with random categories and scores."
