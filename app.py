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

st.title("📄 PDF Dark Mode Converter")

st.markdown("""
Convert your PDFs into a comfortable dark theme while preserving:

- ✅ Hyperlinks
- ✅ Bookmarks
- ✅ Searchable Text
- ✅ PDF Quality
""")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

theme = st.radio(
    "Choose Dark Theme",
    (
        "Soft Dark (Gray)",
        "Pure Black"
    )
)

if uploaded_file:

    st.info(f"Selected Theme: **{theme}**")

    if st.button("🚀 Convert PDF", use_container_width=True):

        unique_id = uuid.uuid4().hex

        input_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_input.pdf")
        output_pdf = os.path.join(tempfile.gettempdir(), f"{unique_id}_output.pdf")

        with open(input_pdf, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if theme == "Soft Dark (Gray)":

            transfer = (
                "{1 exch sub 0.8 mul 0.2 add}"
                "{1 exch sub 0.8 mul 0.2 add}"
                "{1 exch sub 0.8 mul 0.2 add}"
                "{1 exch sub 0.8 mul 0.2 add}"
            )

        else:

            transfer = (
                "{1 exch sub}"
                "{1 exch sub}"
                "{1 exch sub}"
                "{1 exch sub}"
            )

        cmd = [
            "gs",
            "-o",
            output_pdf,
            "-sDEVICE=pdfwrite",
            "-c",
            transfer + " setcolortransfer",
            "-f",
            input_pdf,
        ]

        with st.spinner("Converting PDF..."):

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        if result.returncode == 0:

            st.success("✅ Conversion completed successfully!")

            with open(output_pdf, "rb") as f:

                st.download_button(
                    "⬇ Download Converted PDF",
                    f,
                    file_name="converted.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        else:

            st.error("❌ Ghostscript failed to convert the PDF.")

            st.code(result.stderr.decode())

        if os.path.exists(input_pdf):
            os.remove(input_pdf)

        if os.path.exists(output_pdf):
            os.remove(output_pdf)
