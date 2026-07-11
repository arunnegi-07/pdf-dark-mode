import streamlit as st
import subprocess
import tempfile
import os
import uuid

if st.button("🚀 Convert PDF(s)", use_container_width=True):

    import zipfile

    total = len(uploaded_files)

    progress = st.progress(0)
    status = st.empty()

    # ---------- SINGLE PDF ----------
    if total == 1:

        uploaded_file = uploaded_files[0]

        status.write(f"📄 Processing **{uploaded_file.name}**")

        unique_id = uuid.uuid4().hex

        input_pdf = os.path.join(
            tempfile.gettempdir(),
            f"{unique_id}_input.pdf"
        )

        output_pdf = os.path.join(
            tempfile.gettempdir(),
            f"{unique_id}_output.pdf"
        )

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

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        progress.progress(100)

        if result.returncode == 0:

            status.success("✅ Conversion completed!")

            with open(output_pdf, "rb") as f:

                st.download_button(
                    "⬇ Download Converted PDF",
                    f,
                    file_name=uploaded_file.name,
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

    # ---------- MULTIPLE PDFs ----------
    else:

        zip_path = os.path.join(
            tempfile.gettempdir(),
            f"{uuid.uuid4().hex}.zip"
        )

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for index, uploaded_file in enumerate(uploaded_files):

                status.write(
                    f"📄 Processing **{uploaded_file.name}** ({index+1}/{total})"
                )

                unique_id = uuid.uuid4().hex

                input_pdf = os.path.join(
                    tempfile.gettempdir(),
                    f"{unique_id}_input.pdf"
                )

                output_pdf = os.path.join(
                    tempfile.gettempdir(),
                    f"{unique_id}_output.pdf"
                )

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

                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                if result.returncode != 0:

                    st.error(f"❌ Failed to convert {uploaded_file.name}")
                    st.code(result.stderr.decode())
                    continue

                zipf.write(
                    output_pdf,
                    arcname=uploaded_file.name
                )

                progress.progress((index + 1) / total)

                if os.path.exists(input_pdf):
                    os.remove(input_pdf)

                if os.path.exists(output_pdf):
                    os.remove(output_pdf)

        status.success("✅ All PDFs converted successfully!")

        with open(zip_path, "rb") as f:

            st.download_button(
                "⬇ Download ZIP",
                f,
                file_name="Converted_PDFs.zip",
                mime="application/zip",
                use_container_width=True
            )

        if os.path.exists(zip_path):
            os.remove(zip_path)
