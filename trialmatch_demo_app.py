
import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="TrialMatch Demo", layout="wide")
st.title("TrialMatch - AI התאמה למחקרים קליניים")

st.markdown("הדגמה של אבטיפוס: ניתוח פרוטוקול מחקר + סיכום ביקור של מטופל והשוואה ביניהם")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

protocol_file = st.file_uploader("העלה קובץ PDF של פרוטוקול מחקר", type="pdf")
summary_file = st.file_uploader("העלה קובץ PDF של סיכום ביקור מטופל", type="pdf")

if protocol_file and summary_file:
    protocol_text = extract_text_from_pdf(protocol_file)
    summary_text = extract_text_from_pdf(summary_file)

    prompt = f"""
    אתה מערכת בינה מלאכותית שמסייעת בהתאמת מטופלים למחקרים קליניים.
    קרא את קטעי הטקסט הבאים:

    1. פרוטוקול מחקר:
    {protocol_text}

    2. סיכום רפואי של מטופל:
    {summary_text}

    האם המטופל מתאים למחקר לפי קריטריוני ההכללה והאי-הכללה? נמק בקצרה.
    סכם אילו קריטריונים התקיימו ואילו לא.
    """

    with st.spinner("מבצע ניתוח והשוואה עם GPT..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700,
        )
        result = response.choices[0].message["content"]

    st.subheader("תוצאת ההתאמה:")
    st.write(result)
