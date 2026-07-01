import streamlit as st

# 1. Configuración de la página principal
st.set_page_config(page_title="Menú de Presentaciones", page_icon="📊")

# 2. Definimos las páginas apuntando directo a tus archivos en la misma carpeta
paginas = [
    st.Page("presentacion.py", title="Presentación Principal", icon="📊"),
    st.Page("Objeciones.py", title="Módulo de Objeciones", icon="🎯"),
]

# 3. Inicializamos la navegación nativa
pg = st.navigation(paginas)
pg.run()
