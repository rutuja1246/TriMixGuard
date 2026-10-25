# TriMixGuard: A Multilingual Abusive-Language Detection System

TriMixGuard is a student project that uses a pretrained multilingual transformer model to classify text as **Normal** or **Abusive**. The application accepts text without requiring users to specify its language, making it suitable for experimenting with English, Hindi, Marathi, Romanized text, and code-mixed inputs.

## Features

- **Language-independent input interface:** No manual language selection is required.
- **Binary text classification:** Predicts Normal or Abusive.
- **Model confidence:** Displays the model's confidence score alongside the prediction.
- **Input validation:** Handles empty input and text exceeding the supported length.
- **Simple web interface:** Built with Streamlit.
- **Modular implementation:** Separates the user interface, prediction logic, and transliteration utility.

## Technology Stack

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- Requests
- Google Input Tools transliteration endpoint

## Machine Learning Model

**Model:** [`Hate-speech-CNERG/indic-abusive-allInOne-MuRIL`](https://huggingface.co/Hate-speech-CNERG/indic-abusive-allInOne-MuRIL)

The application maps the model's output labels as follows:

| Model label | Application prediction |
|---|---|
| `LABEL_0` | Normal |
| `LABEL_1` | Abusive |

The model is loaded using Hugging Face Transformers and currently runs on the CPU.

The displayed confidence score represents the model's score for its predicted class. It does not guarantee that the prediction is correct.

## Project Structure

```text
TriMixGuard/
├── app.py
├── predictor.py
├── transliterator.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/              # Local environment; not committed
```

- **`app.py`** — Streamlit interface, text input, prediction display, and explanatory information.
- **`predictor.py`** — Model loading, label mapping, inference, and input validation.
- **`transliterator.py`** — Utility for transliterating Romanized Hindi and Marathi into Devanagari using Google Input Tools.
- **`requirements.txt`** — Python dependencies.
- **`.gitignore`** — Excludes local environment files and generated caches.

## Getting Started

### Prerequisites

- Python installed on your system.
- Git.
- An internet connection for downloading the pretrained model and accessing the transliteration service.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TriMixGuard
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the HTTPS URL of this project's GitHub repository.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

The first model initialization may take time because the pretrained model needs to be downloaded.

## Current Implementation Status

The Streamlit interface and direct classification pipeline are implemented. The standalone transliteration utility has been tested for Hindi and Marathi inputs, but its output quality may vary.

The interface currently sends the original input directly to the classifier. Optional transliteration has **not yet been integrated into the interface**.

## Limitations

- Predictions may be incorrect, particularly for code-mixed text, sarcasm, spelling variations, context-dependent expressions, and underrepresented language varieties.
- Transliteration can produce unnatural or incorrect spellings, particularly for Marathi.
- The application has not yet established a rigorous benchmark of real-world performance.
- Initial example predictions are sanity checks, not a scientific evaluation.
- Model confidence should not be interpreted as guaranteed accuracy.
- Abusive language is not necessarily hate speech. The current application does not identify specific hate categories, castes, religions, protected groups, or targets.

## Future Work

- Integrate optional transliteration with explicit error handling.
- Evaluate direct classification against transliteration-first classification.
- Develop a reviewed, appropriately labelled evaluation dataset.
- Add automated tests for input validation and prediction behavior.
- Prepare reproducible deployment and CI/CD workflows.

## Disclaimer

TriMixGuard is an educational project intended for experimentation and demonstration. Its predictions should not be treated as definitive judgments about a person or a statement.
