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

st.title("🎯 Análisis de Objeciones COE - CUN")

# ==================== RUTA DEL EXCEL (ACTUALIZADA) ====================
RUTA_EXCEL = r"C:\Users\juan_garnicac\Documents\ProyectosVisual\Ventas\presentaciones\salida_con_pago.xlsx"
st.markdown(f"**📂 Archivo cargado:** `{RUTA_EXCEL}`")
st.markdown("---")

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
        st.error(f"❌ No se encuentra el archivo: {RUTA_EXCEL}")
        st.info(f"Asegúrate de que el archivo exista en la ruta indicada.")
        return None, None, None, None, None, None, None

    try:
        df = pd.read_excel(RUTA_EXCEL)
        st.success(f"✅ Archivo cargado. Filas: {len(df)}")
    except Exception as e:
        st.error(f"❌ Error al leer el Excel: {e}")
        return None, None, None, None, None, None, None

    col_prog = "NOM_PROGRAMA"
    col_obj = "Objecion_Detectada"
    col_mod = "MODALIDAD"
    col_ciudad = "Ciudad"
    col_fecha = "Fecha"
    col_estado = "ESTADO_PAGO"

    # Verificar columnas requeridas
    columnas_requeridas = [
        col_prog,
        col_obj,
        col_mod,
        col_ciudad,
        col_fecha,
        col_estado,
    ]
    faltan = [c for c in columnas_requeridas if c not in df.columns]
    if faltan:
        st.error(f"❌ Faltan columnas: {faltan}")
        st.write("Columnas disponibles:", df.columns.tolist())
        return None, None, None, None, None, None, None

    # Limpieza básica
    df[col_prog] = df[col_prog].fillna("Sin Especificar").astype(str).str.strip()
    df[col_obj] = df[col_obj].fillna("Sin Objeción").astype(str).str.strip()
    df[col_mod] = df[col_mod].fillna("Sin Modalidad").astype(str).str.strip()
    df[col_ciudad] = df[col_ciudad].fillna("Sin Ciudad").astype(str).str.strip()
    df[col_estado] = df[col_estado].fillna("Sin Estado").astype(str).str.strip()

    if col_fecha in df.columns:
        df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")

    # Mapear objeciones
    df["es_objecion"] = df[col_obj].map(MAPEO_OBJECION)
    df["es_objecion"] = df["es_objecion"].fillna(True).astype(bool)

    # Mostrar estadísticas de depuración
    st.write("🔍 **Depuración:**")
    st.write(f"- Total de filas en el Excel: {len(df):,}")
    st.write(f"- Columnas: {len(df.columns)}")
    st.write(f"- Valores únicos en ESTADO_PAGO: {sorted(df[col_estado].unique())}")

    if df.empty:
        st.warning("⚠️ Después de limpiar, no quedaron registros válidos.")
    else:
        st.info(f"✅ Datos limpios: {len(df)} filas listas para analizar.")

    return df, col_prog, col_obj, col_mod, col_ciudad, col_fecha, col_estado


df, col_prog, col_obj, col_mod, col_ciudad, col_fecha, col_estado = cargar_datos()
if df is None or df.empty:
    st.stop()

# ==================== FILTROS (SIDEBAR) ====================
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

# Se mantiene todo el dataframe (no se filtra por estado de pago)
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

# ==================== GRÁFICA 1: OBJECIONES ====================
st.subheader("📈 Distribución de Objeciones")
st.markdown(
    """
<div class="explicacion">
<b>❓ ¿Qué pregunta resuelve esta gráfica?</b><br>
<i>¿Cuáles son las principales objeciones que los prospectos expresan durante la llamada y con qué frecuencia ocurren?</i><br>
<b>🔍 Interpretación:</b> Esta gráfica muestra el volumen de cada tipo de objeción detectada. Identificar la objeción dominante (por ejemplo, "Economica" o "No_interesado") permite focalizar las estrategias de abordaje y capacitación de los asesores para superar esas barreras.
</div>
""",
    unsafe_allow_html=True,
)
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

# ==================== GRÁFICA 2: NO OBJECIONES ====================
st.subheader("🔄 Distribución de No Objeciones")
st.markdown(
    """
<div class="explicacion">
<b>❓ ¿Qué pregunta resuelve esta gráfica?</b><br>
<i>¿Qué categorías se registran cuando NO hay una objeción clara y cuál es su frecuencia?</i><br>
<b>🔍 Interpretación:</b> Esta gráfica muestra las situaciones donde no se detectó una objeción tradicional. Categorías como "Tramite_Reintegro" o "Sin_Tiempo_Atender" indican que el prospecto es un estudiante actual o que simplemente no pudo atender, lo que requiere un enfoque diferente al de una objeción clásica.
</div>
""",
    unsafe_allow_html=True,
)
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

# ==================== GRÁFICA 3: PROMEDIOS P1-P7 ====================
st.subheader("📊 Promedios de Calificaciones (P1 - P7)")
st.markdown(
    """
<div class="explicacion">
<b>❓ ¿Qué pregunta resuelve esta gráfica?</b><br>
<i>¿En qué etapas de la llamada (promesa, beneficio, entregables, garantía, regalos, precio, cierre) los asesores obtienen mejores o peores puntajes?</i><br>
<b>🔍 Interpretación:</b> Estos promedios permiten identificar fortalezas y debilidades en el proceso de ventas. Por ejemplo, si "Precio" tiene un puntaje bajo, puede indicar que los asesores necesitan mejorar su manejo de objeciones económicas.
</div>
""",
    unsafe_allow_html=True,
)

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

# ==================== GRÁFICA 4: M2 CONFIANZA ====================
st.subheader("📊 Distribución del Puntaje de Confianza (M2)")
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

# ==================== ACORDEÓN: ANÁLISIS PORCENTUAL ====================
with st.expander("📊 Análisis Porcentual (peso relativo de cada categoría)"):
    st.markdown(
        """
    <div class="explicacion">
    <b>❓ ¿Qué pregunta resuelve esta sección?</b><br>
    <i>¿Qué porcentaje del total de objeciones (o no objeciones) representa cada categoría?</i><br>
    <b>🔍 Interpretación:</b> Permite entender la importancia relativa de cada categoría. Una categoría que representa el 40% de las objeciones es un problema mucho más relevante que una que solo representa el 5%.
    </div>
    """,
        unsafe_allow_html=True,
    )
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

# ==================== NUEVA SECCIÓN: ANÁLISIS POR CIUDAD Y ESTADO DE PAGO ====================
with st.expander("🏙️ Análisis por Ciudad y Estado de Pago"):
    st.markdown(
        """
    <div class="explicacion">
    <b>❓ ¿Qué pregunta resuelve esta sección?</b><br>
    <i>¿Cómo varía la tasa de conversión a PAGO entre las diferentes ciudades? ¿Y cómo se relaciona la calificación de la llamada con el estado de pago?</i><br>
    <b>🔍 Interpretación:</b> Esta sección identifica qué ciudades tienen mejor desempeño comercial y cuáles requieren atención especial. Además, muestra la fuerte relación entre la calidad de la llamada (medida por CALIFICACION_TOTAL) y la probabilidad de que el prospecto termine pagando.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Tabla resumen por ciudad
    st.markdown("### 📋 Resumen por ciudad")
    df_ciudad = (
        df_filtrado.groupby(col_ciudad)
        .agg(
            Total=("es_objecion", "count"),
            PAGO=(col_estado, lambda x: (x == "PAGO").sum()),
            NO_PAGO=(col_estado, lambda x: (x == "NO PAGO").sum()),
        )
        .reset_index()
    )
    df_ciudad["% PAGO"] = (df_ciudad["PAGO"] / df_ciudad["Total"] * 100).round(1)
    df_ciudad["% NO PAGO"] = (df_ciudad["NO_PAGO"] / df_ciudad["Total"] * 100).round(1)
    df_ciudad = df_ciudad.sort_values("% PAGO", ascending=False)
    df_ciudad_show = df_ciudad[df_ciudad["Total"] >= 5].copy()

    if not df_ciudad_show.empty:
        st.dataframe(
            df_ciudad_show,
            column_config={
                col_ciudad: "Ciudad",
                "Total": "Total Llamadas",
                "PAGO": "PAGO",
                "NO_PAGO": "NO PAGO",
                "% PAGO": st.column_config.NumberColumn("% PAGO", format="%.1f%%"),
                "% NO PAGO": st.column_config.NumberColumn(
                    "% NO PAGO", format="%.1f%%"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No hay suficientes datos por ciudad para mostrar (mínimo 5 llamadas).")

    # Gráfico de % PAGO por ciudad
    if not df_ciudad_show.empty:
        fig_ciudad = px.bar(
            df_ciudad_show,
            x="Ciudad",
            y="% PAGO",
            color="% PAGO",
            color_continuous_scale="Greens",
            text="% PAGO",
            title="Porcentaje de PAGO por Ciudad",
            labels={"% PAGO": "% de PAGO"},
        )
        fig_ciudad.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_ciudad.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis_title="",
            yaxis_title="% de conversión a PAGO",
        )
        st.plotly_chart(fig_ciudad, use_container_width=True)

    # Calificación promedio por ciudad y estado de pago
    st.markdown("### 📊 Calificación promedio por ciudad y estado de pago")
    st.markdown(
        """
    <div class="explicacion" style="margin-top:0;">
    <b>❓ ¿Qué pregunta resuelve esta tabla?</b><br>
    <i>¿Cómo influye la calidad de la llamada (medida por CALIFICACION_TOTAL) en la probabilidad de que el prospecto pague?</i><br>
    <b>🔍 Interpretación:</b> En todas las ciudades, las llamadas que terminan en <b>PAGO</b> tienen una calificación promedio <b>significativamente más alta</b> que las que terminan en <b>NO PAGO</b>. Esto confirma que la calidad de la interacción es un predictor clave del resultado final. Cuanto mayor sea la diferencia, más determinante es la calidad de la llamada para esa ciudad.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_calif = "CALIFICACION_TOTAL"
    if col_calif in df_filtrado.columns:
        df_calif = (
            df_filtrado.groupby([col_ciudad, col_estado])[col_calif]
            .mean()
            .reset_index()
        )
        df_calif_pivot = df_calif.pivot(
            index=col_ciudad, columns=col_estado, values=col_calif
        ).reset_index()

        # Renombrar dinámicamente
        nuevos_nombres = {col_ciudad: col_ciudad}
        for col in df_calif_pivot.columns:
            if col != col_ciudad:
                nuevos_nombres[col] = f"Prom_{col}"
        df_calif_pivot.rename(columns=nuevos_nombres, inplace=True)

        # Calcular diferencia solo si existen PAGO y NO_PAGO
        if (
            "Prom_PAGO" in df_calif_pivot.columns
            and "Prom_NO_PAGO" in df_calif_pivot.columns
        ):
            df_calif_pivot["Diferencia (PAGO - NO PAGO)"] = (
                df_calif_pivot["Prom_PAGO"] - df_calif_pivot["Prom_NO_PAGO"]
            ).round(1)
            df_calif_show = df_calif_pivot.dropna(subset=["Prom_PAGO", "Prom_NO_PAGO"])
            if not df_calif_show.empty:
                st.dataframe(
                    df_calif_show,
                    column_config={
                        col_ciudad: "Ciudad",
                        "Prom_PAGO": st.column_config.NumberColumn(
                            "Prom. CALIFICACIÓN (PAGO)", format="%.1f"
                        ),
                        "Prom_NO_PAGO": st.column_config.NumberColumn(
                            "Prom. CALIFICACIÓN (NO PAGO)", format="%.1f"
                        ),
                        "Diferencia (PAGO - NO PAGO)": st.column_config.NumberColumn(
                            "Diferencia", format="%.1f"
                        ),
                    },
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "No hay datos suficientes para comparar calificaciones por estado."
                )
        else:
            st.info(
                "No se encontraron los estados 'PAGO' y 'NO PAGO' en los datos filtrados."
            )
    else:
        st.info("La columna CALIFICACION_TOTAL no está disponible.")

    # Insights textuales
    st.markdown("### 🔍 Insights clave por ciudad")
    if not df_ciudad_show.empty:
        top_ciudad = df_ciudad_show.iloc[0]
        bottom_ciudad = df_ciudad_show.iloc[-1]
        st.markdown(
            f"""<div class="insight-box"><b>🏆 Mejor desempeño:</b> <b>{top_ciudad[col_ciudad]}</b> con un <b>{top_ciudad['% PAGO']:.1f}%</b> de conversión a PAGO.</div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<div class="insight-box" style="border-left-color: #dc3545;"><b>⚠️ Área de mejora:</b> <b>{bottom_ciudad[col_ciudad]}</b> con solo un <b>{bottom_ciudad['% PAGO']:.1f}%</b> de conversión a PAGO.</div>""",
            unsafe_allow_html=True,
        )
        if (
            col_calif in df_filtrado.columns
            and "Prom_PAGO" in locals()
            and "Prom_NO_PAGO" in locals()
        ):
            st.markdown(
                """
            <div class="insight-box">
            <b>📊 Correlación con la calificación:</b> En todas las ciudades, las llamadas que terminan en <b>PAGO</b> tienen una calificación total promedio <b>significativamente más alta</b> que las que terminan en <b>NO PAGO</b>. Esto confirma que la calidad de la interacción es un predictor clave del resultado final.
            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown(
            """
        <div class="insight-box">
        <b>💡 Recomendación:</b> Se sugiere investigar las razones detrás de la baja conversión en ciudades como <b>Neiva</b> y <b>Santa Marta</b> (perfil de prospecto, estrategia de comunicación, seguimiento) y replicar las prácticas exitosas de <b>Bucaramanga</b> y <b>Medellín</b>.
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No hay suficientes datos por ciudad para generar insights.")

st.markdown("---")

# ==================== TABLA DE CLASIFICACIÓN ====================
st.subheader("📋 Clasificación de categorías")
st.markdown(
    """
<div class="explicacion">
<b>❓ ¿Qué pregunta resuelve esta tabla?</b><br>
<i>¿Qué significa cada categoría de objeción y cómo se clasifica?</i><br>
<b>🔍 Interpretación:</b> Esta tabla proporciona una referencia rápida para entender cada tipo de objeción o situación registrada durante las llamadas, facilitando la interpretación de las gráficas anteriores.
</div>
""",
    unsafe_allow_html=True,
)
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
