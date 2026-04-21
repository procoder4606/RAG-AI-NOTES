import streamlit as st
import os
import tempfile
import requests
import bcrypt
import pdfplumber
from pymongo import MongoClient
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="RAG AI", 
    page_icon="🎥", 
    layout="wide"
)

# --- Import your custom processing modules ---
# Ensure these files exist in your directory
try:
    from transcriber import transcribe_audio
    from notes_generator import generate_notes
    from ocr import extract_ocr_text
except ImportError:
    st.error("Missing helper modules (transcriber.py, notes_generator.py, or ocr.py).")

# ================== CONFIG & DB ==================
MONGO_URI = os.getenv("MONGO_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@st.cache_resource
def init_db():
    if not MONGO_URI:
        st.error("MONGO_URI missing in .env")
        st.stop()
    client = MongoClient(MONGO_URI)
    return client["ai_app"]

db = init_db()
users = db["users"]
docs_col = db["documents"]

# ================== HELPERS ==================
def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

def check_password(pw, hashed):
    return bcrypt.checkpw(pw.encode(), hashed)

def export_as_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Handle encoding for standard PDF chars
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

def ask_llm(context, question):
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Answer only from context. If not found, say 'Not in document'."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ]
            }
        )
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# ================== SESSION STATE ==================
if "user" not in st.session_state:
    st.session_state.user = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ================== AUTH PAGE ==================
def auth_page():
    st.title("🎥 RAG AI")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            user = users.find_one({"username": u})
            if user and check_password(p, user["password"]):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid credentials")
    with tab2:
        ru = st.text_input("New Username")
        rp = st.text_input("New Password", type="password")
        if st.button("Register"):
            if users.find_one({"username": ru}): st.error("User exists")
            else:
                users.insert_one({"username": ru, "password": hash_password(rp)})
                st.success("Registered! Please login.")

# ================== MAIN APP ==================
def main_app():
    st.sidebar.title("RAG AI")
    st.sidebar.write(f"Logged in: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = ""
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "💬 Chat & Query", "📚 My Library"])

    # --- TAB 1: PROCESSOR ---
    with tab1:
        st.header("Upload PDF or Video/Audio")
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📄 PDF")
            pdf_file = st.file_uploader("Upload PDF", type="pdf")
            if pdf_file and st.button("Process PDF"):
                with st.spinner("Extracting..."):
                    with pdfplumber.open(pdf_file) as pdf:
                        text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
                    docs_col.insert_one({
                        "user": st.session_state.user, "filename": pdf_file.name,
                        "content": text, "type": "pdf", "uploaded_at": datetime.now()
                    })
                    st.success("PDF Saved!")

        with c2:
            st.subheader("🎥 Video/Audio")
            vid_file = st.file_uploader("Upload Media", type=["mp4","mp3","mov"])
            if vid_file and st.button("🚀 Generate Notes"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(vid_file.name)[1]) as tmp:
                    tmp.write(vid_file.read())
                    tmp_path = tmp.name
                try:
                    bar = st.progress(0, text="Initializing...")
                    # Process
                    is_video = vid_file.name.lower().endswith(('.mp4', '.mov'))
                    ocr_txt = extract_ocr_text(tmp_path) if is_video else ""
                    bar.progress(40, text="🎤 Transcribing...")
                    transcript = transcribe_audio(tmp_path)
                    bar.progress(80, text="🤖 Generating AI Notes...")
                    notes = generate_notes(f"{transcript}\n{ocr_txt}")
                    bar.progress(100, text="✅ Done!")
                    
                    docs_col.insert_one({
                        "user": st.session_state.user, "filename": vid_file.name,
                        "content": notes, "type": "video_notes", "uploaded_at": datetime.now()
                    })
                    st.text_area("Notes Preview", notes, height=200)
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

   # --- TAB 2: CHAT (RAG) ---
   # --- TAB 2: CHAT (RAG) ---
    with tab2:
        st.header("💬 Chat with your Knowledge Base")
    
    # 1. Always fetch docs first
        user_docs = list(docs_col.find({"user": st.session_state.user}))
    
    # 2. Initialize a default state for context
        context = ""

        if not user_docs:
            st.info("Your library is empty. Please upload a PDF or process a video first!")
        else:
        # 3. Create selection options SAFELY
            doc_names = [d.get("filename", "Unnamed Document") for d in user_docs]
            selection_options = ["🔍 All Documents"] + doc_names
        
        # 4. Now render the selectbox
            selected_option = st.selectbox(
            "Which document would you like to chat with?",
            options=selection_options,
            key="chat_doc_selector" # Added a key for stability
        )
        
        # 5. Determine context based on selection
        if selected_option == "🔍 All Documents":
            context = "\n\n".join([d.get("content", "") for d in user_docs])
            st.caption("AI is reading: **Entire Library**")
        else:
            selected_doc = next((d for d in user_docs if d.get("filename") == selected_option), None)
            if selected_doc:
                context = selected_doc.get("content", "")
            st.caption(f"AI is reading: **{selected_option}**")

        st.divider()

        # 6. Display Chat History
        for msg in st.session_state.history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # 7. Handle Input
        if q := st.chat_input("Ask a question..."):
            st.session_state.history.append({"role": "user", "content": q})
            
            with st.chat_message("user"):
                st.write(q)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    # Use the filtered context (limited to 6000 chars for API limits)
                    ans = ask_llm(context[:6000], q)
                    st.write(ans)
            
            st.session_state.history.append({"role": "assistant", "content": ans})
            st.rerun()
   # ==================== Tab 3: My Library ====================
    with tab3:
        st.header("📚 My Library")
    
    # 1. Fetch documents specifically for the logged-in user
    # Convert cursor to list so we can check if it's empty
        my_docs = list(docs_col.find({"user": st.session_state.user}))
    
        if not my_docs:
            st.info("Your library is empty. Upload a PDF or process a video to get started!")
        else:
            st.write(f"Showing **{len(my_docs)}** documents in your library.")
        
        # 2. Loop through each document
        for d in my_docs:
            # DEFENSIVE PROGRAMMING: Use .get() to avoid KeyErrors if fields are missing
            doc_id = d.get('_id')
            filename = d.get('filename', 'Unnamed Document')
            doc_type = d.get('type', 'unknown').upper()
            content = d.get('content', '')
            uploaded_at = d.get('uploaded_at')

            # Create an expander for each document
            with st.expander(f"📄 {filename} ({doc_type})"):
                
                # --- Metadata Section ---
                col_meta1, col_meta2 = st.columns([2, 1])
                
                with col_meta1:
                    # Safe Date Formatting
                    if uploaded_at:
                        formatted_date = uploaded_at.strftime('%Y-%m-%d %H:%M')
                    else:
                        formatted_date = "Date Unknown"
                    st.write(f"**📅 Uploaded:** {formatted_date}")
                
                with col_meta2:
                    st.write(f"**🆔 ID:** `{str(doc_id)[:10]}...`")

                # --- Content Preview ---
                # We use a unique key for the text area to prevent Streamlit duplicate widget errors
                preview_text = content[:1000] + "..." if len(content) > 1000 else content
                st.text_area(
                    "Content Preview", 
                    preview_text, 
                    height=150, 
                    disabled=True, 
                    key=f"preview_{doc_id}"
                )

                # --- Action Buttons ---
                st.markdown("---")
                btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
                
                with btn_col1:
                    # Download PDF Button
                    # Uses the export_as_pdf function defined at the top of your script
                    try:
                        pdf_data = export_as_pdf(content)
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_data,
                            file_name=f"{filename}.pdf",
                            mime="application/pdf",
                            key=f"pdf_btn_{doc_id}"
                        )
                    except Exception as e:
                        st.error("PDF Error")

                with btn_col2:
                    # Delete Button
                    if st.button("🗑️ Delete", key=f"delete_btn_{doc_id}", use_container_width=True):
                        docs_col.delete_one({"_id": doc_id})
                        st.success(f"Deleted {filename}")
                        st.rerun()
                
                with btn_col3:
                    # Info about content size
                    st.caption(f"Total characters: {len(content):,}")
# ================== RUN ==================
if st.session_state.user:
    main_app()
else:
    auth_page()