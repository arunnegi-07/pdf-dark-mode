import streamlit as st
import subprocess
import tempfile
import os
import uuid
import re

# Page configuration
st.set_page_config(page_title="PDF Dark Mode Converter", page_icon="📄", layout="centered")

# CSS: This targets the box in all states (normal, hover, and focus)
st.markdown("""
<style>
    /* Remove default Streamlit focus border and set custom one */
    .stTextInput > div > div > input:focus {
        outline: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>📄 PDF Dark Mode Converter</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Advantages")
    st.markdown("✅ Hyperlinks preserved\n✅ Bookmarks maintained\n✅ Searchable text remains\n✅ Original PDF quality")
with col2:
    st.markdown("#### Limitations")
    st.markdown("❌ Images will be inverted\n❌ Only two color modes")

st.divider()

uploaded_files = st.file_uploader("Upload PDF(s)", type=["pdf"], accept_multiple_files=True)

# Page Range Input
page_range = st.text_input("Page Range (Optional, e.g., 1-10)", placeholder="Leave blank for all pages")

# Validate
is_valid = page_range == "" or re.match(r"^\d+-\d+$", page_range)

# Conditional Border CSS
border_color = "#00FF00" if (page_range == "" or is_valid) else "#FF4B4B"
if page_range:
    st.markdown(f"""
    <style>
        .stTextInput > div > div > input {{
            border: 2px solid {border_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

theme = st.radio("Choose Dark Theme", ("Soft Dark (Gray)", "Pure Black"))

if uploaded_files:
    if st.button("🚀 Convert PDF(s)", use_container_width=True):
        if page_range and not is_valid:
            st.error("Invalid page range format. Please use 'Start-End' (e.g., 1-10).")
        else:
            transfer = "{1 exch sub 0.8 mul 0.2 add}" * 4 if theme == "Soft Dark (Gray)" else "{1 exch sub}" * 4
            
            for uploaded_file in uploaded_files:
                unique_id = uuid.uuid4().hex
                input_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_input.pdf")
                output_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_output.pdf")

                with open(input_pdf, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                cmd = ["gs", "-o", output_pdf, "-sDEVICE=pdfwrite", "-c", transfer + " setcolortransfer"]
                if is_valid and page_range:
                    parts = page_range.split('-')
                    cmd.extend(["-dFirstPage=" + parts[0], "-dLastPage=" + parts[-1]])
                cmd.extend(["-f", input_pdf])

                with st.spinner(f"Converting {uploaded_file.name}..."):
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if result.returncode == 0:
                    with open(output_pdf, "rb") as f:
                        st.download_button(f"⬇ Download {uploaded_file.name}", f, file_name=f"dark_{uploaded_file.name}", use_container_width=True)
                else:
                    st.error(f"❌ Failed to convert {uploaded_file.name}")
                
                if os.path.exists(input_pdf): os.remove(input_pdf)
                if os.path.exists(output_pdf): os.remove(output_pdf)
