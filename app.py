if st.button("🚀 Convert PDF(s)", use_container_width=True):

    import zipfile

    zip_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.zip")

    progress = st.progress(0)
    status = st.empty()

    with zipfile.ZipFile(zip_path, "w") as zipf:

        total = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            status.write(f"📄 Processing **{uploaded_file.name}** ({index+1}/{total})")

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

    os.remove(zip_path)
