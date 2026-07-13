import os
import warnings
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Análisis de Objeciones COE", page_icon="🎯", layout="wide"
)

# ==================== CSS ====================
st.markdown(
    """
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3, h4 { color: #1E5D2F !important; font-family: 'Segoe UI', sans-serif; font-weight: 600; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center;
        border-left: 6px solid #1E5D2F; margin-bottom: 10px;
    }
    .metric-card .label { font-size: 0.9rem; color: #6c757d; font-weight: 500; }
    .metric-card .value { font-size: 2.2rem; font-weight: 700; color: #1E5D2F; margin-top: 5px; }
    .metric-card .delta { font-size: 0.85rem; color: #28a745; }
    .insight-box {
        background-color: #e9f5e9; padding: 15px 20px; border-radius: 10px;
        border-left: 5px solid #1E5D2F; margin: 15px 0;
    }
    table {
        width: 100%; border-collapse: collapse; background-color: white;
        border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    th { background-color: #1E5D2F; color: white; padding: 12px 15px; text-align: left; }
    td { padding: 10px 15px; border-bottom: 1px solid #e9ecef; }
    tr:hover { background-color: #f1f8f1; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎯 Análisis de Objeciones COE - CUN")
st.markdown("---")

# ==================== RUTA DEL EXCEL ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_EXCEL = os.path.join(
    BASE_DIR, "carreras_homologada.xlsx"
)  # Ajusta la extensión si es necesario

# ==================== MAPEO Y DEFINICIONES ====================
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

DEFINICIONES = {
    "Competencia": "Ya se matriculó en otra institución o está comparando opciones.",
    "Economica": "Falta de dinero, costo elevado o problemas financieros.",
    "No_interesado": "No le interesa la oferta académica.",
    "Terceros_Familia": "Depende de la decisión de terceros (padres, esposo, jefe).",
    "Tiempo_flexibilidad": "No tiene tiempo o el horario no le es compatible.",
    "Buzon_De_Voz": "Contestador automático, sin contacto humano.",
    "Datos_Erroneos_No_Registro": "Número equivocado, datos falsos o no registrado.",
    "Ninguna": "No se detectó objeción en la llamada.",
    "Sin_Tiempo_Atender": "Está ocupado ahora y pide llamar después.",
    "Tiempo_Horario_Incomodo": "Está en medio de una actividad personal (almorzando, manejando, etc.).",
    "Tiempo_Trabajo_Ocupado": "Está trabajando o en reunión ahora.",
    "Tramite_Reintegro": "Es estudiante actual o antiguo con trámites administrativos.",
}


# ==================== CARGA DE DATOS ====================
@st.cache_data
def cargar_datos():
    if not os.path.exists(RUTA_EXCEL):
        st.error(f"❌ No se encuentra el archivo en: {RUTA_EXCEL}")
        return None, None, None, None, None, None

    try:
        df = pd.read_excel(RUTA_EXCEL)
        st.success(f"✅ Archivo cargado correctamente. Filas: {len(df)}")
    except Exception as e:
        st.error(f"❌ Error al leer el Excel: {e}")
        return None, None, None, None, None, None

    # --- NOMBRES REALES DE COLUMNAS (CORREGIDO) ---
    col_prog = "PROGRAMA (CRM)"  # 🔥 AQUÍ ESTABA EL ERROR
    col_obj = "Objecion_Detectada (Llamadas)"
    col_mod = "MODALIDAD (CRM)"
    col_ciudad = "ciudad (CRM)"
    col_fecha = "Fecha (Llamadas)"

    # --- LIMPIEZA ROBUSTA ---
    df[col_prog] = df[col_prog].fillna("Sin Especificar").astype(str).str.strip()
    df[col_obj] = df[col_obj].fillna("Sin Objeción").astype(str).str.strip()

    if col_fecha in df.columns:
        df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")

    # Limpiar basura
    basura = [
        "otro / por verificar",
        "otro",
        "no registrado",
        "por verificar",
        "",
        "nan",
        "none",
    ]
    df = df[
        (~df[col_prog].str.lower().isin(basura))
        & (~df[col_obj].str.lower().isin(basura))
    ]

    df["es_objecion"] = df[col_obj].map(MAPEO_OBJECION)
    df["es_objecion"] = df["es_objecion"].fillna(True).astype(bool)

    if df.empty:
        st.warning("⚠️ Después de limpiar, no quedaron registros válidos.")
    else:
        st.info(f"✅ Datos limpios: {len(df)} filas listas para analizar.")

    return df, col_prog, col_obj, col_mod, col_ciudad, col_fecha


df, col_prog, col_obj, col_mod, col_ciudad, col_fecha = cargar_datos()
if df is None or df.empty:
    st.stop()

# ==================== FILTROS ====================
st.sidebar.header("🔍 Criterios de Filtrado")

programas = ["Todos"] + sorted(df[col_prog].unique())
prog_sel = st.sidebar.multiselect(
    "Programa Académico:", options=programas, default=["Todos"]
)
prog_filtro = programas[1:] if "Todos" in prog_sel else prog_sel

modalidades = ["Todos"] + sorted(df[col_mod].dropna().astype(str).unique())
mod_sel = st.sidebar.multiselect("Modalidad:", options=modalidades, default=["Todos"])
mod_filtro = modalidades[1:] if "Todos" in mod_sel else mod_sel

ciudades = ["Todos"] + sorted(df[col_ciudad].dropna().astype(str).unique())
ciu_sel = st.sidebar.multiselect("Ciudad:", options=ciudades, default=["Todos"])
ciu_filtro = ciudades[1:] if "Todos" in ciu_sel else ciu_sel

df_filtrado = df[
    (df[col_prog].isin(prog_filtro))
    & (df[col_mod].isin(mod_filtro))
    & (df[col_ciudad].isin(ciu_filtro))
]

if df_filtrado.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ==================== MÉTRICAS ====================
total_llamadas = len(df_filtrado)
total_obj = df_filtrado["es_objecion"].sum()
total_no_obj = total_llamadas - total_obj

if col_fecha in df_filtrado.columns:
    f_min = df_filtrado[col_fecha].min()
    f_max = df_filtrado[col_fecha].max()
    rango = (
        f"{f_min.strftime('%d/%m/%Y')} al {f_max.strftime('%d/%m/%Y')}"
        if pd.notna(f_min)
        else "Periodo Dinámico"
    )
else:
    rango = "Periodo Dinámico"

# ==================== TARJETAS ====================
st.subheader("📊 Resumen Ejecutivo")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""<div class="metric-card"><div class="label">📞 Llamadas auditadas</div><div class="value">{total_llamadas:,}</div></div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""<div class="metric-card"><div class="label">📅 Período</div><div class="value" style="font-size:1.2rem;">{rango}</div></div>""",
        unsafe_allow_html=True,
    )
with col3:
    pct_obj = (total_obj / total_llamadas * 100) if total_llamadas > 0 else 0
    st.markdown(
        f"""<div class="metric-card" style="border-left-color: #dc3545;"><div class="label">🚫 Objeciones</div><div class="value" style="color:#dc3545;">{total_obj:,}</div><div class="delta">{pct_obj:.1f}% del total</div></div>""",
        unsafe_allow_html=True,
    )
with col4:
    pct_no_obj = (total_no_obj / total_llamadas * 100) if total_llamadas > 0 else 0
    st.markdown(
        f"""<div class="metric-card" style="border-left-color: #007bff;"><div class="label">🔄 No objeciones</div><div class="value" style="color:#007bff;">{total_no_obj:,}</div><div class="delta">{pct_no_obj:.1f}% del total</div></div>""",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==================== SECCIÓN SQL (expandible) ====================
with st.expander("📋 Ver estructura de la consulta SQL (documentación)"):
    st.markdown(
        """
    <div class="insight-box">
    <h4 style="margin-top:0;color:#1E5D2F;">🎯 Objetivo del análisis</h4>
    <p>El objetivo principal de esta consulta es <b>identificar y analizar la gestión realizada sobre los prospectos del período académico <span style="color:#1E5D2F;">26V04</span></b>, integrando la información de las llamadas comerciales con los registros del CRM.</p>
    <p>Para lograrlo, ambas fuentes de información se relacionan mediante el <b>número telefónico normalizado</b>, permitiendo construir una vista única de cada prospecto.</p>
    <ul>
        <li>Relacionar cada llamada con el registro comercial del CRM.</li>
        <li>Identificar las objeciones detectadas durante la conversación.</li>
        <li>Conocer el programa de interés, modalidad, campaña y canal de origen.</li>
        <li>Verificar el estado comercial y la conversión del prospecto.</li>
        <li>Evaluar la gestión comercial realizada sobre la población correspondiente al período <b>26V04</b>.</li>
    </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==================== GRÁFICAS DE OBJECIONES ====================
st.subheader("📈 Distribución de Objeciones")
if total_obj > 0:
    df_obj = (
        df_filtrado[df_filtrado["es_objecion"] == True][col_obj]
        .value_counts()
        .reset_index()
    )
    df_obj.columns = ["Categoría", "Total"]
    fig1 = px.bar(
        df_obj,
        x="Total",
        y="Categoría",
        orientation="h",
        color_discrete_sequence=["#1E5D2F"],
        text="Total",
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No hay objeciones con estos filtros.")

st.subheader("🔄 Distribución de No Objeciones")
if total_no_obj > 0:
    df_no = (
        df_filtrado[df_filtrado["es_objecion"] == False][col_obj]
        .value_counts()
        .reset_index()
    )
    df_no.columns = ["Categoría", "Total"]
    fig2 = px.bar(
        df_no,
        x="Total",
        y="Categoría",
        orientation="h",
        color_discrete_sequence=["#2B6CB0"],
        text="Total",
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No hay no‑objeciones con estos filtros.")

st.markdown("---")

# ==================== GRÁFICA DE PROMEDIOS P1-P7 ====================
st.subheader("📊 Promedios de Calificaciones (P1 - P7)")

columnas_p1p7 = [
    "P1_Promesa (Llamadas)",
    "P2_Beneficio (Llamadas)",
    "P3_Entregables (Llamadas)",
    "P4_Garantia (Llamadas)",
    "P5_Regalos (Llamadas)",
    "P6_Precio (Llamadas)",
    "P7_Cierre (Llamadas)",
]

existentes = [col for col in columnas_p1p7 if col in df_filtrado.columns]

if not existentes:
    st.info("ℹ️ Ninguna de las columnas P1-P7 está disponible en los datos.")
else:
    promedios = []
    for col in existentes:
        serie = pd.to_numeric(df_filtrado[col], errors="coerce")
        promedio = serie.mean(skipna=True)
        if pd.notna(promedio):
            promedios.append({"Columna": col, "Promedio": promedio})

    if promedios:
        df_promedios = pd.DataFrame(promedios)
        fig_p1p7 = px.bar(
            df_promedios,
            x="Columna",
            y="Promedio",
            title="Promedio de calificaciones por columna (P1 - P7)",
            color_discrete_sequence=["#1E5D2F"],
            text="Promedio",
            text_auto=".2f",
        )
        fig_p1p7.update_traces(textposition="outside")
        fig_p1p7.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis_title="",
            yaxis_title="Promedio",
        )
        st.plotly_chart(fig_p1p7, use_container_width=True)
        st.dataframe(
            df_promedios.style.format({"Promedio": "{:.2f}"}),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("⚠️ No se pudo calcular ningún promedio (datos no numéricos).")

# ==================== HISTOGRAMA M2_CONFIANZA_PUNTAJE ====================
st.subheader("📊 Distribución del Puntaje de Confianza (M2)")
col_m2 = "M2_Confianza_Puntaje (Llamadas)"

if col_m2 in df_filtrado.columns:
    serie_m2 = pd.to_numeric(df_filtrado[col_m2], errors="coerce").dropna()
    if not serie_m2.empty:
        fig_m2 = px.histogram(
            serie_m2,
            nbins=20,
            color_discrete_sequence=["#1E5D2F"],
            title="Distribución de M2_Confianza_Puntaje",
            labels={"value": "Puntaje", "count": "Frecuencia"},
        )
        fig_m2.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_m2, use_container_width=True)
    else:
        st.info("ℹ️ No hay datos numéricos para M2_Confianza_Puntaje.")
else:
    st.info("ℹ️ La columna M2_Confianza_Puntaje (Llamadas) no está disponible.")

st.markdown("---")

# ==================== ACORDEÓN: ANÁLISIS PORCENTUAL ====================
with st.expander("📊 Análisis Porcentual (peso relativo de cada categoría)"):
    if total_obj > 0:
        df_obj_pct = (
            df_filtrado[df_filtrado["es_objecion"] == True][col_obj]
            .value_counts()
            .reset_index()
        )
        df_obj_pct.columns = ["Categoría", "Total"]
        df_obj_pct["Porcentaje"] = (df_obj_pct["Total"] / total_obj * 100).round(1)
        fig3 = px.bar(
            df_obj_pct,
            x="Porcentaje",
            y="Categoría",
            orientation="h",
            color_discrete_sequence=["#1E5D2F"],
            text="Porcentaje",
        )
        fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig3.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="% del total de objeciones",
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No hay objeciones para calcular porcentajes.")

    if total_no_obj > 0:
        df_no_pct = (
            df_filtrado[df_filtrado["es_objecion"] == False][col_obj]
            .value_counts()
            .reset_index()
        )
        df_no_pct.columns = ["Categoría", "Total"]
        df_no_pct["Porcentaje"] = (df_no_pct["Total"] / total_no_obj * 100).round(1)
        fig4 = px.bar(
            df_no_pct,
            x="Porcentaje",
            y="Categoría",
            orientation="h",
            color_discrete_sequence=["#2B6CB0"],
            text="Porcentaje",
        )
        fig4.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig4.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="% del total de no objeciones",
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No hay no‑objeciones para calcular porcentajes.")

st.markdown("---")

# ==================== INSIGHTS ====================
st.subheader("💡 Insights clave")
if total_obj > 0:
    top_obj = (
        df_filtrado[df_filtrado["es_objecion"] == True][col_obj].value_counts().idxmax()
    )
    top_obj_pct = (
        df_filtrado[df_filtrado["es_objecion"] == True][col_obj].value_counts().max()
        / total_obj
        * 100
    ).round(1)
    st.markdown(
        f"""<div class="insight-box"><b>🔍 Objeción dominante:</b> <b>{top_obj}</b> representa el <b>{top_obj_pct:.1f}%</b> de todas las objeciones.</div>""",
        unsafe_allow_html=True,
    )

if total_no_obj > 0:
    top_no = (
        df_filtrado[df_filtrado["es_objecion"] == False][col_obj]
        .value_counts()
        .idxmax()
    )
    top_no_pct = (
        df_filtrado[df_filtrado["es_objecion"] == False][col_obj].value_counts().max()
        / total_no_obj
        * 100
    ).round(1)
    st.markdown(
        f"""<div class="insight-box"><b>🔍 No objeción más frecuente:</b> <b>{top_no}</b> representa el <b>{top_no_pct:.1f}%</b> de las llamadas sin objeción.</div>""",
        unsafe_allow_html=True,
    )

if total_obj > 0 and total_no_obj > 0:
    ratio = total_obj / total_no_obj
    if ratio > 1:
        st.markdown(
            f"""<div class="insight-box"><b>⚖️ Proporción:</b> hay <b>{ratio:.2f}</b> veces más llamadas con objeción que sin objeción.</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div class="insight-box"><b>⚖️ Proporción:</b> hay <b>{(1/ratio):.2f}</b> veces más llamadas sin objeción que con objeción.</div>""",
            unsafe_allow_html=True,
        )

st.markdown("---")

# ==================== TABLA DE CLASIFICACIÓN ====================
st.subheader("📋 Clasificación de categorías")
datos_tabla = []
for cat, es_obj in MAPEO_OBJECION.items():
    datos_tabla.append(
        {
            "Categoría": cat,
            "Tipo": "✅ Objeción" if es_obj else "🔄 No objeción",
            "Definición": DEFINICIONES.get(cat, "Sin definición"),
        }
    )
df_tabla = pd.DataFrame(datos_tabla)
st.dataframe(
    df_tabla,
    column_config={
        "Categoría": st.column_config.TextColumn("Categoría"),
        "Tipo": st.column_config.TextColumn("Clasificación"),
        "Definición": st.column_config.TextColumn("Definición"),
    },
    use_container_width=True,
    hide_index=True,
)
