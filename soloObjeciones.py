import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Resumen de Objeciones", page_icon="📊", layout="wide")

st.title("📊 Resumen de Objeciones - CUN")

# ====================== DATOS FIJOS (del correo) ======================
# Totales
total_llamadas = 33203
total_obj = 11546
total_no_obj = 21657
pct_obj = 34.77
pct_no_obj = 65.23

# Detalle de Objeciones
obj_detalle = {
    "No interesado": 6327,
    "Económica": 2905,
    "Terceros / Familia": 1170,
    "Tiempo / Flexibilidad": 930,
    "Competencia": 214,
}

# Detalle de No Objeciones
no_obj_detalle = {
    "Sin tiempo para atender": 11433,
    "Ninguna": 4749,
    "Trámite de reintegro": 3328,
    "Buzón de voz": 1202,
    "Tiempo / Horario incómodo": 512,
    "Datos erróneos / No registro": 328,
    "Tiempo / Trabajo ocupado": 105,
}

# ====================== TARJETAS ======================
st.subheader("📌 Resumen ejecutivo")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📞 Total llamadas", f"{total_llamadas:,}")
with col2:
    st.metric("🚫 Objeciones", f"{total_obj:,}", delta=f"{pct_obj:.2f}%")
with col3:
    st.metric("🔄 No objeciones", f"{total_no_obj:,}", delta=f"{pct_no_obj:.2f}%")

st.markdown("---")

# ====================== GRÁFICA DE BARRAS (Obj vs No Obj) ======================
st.subheader("📊 Comparativa general")
df_resumen = pd.DataFrame(
    {
        "Tipo": ["Objeciones", "No objeciones"],
        "Cantidad": [total_obj, total_no_obj],
        "Porcentaje": [pct_obj, pct_no_obj],
    }
)
fig_resumen = px.bar(
    df_resumen,
    x="Tipo",
    y="Cantidad",
    text="Porcentaje",
    color="Tipo",
    color_discrete_map={"Objeciones": "#dc3545", "No objeciones": "#007bff"},
    labels={"Cantidad": "Número de llamadas", "Tipo": ""},
)
fig_resumen.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
fig_resumen.update_layout(height=350, showlegend=False)
st.plotly_chart(fig_resumen, use_container_width=True)

st.markdown("---")

# ====================== TABLAS DETALLADAS ======================
col_tab1, col_tab2 = st.columns(2)

with col_tab1:
    st.subheader("🚫 Detalle de Objeciones")
    df_obj = pd.DataFrame(list(obj_detalle.items()), columns=["Categoría", "Cantidad"])
    st.dataframe(df_obj, use_container_width=True, hide_index=True)
    # Gráfica de barras horizontal (opcional)
    fig_obj = px.bar(
        df_obj,
        x="Cantidad",
        y="Categoría",
        orientation="h",
        color_discrete_sequence=["#dc3545"],
        text="Cantidad",
        labels={"Cantidad": "Número", "Categoría": ""},
    )
    fig_obj.update_traces(textposition="outside")
    fig_obj.update_layout(height=300, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_obj, use_container_width=True)

with col_tab2:
    st.subheader("🔄 Detalle de No Objeciones")
    df_no = pd.DataFrame(
        list(no_obj_detalle.items()), columns=["Categoría", "Cantidad"]
    )
    st.dataframe(df_no, use_container_width=True, hide_index=True)
    fig_no = px.bar(
        df_no,
        x="Cantidad",
        y="Categoría",
        orientation="h",
        color_discrete_sequence=["#007bff"],
        text="Cantidad",
        labels={"Cantidad": "Número", "Categoría": ""},
    )
    fig_no.update_traces(textposition="outside")
    fig_no.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_no, use_container_width=True)

st.markdown("---")
st.caption("Datos basados en el resumen del correo del 15/07/2026")
