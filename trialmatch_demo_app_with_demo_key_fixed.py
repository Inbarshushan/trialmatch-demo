
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
import os

# כותרת
st.title("TrialMatch - AI התאמה למחקרים קליניים")
st.subheader("הדגמה של אבטיפוס: ניתוח פרוטוקול של מחקר + סיכום ביקור והשוואה ביניהם")

# העלאת קובץ פרוטוקול מחקר
protocol_file = st.file_uploader("העלאת קובץ PDF של פרוטוקול מחקר", type="pdf")

# העלאת קובץ סיכום ביקור
visit_file = st.file_uploader("העלאת סיכום ביקור מטופל כקובץ PDF", type="pdf")

def extract_text_from_pdf(uploaded_file):
    text = ""
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    return text

# עיבוד קבצים
if protocol_file and visit_file:
    protocol_text = extract_text_from_pdf(protocol_file)
    visit_text = extract_text_from_pdf(visit_file)

    with st.spinner("מבצע ניתוח והשוואה בין הנתונים..."):
        client = OpenAI(api_key="sk-demo-example-for-show-only-doesnt-work")  # DEMO KEY placeholder

        prompt = f"""
אתה עוזר מחקר קליני. קיבלת את פרוטוקול המחקר הבא:
---
{protocol_text}
---
וסיכום ביקור של מטופל:
---
{visit_text}
---
בדוק האם המטופל עומד בקריטריוני ההכללה או ההוצאה מהמחקר, ונמק בקצרה.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            st.subheader("תוצאת ההתאמה:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error("אירעה שגיאה בעת יצירת תשובה מהמודל. ייתכן שהמפתח אינו תקף או שהמכסה מוצתה.")
            st.code(str(e))
