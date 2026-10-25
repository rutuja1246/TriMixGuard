
import re
import requests

GOOGLE_INPUT_TOOLS_URL = (
    "https://inputtools.google.com/request"
)

SUPPORTED_LANGUAGES = {"hi", "mr"}


class TransliterationError(Exception):
    """Raised when transliteration cannot be completed."""


def transliterate_sentence(text, language="hi"):
    """
    Transliterate Romanized Hindi or Marathi into Devanagari
    using Google Input Tools.

    Raises TransliterationError if the request fails or the
    response does not contain usable converted text.
    """

    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Please enter text to transliterate.")

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            "Language must be 'hi' for Hindi or 'mr' for Marathi."
        )

    # This function is intended for Romanized input.
    if not text.isascii():
        raise TransliterationError(
            "Input contains non-ASCII characters. "
            "It may already use a native script."
        )

    words = text.split()
    converted_words = []

    try:
        for word in words:
            # Keep punctuation-only tokens unchanged.
            if not re.search(r"[A-Za-z]", word):
                converted_words.append(word)
                continue

            # Keep English words unchanged where possible by
            # allowing the user to transliterate only selected
            # Romanized text rather than whole code-mixed input.
            params = {
                "text": word,
                "itc": f"{language}-t-i0-und",
                "num": 1,
                "cp": 0,
                "cs": 1,
                "ie": "utf-8",
                "oe": "utf-8",
            }

            response = requests.get(
                GOOGLE_INPUT_TOOLS_URL,
                params=params,
                timeout=8,
            )
            response.raise_for_status()

            data = response.json()

            # Expected response shape:
            # ["SUCCESS", [["word", ["converted_word", ...]]]]
            if (
                not isinstance(data, list)
                or len(data) < 2
                or data[0] != "SUCCESS"
                or not data[1]
                or not data[1][0]
                or len(data[1][0]) < 2
                or not data[1][0][1]
            ):
                raise TransliterationError(
                    f"No conversion returned for token: {word}"
                )

            candidates = data[1][0][1]

            if not isinstance(candidates, list) or not candidates:
                raise TransliterationError(
                    f"Invalid conversion for token: {word}"
                )

            converted_words.append(candidates[0])

    except TransliterationError:
        raise
    except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
        raise TransliterationError(
            "Transliteration service failed. Check your connection "
            "and try again."
        ) from exc

    converted_text = " ".join(converted_words)

    if not converted_text:
        raise TransliterationError(
            "The service returned no converted text."
        )

    return converted_text
