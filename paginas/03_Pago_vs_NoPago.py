"""
03_Pago_vs_NoPago.py
Diagnóstico Comercial - Pago vs No Pago
"""

import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore")

# ==================== CONFIGURACIÓN ====================
st.set_page_config(page_title="Pago vs No Pago | CUN", page_icon="🎓", layout="wide")

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
        background: #e8f5e9;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #2e7d32;
        margin: 8px 0;
        font-size: 0.9rem;
        color: #1a2b4a;
    }
    .insight-box strong {
        color: #1b5e20;
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
</style>
""",
    unsafe_allow_html=True,
)


# ==================== CARGA DE DATOS ====================
@st.cache_data
def cargar_datos():
    archivo_excel = "cruceZohovsVistaSofia.xlsx"

    try:
        df = pd.read_excel(archivo_excel)
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo '{archivo_excel}'")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        st.stop()

    # ========== MAPEO DE COLUMNAS ==========
    mapeo = {
        "modalidades": "modalidad",
        "objeciones_detectadas": "Objecion_Detectada",
        "promedio_calificacion_total": "CALIFICACION_TOTAL",
        "promedio_p1_promesa": "P1_Promesa",
        "promedio_p2_beneficio": "P2_Beneficio",
        "promedio_p3_entregables": "P3_Entregables",
        "promedio_p4_garantia": "P4_Garantia",
        "promedio_p5_regalos": "P5_Regalos",
        "promedio_p6_precio": "P6_Precio",
        "promedio_p7_cierre": "P7_Cierre",
        "canales_fuente": "canal_fuente",
        "fuentes": "fuente",
        "tipos_fuente": "tipo_de_fuente",
        "programas_detectados": "Programa_Detected",
        "fuerzas_comerciales": "fuerzacomercial",
    }

    df.rename(columns=mapeo, inplace=True)

    # ========== VERIFICAR COLUMNAS ==========
    columnas_requeridas = [
        "ciudad_residencia",
        "NOM_PROGRAMA",
        "modalidad",
        "ESTADO_PAGO",
        "CALIFICACION_TOTAL",
        "periodo",
        "P1_Promesa",
        "P2_Beneficio",
        "P3_Entregables",
        "P4_Garantia",
        "P5_Regalos",
        "P6_Precio",
        "P7_Cierre",
        "canal_fuente",
        "fuente",
        "tipo_de_fuente",
        "Programa_Detected",
        "fuerzacomercial",
    ]

    for col in columnas_requeridas:
        if col not in df.columns:
            st.warning(f"⚠️ Columna '{col}' no encontrada. Se creará vacía.")
            df[col] = "Sin Dato"

    # ========== LIMPIEZA ==========
    # Usar ciudad normalizada si existe, si no usar ciudad_residencia
    if "ciudad" in df.columns:
        df["ciudad_para_filtro"] = df["ciudad"].fillna("Sin Ciudad").astype(str)
    else:
        df["ciudad_para_filtro"] = (
            df["ciudad_residencia"].fillna("Sin Ciudad").astype(str)
        )

    df["NOM_PROGRAMA"] = df["NOM_PROGRAMA"].fillna("Sin Programa").astype(str)

    # Usar modalidad_normalizada si existe, si no usar modalidad
    if "modalidad_normalizada" in df.columns:
        df["modalidad_para_filtro"] = (
            df["modalidad_normalizada"].fillna("Sin Modalidad").astype(str)
        )
    else:
        df["modalidad_para_filtro"] = (
            df["modalidad"].fillna("Sin Modalidad").astype(str)
        )

    df["ESTADO_PAGO"] = df["ESTADO_PAGO"].fillna("Sin Estado").astype(str).str.upper()
    df["periodo"] = df["periodo"].fillna("Sin Periodo").astype(str)
    df["canal_fuente"] = df["canal_fuente"].fillna("Sin Canal").astype(str)
    df["fuente"] = df["fuente"].fillna("Sin Fuente").astype(str)
    df["tipo_de_fuente"] = df["tipo_de_fuente"].fillna("Sin Tipo Fuente").astype(str)
    df["fuerzacomercial"] = df["fuerzacomercial"].fillna("Sin Fuerza").astype(str)

    # Convertir calificaciones a numérico
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
        else:
            df[col] = 0

    if "CALIFICACION_TOTAL" in df.columns:
        df["CALIFICACION_TOTAL"] = pd.to_numeric(
            df["CALIFICACION_TOTAL"], errors="coerce"
        )
    else:
        df["CALIFICACION_TOTAL"] = 0

    # ========== CLASIFICACIÓN DE OBJECIONES (USANDO MÚLTIPLES COLUMNAS) ==========
    objeciones_lista = [
        "Competencia",
        "Economica",
        "No_interesado",
        "Terceros_Familia",
        "Tiempo_flexibilidad",
    ]

    no_objeciones_lista = [
        "Datos_Erroneos_No_Registro",
        "Ninguna",
        "Sin_Tiempo_Atender",
        "Tiempo_Horario_Incomodo",
        "Tiempo_Trabajo_Ocupado",
        "Tramite_Reintegro",
    ]

    # Identificar columnas de objeciones (objecion_1 a objecion_12)
    columnas_objeciones = [col for col in df.columns if col.startswith("objecion_")]

    # Si no hay columnas objecion_*, crear una desde Objecion_Detectada
    if not columnas_objeciones:
        if "Objecion_Detectada" in df.columns:
            df["objecion_1"] = df["Objecion_Detectada"]
            columnas_objeciones = ["objecion_1"]
        else:
            df["objecion_1"] = "Sin Clasificar"
            columnas_objeciones = ["objecion_1"]

    # Función para determinar si una fila tiene objeción o no
    def clasificar_fila(row):
        for col in columnas_objeciones:
            valor = row.get(col, "")
            if pd.isna(valor):
                continue
            if valor in objeciones_lista:
                return "Objeción"
            if valor in no_objeciones_lista:
                return "No Objeción"
        return "Sin Clasificar"

    df["Tipo"] = df.apply(clasificar_fila, axis=1)

    return df, columnas_objeciones


df, columnas_objeciones = cargar_datos()


# ==================== FUNCIÓN PARA COMBINAR OBJECIONES ====================
def obtener_todas_objeciones(df, columnas_objeciones):
    """Combina todas las columnas de objeciones en una sola Serie"""
    todas = []
    for col in columnas_objeciones:
        if col in df.columns:
            valores = df[col].dropna()
            valores = valores[valores != ""]
            valores = valores[valores != "Sin Clasificar"]
            todas.extend(valores.tolist())
    return pd.Series(todas)


# ==================== FILTROS ====================
st.sidebar.header("🔍 Filtros")
st.sidebar.caption(
    "💡 Seleccione los criterios específicos o marque **'Todos'** para abrir el segmento."
)

# Opciones para filtros usando columnas normalizadas
ciudades_opciones = ["Todos"] + sorted(list(df["ciudad_para_filtro"].unique()))
programas_opciones = ["Todos"] + sorted(list(df["NOM_PROGRAMA"].unique()))
modalidades_opciones = ["Todos"] + sorted(list(df["MODALIDAD"].unique()))
periodos_opciones = ["Todos"] + sorted(list(df["periodo"].unique()))

ciudad = st.sidebar.multiselect("📍 Ciudad", options=ciudades_opciones, default=[])
programa = st.sidebar.multiselect("🎓 Programa", options=programas_opciones, default=[])
modalidad = st.sidebar.multiselect(
    "📚 Modalidad", options=modalidades_opciones, default=[]
)
periodo = st.sidebar.multiselect("📅 Período", options=periodos_opciones, default=[])

# ==================== VALIDACIÓN CRÍTICA DE FILTROS VACÍOS ====================
if not (ciudad or programa or modalidad or periodo):
    st.markdown("# 🎓 Diagnóstico Comercial")
    st.markdown("### Pago vs No Pago")
    st.info(
        "👋 **Bienvenido al módulo de Diagnóstico Comercial.** \n\n"
        "Por favor, use el panel de la **barra lateral izquierda** 👈 para seleccionar la combinación que desea analizar. "
        "Recuerde que puede marcar la opción explícita **'Todos'** si desea evaluar la totalidad de los datos para ese campo."
    )
    st.stop()

# ==================== MOSTRAR FILTROS SELECCIONADOS ====================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Filtros aplicados:")
if ciudad:
    st.sidebar.markdown(f"- **Ciudad:** {', '.join(ciudad)}")
if programa:
    st.sidebar.markdown(f"- **Programa:** {', '.join(programa)}")
if modalidad:
    st.sidebar.markdown(f"- **Modalidad:** {', '.join(modalidad)}")
if periodo:
    st.sidebar.markdown(f"- **Período:** {', '.join(periodo)}")

# ==================== APLICAR FILTROS ====================
df_filtrado = df.copy()

if ciudad and "Todos" not in ciudad:
    df_filtrado = df_filtrado[df_filtrado["ciudad_para_filtro"].isin(ciudad)]

if programa and "Todos" not in programa:
    df_filtrado = df_filtrado[df_filtrado["NOM_PROGRAMA"].isin(programa)]

if modalidad and "Todos" not in modalidad:
    df_filtrado = df_filtrado[df_filtrado["MODALIDAD"].isin(modalidad)]

if periodo and "Todos" not in periodo:
    df_filtrado = df_filtrado[df_filtrado["periodo"].isin(periodo)]

if df_filtrado.empty:
    st.warning(
        "⚠️ No se encontraron registros coincidentes para la combinación seleccionada. Intente con otros criterios."
    )
    st.stop()

# ==================== DEFINICIONES ====================
OBJECIONES_LISTA = [
    "Competencia",
    "Economica",
    "No_interesado",
    "Terceros_Familia",
    "Tiempo_flexibilidad",
]
NO_OBJECIONES_LISTA = [
    "Datos_Erroneos_No_Registro",
    "Ninguna",
    "Sin_Tiempo_Atender",
    "Tiempo_Horario_Incomodo",
    "Tiempo_Trabajo_Ocupado",
    "Tramite_Reintegro",
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

COLOR_VERDE = "#2e7d32"


# ==================== FUNCIONES DE CÁLCULO ====================
def calcular_conversion(df):
    if df.empty:
        return 0
    total = len(df)
    pago = len(df[df["ESTADO_PAGO"] == "PAGO"])
    return (pago / total * 100) if total > 0 else 0


def obtener_moda(df, columna):
    if df.empty or columna not in df.columns:
        return "N/A"
    valores = df[columna].value_counts()
    if valores.empty:
        return "N/A"
    return valores.index[0]


# ==================== FUNCIONES GRÁFICAS ====================
def crear_grafico_barras_porcentaje(series, titulo, color):
    """Crea gráfico de barras a partir de una Serie de valores"""
    if series.empty:
        return None, None

    data = series.value_counts().reset_index()
    data.columns = ["Categoria", "Cantidad"]

    total_grupo = len(series)
    data["Porcentaje"] = (data["Cantidad"] / total_grupo * 100).round(1)
    data = data.sort_values("Porcentaje", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=data["Categoria"],
            x=data["Porcentaje"],
            orientation="h",
            text=data["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            marker=dict(color=color),
            hovertemplate="<b>%{y}</b><br>Porcentaje: %{x:.1f}%<br>Cantidad: %{customdata:,}<extra></extra>",
            customdata=data["Cantidad"],
        )
    )

    fig.update_layout(
        height=400,
        xaxis_title="Porcentaje de aparición (%)",
        yaxis_title="",
        xaxis=dict(range=[0, 100]),
        margin=dict(l=10, r=30, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    insights = []
    if not data.empty:
        top = data.iloc[-1]
        bottom = data.iloc[0]
        insights.append(
            f"🔹 **{top['Categoria']}** es la categoría con mayor participación ({top['Porcentaje']:.1f}%)."
        )
        insights.append(
            f"🔹 **{bottom['Categoria']}** es la categoría con menor participación ({bottom['Porcentaje']:.1f}%)."
        )

    return fig, insights


def crear_grafico_barras_p1p7(df, titulo, color):
    if df.empty:
        return None, None

    promedios = {}
    for p in COLUMNAS_P:
        if p in df.columns:
            prom = df[p].mean()
            promedios[p.replace("P", "P ")] = prom if pd.notna(prom) else 0

    if not promedios:
        return None, None

    data = pd.DataFrame(list(promedios.items()), columns=["Pilar", "Promedio"])
    data = data.sort_values("Promedio", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=data["Pilar"],
            x=data["Promedio"],
            orientation="h",
            text=data["Promedio"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            marker=dict(
                color=data["Promedio"],
                colorscale="Greens",
                showscale=True,
                colorbar=dict(title="%"),
            ),
            hovertemplate="<b>%{y}</b><br>Promedio: %{x:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        height=400,
        xaxis_title="Promedio (%)",
        yaxis_title="",
        xaxis=dict(range=[0, 100]),
        margin=dict(l=10, r=30, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    insights = []
    if not data.empty:
        top = data.iloc[-1]
        bottom = data.iloc[0]
        insights.append(
            f"🔹 **{top['Pilar']}** es el pilar con mejor desempeño ({top['Promedio']:.1f}%)."
        )
        insights.append(
            f"🔹 **{bottom['Pilar']}** es el pilar con peor desempeño ({bottom['Promedio']:.1f}%)."
        )

    return fig, insights


def crear_grafico_comparativo_objeciones(df, series_pago, series_no_pago, titulo):
    """Crea gráfico comparativo entre Pago y No Pago usando Series de objeciones"""
    if series_pago.empty and series_no_pago.empty:
        return None, None

    total_pago = len(series_pago)
    total_no_pago = len(series_no_pago)

    if total_pago == 0 or total_no_pago == 0:
        return None, None

    pago_data = series_pago.value_counts().reset_index()
    pago_data.columns = ["Categoria", "Cantidad"]
    pago_data["% en Pago"] = (pago_data["Cantidad"] / total_pago * 100).round(1)

    no_pago_data = series_no_pago.value_counts().reset_index()
    no_pago_data.columns = ["Categoria", "Cantidad"]
    no_pago_data["% en No Pago"] = (
        no_pago_data["Cantidad"] / total_no_pago * 100
    ).round(1)

    data = pd.merge(pago_data, no_pago_data, on="Categoria", how="outer").fillna(0)
    data = data.sort_values("Cantidad_x", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=data["Categoria"],
            x=data["% en Pago"],
            name="Pago",
            orientation="h",
            marker=dict(color=COLOR_VERDE),
            text=data["% en Pago"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Pago: %{x:.1f}%<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            y=data["Categoria"],
            x=data["% en No Pago"],
            name="No Pago",
            orientation="h",
            marker=dict(color="#2E86C1"),
            text=data["% en No Pago"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>No Pago: %{x:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        height=450,
        xaxis_title="Porcentaje de aparición (%)",
        yaxis_title="",
        xaxis=dict(range=[0, 100]),
        barmode="group",
        margin=dict(l=10, r=30, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )

    insights = []
    if not data.empty:
        data["Diferencia"] = abs(data["% en Pago"] - data["% en No Pago"])
        max_diff = data.loc[data["Diferencia"].idxmax()]
        insights.append(
            f"🔹 **{max_diff['Categoria']}** presenta la mayor diferencia de comportamiento entre ambos grupos ({max_diff['Diferencia']:.1f}%)."
        )

    return fig, insights


def crear_radar_chart(df):
    if df.empty:
        return None, None

    df_pago = df[df["ESTADO_PAGO"] == "PAGO"]
    df_no_pago = df[df["ESTADO_PAGO"] == "NO PAGO"]

    promedios_pago = {}
    promedios_no_pago = {}

    for p in COLUMNAS_P:
        prom_pago = df_pago[p].mean() if not df_pago.empty else 0
        prom_no_pago = df_no_pago[p].mean() if not df_no_pago.empty else 0
        promedios_pago[p.replace("P", "P ")] = prom_pago if pd.notna(prom_pago) else 0
        promedios_no_pago[p.replace("P", "P ")] = (
            prom_no_pago if pd.notna(prom_no_pago) else 0
        )

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=list(promedios_pago.values()),
            theta=list(promedios_pago.keys()),
            fill="toself",
            name="🟢 Pago",
            line_color=COLOR_VERDE,
            fillcolor="rgba(46, 125, 50, 0.2)",
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=list(promedios_no_pago.values()),
            theta=list(promedios_no_pago.keys()),
            fill="toself",
            name="🔵 No Pago",
            line_color="#2E86C1",
            fillcolor="rgba(46, 134, 193, 0.2)",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickformat=".0f%")),
        height=450,
        showlegend=True,
        margin=dict(l=40, r=40, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    insights = []
    if promedios_pago and promedios_no_pago:
        pago_prom = sum(promedios_pago.values()) / len(promedios_pago)
        no_pago_prom = sum(promedios_no_pago.values()) / len(promedios_no_pago)
        insights.append(
            f"🔹 Desempeño promedio global del Speech: **{pago_prom:.1f}%** en Pago vs **{no_pago_prom:.1f}%** en No Pago."
        )

    return fig, insights


def crear_heatmap(df):
    if df.empty:
        return None, None

    heatmap_data = []
    for estado in ["PAGO", "NO PAGO"]:
        row = [estado]
        for p in COLUMNAS_P:
            prom = df[df["ESTADO_PAGO"] == estado][p].mean()
            row.append(prom if pd.notna(prom) else 0)
        heatmap_data.append(row)

    df_heatmap = pd.DataFrame(
        heatmap_data,
        columns=["Estado"] + [p.replace("P", "P ") for p in COLUMNAS_P],
    )

    fig = px.imshow(
        df_heatmap.set_index("Estado"),
        text_auto=".1f",
        color_continuous_scale="Greens",
        aspect="auto",
        title="Matriz de Calificaciones por Pilar y Estado",
    )
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    insights = []
    if not df_heatmap.empty:
        pago_row = df_heatmap[df_heatmap["Estado"] == "PAGO"]
        if not pago_row.empty:
            pago_values = pago_row.iloc[0, 1:].values
            max_pago_idx = np.argmax(pago_values)
            max_pago_col = df_heatmap.columns[max_pago_idx + 1]
            insights.append(
                f"🔹 El pilar con mayor efectividad para los que pagaron es **{max_pago_col}** con **{pago_values[max_pago_idx]:.1f}%**."
            )

    return fig, insights


def mostrar_insights(insights):
    if insights:
        for insight in insights:
            st.markdown(
                f'<div class="insight-box">{insight}</div>',
                unsafe_allow_html=True,
            )


# ==================== TÍTULO Y PRESENTACIÓN ====================
st.markdown("# 🎓 Diagnóstico Comercial")
st.markdown("### Pago vs No Pago")
st.markdown(
    """
*Este dashboard permite identificar los factores comerciales, operativos y del speech que diferencian a los prospectos que realizaron el pago frente a aquellos que no finalizaron su proceso de matrícula.*
"""
)

# ==================== GUÍA DE MANEJO DE GRÁFICOS ====================
with st.expander("💡 ¿Cómo interactuar y manejar los gráficos interactivos?"):
    st.markdown(
        """
    Todos los gráficos de este dashboard son interactivos gracias a **Plotly**. Aquí tienes una guía rápida para sacarles el máximo provecho:
    
    1. **Ver valores exactos (Hover):** Pasa el cursor o presiona sobre cualquier barra, punto o sección del gráfico para ver una tarjeta flotante con los datos numéricos y porcentajes exactos.
    2. **Ocultar o aislar series (Leyenda):** En los gráficos comparativos (como el Radar o las barras agrupadas), haz clic en los elementos de la leyenda (ej. 🟢 *Pago* o 🔵 *No Pago*) para encender o apagar esa población en la vista.
    3. **Zoom dinámico:** Haz clic y arrastra sobre cualquier región del gráfico para hacer zoom en un área específica. Doble clic en cualquier parte del gráfico restablecerá la vista original.
    4. **Barra de herramientas flotante:** Al pasar el cursor por la esquina superior derecha de cualquier gráfico, verás herramientas adicionales para descargar el gráfico como imagen PNG, hacer paneo o activar líneas de guía.
    """
    )

st.markdown("---")

# ==================== KPIs SUPERIORES ====================
st.subheader("📊 Resumen Ejecutivo (Segmento Seleccionado)")

total = len(df_filtrado)
total_pago = len(df_filtrado[df_filtrado["ESTADO_PAGO"] == "PAGO"])
total_no_pago = len(df_filtrado[df_filtrado["ESTADO_PAGO"] == "NO PAGO"])
conversion = (total_pago / total * 100) if total > 0 else 0
calif_prom = df_filtrado["CALIFICACION_TOTAL"].mean()
calif_prom = calif_prom if pd.notna(calif_prom) else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("📞 Total Prospectos", f"{total:,}")
with col2:
    st.metric(
        "🟢 Pago",
        f"{total_pago:,}",
        f"{total_pago/total*100:.1f}%" if total > 0 else "0%",
    )
with col3:
    st.metric(
        "🔵 No Pago",
        f"{total_no_pago:,}",
        f"{total_no_pago/total*100:.1f}%" if total > 0 else "0%",
    )
with col4:
    st.metric("📈 Conversión", f"{conversion:.1f}%")
with col5:
    st.metric("⭐ Calificación Promedio", f"{calif_prom:.2f}")

st.markdown("---")

# ==================== EXPANDER 1: PANORAMA GENERAL ====================
with st.expander("📊 Panorama General", expanded=True):
    st.markdown("### Seleccione una población para analizar")

    poblacion = st.radio(
        "Población:",
        options=["Todos", "Pago", "No Pago"],
        horizontal=True,
        key="poblacion_selector",
    )

    df_panorama = df_filtrado.copy()
    if poblacion == "Pago":
        df_panorama = df_panorama[df_panorama["ESTADO_PAGO"] == "PAGO"]
    elif poblacion == "No Pago":
        df_panorama = df_panorama[df_panorama["ESTADO_PAGO"] == "NO PAGO"]

    if df_panorama.empty:
        st.warning(f"⚠️ No hay datos para la población seleccionada.")
    else:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric("📞 Total", f"{len(df_panorama):,}")
        with col2:
            pago = len(df_panorama[df_panorama["ESTADO_PAGO"] == "PAGO"])
            st.metric("🟢 Pago", f"{pago:,}")
        with col3:
            no_pago = len(df_panorama[df_panorama["ESTADO_PAGO"] == "NO PAGO"])
            st.metric("🔵 No Pago", f"{no_pago:,}")
        with col4:
            conv = calcular_conversion(df_panorama)
            st.metric("📈 Conversión", f"{conv:.1f}%")
        with col5:
            calif = df_panorama["CALIFICACION_TOTAL"].mean()
            calif = calif if pd.notna(calif) else 0
            st.metric("⭐ Calificación", f"{calif:.2f}")
        with col6:
            # Obtener la objeción más frecuente usando todas las columnas
            todas_obj = obtener_todas_objeciones(df_panorama, columnas_objeciones)
            if not todas_obj.empty:
                moda = todas_obj.value_counts().index[0]
            else:
                moda = "N/A"
            st.metric("🎯 Objeción más frecuente", moda)

        st.markdown("---")

        # ===== GRÁFICO 1: OBJECIONES =====
        st.markdown("#### ✅ Distribución de Objeciones")
        todas_obj = obtener_todas_objeciones(df_panorama, columnas_objeciones)
        # Filtrar solo las que están en OBJECIONES_LISTA
        obj_filtradas = todas_obj[todas_obj.isin(OBJECIONES_LISTA)]
        fig_obj, insights_obj = crear_grafico_barras_porcentaje(
            obj_filtradas, "Objeciones", COLOR_VERDE
        )
        if fig_obj:
            st.plotly_chart(fig_obj, use_container_width=True)
            mostrar_insights(insights_obj)
        else:
            st.info("ℹ️ No hay objeciones para mostrar")

        st.markdown("---")

        # ===== GRÁFICO 2: NO OBJECIONES =====
        st.markdown("#### 🔄 Distribución de No Objeciones")
        # Filtrar solo las que están en NO_OBJECIONES_LISTA
        no_obj_filtradas = todas_obj[todas_obj.isin(NO_OBJECIONES_LISTA)]
        fig_no_obj, insights_no_obj = crear_grafico_barras_porcentaje(
            no_obj_filtradas, "No Objeciones", COLOR_VERDE
        )
        if fig_no_obj:
            st.plotly_chart(fig_no_obj, use_container_width=True)
            mostrar_insights(insights_no_obj)
        else:
            st.info("ℹ️ No hay no objeciones para mostrar")

        st.markdown("---")

        # ===== GRÁFICO 3: CALIFICACIÓN P1-P7 =====
        st.markdown("#### ⭐ Calificación de Llamadas (P1 - P7)")
        fig_p1p7, insights_p1p7 = crear_grafico_barras_p1p7(
            df_panorama, "Calificación P1-P7", COLOR_VERDE
        )
        if fig_p1p7:
            st.plotly_chart(fig_p1p7, use_container_width=True)
            mostrar_insights(insights_p1p7)
        else:
            st.info("ℹ️ No hay datos de calificación P1-P7 para mostrar")


# ==================== EXPANDER 2: PAGO vs NO PAGO ====================
with st.expander("⚔️ Pago vs No Pago", expanded=False):
    st.markdown(
        "### Descubre las diferencias entre los prospectos que pagaron y los que no"
    )

    if df_filtrado.empty:
        st.warning("⚠️ No hay datos con los filtros seleccionados.")
    else:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        pago_total = len(df_filtrado[df_filtrado["ESTADO_PAGO"] == "PAGO"])
        no_pago_total = len(df_filtrado[df_filtrado["ESTADO_PAGO"] == "NO PAGO"])
        conversion_total = calcular_conversion(df_filtrado)

        calif_pago = df_filtrado[df_filtrado["ESTADO_PAGO"] == "PAGO"][
            "CALIFICACION_TOTAL"
        ].mean()
        calif_pago = calif_pago if pd.notna(calif_pago) else 0

        calif_no_pago = df_filtrado[df_filtrado["ESTADO_PAGO"] == "NO PAGO"][
            "CALIFICACION_TOTAL"
        ].mean()
        calif_no_pago = calif_no_pago if pd.notna(calif_no_pago) else 0

        diff_calif = calif_pago - calif_no_pago

        with col1:
            st.metric(
                "🟢 Pago",
                f"{pago_total:,}",
                (
                    f"{pago_total/(pago_total+no_pago_total)*100:.1f}%"
                    if (pago_total + no_pago_total) > 0
                    else "0%"
                ),
            )
        with col2:
            st.metric(
                "🔵 No Pago",
                f"{no_pago_total:,}",
                (
                    f"{no_pago_total/(pago_total+no_pago_total)*100:.1f}%"
                    if (pago_total + no_pago_total) > 0
                    else "0%"
                ),
            )
        with col3:
            st.metric("📈 Conversión", f"{conversion_total:.1f}%")
        with col4:
            st.metric("⭐ Calificación Pago", f"{calif_pago:.2f}")
        with col5:
            st.metric("⭐ Calificación No Pago", f"{calif_no_pago:.2f}")
        with col6:
            color_delta = "normal" if diff_calif > 0 else "inverse"
            st.metric("📊 Diferencia", f"{diff_calif:+.2f}", delta_color=color_delta)

        st.markdown("---")

        # ===== GRÁFICO 1: COMPARACIÓN OBJECIONES =====
        st.markdown("#### 📌 Comparación de Objeciones")

        # Obtener objeciones para Pago y No Pago
        df_pago = df_filtrado[df_filtrado["ESTADO_PAGO"] == "PAGO"]
        df_no_pago = df_filtrado[df_filtrado["ESTADO_PAGO"] == "NO PAGO"]

        obj_pago = obtener_todas_objeciones(df_pago, columnas_objeciones)
        obj_no_pago = obtener_todas_objeciones(df_no_pago, columnas_objeciones)

        # Filtrar solo objeciones
        obj_pago_filt = obj_pago[obj_pago.isin(OBJECIONES_LISTA)]
        obj_no_pago_filt = obj_no_pago[obj_no_pago.isin(OBJECIONES_LISTA)]

        fig_obj_comp, insights_obj_comp = crear_grafico_comparativo_objeciones(
            df_filtrado, obj_pago_filt, obj_no_pago_filt, "Comparación de Objeciones"
        )
        if fig_obj_comp:
            st.plotly_chart(fig_obj_comp, use_container_width=True)
            mostrar_insights(insights_obj_comp)
        else:
            st.info("ℹ️ No hay datos de objeciones para comparar")

        st.markdown("---")

        # ===== GRÁFICO 2: COMPARACIÓN NO OBJECIONES =====
        st.markdown("#### 🔄 Comparación de No Objeciones")

        # Filtrar solo no objeciones
        no_obj_pago_filt = obj_pago[obj_pago.isin(NO_OBJECIONES_LISTA)]
        no_obj_no_pago_filt = obj_no_pago[obj_no_pago.isin(NO_OBJECIONES_LISTA)]

        fig_no_obj_comp, insights_no_obj_comp = crear_grafico_comparativo_objeciones(
            df_filtrado,
            no_obj_pago_filt,
            no_obj_no_pago_filt,
            "Comparación de No Objeciones",
        )
        if fig_no_obj_comp:
            st.plotly_chart(fig_no_obj_comp, use_container_width=True)
            mostrar_insights(insights_no_obj_comp)
        else:
            st.info("ℹ️ No hay datos de no objeciones para comparar")

        st.markdown("---")

        # ===== GRÁFICO 3: RADAR DEL SPEECH =====
        st.markdown("#### 🧬 Radar del Speech Comercial")
        fig_radar, insights_radar = crear_radar_chart(df_filtrado)
        if fig_radar:
            st.plotly_chart(fig_radar, use_container_width=True)
            mostrar_insights(insights_radar)
        else:
            st.info("ℹ️ No hay datos para el radar")

        st.markdown("---")

        # ===== GRÁFICO 4: HEATMAP =====
        st.markdown("#### 🗺️ Heatmap de Calificaciones")
        fig_heatmap, insights_heatmap = crear_heatmap(df_filtrado)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
            mostrar_insights(insights_heatmap)
        else:
            st.info("ℹ️ No hay datos para el heatmap")


# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #6b7a8f; font-size: 0.8rem;">
    <b>Pago vs No Pago</b> | Inteligencia Comercial CUN
</div>
""",
    unsafe_allow_html=True,
)
