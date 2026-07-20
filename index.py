import streamlit as st
import os

# 1. Configuración de la pestaña del navegador
st.set_page_config(page_title="Ecosistema Comercial CUN", page_icon="🎓", layout="wide")

# 2. Definimos la ruta exacta de tu carpeta de páginas
CARPETA_PAGINAS = os.path.abspath("paginas")

pag_operativa = st.Page(
    os.path.join(CARPETA_PAGINAS, "01_Radiografia_Operativa.py"),
    title="1. Radiografía Operativa",
    icon="📊",
)

pag_comercial = st.Page(
    os.path.join(CARPETA_PAGINAS, "02_Diagnostico_Comercial.py"),
    title="2. Diagnóstico Comercial",
    icon="📈",
)

pag_pagos = st.Page(
    os.path.join(CARPETA_PAGINAS, "03_Pago_vs_NoPago.py"),
    title="3. Pago vs No Pago",
    icon="💰",
)

# 3. Crear la navegación
pg = st.navigation([pag_operativa, pag_comercial, pag_pagos])

# 4. Ejecutar la app
pg.run()
