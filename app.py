import streamlit as st
from PIL import Image
import os

# Create upload directory if it doesn't exist
UPLOAD_DIR = "uploaded_arts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Arts & Crafts Gallery", layout="wide")

st.title("🎨 Arts & Crafts Web App")
st.markdown("Upload and explore beautiful artworks and handmade crafts!")

# Upload Section
st.header("📤 Upload Your Artwork")
with st.form("upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    title = st.text_input("Title of the artwork")
    description = st.text_area("Description (optional)")
    submit = st.form_submit_button("Upload")

    if submit and uploaded_file:
        filepath = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Artwork uploaded!")

        # Save description
        meta_file = filepath + ".txt"
        with open(meta_file, "w") as f:
            f.write(f"{title}\n{description}")

# Gallery Section
st.header("🖼️ Art Gallery")

cols = st.columns(3)
files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

if not files:
    st.info("No artworks uploaded yet.")
else:
    for index, file in enumerate(files):
        img_path = os.path.join(UPLOAD_DIR, file)
        meta_path = img_path + ".txt"

        with cols[index % 3]:
            image = Image.open(img_path)
            st.image(image, use_column_width=True)

            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    lines = f.readlines()
                    title = lines[0].strip() if lines else "Untitled"
                    desc = lines[1].strip() if len(lines) > 1 else ""
                st.subheader(title)
                st.caption(desc)
