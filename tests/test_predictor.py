
import pytest
from unittest.mock import patch

# Mock the Transformers pipeline BEFORE importing predictor.
# This prevents MuRIL from downloading during tests.
with patch("transformers.pipeline") as mock_pipeline:
    mock_pipeline.return_value = lambda *args, **kwargs: [
        {"label": "LABEL_0", "score": 0.95}
    ]
    import predictor


@pytest.fixture
def mock_classifier():
    """Provide a predictable fake classifier for each test."""
    with patch.object(
        predictor, "classifier"
    ) as mock:
        mock.return_value = [
            {"label": "LABEL_0", "score": 0.95}
        ]
        yield mock


def test_empty_input_is_rejected(mock_classifier):
    with pytest.raises(ValueError):
        predictor.predict_abuse("")


def test_whitespace_input_is_rejected(mock_classifier):
    with pytest.raises(ValueError):
        predictor.predict_abuse("   \t\n")


def test_input_over_1000_characters_is_rejected(mock_classifier):
    with pytest.raises(ValueError):
        predictor.predict_abuse("a" * 1001)


def test_non_string_input_is_rejected(mock_classifier):
    with pytest.raises(TypeError):
        predictor.predict_abuse(123)


def test_normal_label_mapping(mock_classifier):
    result = predictor.predict_abuse("Hello, how are you?")

    assert result["prediction"] == "Normal"
    assert result["confidence"] == 95.0


def test_abusive_label_mapping(mock_classifier):
    mock_classifier.return_value = [
        {"label": "LABEL_1", "score": 0.87}
    ]

    result = predictor.predict_abuse("Test abusive text")

    assert result["prediction"] == "Abusive"
    assert result["confidence"] == 87.0


def test_output_structure(mock_classifier):
    result = predictor.predict_abuse("Hello")

    assert set(result.keys()) == {"prediction", "confidence"}
    assert isinstance(result["prediction"], str)
    assert isinstance(result["confidence"], float)


def test_classifier_receives_valid_input(mock_classifier):
    predictor.predict_abuse("  Hello  ")

    mock_classifier.assert_called_once_with(
        "Hello", truncation=True
    )


def test_unknown_model_label_is_rejected(mock_classifier):
    mock_classifier.return_value = [
        {"label": "LABEL_9", "score": 0.50}
    ]

    with pytest.raises(ValueError, match="Unexpected model label"):
        predictor.predict_abuse("Some text")


def test_classifier_error_is_propagated(mock_classifier):
    mock_classifier.side_effect = RuntimeError("Model unavailable")

    with pytest.raises(RuntimeError, match="Model unavailable"):
        predictor.predict_abuse("Hello")


def test_confidence_is_rounded_to_two_decimal_places(mock_classifier):
    mock_classifier.return_value = [
        {"label": "LABEL_1", "score": 0.87654}
    ]

    result = predictor.predict_abuse("Test text")

    assert result["confidence"] == 87.65
