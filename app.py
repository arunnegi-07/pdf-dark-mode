import streamlit as st
import subprocess
import os

st.title("PDF Dark Mode Converter")
st.write("Upload your PDF to convert it with your preferred dark theme.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file
    with open("input.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    output_file = "output.pdf"
    
    # Selection for mode
    mode = st.selectbox(
        "Choose your Dark Mode variation:",
        ("Classic Invert", "Pitch Black", "Greenish Terminal")
    )

    # Command logic based on selection
    if mode == "Classic Invert":
        cmd = [
            "gs", "-o", output_file, "-sDEVICE=pdfwrite",
            "-c", "{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add} setcolortransfer",
            "-f", "input.pdf"
        ]
    elif mode == "Pitch Black":
        # Force grayscale for high contrast black
        cmd = ["gs", "-o", output_file, "-sDEVICE=pdfwrite", "-sColorConversionStrategy=Gray", "-f", "input.pdf"]
    elif mode == "Greenish Terminal":
        # Strategy to encourage RGB processing for a tinted look
        cmd = ["gs", "-o", output_file, "-sDEVICE=pdfwrite", "-sColorConversionStrategy=RGB", "-f", "input.pdf"]

    if st.button("Convert to Dark Mode"):
        subprocess.run(cmd)

        # Provide download button
        if os.path.exists(output_file):
            with open(output_file, "rb") as f:
                st.download_button("Download Converted PDF", f, file_name="converted.pdf")
            st.success("Conversion complete!")
        else:
            st.error("Conversion failed. Please try again.")
