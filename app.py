import streamlit as st
import subprocess
import tempfile
import os
import uuid

st.set_page_config(
    page_title="PDF Dark Mode Converter",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>
.stTextInput > div > div > input:focus {
    outline: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📄 PDF Dark Mode Converter</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Advantages")
    st.markdown("""
✅ Hyperlinks preserved

✅ Bookmarks maintained

✅ Searchable text remains

✅ Original PDF quality
""")

with col2:
    st.markdown("#### Limitations")
    st.markdown("""
❌ Images will be inverted

❌ Only two color modes
""")

st.divider()

uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

st.markdown("### Page Range (Optional)")

use_page_range = st.checkbox("Convert only selected pages")

if use_page_range:
    c1, c2 = st.columns(2)

    with c1:
        start_page = st.number_input(
            "From Page",
            min_value=1,
            value=1,
            step=1
        )

    with c2:
        end_page = st.number_input(
            "To Page",
            min_value=start_page,
            value=start_page,
            step=1
        )

    st.success(f"Selected pages: {start_page} to {end_page}")

theme = st.radio(
    "Choose Dark Theme",
    ("Soft Dark (Gray)", "Pure Black")
)

if uploaded_files:

    if st.button("🚀 Convert PDF(s)", use_container_width=True):

        transfer = "{1 exch sub 0.8 mul 0.2 add}" * 4 if theme == "Soft Dark (Gray)" else "{1 exch sub}" * 4

        for uploaded_file in uploaded_files:

            unique_id = uuid.uuid4().hex

            input_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_input.pdf")
            output_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_output.pdf")

            with open(input_pdf, "wb") as f:
                f.write(uploaded_file.getbuffer())

            cmd = [
                "gs",
                "-o", output_pdf,
                "-sDEVICE=pdfwrite",
                "-c", transfer + " setcolortransfer"
            ]

            if use_page_range:
                cmd.extend([
                    f"-dFirstPage={start_page}",
                    f"-dLastPage={end_page}"
                ])

            cmd.extend(["-f", input_pdf])

            with st.spinner(f"Converting {uploaded_file.name}..."):
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            if result.returncode == 0:
                with open(output_pdf, "rb") as f:
                    st.download_button(
                        label=f"⬇ Download {uploaded_file.name}",
                        data=f,
                        file_name=f"dark_{uploaded_file.name}",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.error(f"❌ Failed to convert {uploaded_file.name}")
                st.code(result.stderr.decode())

            if os.path.exists(input_pdf):
                os.remove(input_pdf)

            if os.path.exists(output_pdf):
                os.remove(output_pdf)
