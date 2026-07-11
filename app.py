import streamlit as st
import subprocess
import os

st.title("PDF Dark Mode Converter")
# Get the absolute path to the current working directory
base_path = os.getcwd()
input_pdf = os.path.join(base_path, "input.pdf")
output_pdf = os.path.join(base_path, "output.pdf")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with open(input_pdf, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    mode = st.selectbox("Choose variation:", ("Classic Invert", "Pitch Black", "Greenish Terminal"))

    if st.button("Convert to Dark Mode"):
        # Define base command parts
        base_cmd = ["gs", "-o", output_pdf, "-sDEVICE=pdfwrite", "-f", input_pdf]
        
        # Define mode-specific flags
        if mode == "Classic Invert":
            cmd = ["gs", "-o", output_pdf, "-sDEVICE=pdfwrite", 
                   "-c", "{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add}{1 exch sub 0.8 mul 0.2 add} setcolortransfer", 
                   "-f", input_pdf]
        elif mode == "Pitch Black":
            # Using Gray color strategy to force high-contrast black
            cmd = ["gs", "-o", output_pdf, "-sDEVICE=pdfwrite", "-sColorConversionStrategy=Gray", "-f", input_pdf]
        elif mode == "Greenish Terminal":
            # Using standard RGB conversion
            cmd = ["gs", "-o", output_pdf, "-sDEVICE=pdfwrite", "-sColorConversionStrategy=RGB", "-f", input_pdf]

        try:
            # Run the command and capture output
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if os.path.exists(output_pdf):
                with open(output_pdf, "rb") as f:
                    st.download_button("Download Converted PDF", f, file_name="converted.pdf")
                st.success("Conversion complete!")
            else:
                st.error("Output file was not generated.")
        except subprocess.CalledProcessError as e:
            st.error(f"Ghostscript Error: {e.stderr}")
            st.write("Debugging Info:", e.cmd)
