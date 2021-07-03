import streamlit as st
from PIL import Image
from beach import Beach


def render():
    st.title("Beach fractal")
    mask = st.file_uploader(
        "Mask image (white for beach, black for rest)", type=["png"]
    )
    if mask is None:
        return
    beach = Beach.from_image(Image.open(mask))
    render = st.image(beach.render("distance"))
    while len(beach.free) > 0:
        beach = beach.next
        render.image(beach.render("distance"))


render()
