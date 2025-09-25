# models.py
class AIModel:
    """Clase base para futuros modelos."""
    def __init__(self, model_name: str):
        self.model_name = model_name

    def run(self, input_data):
        """Método a sobrescribir en subclases."""
        return f"Salida simulada para '{input_data}'"

class HFTextGenerator(AIModel):
    def run(self, prompt: str, max_length=60):
        return f"[Simulado] Generando texto para: {prompt}"

class HFImageClassifier(AIModel):
    def run(self, image_path_or_bytes):
        return "[Simulado] Clasificación de imagen"
