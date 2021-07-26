import streamlit as st
from PIL import Image
from stqdm import stqdm
from beach import Beach


def render():
    st.title("Beach fractal")
    with st.beta_expander("What's this all about?", expanded=True):
        st.markdown(
            "It's 6am. You're first at the beach. "
            "The strategic question arises: where should you put your towel? "
            "After brief consideration, you lie down in the very middle - it's *your* beach, after all."
        )
        st.markdown(
            "It's 6:15am. That annoying local beach amateur swoops by. "
            "She lies down in the middle of the remaining space "
            "- as far away from you and the edges of the beach as possible."
        )
        st.markdown(
            "By 8am, the beach is full of families with children. "
            "To distract yourself from the constant screaming, you start thinking about mathematics."
        )
        st.markdown(
            "Everyone who came took the place that was farthest from other beachmongers and the edge. "
            "Could this be... **a fractal pattern**? Let's find out!"
        )

    shape_selection = st.selectbox(
        "Which beach shape to use?", options=["Example shape", "Custom shape"]
    )
    if shape_selection == "Example shape":
        mask_file = "./sample.png"
        if not st.button("Let's go!"):
            return
    else:
        mask_file = st.file_uploader(
            "Beach shape image (white for beach, black for non-beach)", type=["png"]
        )
    if mask_file is None:
        return

    beach = Beach.from_image(Image.open(mask_file))
    progress_container = st.beta_container()
    render = st.empty()
    with st.beta_expander("What do the colors mean?"):
        st.markdown(
            "The brightness of a point on the beach corresponds to the distance from that point to "
            "the nearest edge/other beachmonger when that point was taken."
        )
    with st.beta_expander("Where can I read more?"):
        st.markdown(
            "I don't know if someone thought of this particular fractal yet, "
            "but you can read about fractals in general on [Wikipedia](https://en.wikipedia.org/wiki/Fractal) - "
            "they have pretty pictures!"
        )

    for _ in stqdm(
        range(len(beach.free)), desc="Populating beach", st_container=progress_container
    ):
        beach = beach.next
        render.image(beach.render(), use_column_width=True)


render()
