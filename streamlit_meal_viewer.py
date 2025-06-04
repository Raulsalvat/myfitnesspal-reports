import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from openai import OpenAI
from shared.supabase_client import get_supabase_client
import csv, io

st.set_page_config(layout="wide")
st.title("🐶 Nutrition & Chat Assistant — All in One")

# Initialize
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
supabase = get_supabase_client()

# Sidebar Upload → Supabase
with st.sidebar.expander("📤 Upload Meals"):
    uf = st.file_uploader("Upload CSV", type="csv")
    if uf:
        content = uf.getvalue().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        inserted, skipped = 0, 0
        for row in reader:
            # map/clean (same HEADER_MAP logic)
            # duplicate skip or insert to supabase...
            pass
        st.success(f"{inserted} inserted, {skipped} skipped.")

# Fetch & Display Data
resp = supabase.table("meals").select("*").execute()
df = pd.DataFrame(resp.data)
st.subheader("📊 Meals Data")
st.dataframe(df)

# Q&A Chat Section
st.subheader("🤖 Ask Nutrition Coach")
user_q = st.text_input("Your question:")
if user_q:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    context_csv = df.to_csv(index=False)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a nutrition coach."},
            {"role":"user","content":user_q},
            {"role":"user","content":f"Data:\n{context_csv}"}
        ]
    )
    ans = resp.choices[0].message.content.strip()
    st.session_state.chat_history.append((user_q, ans))

for q, a in st.session_state.chat_history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Coach:** {a}")

# PDF Export Entire View
def export_pdf():
    buf = BytesIO()
    c = Canvas(buf, pagesize=letter)
    c.drawString(30, 770, "Meals & Chat Summary")
    # Add a table or charts you'd like (omitted for brevity)
    y = 740
    for (q, a) in st.session_state.chat_history:
        c.drawString(30, y, f"You: {q}")
        y -= 14
        c.drawString(30, y, f"Coach: {a}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 770
    c.save()
    buf.seek(0)
    return buf

if st.button("📄 Export All as PDF"):
    pdf = export_pdf()
    st.download_button("Download PDF", pdf, "summary.pdf", "application/pdf")
