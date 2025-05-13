
import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

# Load API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page settings and logo
st.set_page_config(page_title="TrialMatch Demo", page_icon="🔬")
st.image("A_logo_for_a_company_named_TrialMatch_is_displayed.png", width=200)
st.title("TrialMatch – התאמת מטופלים למחקרים קליניים באמצעות בינה מלאכותית")

# Upload section
protocol_file = st.file_uploader("📄 העלה את פרוטוקול המחקר (PDF)", type="pdf")
medical_files = st.file_uploader("📁 העלה קבצי מידע רפואי של המטופל (PDF)", type="pdf", accept_multiple_files=True)

if protocol_file and medical_files:
    with st.spinner("🔍 מבצע ניתוח והשוואה..."):
        # Read protocol
        protocol_reader = PdfReader(protocol_file)
        protocol_text = "\n".join([page.extract_text() for page in protocol_reader.pages])

        # Step 1: Extract criteria
        extraction_prompt = f"""
        להלן טקסט מתוך פרוטוקול מחקר קליני. אתר רק את סעיפי הקריטריונים להכללה ואי-הכללה.
        החזר את הטקסט שלהם בלבד בפורמט ברור:
        ### קריטריוני הכללה:
        ...
        ### קריטריוני אי-הכללה:
        ...
        
        פרוטוקול:
        {protocol_text[:10000]}
