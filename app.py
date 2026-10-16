import io
import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="AI FASHION DESIGNER", page_icon="👗", layout="wide")

st.title("👗 AI FASHION DESIGNER")
st.caption("Design your own Men's & Women's Fashion")

COLORS = {
    "Black": "#242424", "White": "#F5F5F5", "Red": "#D62839",
    "Blue": "#2455A4", "Green": "#23865A", "Pink": "#E989B9",
    "Purple": "#8056A1", "Yellow": "#F4C542", "Brown": "#875B42"
}

CLOTHES = {
    "Men's Fashion": ["T-Shirt", "Shirt", "Jacket", "Jeans"],
    "Women's Fashion": ["Kurti", "Dress", "Gown", "Saree"]
}

def make_design(category, garment, color, fabric, style, idea):
    im = Image.new("RGB", (700, 700), "#F5F0E8")
    d = ImageDraw.Draw(im)
    d.text((25, 20), "FASHION DESIGN STUDIO", fill="#222222")
    d.text((25, 50), f"{category} - {garment}", fill="#555555")

    c = COLORS[color]
    outline = "#292929"

    if garment in ("T-Shirt", "Shirt", "Jacket"):
        d.polygon([
            (270,150),(220,175),(155,300),(220,325),
            (260,260),(260,490),(440,490),(440,260),
            (480,325),(545,300),(480,175),(430,150)
        ], fill=c, outline=outline)
        d.polygon([(320,145),(350,185),(380,145)],
                  fill="#F5F0E8", outline=outline)
        if garment == "Shirt":
            d.line((350,185,350,490), fill=outline, width=3)
            for y in range(220,450,55):
                d.ellipse((345,y,352,y+7), fill="white")

    elif garment == "Jeans":
        d.polygon([
            (255,160),(445,160),(430,280),(415,500),
            (355,500),(350,280),(335,500),(275,500),(270,280)
        ], fill=c, outline=outline)
        d.line((350,280,350,490), fill=outline, width=3)

    else:
        if garment == "Kurti":
            points = [(300,150),(400,150),(445,225),
                      (420,480),(280,480),(255,225)]
        elif garment == "Gown":
            points = [(300,150),(400,150),(425,250),
                      (520,500),(180,500),(275,250)]
        elif garment == "Saree":
            points = [(300,150),(400,150),(435,260),
                      (470,490),(230,490),(265,260)]
        else:
            points = [(300,150),(400,150),(435,260),
                      (470,400),(230,400),(265,260)]

        d.polygon(points, fill=c, outline=outline)
        d.line((300,150,350,205), fill=outline, width=2)
        d.line((400,150,350,205), fill=outline, width=2)

        if garment == "Saree":
            d.polygon([(400,170),(480,220),(530,480),
                       (465,490),(370,245)], fill=c, outline=outline)
            d.line((465,220,510,470), fill="#E9C46A", width=7)

    if style == "Striped":
        for y in range(260,460,45):
            d.line((280,y,420,y), fill="white", width=3)
    elif style == "Floral":
        for x,y in [(310,280),(375,330),(325,390),(390,430)]:
            d.ellipse((x,y,x+15,y+15), fill="#FFD166")
    elif style == "Classic":
        d.rectangle((320,300,380,350), outline="white", width=3)

    d.line((25,540,675,540), fill="#BBBBBB", width=2)
    d.text((25,560), f"Fabric: {fabric}", fill="#222222")
    d.text((25,590), f"Color: {color} | Style: {style}", fill="#222222")
    d.text((25,620), f"Idea: {idea[:60]}", fill="#555555")
    return im

left, right = st.columns([1, 1.2])

with left:
    st.subheader("Design Details")
    category = st.selectbox("Fashion Category", list(CLOTHES.keys()))
    garment = st.selectbox("Clothing", CLOTHES[category])
    color = st.selectbox("Color", list(COLORS.keys()))
    fabric = st.selectbox(
        "Fabric", ["Cotton", "Denim", "Silk", "Linen", "Velvet", "Georgette"]
    )
    style = st.selectbox("Style", ["Classic", "Minimal", "Striped", "Floral"])
    idea = st.text_area("Describe your design idea")
    generate = st.button("Create Design Preview", type="primary")

if generate or "design" not in st.session_state:
    st.session_state.design = make_design(
        category, garment, color, fabric, style, idea
    )
    st.session_state.details = {
        "category": category, "garment": garment,
        "color": color, "fabric": fabric, "style": style,
        "idea": idea, "created_at": datetime.now().isoformat()
    }

with right:
    st.subheader("Your Design")
    image = st.session_state.design
    st.image(image, use_container_width=True)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    st.download_button(
        "Download Design PNG", buffer.getvalue(),
        file_name="fashion_design.png", mime="image/png"
    )

    st.download_button(
        "Download Design JSON",
        json.dumps(st.session_state.details, indent=2, ensure_ascii=False),
        file_name="fashion_design.json", mime="application/json"
    )

    if st.button("Save Design to Computer"):
        folder = Path("saved_designs")
        folder.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image.save(folder / f"design_{stamp}.png")
        (folder / f"design_{stamp}.json").write_text(
            json.dumps(st.session_state.details, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        st.success("Design saved in saved_designs folder!")

st.info("Basic version: illustrative clothing previews, not photorealistic AI images.")
