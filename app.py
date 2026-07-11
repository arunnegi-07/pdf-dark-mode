progress_bar = st.progress(0)
status = st.empty()

status.text("Preparing PDF...")

import threading
import time

conversion_done = False

def run_conversion():
    global conversion_done
    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    conversion_done = True

thread = threading.Thread(target=run_conversion)
thread.start()

progress = 0

while not conversion_done:

    if progress < 85:
        progress += 1
    elif progress < 95:
        progress += 0.2

    progress_bar.progress(min(int(progress), 95))

    if progress < 30:
        status.text("Preparing PDF...")
    elif progress < 70:
        status.text("Applying dark theme...")
    else:
        status.text("Finalizing PDF...")

    time.sleep(0.08)

thread.join()

progress_bar.progress(100)
status.text("Conversion completed!")
