import streamlit as st
import subprocess
import os

st.title("PDF Dark Mode Converter")
st.write("Upload your PDF to convert it with your preferred dark theme.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with open("input.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    output_file = "output.pdf"
    
    mode = st.selectbox(
        "Choose your Dark Mode variation:",
        ("Classic Invert", "Pitch Black", "Greenish Terminal")
    )

    if st.button("Convert to Dark Mode"):
        # Define command
        if mode == "Classic Invert":
            cmd = [
                "gs", "-o", output_file, "-sDEVICE=pdfwrite",
                "-c", "{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add} setcolortransfer",
                "-f", "input.pdf"
            ]
        elif mode == "Pitch Black":
            cmd = ["gs", "-o", output_file, "-sDEVICE=pdfwrite", "-sColorConversionStrategy=Gray", "-f", "input.pdf"]
        elif mode == "Greenish Terminal":
            # Using sRGB profile to attempt tint
            cmd = ["gs", "-o", output_file, "-sDEVICE=pdfwrite", "-sColorConversionStrategy=RGB", "-f", "input.pdf"]

        # Run process and catch errors
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if os.path.exists(output_file):
                with open(output_file, "rb") as f:
                    st.download_button("Download Converted PDF", f, file_name="converted.pdf")
                st.success("Conversion complete!")
            else:
                st.error("Conversion failed: Output file was not created.")
        except subprocess.CalledProcessError as e:
            st.error(f"Ghostscript Error: {e.stderr}")
