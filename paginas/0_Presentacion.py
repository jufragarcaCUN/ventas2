import streamlit as st
import pandas as pd

# ==================== CONFIGURACIÓN ====================
st.set_page_config(page_title="Modelo Comercial CUN", page_icon="📋", layout="wide")

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

# ==================== TÍTULO ====================
st.title("📋 Modelo Comercial CUN")
st.markdown("### Clasificación de Objeciones y Pilares del Speech")
st.markdown("---")

# ==================== 1. RADIOGRAFÍA OPERATIVA ====================
st.markdown("## 1. Radiografía Operativa")
st.markdown("**Propósito:** ¿Cómo está el equipo comercial en general?")

st.markdown("### Gráficos:")

st.markdown("**Gráfico 1: Distribución de Objeciones (Barras horizontales)**")
st.markdown("- **Pregunta:** ¿Cuáles son las objeciones más frecuentes?")
st.markdown(
    "- **Por qué:** Identificar el principal obstáculo comercial para priorizar entrenamiento."
)
st.markdown(
    "- **Cómo:** Toma la columna `Objecion_Detectada`, cuenta frecuencias, ordena de mayor a menor y grafica barras horizontales."
)
st.markdown(
    "- **Ejemplo:** Económica 45% | Competencia 25% | No interesado 15% | Tiempo 10% | Terceros 5%"
)
st.markdown(
    "- **Decisión:** Si 'Económica' es la principal → entrenar en manejo de objeciones de precio."
)

st.markdown("**Gráfico 2: Distribución de No Objeciones (Barras horizontales)**")
st.markdown("- **Pregunta:** ¿Cuáles son las no objeciones más frecuentes?")
st.markdown(
    "- **Por qué:** Identificar problemas operativos de contacto (teléfonos, horarios)."
)
st.markdown(
    "- **Cómo:** Filtra solo los registros clasificados como 'No Objeción', cuenta frecuencias y grafica barras."
)
st.markdown(
    "- **Ejemplo:** Sin Tiempo Atender 30% | Buzón de Voz 25% | Tiempo Trabajo Ocupado 20%"
)
st.markdown(
    "- **Decisión:** Si 'Buzón de Voz' es alto → revisar calidad de los datos de contacto."
)

st.markdown("**Gráfico 3: Radar de los 7 Pilares del Speech**")
st.markdown("- **Pregunta:** ¿En qué pilares del speech estamos débiles?")
st.markdown(
    "- **Por qué:** Identificar qué parte del discurso comercial necesita refuerzo."
)
st.markdown(
    "- **Cómo:** Calcula el promedio de calificación de cada pilar (P1 a P7) y los dibuja en un radar."
)
st.markdown(
    "- **Ejemplo:** P1 70% | P2 65% | P3 55% | P4 60% | P5 40% | P6 35% | P7 50%"
)
st.markdown(
    "- **Decisión:** Si 'Precio' y 'Regalos' son los más bajos → entrenar en manejo de objeciones de precio y uso de incentivos."
)

st.markdown("### Filtros:")
st.markdown("- 📍 **Ciudad:** Ver desempeño por región geográfica")
st.markdown("- 🎓 **Programa:** Ver desempeño por programa académico")
st.markdown("- 📚 **Modalidad:** Ver diferencias entre PRESENCIAL y VIRTUAL")
st.markdown("- 📅 **Período:** Ver evolución en el tiempo")
st.markdown("- 📋 **Tipo Registro:** Filtrar por tipo de registro")

st.markdown(
    "**Ejemplo estratégico:** Filtrar por 'Bogotá' + 'Modalidad Virtual' para ver si el problema de precio es solo en esa combinación."
)
st.markdown("---")

# ==================== 2. DIAGNÓSTICO COMERCIAL ====================
st.markdown("## 2. Diagnóstico Comercial")
st.markdown("**Propósito:** ¿Por qué está pasando y cómo solucionarlo?")

st.markdown("### Gráficos:")

st.markdown("**Gráfico 1: Distribución de Objeciones (Barras)**")
st.markdown("- **Pregunta:** ¿Cuáles son las objeciones más frecuentes?")
st.markdown("- **Por qué:** Igual que en 01, pero con más detalle.")
st.markdown("- **Cómo:** Misma lógica que 01.")

st.markdown("**Gráfico 2: Distribución de No Objeciones (Barras)**")
st.markdown("- **Pregunta:** ¿Cuáles son las no objeciones más frecuentes?")
st.markdown("- **Por qué:** Igual que en 01.")
st.markdown("- **Cómo:** Misma lógica que 01.")

st.markdown("**Gráfico 3: Radar del Speech para Objeción Seleccionada**")
st.markdown("- **Pregunta:** ¿Qué pilar del speech falla cuando aparece esta objeción?")
st.markdown(
    "- **Por qué:** Identificar la causa raíz de cada objeción para entrenar específicamente."
)
st.markdown(
    "- **Cómo:** Filtra los registros que tienen la objeción seleccionada, calcula el promedio de cada pilar SOLO para esos registros y lo dibuja en un radar."
)
st.markdown(
    "- **Ejemplo:** Selecciono 'Económica' y veo que P6 (Precio) está en 20% → los asesores no manejan bien la objeción de precio."
)
st.markdown(
    "- **Decisión:** Entrenar a los asesores en cómo presentar opciones de pago, financiación y descuentos."
)

st.markdown("**Gráfico 4: Heatmap de Calificaciones**")
st.markdown("- **Pregunta:** ¿Cómo se correlacionan los pilares?")
st.markdown(
    "- **Por qué:** Identificar patrones: si un pilar es bajo, ¿cuáles más están bajos?"
)
st.markdown(
    "- **Cómo:** Crea una matriz con los promedios de cada pilar, usa colores para mostrar fortalezas (verde) y debilidades (rojo)."
)
st.markdown(
    "- **Ejemplo:** P1 70% 🟢 | P2 65% 🟢 | P3 55% 🟡 | P4 60% 🟢 | P5 40% 🔴 | P6 35% 🔴 | P7 50% 🟡"
)
st.markdown(
    "- **Decisión:** Si P5 y P6 son rojos → el problema está en 'Regalos' y 'Precio'. Entrenar en esas dos áreas."
)

st.markdown("**Gráfico 5: Comparador de Objeciones (Radar múltiple)**")
st.markdown("- **Pregunta:** ¿Qué objeciones tienen perfiles similares?")
st.markdown(
    "- **Por qué:** Agrupar objeciones con causas comunes para entrenamientos conjuntos."
)
st.markdown(
    "- **Cómo:** Dibuja varios radares superpuestos, uno por cada objeción seleccionada."
)
st.markdown(
    "- **Ejemplo:** Selecciono 'Económica' y 'Competencia'. Ambas tienen P6 (Precio) bajo → el problema de precio aparece en ambas objeciones."
)
st.markdown(
    "- **Decisión:** Entrenar a los asesores en manejo de precio, que servirá para ambas objeciones."
)

st.markdown("### Filtros:")
st.markdown("- 📍 **Ciudad:** Ver por región")
st.markdown("- 🎓 **Programa:** Ver por programa")
st.markdown("- 📚 **Modalidad:** Ver diferencias PRESENCIAL/VIRTUAL")
st.markdown("- 📅 **Período:** Ver evolución temporal")
st.markdown("- 📋 **Tipo Registro:** Filtrar por tipo")

st.markdown("### Selector adicional:")
st.markdown(
    "- 🎯 **Selecciona una objeción:** Analizar una objeción específica y ver qué pilar falla"
)
st.markdown("---")

# ==================== 3. PAGO VS NO PAGO ====================
st.markdown("## 3. Pago vs No Pago")
st.markdown("**Propósito:** ¿Qué diferencia a los que pagan de los que no?")

st.markdown("### Gráficos:")

st.markdown("**Gráfico 1: Distribución de Objeciones**")
st.markdown("- **Pregunta:** ¿Qué objeciones tienen los que pagan vs los que no pagan?")
st.markdown(
    "- **Por qué:** Identificar qué objeciones son más letales para la conversión."
)
st.markdown(
    "- **Cómo:** Separa los datos en dos grupos (PAGO y NO PAGO), cuenta objeciones en cada grupo y las compara."
)
st.markdown("- **Ejemplo:** NO PAGO: Económica 50% | PAGO: Económica 10%")
st.markdown(
    "- **Decisión:** Si 'Económica' es mucho más alta en NO PAGO → el manejo de precio es crítico para la conversión."
)

st.markdown("**Gráfico 2: Distribución de No Objeciones**")
st.markdown(
    "- **Pregunta:** ¿Qué no objeciones tienen los que pagan vs los que no pagan?"
)
st.markdown(
    "- **Por qué:** Identificar problemas de contacto que afectan la conversión."
)
st.markdown(
    "- **Cómo:** Separa los datos en PAGO y NO PAGO, cuenta no objeciones en cada grupo y las compara."
)
st.markdown(
    "- **Ejemplo:** NO PAGO: Sin Tiempo Atender 40% | PAGO: Sin Tiempo Atender 10%"
)
st.markdown(
    "- **Decisión:** Si 'Sin Tiempo Atender' es alto en NO PAGO → mejorar el seguimiento y agendamiento de llamadas."
)

st.markdown("**Gráfico 3: Radar Comparativo Pago vs No Pago**")
st.markdown("- **Pregunta:** ¿En qué pilares del speech se diferencian PAGO y NO PAGO?")
st.markdown(
    "- **Por qué:** Identificar qué parte del speech impacta más la conversión."
)
st.markdown(
    "- **Cómo:** Calcula el promedio de cada pilar para PAGO y para NO PAGO, dibuja dos radares superpuestos."
)
st.markdown("- **Ejemplo:** PAGO: P6 75% | NO PAGO: P6 35% | Diferencia: 40%")
st.markdown(
    "- **Decisión:** Si la mayor diferencia está en P6 (Precio) → entrenar en manejo de precio es la prioridad #1 para aumentar conversión."
)

st.markdown("**Gráfico 4: Heatmap de Calificaciones**")
st.markdown("- **Pregunta:** ¿Cómo se correlacionan los pilares con el pago?")
st.markdown("- **Por qué:** Identificar qué combinación de pilares predice el pago.")
st.markdown("- **Cómo:** Misma lógica que 02, pero separando PAGO y NO PAGO.")

st.markdown("### Filtros:")
st.markdown("- 📍 **Ciudad:** Ver por región")
st.markdown("- 🎓 **Programa:** Ver por programa")
st.markdown("- 📚 **Modalidad:** Ver diferencias PRESENCIAL/VIRTUAL")
st.markdown("- 📅 **Período:** Ver evolución temporal")

st.markdown("### Selector adicional:")
st.markdown("- 👥 **Población:** Ver solo PAGO, solo NO PAGO o TODOS")
st.markdown("---")

# ==================== TABLA: OBJECIONES ====================
st.markdown("## 📊 Tabla de Clasificación de Objeciones")

st.markdown("### ✅ OBJECIONES (Barreras reales)")

data_obj = {
    "Categoría": [
        "Competencia",
        "Económica",
        "No interesado",
        "Terceros Familia",
        "Tiempo flexibilidad",
    ],
    "Tipo": ["✅ Objeción"] * 5,
    "Significado": [
        "Ya se matriculó en otra institución o está comparando opciones.",
        "Falta de dinero, costo elevado o problemas financieros.",
        "No le interesa la oferta académica.",
        "Depende de la decisión de terceros (padres, esposo, jefe).",
        "No tiene tiempo o el horario no le es compatible.",
    ],
    "Qué hacer": [
        "Reforzar diferenciación y beneficios exclusivos de la CUN.",
        "Mejorar manejo de opciones de pago, financiación y descuentos.",
        "Trabajar en la apertura de la llamada y captación de interés.",
        "Enseñar técnicas para manejar decisiones con terceros.",
        "Reforzar la flexibilidad y modalidades del programa.",
    ],
}
st.dataframe(pd.DataFrame(data_obj), use_container_width=True, hide_index=True)

st.markdown("### 🔄 NO OBJECIONES (Situacionales / Temporales)")

data_no_obj = {
    "Categoría": [
        "Buzón De Voz",
        "Datos Erróneos No Registro",
        "Ninguna",
        "Sin Tiempo Atender",
        "Tiempo Horario Incómodo",
        "Tiempo Trabajo Ocupado",
        "Trámite Reintegro",
    ],
    "Tipo": ["🔄 No objeción"] * 7,
    "Significado": [
        "Contestador automático, sin contacto humano.",
        "Número equivocado, datos falsos o no registrado.",
        "No se detectó objeción en la llamada.",
        "Está ocupado ahora y pide llamar después.",
        "Está en medio de una actividad personal.",
        "Está trabajando o en reunión ahora.",
        "Es estudiante actual o antiguo con trámites administrativos.",
    ],
    "Qué hacer": [
        "Verificar calidad de datos y mejorar estrategia de contacto.",
        "Depurar base de datos y validar información.",
        "Seguir con el proceso de cierre.",
        "Agendar follow-up y mejorar timing de llamadas.",
        "Llamar en horarios más estratégicos.",
        "Agendar llamada en horario laboral adecuado.",
        "Derivar a área de trámites o seguimiento especializado.",
    ],
}
st.dataframe(pd.DataFrame(data_no_obj), use_container_width=True, hide_index=True)

st.markdown("---")

# ==================== TABLA: PILARES DEL SPEECH ====================
st.markdown("## 🧬 Los 7 Pilares del Speech Comercial")

data_pilares = {
    "Pilar": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],
    "Nombre": [
        "Promesa",
        "Beneficio",
        "Entregables",
        "Garantía",
        "Regalos",
        "Precio",
        "Cierre",
    ],
    "¿Qué mide?": [
        "¿El asesor logra captar la atención con una promesa de valor clara?",
        "¿Explica claramente los beneficios de estudiar en la CUN?",
        "¿Presenta los entregables del programa (certificados, títulos, etc.)?",
        "¿Transmite confianza y respaldo institucional?",
        "¿Utiliza incentivos o beneficios adicionales?",
        "¿Maneja correctamente la objeción de precio y presenta opciones de pago?",
        "¿Logra cerrar la venta o agendar un paso siguiente?",
    ],
    "Si es bajo (0-40%)": [
        "El asesor no logra enganchar al prospecto en los primeros segundos.",
        "El prospecto no entiende qué gana estudiando en la CUN.",
        "El prospecto no sabe qué obtiene al finalizar el programa.",
        "El prospecto duda de la calidad o seriedad de la CUN.",
        "El asesor no usa ningún incentivo para motivar la decisión.",
        "El asesor no sabe manejar la objeción de precio.",
        "El asesor no logra avanzar en el proceso de venta.",
    ],
    "Si es alto (80-100%)": [
        "El asesor capta atención inmediata y genera interés.",
        "El prospecto ve claramente el valor de estudiar en la CUN.",
        "El prospecto conoce claramente los certificados y títulos.",
        "El prospecto confía en la institución.",
        "El asesor usa descuentos, becas o bonos para cerrar.",
        "El asesor presenta opciones de pago y financiación.",
        "El asesor cierra la venta o agenda el siguiente paso.",
    ],
}
st.dataframe(pd.DataFrame(data_pilares), use_container_width=True, hide_index=True)

st.markdown("---")

# ==================== EJEMPLO PRÁCTICO ====================
st.markdown("## 📋 Ejemplo Práctico de Uso")
st.markdown(
    """
**Paso 1:** Abro **01_Radiografia** y veo que "Económica" es la objeción más frecuente (45%).

**Paso 2:** Abro **02_Diagnostico**, selecciono "Económica" y veo que P6 (Precio) está en 20%.

**Paso 3:** Abro **03_Pago_vs_NoPago** y veo que en NO PAGO, P6 está en 20%, pero en PAGO está en 75%.

**Conclusión:** El problema principal es el manejo de precio. Los asesores no están presentando bien las opciones de pago, y eso está matando la conversión.

**Decisión:** Entrenar a todo el equipo en manejo de objeciones de precio, presentación de financiación y opciones de pago.
"""
)

st.markdown("---")

# ==================== FOOTER ====================
st.caption("📋 Modelo Comercial CUN | Clasificación de Objeciones y Pilares del Speech")
