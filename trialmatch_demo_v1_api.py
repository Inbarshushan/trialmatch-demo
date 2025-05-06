
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI

# Load logo
st.image("trialmatch_logo.png", width=150)

# Title
st.title("TrialMatch - בדיקת התאמה למחקר קליני")

# Upload multiple medical documents
uploaded_medical_files = st.file_uploader("העלאת מסמכים רפואיים (PDF)", type="pdf", accept_multiple_files=True)

# Upload trial protocol
uploaded_protocol_file = st.file_uploader("העלאת פרוטוקול מחקר (PDF)", type="pdf")

# Function to extract text from PDFs
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Process and display result
if uploaded_medical_files and uploaded_protocol_file and st.button("בדוק התאמה"):
    # Extract texts
    medical_texts = [extract_text_from_pdf(file) for file in uploaded_medical_files]
    combined_medical_text = "\n---\n".join(medical_texts)
    protocol_text = extract_text_from_pdf(uploaded_protocol_file)

    # Prepare prompt for GPT
    prompt = f"""
    אתה מערכת תומכת החלטה למחקרים קליניים. 
    פרוטוקול מחקר:\n{protocol_text}\n
    סיכום רפואי של המטופל:\n{combined_medical_text}\n
    האם המטופל עומד בקריטריוני ההכללה והאי-הכללה? פרט והסבר אילו קריטריונים מתקיימים ואילו לא.
    """

    # Authenticate with OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Get completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Display result
    st.subheader("תוצאת ההתאמה:")
    st.write(response.choices[0].message.content)
