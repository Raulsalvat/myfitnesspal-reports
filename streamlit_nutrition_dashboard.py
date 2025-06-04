# ======================================
# 🤖 Chat with Your Nutrition Coach
# ======================================
st.header("🤖 Chat with Your Nutrition Coach")

# Initialize once
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_q = st.text_input("Ask a question about your nutrition...", key="user_q")

# Process user question once per submit
if st.session_state.get("user_q_submitted") != user_q and user_q:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    context = df.to_csv(index=False)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a nutrition coach."},
            {"role": "user", "content": user_q},
            {"role": "user", "content": f"Data:\n{context}"}
        ]
    )
    answer = resp.choices[0].message.content.strip()
    st.session_state.chat_history.append((user_q, answer))
    st.session_state.user_q_submitted = user_q  # Prevent re-processing

# Display history
for q, a in st.session_state.chat_history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Coach:** {a}")

# 📄 Export Chat as PDF
def create_chat_pdf():
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setFont("Helvetica-Bold", 14); c.drawString(50, 750, "Nutrition Chat History")
    y = 730
    c.setFont("Helvetica", 10)
    for q, a in st.session_state.chat_history:
        for line in [f"You: {q}", f"Coach: {a}", ""]:
            c.drawString(50, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                y = 750
    c.save()
    buf.seek(0)
    return buf

if st.button("📄 Export Chat as PDF"):
    pdf = create_chat_pdf()
    st.download_button("Download Chat PDF", pdf, "nutrition_chat.pdf", "application/pdf")
