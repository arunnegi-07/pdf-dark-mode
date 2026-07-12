import streamlit as st
import subprocess
import tempfile
import os
import uuid

# Page configuration
st.set_page_config(
    page_title="PDF Dark Mode Converter",
    page_icon="📄",
    layout="centered"
)

# Website Name Header (Top-Left)
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <h1 style="margin: 0;">📄 PDF Dark Mode Converter</h1>
</div>
""", unsafe_allow_html=True)

# Side-by-side layout for Advantages and Limitations
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Advantages")
    st.markdown("""
      ✅ Hyperlinks preserved\n
      ✅ Bookmarks maintained\n
      ✅ Searchable text remains\n
      ✅ Original PDF quality\n
    """)

with col2:
    st.markdown("#### Limitations")
    st.markdown("""
        ❌ Images will be inverted\n
        ❌ Only two color modes\n
    """)

st.divider()

# Input widgets
uploaded_files = st.file_uploader(
    "Upload PDF(s)", 
    type=["pdf"], 
    accept_multiple_files=True
)

page_range = st.text_input(
    "Page Range (Optional, e.g., 1-10)", 
    placeholder="Leave blank for all pages"
)

theme = st.radio(
    "Choose Dark Theme", 
    ("Soft Dark (Gray)", "Pure Black")
)

# Conversion Logic
if uploaded_files:
    if st.button("🚀 Convert PDF(s)", use_container_width=True):
        
        # Determine Ghostscript color transfer function
        if theme == "Soft Dark (Gray)":
            transfer = "{1 exch sub 0.8 mul 0.2 add}" * 4
        else:
            transfer = "{1 exch sub}" * 4
            
        for uploaded_file in uploaded_files:
            unique_id = uuid.uuid4().hex
            input_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_input.pdf")
            output_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_output.pdf")

            with open(input_pdf, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Prepare Ghostscript command
            cmd = [
                "gs", 
                "-o", output_pdf, 
                "-sDEVICE=pdfwrite", 
                "-c", transfer + " setcolortransfer"
            ]
            
            if page_range:
                parts = page_range.split('-')
                cmd.extend(["-dFirstPage=" + parts[0], "-dLastPage=" + parts[-1]])
            
            cmd.extend(["-f", input_pdf])

            # Process with Spinner
            with st.spinner(f"Converting {uploaded_file.name}... this may take a moment."):
                result = subprocess.run(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )

            # Handle result
            if result.returncode == 0:
                with open(output_pdf, "rb") as f:
                    st.download_button(
                        f"⬇ Download {uploaded_file.name}", 
                        f, 
                        file_name=f"dark_{uploaded_file.name}", 
                        use_container_width=True
                    )
            else:
                st.error(f"❌ Failed to convert {uploaded_file.name}")
            
            # Cleanup temporary files
            if os.path.exists(input_pdf): 
                os.remove(input_pdf)
            if os.path.exists(output_pdf): 
                os.remove(output_pdf)
