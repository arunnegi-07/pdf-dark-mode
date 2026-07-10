import streamlit as st
import subprocess
import os

st.title("PDF Dark Mode Converter")
st.write("Upload your PDF to invert colors with your custom dark theme.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file
    with open("input.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Run Ghostscript command
    output_file = "output.pdf"
    cmd = [
        "gs", "-o", output_file, "-sDEVICE=pdfwrite",
        "-c", "{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add} setcolortransfer",
        "-f", "input.pdf"
    ]
    
    if st.button("Convert to Dark Mode"):
        subprocess.run(cmd)
        
        # Provide download button
        with open(output_file, "rb") as f:
            st.download_button("Download Inverted PDF", f, file_name="inverted.pdf")
            st.success("Conversion complete!")
