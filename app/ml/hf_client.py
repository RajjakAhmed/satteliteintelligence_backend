from gradio_client import Client
from app.config import settings


# ✅ Load Hugging Face Space Client
client = Client("Rajjakahmed/spaceai-terrain-model")


def predict_from_huggingface(image_url: str):
    """
    Sends Supabase Image URL to HuggingFace Space
    Returns: label + confidence
    """

    try:
        result = client.predict(
            image_url=image_url,
            api_name="/predict"
        )

        # result = ["Forest", 0.92]
        label = result[0]
        confidence = float(result[1])

        return label, confidence

    except Exception as e:
        raise Exception(f"Hugging Face Prediction Error: {str(e)}")
