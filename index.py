import streamlit as st

st.set_page_config(page_title="Menú de Presentaciones", page_icon="📊", layout="wide")

paginas = [
    st.Page("presentacion.py", title="Presentación Principal", icon="📊"),
    st.Page("Objeciones.py", title="Módulo de Objeciones", icon="🎯"),
    st.Page("cambios.py", title="Cambios Modelo de Objeciones", icon="🔄"),
    st.Page("videos.py", title="Rendimiento AWS & Videos", icon="⚙️"),
    st.Page("objeciones_NO_pago.py", title="No pago", icon="⚙️"),
    st.Page("objeciones_pago.py", title="objeciones_pago.py", icon="⚙️"),
    st.Page("soloObjeciones.py", title="soloObjeciones.py", icon="⚙️"),
]

pg = st.navigation(paginas)
pg.run()
