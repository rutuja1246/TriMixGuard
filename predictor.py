
from transformers import pipeline

MODEL_NAME = "Hate-speech-CNERG/indic-abusive-allInOne-MuRIL"

LABEL_NAMES = {
    "LABEL_0": "Normal",
    "LABEL_1": "Abusive",
}

# Load the model once when this module is imported.
classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME,
    device=-1,
)


def predict_abuse(text):
    """Classify input text as Normal or Abusive."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Please enter some text.")

    if len(text) > 1000:
        raise ValueError("Text must be 1000 characters or fewer.")

    result = classifier(text, truncation=True)[0]

    label = result["label"]

    if label not in LABEL_NAMES:
        raise ValueError(f"Unexpected model label: {label}")

    return {
        "prediction": LABEL_NAMES[label],
        "confidence": round(float(result["score"]) * 100, 2),
    }
