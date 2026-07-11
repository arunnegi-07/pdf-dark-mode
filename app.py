import streamlit as st
import subprocess

st.set_page_config(page_title="PDF Dark Mode Converter")

st.title("📄 PDF Dark Mode Converter")
st.write("Upload your PDF and choose a dark theme.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

theme = st.radio(
    "Choose Theme",
    [
        "Soft Dark (Gray)",
        "Pure Black",
        "Green Dark"
    ]
)

if uploaded_file is not None:

    # Save uploaded file
    with open("input.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Select Ghostscript color transfer
    if theme == "Soft Dark (Gray)":
        transfer = (
            "{1 exch sub 0.8 mul 0.2 add}"
            "{1 exch sub 0.8 mul 0.2 add}"
            "{1 exch sub 0.8 mul 0.2 add}"
            "{1 exch sub 0.8 mul 0.2 add}"
        )

    elif theme == "Pure Black":
        transfer = (
            "{1 exch sub}"
            "{1 exch sub}"
            "{1 exch sub}"
            "{1 exch sub}"
        )

    elif theme == "Green Dark":
        # Approximate green theme
        transfer = (
            "{1 exch sub 0.65 mul 0.10 add}"   # Red
            "{1 exch sub}"                     # Green
            "{1 exch sub 0.65 mul 0.10 add}"   # Blue
            "{1 exch sub 0.65 mul 0.10 add}"   # Gray
        )

    output_file = "output.pdf"

    cmd = [
        "gs",
        "-o",
        output_file,
        "-sDEVICE=pdfwrite",
        "-c",
        transfer + " setcolortransfer",
        "-f",
        "input.pdf",
    ]

    if st.button("Convert"):

        result = subprocess.run(cmd)

        if result.returncode == 0:

            with open(output_file, "rb") as f:
                st.download_button(
                    "⬇ Download Converted PDF",
                    f,
                    file_name="converted.pdf",
                    mime="application/pdf",
                )

            st.success("Conversion completed!")

        else:
            st.error("Ghostscript failed to convert the PDF.")
