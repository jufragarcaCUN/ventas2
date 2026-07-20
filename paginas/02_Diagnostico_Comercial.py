import warnings
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

warnings.filterwarnings("ignore")

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Diagnóstico Comercial | CUN", page_icon="🎯", layout="wide"
)

# ==================== CSS ====================
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
    
    .insight-box {
        background: white;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86C1;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .insight-box strong {
        color: #1a2b4a;
    }
    
    .recomendacion-box {
        background: #e8f5e9;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin: 10px 0;
    }
    .recomendacion-box strong {
        color: #1a2b4a;
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
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.9) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2) !important;
    }
    
    .stExpander {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: none;
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
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo '{archivo_excel}'")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        st.stop()

    columnas = [
        "ciudad_residencia",
        "programalimpio",
        "modalidad_normalizada",  # ✅ CORREGIDO: usar modalidad_normalizada
        "Objecion_Detectada",
        "CALIFICACION_TOTAL",
        "periodo",
        "tipo_registro",
        "P1_Promesa",
        "P2_Beneficio",
        "P3_Entregables",
        "P4_Garantia",
        "P5_Regalos",
        "P6_Precio",
        "P7_Cierre",
        "canal_fuente",
        "fuerzacomercial",
        "ciudad",  # ✅ AGREGADO: columna ciudad normalizada
    ]

    for col in columnas:
        if col not in df.columns:
            st.warning(f"⚠️ Columna '{col}' no encontrada. Se omitirá.")

    # ==================== CORRECCIÓN: USAR CIUDAD NORMALIZADA ====================
    # Si existe la columna 'ciudad' (normalizada) usarla, si no usar 'ciudad_residencia'
    if "ciudad" in df.columns:
        df["ciudad_para_filtro"] = df["ciudad"].fillna("Sin Ciudad").astype(str)
    else:
        df["ciudad_para_filtro"] = (
            df["ciudad_residencia"].fillna("Sin Ciudad").astype(str)
        )

    df["programalimpio"] = df["programalimpio"].fillna("Sin Programa").astype(str)

    # ==================== CORRECCIÓN: USAR MODALIDAD_NORMALIZADA ====================
    if "modalidad_normalizada" in df.columns:
        df["modalidad_para_filtro"] = (
            df["modalidad_normalizada"].fillna("Sin Modalidad").astype(str)
        )
    else:
        df["modalidad_para_filtro"] = (
            df["modalidad_limpia"].fillna("Sin Modalidad").astype(str)
        )

    df["Objecion_Detectada"] = (
        df["Objecion_Detectada"].fillna("Sin Clasificar").astype(str)
    )
    df["periodo"] = df["periodo"].fillna("Sin Periodo").astype(str)
    df["tipo_registro"] = df["tipo_registro"].fillna("Sin Tipo").astype(str)
    df["canal_fuente"] = df["canal_fuente"].fillna("Sin Canal").astype(str)
    df["fuerzacomercial"] = df["fuerzacomercial"].fillna("Sin Fuerza").astype(str)

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

# ==================== FILTROS (MULTISELECT CON "TODOS") ====================
st.sidebar.header("🔍 Filtros Globales")

# ==================== CORRECCIÓN: USAR COLUMNAS CORRECTAS ====================
opciones_ciudad = ["Todos"] + sorted(
    df["ciudad_para_filtro"].dropna().unique().tolist()
)
opciones_programa = ["Todos"] + sorted(df["programalimpio"].dropna().unique().tolist())
opciones_modalidad = ["Todos"] + sorted(
    df["modalidad_para_filtro"].dropna().unique().tolist()
)
opciones_periodo = ["Todos"] + sorted(df["periodo"].dropna().unique().tolist())
opciones_tipo = ["Todos"] + sorted(df["tipo_registro"].dropna().unique().tolist())

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

# ==================== MOSTRAR FILTROS SELECCIONADOS ====================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Filtros activos:")

filtros_activos = []

if ciudad_seleccionada and "Todos" not in ciudad_seleccionada:
    filtros_activos.append(f"📍 **Ciudad:** {', '.join(ciudad_seleccionada)}")
if programa_seleccionado and "Todos" not in programa_seleccionado:
    filtros_activos.append(f"🎓 **Programa:** {', '.join(programa_seleccionado)}")
if modalidad_seleccionada and "Todos" not in modalidad_seleccionada:
    filtros_activos.append(f"📚 **Modalidad:** {', '.join(modalidad_seleccionada)}")
if periodo_seleccionado and "Todos" not in periodo_seleccionado:
    filtros_activos.append(f"📅 **Período:** {', '.join(periodo_seleccionado)}")
if tipo_registro_seleccionado and "Todos" not in tipo_registro_seleccionado:
    filtros_activos.append(
        f"📋 **Tipo Registro:** {', '.join(tipo_registro_seleccionado)}"
    )

if filtros_activos:
    for filtro in filtros_activos:
        st.sidebar.markdown(f"- {filtro}")
else:
    st.sidebar.markdown("- **Todos los filtros aplicados**")

# ==================== APLICAR FILTROS ====================
df_filtrado = df.copy()

# ==================== CORRECCIÓN: USAR COLUMNAS CORRECTAS ====================
if ciudad_seleccionada and "Todos" not in ciudad_seleccionada:
    df_filtrado = df_filtrado[
        df_filtrado["ciudad_para_filtro"].isin(ciudad_seleccionada)
    ]

if programa_seleccionado and "Todos" not in programa_seleccionado:
    df_filtrado = df_filtrado[df_filtrado["programalimpio"].isin(programa_seleccionado)]

if modalidad_seleccionada and "Todos" not in modalidad_seleccionada:
    df_filtrado = df_filtrado[
        df_filtrado["modalidad_para_filtro"].isin(modalidad_seleccionada)
    ]

if periodo_seleccionado and "Todos" not in periodo_seleccionado:
    df_filtrado = df_filtrado[df_filtrado["periodo"].isin(periodo_seleccionado)]

if tipo_registro_seleccionado and "Todos" not in tipo_registro_seleccionado:
    df_filtrado = df_filtrado[
        df_filtrado["tipo_registro"].isin(tipo_registro_seleccionado)
    ]

if df_filtrado.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ==================== DEFINICIONES ====================
DEFINICIONES = {
    "Competencia": "El prospecto ya se matriculó en otra institución o está comparando opciones.",
    "Economica": "El prospecto manifiesta problemas económicos o considera el costo elevado.",
    "No_interesado": "El prospecto expresa que no desea continuar con el proceso.",
    "Terceros_Familia": "La decisión depende de otra persona (padres, pareja, jefe).",
    "Tiempo_flexibilidad": "El horario o la disponibilidad no permiten estudiar.",
    "Sin_Tiempo_Atender": "El prospecto estaba ocupado y pidió volver a llamar.",
    "Tiempo_Horario_Incomodo": "El prospecto estaba realizando otra actividad.",
    "Tiempo_Trabajo_Ocupado": "El prospecto estaba trabajando o en reunión.",
}

OBJECIONES_LISTA = [
    "Competencia",
    "Economica",
    "No_interesado",
    "Terceros_Familia",
    "Tiempo_flexibilidad",
]
RECUPERABLES_LISTA = [
    "Sin_Tiempo_Atender",
    "Tiempo_Horario_Incomodo",
    "Tiempo_Trabajo_Ocupado",
]
COLUMNAS_P = [
    "P1_Promesa",
    "P2_Beneficio",
    "P3_Entregables",
    "P4_Garantia",
    "P5_Regalos",
    "P6_Precio",
    "P7_Cierre",
]


# ==================== FUNCIONES ====================
def calcular_promedios_p(df, objecion):
    df_obj = df[df["Objecion_Detectada"] == objecion]
    promedios = {}
    for p in COLUMNAS_P:
        if p in df_obj.columns:
            prom = df_obj[p].mean()
            promedios[p.replace("P", "P ")] = prom if pd.notna(prom) else 0
    return promedios


# ==================== TÍTULO Y GUÍA DE INSTRUCCIONES ====================
st.title("🎯 Diagnóstico Comercial")
st.markdown("### Inteligencia Comercial CUN")

with st.expander(
    "📖 Haz clic aquí para ver las instrucciones del tablero 📋", expanded=True
):
    st.markdown(
        """
        ### ¿Cómo interactuar con los gráficos y filtros del tablero?
        
        * **Filtros Laterales 🔍 :** Usa los desplegables de la izquierda si deseas acotar los datos por una **Ciudad, Programa o Modalidad** específica. Por defecto, están en **'Todos'**.
        * **Sección 1 (Análisis de Objeciones) 🎯 :** 
          Haz clic abajo en el desplegable de **Selecciona una objeción** ⬇️ y elige una (ej. *Económica* o *Competencia*) para ver detalladamente en el gráfico de radar qué parte del speech comercial se debilita cuando surge ese problema.
        * **Sección 2 (Recuperación de Leads) 🔄 :** 
          Haz clic en el selector de **Categoría recuperable** ⬇️ para enfocar el análisis únicamente en prospectos que pidieron rellamada o estaban ocupados.
        * **Sección 3 (Análisis por Pilar) 🧬 :** 
          Haz clic en el selector de **Pilar del speech** ⬇️ para cambiar de criterio (ej. de *P1_Promesa* a *P6_Precio*) y observar qué objeciones específicas se disparan con mayor frecuencia bajo esa métrica.
        """
    )

# ==================== RESUMEN ====================
st.markdown("---")
st.subheader("📊 Resumen Ejecutivo")

total = len(df_filtrado)
total_obj = len(df_filtrado[df_filtrado["Tipo"] == "Objeción"])
pct_obj = (total_obj / total * 100) if total > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="label">📞 Total Llamadas</div>
            <div class="value">{total:,}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-bottom-color: #c62828;">
            <div class="label">✅ Objeciones Comerciales</div>
            <div class="value" style="color:#c62828;">{total_obj:,}</div>
            <div class="sub">{pct_obj:.1f}%</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    calif_prom = df_filtrado["CALIFICACION_TOTAL"].mean()
    calif_prom = calif_prom if pd.notna(calif_prom) else 0
    st.markdown(
        f"""
        <div class="kpi-card" style="border-bottom-color: #6a1b9a;">
            <div class="label">⭐ Calificación Promedio</div>
            <div class="value" style="color:#6a1b9a;">{calif_prom:.1f}%</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==================== SECCIÓN 1: OBJECIONES ====================
st.markdown("## 🎯 ¿Cómo manejar cada objeción?")
st.markdown(
    """
<div style="background: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <strong>🎯 Objetivo:</strong> Entender qué parte del speech comercial falla cuando aparece cada objeción.
    <br>📊 <strong>Análisis:</strong> Cada objeción se califica con los 7 pilares del speech para identificar áreas de mejora.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "##### Haz clic aquí abajo y selecciona la objeción para actualizar los gráficos ⬇️"
)
obj_seleccionada = st.selectbox(
    "Selecciona una objeción para analizar:",
    options=OBJECIONES_LISTA,
    key="obj_selector",
    label_visibility="collapsed",
)

df_obj = df_filtrado[df_filtrado["Objecion_Detectada"] == obj_seleccionada]

if df_obj.empty:
    st.warning(f"⚠️ No hay datos para '{obj_seleccionada}' con estos filtros.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📞 Total Llamadas", f"{len(df_obj):,}")
    with col2:
        pct = (len(df_obj) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
        st.metric("📊 Participación", f"{pct:.1f}%")
    with col3:
        calif = df_obj["CALIFICACION_TOTAL"].mean()
        st.metric(
            "⭐ Calificación Promedio", f"{calif:.1f}%" if pd.notna(calif) else "N/A"
        )

    st.markdown("---")
    st.markdown("#### 🧬 Anatomía del Speech Comercial")
    st.caption(
        "¿Qué pilar del speech tiene el peor desempeño cuando aparece esta objeción?"
    )

    promedios = calcular_promedios_p(df_filtrado, obj_seleccionada)

    if promedios:
        col1, col2 = st.columns([1, 1])

        with col1:
            categorias = list(promedios.keys())
            valores = list(promedios.values())

            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=valores,
                    theta=categorias,
                    fill="toself",
                    name=obj_seleccionada,
                    line_color="#c62828",
                    fillcolor="rgba(198, 40, 40, 0.2)",
                )
            )

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickformat=".0f%")
                ),
                height=400,
                showlegend=True,
                margin=dict(l=40, r=40, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            df_prom = pd.DataFrame(
                list(promedios.items()), columns=["Pilar", "Promedio"]
            )
            df_prom = df_prom.sort_values("Promedio", ascending=True)

            fig_barras = go.Figure()
            fig_barras.add_trace(
                go.Bar(
                    y=df_prom["Pilar"],
                    x=df_prom["Promedio"],
                    orientation="h",
                    text=df_prom["Promedio"].apply(lambda x: f"{x:.1f}%"),
                    textposition="outside",
                    marker=dict(
                        color=df_prom["Promedio"],
                        colorscale="Reds",
                        showscale=True,
                        colorbar=dict(title="%"),
                    ),
                )
            )

            fig_barras.update_layout(
                height=400,
                xaxis_title="Promedio (%)",
                yaxis_title="",
                xaxis=dict(range=[0, 100]),
                margin=dict(l=10, r=30, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_barras, use_container_width=True)

        st.markdown("---")
        pilar_min = min(promedios, key=promedios.get)
        pilar_max = max(promedios, key=promedios.get)

        st.markdown(
            f"""
        <div class="recomendacion-box">
            <strong>💡 Recomendación para "{obj_seleccionada}":</strong><br><br>
            🔹 <strong>Pilar más débil:</strong> <strong>{pilar_min}</strong> ({promedios[pilar_min]:.1f}%) - 
            <span style="color:#c62828;">¡ENFOCAR ENTRENAMIENTO AQUÍ!</span><br>
            🔹 <strong>Pilar más fuerte:</strong> {pilar_max} ({promedios[pilar_max]:.1f}%)<br>
            🔹 <strong>Definición:</strong> {DEFINICIONES.get(obj_seleccionada, '')}
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### 🔄 Comparador de Objeciones")
    st.caption("Compara el perfil de diferentes objeciones para identificar patrones.")

    obj_multi = st.multiselect(
        "Selecciona las objeciones que deseas comparar simultáneamente en el gráfico ⬇️",
        OBJECIONES_LISTA,
        default=(
            [OBJECIONES_LISTA[0], OBJECIONES_LISTA[1]]
            if len(OBJECIONES_LISTA) >= 2
            else OBJECIONES_LISTA[:1]
        ),
        key="obj_comparador",
    )

    if len(obj_multi) >= 2:
        fig_compare = go.Figure()
        colores = ["#c62828", "#2E86C1", "#2e7d32", "#e65100", "#6a1b9a"]

        for i, obj in enumerate(obj_multi):
            promedios_obj = calcular_promedios_p(df_filtrado, obj)
            if promedios_obj:
                fig_compare.add_trace(
                    go.Scatterpolar(
                        r=list(promedios_obj.values()),
                        theta=list(promedios_obj.keys()),
                        fill="toself",
                        name=obj,
                        line_color=colores[i % len(colores)],
                        fillcolor=f"rgba({i*50+50}, {i*30+30}, {i*20+20}, 0.1)",
                    )
                )

        fig_compare.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickformat=".0f%")
            ),
            height=450,
            showlegend=True,
            margin=dict(l=40, r=40, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_compare, use_container_width=True)
    else:
        st.info("ℹ️ Selecciona al menos dos objeciones para compararlas gráficamente.")

st.markdown("---")

# ==================== SECCIÓN 2: RECUPERACIÓN ====================
st.markdown("## 🔄 ¿Cómo recuperar leads?")
st.markdown(
    """
<div style="background: #e8f5e9; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <strong>🎯 Objetivo:</strong> Identificar leads que pidieron ser contactados nuevamente.
    <br>📊 <strong>Análisis:</strong> Sabemos qué objeciones tienen y qué pilar del speech debemos mejorar para la próxima llamada.
</div>
""",
    unsafe_allow_html=True,
)

df_recuperables = df_filtrado[
    df_filtrado["Objecion_Detectada"].isin(RECUPERABLES_LISTA)
]

if not df_recuperables.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📞 Leads Recuperables", f"{len(df_recuperables):,}")
    with col2:
        pct_rec = (
            (len(df_recuperables) / len(df_filtrado) * 100)
            if len(df_filtrado) > 0
            else 0
        )
        st.metric("📊 Del Total", f"{pct_rec:.1f}%")

    st.markdown("---")

    st.markdown(
        "##### Haz clic aquí abajo y selecciona la categoría para ver las recomendaciones de rellamada ⬇️"
    )
    cat_seleccionada = st.selectbox(
        "Selecciona una categoría para analizar:",
        RECUPERABLES_LISTA,
        key="recuperable_selector",
        label_visibility="collapsed",
    )

    df_cat = df_filtrado[df_filtrado["Objecion_Detectada"] == cat_seleccionada]

    if df_cat.empty:
        st.warning(f"⚠️ No hay datos para '{cat_seleccionada}' con estos filtros.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📞 Total", f"{len(df_cat):,}")
        with col2:
            pct = (len(df_cat) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
            st.metric("📊 Participación", f"{pct:.1f}%")

        st.markdown("---")
        st.markdown("#### 💡 Recomendación para la próxima llamada")

        promedios_cat = calcular_promedios_p(df_filtrado, cat_seleccionada)

        if promedios_cat:
            pilar_debil = min(promedios_cat, key=promedios_cat.get)

            st.markdown(
                f"""
            <div class="recomendacion-box" style="border-left-color: #e65100; background: #fff3e0;">
                <strong>📌 Plan de acción para "{cat_seleccionada}":</strong><br><br>
                🔹 <strong>Pilar a reforzar:</strong> <strong style="color:#c62828;">{pilar_debil}</strong> ({promedios_cat[pilar_debil]:.1f}%)<br><br>
                <strong>✅ Recomendación:</strong> En la próxima llamada, enfocar el entrenamiento en <strong>{pilar_debil}</strong> 
                para mejorar la conversión de estos leads.
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("#### 🧬 Perfil del Speech para esta categoría")

            fig_radar_rec = go.Figure()
            fig_radar_rec.add_trace(
                go.Scatterpolar(
                    r=list(promedios_cat.values()),
                    theta=list(promedios_cat.keys()),
                    fill="toself",
                    name=cat_seleccionada,
                    line_color="#2e7d32",
                    fillcolor="rgba(46, 125, 50, 0.2)",
                )
            )

            fig_radar_rec.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickformat=".0f%")
                ),
                height=350,
                showlegend=True,
                margin=dict(l=40, r=40, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_radar_rec, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 📖 Definición")
        st.info(
            f"**{cat_seleccionada}**: {DEFINICIONES.get(cat_seleccionada, 'Sin definición.')}"
        )
else:
    st.info("ℹ️ No hay leads recuperables con los filtros actuales.")

st.markdown("---")

# ==================== SECCIÓN 3: ANÁLISIS POR PILAR ====================
st.markdown("## 🧬 Análisis por Pilar del Speech")
st.markdown(
    """
<div style="background: #f0f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <strong>🎯 Objetivo:</strong> Identificar qué objeciones y no objeciones están más asociadas a cada pilar del speech.
    <br>📊 <strong>Análisis:</strong> Selecciona un pilar y observa la distribución de objeciones y no objeciones relacionadas.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "##### Haz clic aquí abajo y cambia el pilar del speech para redistribuir las métricas ⬇️"
)
pilar_seleccionado = st.selectbox(
    "Selecciona un pilar del speech para analizar:",
    options=COLUMNAS_P,
    key="pilar_selector",
    label_visibility="collapsed",
)

nombre_pilar = pilar_seleccionado.replace("P", "P ")

df_pilar = df_filtrado[df_filtrado[pilar_seleccionado].notna()]

if df_pilar.empty:
    st.warning(
        f"⚠️ No hay datos para el pilar '{nombre_pilar}' con los filtros seleccionados."
    )
else:
    st.info(
        f"📊 **{len(df_pilar):,}** registros con calificación en **{nombre_pilar}**"
    )

    st.markdown("---")

    # ===== GRÁFICO 1: OBJECIONES =====
    st.markdown(f"### ✅ Objeciones")

    df_obj_pilar = df_pilar[df_pilar["Tipo"] == "Objeción"]

    if not df_obj_pilar.empty:
        obj_pilar_data = df_obj_pilar["Objecion_Detectada"].value_counts().reset_index()
        obj_pilar_data.columns = ["Objeción", "Cantidad"]
        obj_pilar_data["Porcentaje"] = (
            obj_pilar_data["Cantidad"] / obj_pilar_data["Cantidad"].sum() * 100
        ).round(1)
        obj_pilar_data = obj_pilar_data.sort_values("Cantidad", ascending=True)

        fig_obj_pilar = go.Figure()
        fig_obj_pilar.add_trace(
            go.Bar(
                y=obj_pilar_data["Objeción"],
                x=obj_pilar_data["Cantidad"],
                orientation="h",
                text=obj_pilar_data["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
                textposition="outside",
                marker=dict(
                    color=obj_pilar_data["Cantidad"],
                    colorscale="Reds",
                    showscale=True,
                    colorbar=dict(title="Cantidad"),
                ),
            )
        )
        fig_obj_pilar.update_layout(
            height=400,
            xaxis_title="Cantidad",
            yaxis_title="",
            margin=dict(l=10, r=30, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_obj_pilar, use_container_width=True)

    else:
        st.info(f"ℹ️ No hay objeciones para este pilar")

    st.markdown("---")

    # ===== GRÁFICO 2: NO OBJECIONES =====
    st.markdown(f"### 🔄 No Objeciones")

    df_no_obj_pilar = df_pilar[df_pilar["Tipo"] == "No Objeción"]

    if not df_no_obj_pilar.empty:
        no_obj_pilar_data = (
            df_no_obj_pilar["Objecion_Detectada"].value_counts().reset_index()
        )
        no_obj_pilar_data.columns = ["Categoría", "Cantidad"]
        no_obj_pilar_data["Porcentaje"] = (
            no_obj_pilar_data["Cantidad"] / no_obj_pilar_data["Cantidad"].sum() * 100
        ).round(1)
        no_obj_pilar_data = no_obj_pilar_data.sort_values("Cantidad", ascending=True)

        fig_no_obj_pilar = go.Figure()
        fig_no_obj_pilar.add_trace(
            go.Bar(
                y=no_obj_pilar_data["Categoría"],
                x=no_obj_pilar_data["Cantidad"],
                orientation="h",
                text=no_obj_pilar_data["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
                textposition="outside",
                marker=dict(
                    color=no_obj_pilar_data["Cantidad"],
                    colorscale="Greens",
                    showscale=True,
                    colorbar=dict(title="Cantidad"),
                ),
            )
        )
        fig_no_obj_pilar.update_layout(
            height=400,
            xaxis_title="Cantidad",
            yaxis_title="",
            margin=dict(l=10, r=30, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_no_obj_pilar, use_container_width=True)

    else:
        st.info(f"ℹ️ No hay no objeciones para este pilar")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #6b7a8f; font-size: 0.8rem;">
    <b>Diagnóstico Comercial CUN</b> | Inteligencia Comercial
</div>
""",
    unsafe_allow_html=True,
)
