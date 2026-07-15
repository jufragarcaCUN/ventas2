import warnings
import pathlib
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Análisis Consolidado de Objeciones", page_icon="📊", layout="wide"
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
    .explicacion {
        background-color: #f0f4f8;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0 15px 0;
        border-left: 4px solid #1E5D2F;
        font-size: 0.95rem;
        color: #2c3e50;
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

st.title("📊 Análisis Consolidado de Objeciones")

# ==================== RUTA DEL EXCEL ====================
script_dir = pathlib.Path(__file__).parent.absolute()
RUTA_EXCEL = script_dir / "salida_consolidada.xlsx"

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
    try:
        df = pd.read_excel(RUTA_EXCEL)
    except Exception as e:
        st.error(f"❌ Error al leer el Excel: {e}")
        st.stop()

    # Nombres de columnas según tu consulta SQL
    col_prog = "Programa_Detected"
    col_obj = "Objecion_Detectada"
    col_mod = "Zoho_Modalidad"
    col_ciudad = "Zoho_Ciudad"
    col_periodo = "Zoho_Periodo"
    col_fecha = "Fecha"
    # Detectar automáticamente el nombre de la columna de estado de pago
    columnas_reales = df.columns.tolist()
    if "Zoho_Estado_Pago" in columnas_reales:
        col_estado = "Zoho_Estado_Pago"
    elif "ESTADO_PAGO" in columnas_reales:
        col_estado = "ESTADO_PAGO"
    else:
        st.error(
            "❌ No se encontró ninguna columna de estado de pago (Zoho_Estado_Pago o ESTADO_PAGO)."
        )
        st.write("Columnas disponibles:", columnas_reales)
        st.stop()

    # Verificar columnas obligatorias
    for col in [col_prog, col_obj, col_fecha]:
        if col not in columnas_reales:
            st.error(f"❌ Columna requerida '{col}' no encontrada.")
            st.write("Columnas disponibles:", columnas_reales)
            st.stop()

    # Limpieza
    df[col_prog] = df[col_prog].fillna("Sin Especificar").astype(str).str.strip()
    df[col_obj] = df[col_obj].fillna("Sin Objeción").astype(str).str.strip()
    df[col_estado] = df[col_estado].fillna("Sin Estado").astype(str).str.strip()
    df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")

    # Modalidad (opcional)
    if col_mod in columnas_reales:
        df[col_mod] = df[col_mod].fillna("Sin Modalidad").astype(str).str.strip()
    else:
        df[col_mod] = "Sin Modalidad"

    # Ciudad (opcional)
    if col_ciudad in columnas_reales:
        df[col_ciudad] = df[col_ciudad].fillna("Sin Ciudad").astype(str).str.strip()
    else:
        df[col_ciudad] = "Sin Ciudad"

    # Período (opcional)
    if col_periodo in columnas_reales:
        df[col_periodo] = df[col_periodo].fillna("Sin Período").astype(str).str.strip()
    else:
        df[col_periodo] = "Sin Período"

    # Mapear objeciones
    df["es_objecion"] = df[col_obj].map(MAPEO_OBJECION)
    df["es_objecion"] = df["es_objecion"].fillna(True).astype(bool)

    return (
        df,
        col_prog,
        col_obj,
        col_mod,
        col_ciudad,
        col_periodo,
        col_fecha,
        col_estado,
    )


df, col_prog, col_obj, col_mod, col_ciudad, col_periodo, col_fecha, col_estado = (
    cargar_datos()
)

# ==================== FILTROS (SIDEBAR) ====================
st.sidebar.header("🔍 Criterios de Filtrado")

# Filtro 1: Programa
programas = ["Todos"] + sorted(df[col_prog].unique())
prog_sel = st.sidebar.multiselect(
    "Programa Académico:", options=programas, default=["Todos"]
)
prog_filtro = programas[1:] if "Todos" in prog_sel else prog_sel

# Filtro 2: Modalidad
modalidades = ["Todos"] + sorted(df[col_mod].dropna().astype(str).unique())
mod_sel = st.sidebar.multiselect("Modalidad:", options=modalidades, default=["Todos"])
mod_filtro = modalidades[1:] if "Todos" in mod_sel else mod_sel

# Filtro 3: Ciudad
ciudades = ["Todos"] + sorted(df[col_ciudad].dropna().astype(str).unique())
ciu_sel = st.sidebar.multiselect("Ciudad:", options=ciudades, default=["Todos"])
ciu_filtro = ciudades[1:] if "Todos" in ciu_sel else ciu_sel

# Filtro 4: Período
periodos = ["Todos"] + sorted(df[col_periodo].dropna().astype(str).unique())
per_sel = st.sidebar.multiselect("Período:", options=periodos, default=["Todos"])
per_filtro = periodos[1:] if "Todos" in per_sel else per_sel

# 🔹 Filtro 5: Estado de Pago (AHORA SÍ USA LA COLUMNA CORRECTA)
estados = ["Todos"] + sorted(df[col_estado].dropna().astype(str).unique())
est_sel = st.sidebar.multiselect("Estado de Pago:", options=estados, default=["Todos"])
est_filtro = estados[1:] if "Todos" in est_sel else est_sel

# Aplicar todos los filtros
df_filtrado = df[
    (df[col_prog].isin(prog_filtro))
    & (df[col_mod].isin(mod_filtro))
    & (df[col_ciudad].isin(ciu_filtro))
    & (df[col_periodo].isin(per_filtro))
    & (df[col_estado].isin(est_filtro))
]

if df_filtrado.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ==================== MÉTRICAS ====================
total_llamadas = len(df_filtrado)
total_obj = df_filtrado["es_objecion"].sum()
total_no_obj = total_llamadas - total_obj

fechas_validas = df_filtrado[col_fecha].dropna()
if not fechas_validas.empty:
    f_min = fechas_validas.min()
    f_max = fechas_validas.max()
    rango = f"{f_min.strftime('%d/%m/%Y')} al {f_max.strftime('%d/%m/%Y')}"
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

# ==================== GRÁFICAS PRINCIPALES (SIEMPRE VISIBLES) ====================
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

# ==================== PROMEDIOS P1-P7 (FUERA DEL EXPANDER) ====================
st.subheader("📊 Promedios de Calificaciones (P1 - P7)")
columnas_p1p7 = [
    "P1_Promesa",
    "P2_Beneficio",
    "P3_Entregables",
    "P4_Garantia",
    "P5_Regalos",
    "P6_Precio",
    "P7_Cierre",
]
existentes = [col for col in columnas_p1p7 if col in df_filtrado.columns]
if not existentes:
    st.info("ℹ️ Ninguna de las columnas P1-P7 está disponible.")
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
            color_discrete_sequence=["#1E5D2F"],
            text="Promedio",
            text_auto=".2f",
        )
        fig_p1p7.update_traces(textposition="outside")
        fig_p1p7.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_p1p7, use_container_width=True)
    else:
        st.warning("⚠️ No se pudo calcular ningún promedio.")

st.markdown("---")

# ==================== ANÁLISIS PORCENTUAL (FUERA DEL EXPANDER) ====================
st.subheader("📊 Análisis Porcentual (peso relativo)")
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
    fig3.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
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
    fig4.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No hay no‑objeciones para calcular porcentajes.")

st.markdown("---")

# ==================== ANÁLISIS POR CIUDAD Y ESTADO DE PAGO (FUERA DEL EXPANDER) ====================
st.subheader("🏙️ Análisis por Ciudad y Estado de Pago")
if col_ciudad in df_filtrado.columns and df_filtrado[col_ciudad].nunique() > 1:
    df_ciudad = (
        df_filtrado.groupby([col_ciudad, col_estado]).size().reset_index(name="Total")
    )
    pivot = df_ciudad.pivot(
        index=col_ciudad, columns=col_estado, values="Total"
    ).fillna(0)
    pivot["Total"] = pivot.sum(axis=1)
    for estado in pivot.columns:
        if estado != "Total":
            pivot[f"% {estado}"] = (pivot[estado] / pivot["Total"] * 100).round(1)
    pivot = pivot.reset_index().sort_values("Total", ascending=False)
    st.dataframe(pivot, use_container_width=True, hide_index=True)

    estados_disponibles = [
        col
        for col in pivot.columns
        if col not in ["Ciudad", "Total"] and not col.startswith("%")
    ]
    if estados_disponibles:
        fig_ciudad = px.bar(
            pivot,
            x=col_ciudad,
            y=estados_disponibles,
            title="Distribución de Estados de Pago por Ciudad",
            labels={"value": "Número de llamadas", "variable": "Estado"},
            barmode="stack",
            text_auto=True,
        )
        fig_ciudad.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_ciudad, use_container_width=True)
else:
    st.info("Columna 'Ciudad' no disponible o con un solo valor.")

st.markdown("---")

# ==================== ¡SOLO M2 DENTRO DE EXPANDER! ====================
with st.expander("📊 Ver Distribución del Puntaje de Confianza (M2)"):
    st.markdown(
        """
    <div class="explicacion">
    <b>❓ ¿Qué pregunta resuelve esta gráfica?</b><br>
    <i>¿Cómo se distribuyen los puntajes de confianza (M2) entre los prospectos?</i><br>
    <b>🔍 Interpretación:</b> Mide el nivel de confianza transmitido durante la llamada. Una distribución sesgada a la derecha (puntajes altos) es deseable, mientras que una concentración en puntajes bajos puede indicar problemas en la comunicación o en el rapport con el prospecto.
    </div>
    """,
        unsafe_allow_html=True,
    )
    col_m2 = "M2_Confianza_Puntaje"
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
        st.info("ℹ️ La columna M2_Confianza_Puntaje no está disponible.")

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
        "Categoría": "Categoría",
        "Tipo": "Clasificación",
        "Definición": "Definición",
    },
    use_container_width=True,
    hide_index=True,
)
