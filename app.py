import streamlit as st
import joblib
import numpy as np
import re
from nltk.corpus import stopwords

# Download stopwords dataset
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))

#load model
model = joblib.load('fake_job_model.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')

feature_names = tfidf.get_feature_names_out()
coefficients = model.coef_[0]

top_fake_indices = np.argsort(coefficients)[-20:]
suspicious_words = [feature_names[i] for i in top_fake_indices]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]',' ',text)
    words = text.split()
    words = [w for w in words if w not in stopwords]

    return ' '.join(words)

def predict_job(text):
    cleaned = clean_text(text)

    vector = tfidf.transform([cleaned])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0][1]

    return prediction, probability
def find_suspicious_words(text):

    words = text.lower().split()

    found = [w for w in words if w in suspicious_words]

    return list(set(found))
def highlight_words(text, suspicious):

    words = text.split()

    highlighted = []

    for w in words:
        clean = w.lower()

        if clean in suspicious:
            highlighted.append(f"<span style='color:red;font-weight:bold'>{w}</span>")
        else:
            highlighted.append(w)

    return " ".join(highlighted)


st.title('Fake Job Posting Dectector AI')

job_text = st.text_area('Paste Job Description')

if st.button('Detect Job Fraud'):
    pred, prob = predict_job(job_text)

    suspicious = find_suspicious_words(job_text)

    if pred == 1:
        st.error(f"⚠ Fake Job Detected (Probability: {prob:.2f})")
        highlighted = highlight_words(job_text, suspicious)

        st.markdown("### ⚠ Suspicious words detected")
        st.markdown(highlighted, unsafe_allow_html=True)
    else:
        st.success(f"✅ Real Job Posting (Fake Probability: {prob:.2f})")

    
    
