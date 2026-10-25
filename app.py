
import streamlit as st
from predictor import predict_abuse

st.set_page_config(
    page_title="TriMixGuard",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ TriMixGuard")
st.subheader("Multilingual Abusive-Language Detection")

st.write(
    "Enter text in English, Hindi, Marathi, Romanized Hindi, "
    "Romanized Marathi, or a mix of languages."
)

text_input = st.text_area(
    "Enter text to analyze",
    placeholder="Type or paste your text here...",
    height=150,
    max_chars=1000,
)

if st.button(
    "Analyze text",
    type="primary",
    use_container_width=True,
):
    cleaned_text = text_input.strip()

    if not cleaned_text:
        st.warning("Please enter some text first.")

    else:
        with st.spinner("Analyzing text..."):
            try:
                result = predict_abuse(cleaned_text)

                st.divider()
                st.subheader("Analysis Result")

                if result["prediction"] == "Normal":
                    st.success("Prediction: Normal")
                else:
                    st.warning("Prediction: Abusive")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Model confidence",
                        f'{result["confidence"]:.2f}%',
                    )

                with col2:
                    st.metric(
                        "Characters",
                        len(cleaned_text),
                    )

                with st.expander("View submitted text"):
                    st.write(cleaned_text)

                st.caption(
                    "Confidence is not a guarantee of correctness. "
                    "The prediction may be unreliable for code-mixed "
                    "text, sarcasm, spelling variations, or languages "
                    "underrepresented in the model's training data."
                )

            except Exception as exc:
                st.error(
                    "The prediction could not be completed. "
                    "Please try again."
                )
                st.caption(
                    f"Technical details: {type(exc).__name__}: {exc}"
                )

st.divider()

with st.expander("About TriMixGuard"):
    st.write(
        "TriMixGuard uses a pretrained multilingual transformer "
        "model to classify text as Normal or Abusive."
    )
    st.write(
        "Abusive language is not necessarily hate speech. "
        "This application does not identify specific hate "
        "categories, protected groups, or targets."
    )

st.caption(
    "For educational demonstration only. Model predictions "
    "may be incorrect and should not be treated as definitive."
)
