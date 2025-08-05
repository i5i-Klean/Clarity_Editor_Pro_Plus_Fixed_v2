
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import io
import zipfile
import os

st.set_page_config(page_title="Clarity Editor Pro+", layout="centered")

st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: white;
    }
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    .block-container {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("### ✨ Clarity Editor Pro+")
st.markdown("**Polished. Powerful. Magical.**")
st.markdown("---")

use_color_bg = st.toggle("🎨 Use background color instead of uploading an image")

if use_color_bg:
    bg_color = st.color_picker("Select background color", "#222222")
    width = st.slider("Width", 600, 1080, 720)
    height = st.slider("Height", 400, 1080, 720)
    image = Image.new("RGBA", (width, height), bg_color)
else:
    uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGBA")
    else:
        image = None

font_files = {
    "Poppins": "fonts/Poppins-Regular.ttf",
    "Montserrat": "fonts/Montserrat-Regular.ttf",
    "Playfair Display": "fonts/PlayfairDisplay-Regular.ttf",
    "Sora": "fonts/Sora-Regular.ttf",
    "Inter": "fonts/Inter-Regular.ttf"
}

font_choice = st.selectbox("🔠 Choose font", list(font_files.keys()))
font_size = st.slider("Font size", 20, 60, 36)
text_color = st.color_picker("Text color", "#FFFFFF")
text_shadow = st.toggle("🕶 Add text shadow")
alignment = st.selectbox("🧭 Text alignment", ["left", "center", "right"])
padding = st.slider("Padding from bottom", 10, 200, 60)

quote1 = st.text_input("💬 Quote 1", "")
quote2 = st.text_input("💬 Quote 2", "")
quote3 = st.text_input("💬 Quote 3", "")

st.markdown("### ✨ Magic Effects")
brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
blur = st.slider("Blur", 0.0, 5.0, 0.0)

if image and (quote1 or quote2 or quote3):
    image = ImageEnhance.Brightness(image).enhance(brightness)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    if blur > 0:
        image = image.filter(ImageFilter.GaussianBlur(blur))

    draw = ImageDraw.Draw(image)

    try:
        font_path = font_files[font_choice]
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    quotes = [quote1, quote2, quote3]
    spacing = font_size + 10
    y_start = image.height - padding - (len(quotes) * spacing)

    for q in quotes:
        if q:
            w, _ = font.getsize(q)
            x = 30 if alignment == "left" else image.width // 2 - w // 2 if alignment == "center" else image.width - w - 30
            if text_shadow:
                draw.text((x+1, y_start+1), q, font=font, fill="#000000")
            draw.text((x, y_start), q, font=font, fill=text_color)
            y_start += spacing

    st.image(image, caption="🔍 Final Preview", use_container_width=True)

    output = io.BytesIO()
    image.save(output, format="PNG")
    st.download_button("📥 Download Image", output.getvalue(), file_name="clarity_pro_plus.png")

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("quotes.txt", "\n".join([q for q in quotes if q]))
        output.seek(0)
        zipf.writestr("clarity_pro_plus.png", output.read())
    zip_buf.seek(0)
    st.download_button("📦 Download Pro Kit (.zip)", zip_buf, file_name="clarity_pro_plus_kit.zip")
else:
    st.info("Please upload an image or choose background color and enter a quote.")
