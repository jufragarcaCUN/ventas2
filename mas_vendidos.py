import os
import warnings
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Análisis Programas Seleccionados", layout="wide")

st.title("🎯 Análisis de Programas Seleccionados")
st.markdown("""
**Más vendidos:** INGENIERIA DE SISTEMAS, CONTADURIA PUBLICA, ADMINISTRACION DE EMPRESAS  
**Menos vendidos:** MARKETING DIGITAL, AGROINDUSTRIALES, DISEÑO DE EXPERIENCIAS INTERACTIVAS
""")

# Ruta del Excel
RUTA_EXCEL = r"C:\Users\juan_garnicac\Documents\ProyectosVisual\Ventas\presentaciones\salida_con_pago.xlsx"

# SOLO estos programas
PROGRAMAS_INTERES = [
    "INGENIERIA DE SISTEMAS",
    "CONTADURIA PUBLICA",
    "ADMINISTRACION DE EMPRESAS",
    "MARKETING DIGITAL",
    "AGROINDUSTRIALES",
    "DISEÑO DE EXPERIENCIAS INTERACTIVAS",
]

MAPEO_OBJECION = {
    "Competencia": True,
    "Economica": True,
    "No_interesado": True,
    "Terceros_Familia": True,
    "Tiempo_flexibilidad": True,
    "Buzon_De_Voz": False,
    "Datos_Erroneos_No_Registro": False,
    "Ninguna": False,
    "Sin_Tiempo_Atender": False,
    "Tiempo_Horario_Incomodo": False,
    "Tiempo_Trabajo_Ocupado": False,
    "Tramite_Reintegro": False,
}


@st.cache_data
def cargar_datos():
    if not os.path.exists(RUTA_EXCEL):
        st.error(f"❌ No se encuentra el archivo: {RUTA_EXCEL}")
        return None
    df = pd.read_excel(RUTA_EXCEL)
    col_prog = "NOM_PROGRAMA"
    col_obj = "Objecion_Detectada"
    col_estado = "ESTADO_PAGO"

    df[col_prog] = df[col_prog].fillna("").astype(str).str.strip().str.upper()
    df[col_obj] = df[col_obj].fillna("Sin Objeción").astype(str).str.strip()
    if col_estado in df.columns:
        df[col_estado] = df[col_estado].fillna("Sin Estado").astype(str).str.strip()
    else:
        df[col_estado] = "Sin Estado"

    # **FILTRO ESTRICTO: SOLO estos programas**
    df_filt = df[df[col_prog].isin(PROGRAMAS_INTERES)].copy()
    df_filt["es_objecion"] = (
        df_filt[col_obj].map(MAPEO_OBJECION).fillna(True).astype(bool)
    )
    return df_filt, col_prog, col_obj, col_estado


df, col_prog, col_obj, col_estado = cargar_datos()
if df is None or df.empty:
    st.warning("⚠️ No se encontraron datos para los programas especificados.")
    st.stop()

# Métricas
total = len(df)
total_obj = df["es_objecion"].sum()
total_no = total - total_obj

col1, col2, col3, col4 = st.columns(4)
col1.metric("📞 Total llamadas", f"{total:,}")
col2.metric("🚫 Con objeción", f"{total_obj:,}", f"{total_obj/total*100:.1f}%")
col3.metric("🔄 Sin objeción", f"{total_no:,}", f"{total_no/total*100:.1f}%")
col4.metric("📅 Programas", len(df[col_prog].unique()))

st.markdown("---")

# Gráfico 1: Llamadas por programa
st.subheader("📊 Llamadas por programa")
fig1 = px.bar(
    df[col_prog].value_counts().reset_index(),
    x="count",
    y="NOM_PROGRAMA",
    orientation="h",
    color_discrete_sequence=["#1E5D2F"],
    text="count",
    labels={"count": "N° llamadas", "NOM_PROGRAMA": "Programa"},
)
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: % Objeciones por programa
st.subheader("🚫 Porcentaje de objeciones por programa")
obj_pct = (
    df.groupby(col_prog)
    .apply(lambda x: x["es_objecion"].sum() / len(x) * 100)
    .sort_values(ascending=False)
)
df_pct = obj_pct.reset_index().rename(columns={0: "% Objeción"})
fig2 = px.bar(
    df_pct,
    x="% Objeción",
    y=col_prog,
    orientation="h",
    color="% Objeción",
    color_continuous_scale="Reds",
    text="% Objeción",
)
fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Top objeciones
st.subheader("🏆 Principales objeciones")
top_obj = df[df["es_objecion"] == True][col_obj].value_counts().head(5).reset_index()
top_obj.columns = ["Categoría", "Total"]
fig3 = px.bar(
    top_obj,
    x="Total",
    y="Categoría",
    orientation="h",
    color_discrete_sequence=["#DC3545"],
    text="Total",
)
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: % PAGO por programa
st.subheader("💰 Conversión a PAGO por programa")
pago_df = df.groupby(col_prog)[col_estado].value_counts().unstack(fill_value=0)
if "PAGO" in pago_df.columns:
    pago_df["% PAGO"] = (pago_df["PAGO"] / pago_df.sum(axis=1) * 100).round(1)
    pago_df = pago_df.sort_values("% PAGO", ascending=False)
    st.dataframe(pago_df[["PAGO", "NO PAGO", "% PAGO"]], use_container_width=True)

    fig4 = px.bar(
        pago_df.reset_index(),
        x=col_prog,
        y="% PAGO",
        color="% PAGO",
        color_continuous_scale="Greens",
        text="% PAGO",
        title="Tasa de PAGO por programa",
    )
    fig4.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No hay datos de PAGO/NO PAGO en el Excel.")
