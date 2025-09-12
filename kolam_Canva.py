# kolam_drawing_app.py
import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Kolam Drawing Canvas", layout="wide")
st.title("🎨 Kolam Drawing Canvas — Multi-Brush + Symmetry")

# -----------------------------
# Instructions / Tips
# -----------------------------
st.info("""
**Tips for Drawing Kolam:**  
- Use light colors for intricate patterns.  
- Try different brush sizes and shapes.  
- Enable mirror symmetry for authentic Kolam designs.  
- Download your final drawing when done.
""")

# -----------------------------
# Canvas & Brush Settings
# -----------------------------
st.header("Canvas & Brush Settings")
canvas_size = 900  # Fixed canvas size

# Background color
bg_color = st.color_picker("Background Color", "#071029")

# Brush width
stroke_width = st.slider("Stroke Width", 1, 20, 3)

# Brush shape
drawing_mode = st.selectbox("Brush Shape", ["freedraw", "line", "circle", "rect"])

# Mirror count
mirror_count = st.selectbox("Number of Mirrors", [1, 2, 4, 6, 8], index=0)

# Define colors with names
color_options = {
    "Pink": "#FFD6FF",
    "Cyan": "#66FFF0",
    "Orange": "#FF7B2F",
    "Mint": "#2AF598",
    "Blue": "#00C6FF",
    "Yellow": "#FFFA66",
    "Magenta": "#FF66A3"
}

# Responsive color buttons
st.write("**Brush Color:**")
stroke_color = st.session_state.get("selected_color", "#FFD6FF")
color_cols = st.columns(len(color_options))
for i, (name, hex_color) in enumerate(color_options.items()):
    if color_cols[i].button(name, key=f"color_{name}"):
        stroke_color = hex_color
        st.session_state["selected_color"] = hex_color

# -----------------------------
# Mirror Symmetry Function
# -----------------------------
def apply_mirror(strokes_img: Image.Image, mirrors: int, bg_rgb: tuple) -> Image.Image:
    """Replicates strokes around center with N-way rotational symmetry."""
    if mirrors == 1:
        return strokes_img

    cx, cy = strokes_img.size[0] // 2, strokes_img.size[1] // 2
    base = strokes_img.convert("RGBA")

    # Make strokes transparent except actual drawing
    datas = base.getdata()
    new_data = []
    for item in datas:
        if item[:3] == bg_rgb:  # background pixel
            new_data.append((0, 0, 0, 0))  # transparent
        else:
            new_data.append(item)
    base.putdata(new_data)

    result = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for i in range(mirrors):
        rotated = base.rotate((360.0 / mirrors) * i, center=(cx, cy))
        result = Image.alpha_composite(result, rotated)

    return result

# -----------------------------
# Canvas
# -----------------------------
canvas_result = st_canvas(
    fill_color=None,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_size,
    width=canvas_size,
    drawing_mode=drawing_mode,
    key="kolam_canvas"
)

# Convert background color hex → RGB for transparency check
bg_rgb = tuple(int(bg_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

# -----------------------------
# Handle drawing
# -----------------------------
if canvas_result.image_data is not None:
    img_current = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")

    # Apply mirror symmetry
    mirrored_strokes = apply_mirror(img_current, mirror_count, bg_rgb)

    # Merge with solid background
    bg_layer = Image.new("RGBA", (canvas_size, canvas_size), bg_rgb + (255,))
    final_img = Image.alpha_composite(bg_layer, mirrored_strokes)

    # Display the drawing
    st.subheader("Your Drawing (with Symmetry)")
    st.image(final_img, width=canvas_size)

    # -----------------------------
    # Download drawing
    # -----------------------------
    buf = io.BytesIO()
    final_img.save(buf, format="PNG")
    st.download_button(
        "💾 Download Drawing",
        data=buf,
        file_name="kolam_drawing.png",
        mime="image/png"
    )
