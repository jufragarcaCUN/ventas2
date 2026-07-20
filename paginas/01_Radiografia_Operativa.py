import warnings
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Diagnóstico Comercial | CUN", page_icon="🎯", layout="wide"
)

# ==================== CSS (TUS ESTILOS INTACTOS) ====================
st.markdown(
    """
<style>
    .stApp { background-color: #f5f7fa; }
    h1, h2, h3, h4 { color: #1a2b4a; font-weight: 600; }
    
    .kpi-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        border-bottom: 4px solid #2E86C1;
        height: 100%;
    }
    .kpi-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a2b4a;
    }
    .kpi-card .label {
        font-size: 0.75rem;
        color: #6b7a8f;
        text-transform: uppercase;
        font-weight: 500;
    }
    .kpi-card .sub {
        font-size: 0.8rem;
        color: #6b7a8f;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a5276 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stMultiSelect label {
        color: white !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div {
        color: white !important;
    }
    [data-testid="stSidebar"] .stMultiSelect svg {
        fill: white !important;
    }
    [data-testid="stSidebar"] .stMultiSelect input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
    div[data-baseweb="select"] * {
        font-weight: bold !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ==================== CARGA DE DATOS ====================
@st.cache_data
def cargar_datos():
    archivo_excel = "sofiaMenosStiven.xlsx"
    try:
        df = pd.read_excel(archivo_excel)
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        st.stop()

    # Formatear textos
    df["ciudad"] = df["ciudad"].fillna("Sin Ciudad").astype(str)
    df["programalimpio"] = df["programalimpio"].fillna("Sin Programa").astype(str)
    df["modalidad_normalizada"] = (
        df["modalidad_normalizada"].fillna("Sin Modalidad").astype(str)
    )
    df["Objecion_Detectada"] = (
        df["Objecion_Detectada"].fillna("Sin Clasificar").astype(str)
    )
    df["periodo"] = df["periodo"].fillna("Sin Periodo").astype(str)
    df["tipo_registro"] = df["tipo_registro"].fillna("Sin Tipo").astype(str)

    # Convertir notas
    columnas_p = [
        "P1_Promesa",
        "P2_Beneficio",
        "P3_Entregables",
        "P4_Garantia",
        "P5_Regalos",
        "P6_Precio",
        "P7_Cierre",
    ]
    for col in columnas_p:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["CALIFICACION_TOTAL"] = pd.to_numeric(df["CALIFICACION_TOTAL"], errors="coerce")

    # Segmentar tipos
    objeciones = [
        "Competencia",
        "Economica",
        "No_interesado",
        "Terceros_Familia",
        "Tiempo_flexibilidad",
    ]
    no_objeciones = [
        "Buzon_De_Voz",
        "Datos_Erroneos_No_Registro",
        "Ninguna",
        "Sin_Tiempo_Atender",
        "Tiempo_Horario_Incomodo",
        "Tiempo_Trabajo_Ocupado",
        "Tramite_Reintegro",
    ]

    df["Tipo"] = df["Objecion_Detectada"].apply(
        lambda x: (
            "Objeción"
            if x in objeciones
            else ("No Objeción" if x in no_objeciones else "Sin Clasificar")
        )
    )
    return df


df = cargar_datos()

# ==================== FILTROS DE TU BARRA LATERAL ====================
st.sidebar.header("🔍 Filtros")
st.sidebar.markdown("---")

# ==================== CORRECCIÓN: USAR COLUMNAS CORRECTAS ====================
# Obtener opciones únicas de cada columna (excluyendo valores nulos)
opciones_ciudad = ["Todos"] + sorted(df["ciudad"].dropna().unique().tolist())
opciones_programa = ["Todos"] + sorted(df["programalimpio"].dropna().unique().tolist())
opciones_modalidad = ["Todos"] + sorted(
    df["modalidad_normalizada"].dropna().unique().tolist()
)  # ✅ CORREGIDO: usar modalidad_normalizada
opciones_periodo = ["Todos"] + sorted(df["periodo"].dropna().unique().tolist())
opciones_tipo = ["Todos"] + sorted(df["tipo_registro"].dropna().unique().tolist())

# Render de los componentes Multiselect con "Todos" por defecto
ciudad_seleccionada = st.sidebar.multiselect(
    "📍 Ciudad", options=opciones_ciudad, default=["Todos"]
)

programa_seleccionado = st.sidebar.multiselect(
    "🎓 Programa", options=opciones_programa, default=["Todos"]
)

modalidad_seleccionada = st.sidebar.multiselect(
    "📚 Modalidad", options=opciones_modalidad, default=["Todos"]
)

periodo_seleccionado = st.sidebar.multiselect(
    "📅 Período", options=opciones_periodo, default=["Todos"]
)

tipo_registro_seleccionado = st.sidebar.multiselect(
    "📋 Tipo de Registro", options=opciones_tipo, default=["Todos"]
)

# ==================== LÓGICA DE FILTRADO ====================
df_filtrado = df.copy()

# Filtrar por CIUDAD (usando la columna 'ciudad' que ya fue normalizada)
if ciudad_seleccionada and "Todos" not in ciudad_seleccionada:
    df_filtrado = df_filtrado[df_filtrado["ciudad"].isin(ciudad_seleccionada)]

# Filtrar por PROGRAMA
if programa_seleccionado and "Todos" not in programa_seleccionado:
    df_filtrado = df_filtrado[df_filtrado["programalimpio"].isin(programa_seleccionado)]

# Filtrar por MODALIDAD (usando 'modalidad_normalizada')
if modalidad_seleccionada and "Todos" not in modalidad_seleccionada:
    df_filtrado = df_filtrado[
        df_filtrado["modalidad_normalizada"].isin(modalidad_seleccionada)
    ]

# Filtrar por PERÍODO
if periodo_seleccionado and "Todos" not in periodo_seleccionado:
    df_filtrado = df_filtrado[df_filtrado["periodo"].isin(periodo_seleccionado)]

# Filtrar por TIPO DE REGISTRO
if tipo_registro_seleccionado and "Todos" not in tipo_registro_seleccionado:
    df_filtrado = df_filtrado[
        df_filtrado["tipo_registro"].isin(tipo_registro_seleccionado)
    ]

# ==================== TÍTULO Y RESTRUCTURACIÓN DE LA PÁGINA ====================
st.title("🎯 Diagnóstico Comercial")
st.markdown("### Inteligencia Comercial CUN")
st.markdown("---")

# KPIs de cabecera
total = len(df_filtrado)
total_obj = len(df_filtrado[df_filtrado["Tipo"] == "Objeción"])
total_no_obj = len(df_filtrado[df_filtrado["Tipo"] == "No Objeción"])

pct_obj = (total_obj / total * 100) if total > 0 else 0
pct_no_obj = (total_no_obj / total * 100) if total > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f'<div class="kpi-card"><div class="label">📞 Total Llamadas</div><div class="value">{total:,}</div></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="kpi-card" style="border-bottom-color: #c62828;"><div class="label">❌ Objeciones Comerciales</div><div class="value" style="color:#c62828;">{total_obj:,}</div><div class="sub">{pct_obj:.1f}%</div></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f'<div class="kpi-card" style="border-bottom-color: #2e7d32;"><div class="label">🔄 No Objeciones</div><div class="value" style="color:#2e7d32;">{total_no_obj:,}</div><div class="sub">{pct_no_obj:.1f}%</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==================== GRÁFICAS 1 Y 2 CODO A CODO ====================
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("📊 1. Distribución de Objeciones")
    df_obj_only = df_filtrado[df_filtrado["Tipo"] == "Objeción"]
    if not df_obj_only.empty:
        data_obj = df_obj_only["Objecion_Detectada"].value_counts().reset_index()
        data_obj.columns = ["Objeción", "Cantidad"]
        data_obj = data_obj.sort_values("Cantidad", ascending=True)

        fig_obj = go.Figure(
            go.Bar(
                y=data_obj["Objeción"],
                x=data_obj["Cantidad"],
                orientation="h",
                text=data_obj["Cantidad"],
                textposition="outside",
                marker=dict(color=data_obj["Cantidad"], colorscale="Reds"),
            )
        )
        fig_obj.update_layout(
            height=350,
            margin=dict(l=10, r=40, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_obj, use_container_width=True)
    else:
        st.info("No hay registros de tipo Objeción")

with col_der:
    st.subheader("🔄 2. Distribución de No Objeciones")
    df_no_obj_only = df_filtrado[df_filtrado["Tipo"] == "No Objeción"]
    if not df_no_obj_only.empty:
        data_no_obj = df_no_obj_only["Objecion_Detectada"].value_counts().reset_index()
        data_no_obj.columns = ["Categoría", "Cantidad"]
        data_no_obj = data_no_obj.sort_values("Cantidad", ascending=True)

        fig_no_obj = go.Figure(
            go.Bar(
                y=data_no_obj["Categoría"],
                x=data_no_obj["Cantidad"],
                orientation="h",
                text=data_no_obj["Cantidad"],
                textposition="outside",
                marker=dict(color=data_no_obj["Cantidad"], colorscale="Greens"),
            )
        )
        fig_no_obj.update_layout(
            height=350,
            margin=dict(l=10, r=40, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_no_obj, use_container_width=True)
    else:
        st.info("No hay registros de tipo No Objeción")

st.markdown("---")

# ==================== 3. PILARES DEL MODELO ====================
st.subheader("🧬 3. Desempeño General por Pilares del Speech")

columnas_p = [
    "P1_Promesa",
    "P2_Beneficio",
    "P3_Entregables",
    "P4_Garantia",
    "P5_Regalos",
    "P6_Precio",
    "P7_Cierre",
]
pilares_nombres = [c.replace("_", " ") for c in columnas_p]

valores_pilares = []
for col in columnas_p:
    if col in df_filtrado.columns:
        val = df_filtrado[col].mean()
        if pd.notna(val):
            valores_pilares.append(val if val > 1 else val * 100)
        else:
            valores_pilares.append(0)
    else:
        valores_pilares.append(0)

if sum(valores_pilares) > 0:
    fig_radar = go.Figure(
        go.Scatterpolar(
            r=valores_pilares,
            theta=pilares_nombres,
            fill="toself",
            line_color="#2E86C1",
            fillcolor="rgba(46, 134, 193, 0.2)",
        )
    )
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickformat=".0f")),
        height=400,
        margin=dict(l=40, r=40, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("No hay datos de calificaciones de pilares para los filtros seleccionados.")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6b7a8f; font-size: 0.8rem;"><b>Diagnóstico Comercial CUN</b> | Inteligencia Comercial</div>',
    unsafe_allow_html=True,
)
