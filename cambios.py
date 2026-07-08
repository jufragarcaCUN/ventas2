import streamlit as st

# 1. Inyección de estilos CSS y fuentes para maquetar la interfaz ejecutiva
st.markdown(
    """
    <!-- Importamos fuentes modernas de Google y FontAwesome para iconos -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
    /* Estilos globales de contenedores */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 2px;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        color: #64748B;
        margin-bottom: 20px;
    }

    /* Paneles de Contenido */
    .content-box {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    
    .box-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Badges y Alertas */
    .alert-banner {
        background: linear-gradient(90deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 5px solid #D97706;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .alert-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #92400E;
        margin-bottom: 6px;
    }

    /* Estilos de Pasos de Metodología */
    .step-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px;
        height: 100%;
        text-align: center;
        transition: transform 0.2s;
    }
    .step-card:hover {
        transform: translateY(-2px);
        border-color: #CBD5E1;
    }
    .step-num {
        font-family: 'Montserrat', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: #3B82F6;
        margin-bottom: 8px;
    }
    .step-title {
        font-weight: 600;
        font-size: 15px;
        color: #0F172A;
        margin-bottom: 6px;
    }

    /* Listas de Matrices */
    .list-item {
        padding: 8px 12px;
        border-bottom: 1px solid #F1F5F9;
        font-size: 14px;
    }
    .list-item:last-child {
        border-bottom: none;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado principal limpio sin menús laterales
st.markdown(
    '<p class="main-header">Reconstrucción del Análisis de Objeciones</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">Módulo de auditoría semántica y planificación de reentrenamiento técnico</p>',
    unsafe_allow_html=True,
)

# 2. SISTEMA DE PESTAÑAS HORIZONTALES (Sin barras laterales para integrarse al index)
tab_diag, tab_metodo, tab_matriz, tab_modelo = st.tabs(
    [
        "🔍 Diagnóstico Inicial",
        "🛠️ Metodología",
        "🗂️ Nueva Matriz Semántica",
        "📅 Plan de 2 Semanas",
    ]
)

# --- PESTAÑA 1: DIAGNÓSTICO INICIAL (SIN NÚMEROS) ---
with tab_diag:
    st.markdown(
        """
        <div class="content-box">
            <div class="box-title"><i class="fa-solid fa-triangle-exclamation" style="color: #EF4444;"></i> El Hallazgo Crítico</div>
            <p style="font-size: 15px; line-height: 1.6; color: #334155; margin-bottom: 12px;">
                Durante la auditoría del pipeline comercial anterior, identificamos un sesgo sistémico que afectaba directamente la toma de decisiones:
            </p>
            <div style="background-color: #FFF5F5; border-left: 4px solid #F87171; padding: 18px; border-radius: 6px; margin: 15px 0;">
                <strong style="color: #991B1B; font-size: 16px;">La anomalía del "60%":</strong> 
                Una sola categoría llamada <strong>"Tiempo/Flexibilidad"</strong> estaba absorbiendo y concentrando de manera artificial el 60% de todas las objeciones registradas de manera general.
            </div>
            <p style="font-size: 15px; line-height: 1.6; color: #334155;">
                Esta categoría se había convertido en un <strong>"cajón de sastre"</strong>. Al analizar en detalle, descubrimos que mezclaba objeciones reales de agenda con llamadas de desinterés explícito, buzones de voz automáticos, datos erróneos de formulario o simples trámites administrativos de estudiantes antiguos.
            </p>
            <p style="font-size: 15px; line-height: 1.6; color: #334155;">
                Al carecer de una frontera clara entre <strong>lo operativo y lo netamente comercial</strong>, era imposible medir de forma confiable el verdadero comportamiento del prospecto frente a la oferta académica.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- PESTAÑA 2: METODOLOGÍA DE RECONSTRUCCIÓN (CON ALERTA EN DIARIZACIÓN) ---
with tab_metodo:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="box-title"><i class="fa-solid fa-gears"></i> Proceso de Reestructuración Semántica</div>',
        unsafe_allow_html=True,
    )

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-num">01</div>
                <div class="step-title">Definir Categorías</div>
                <p style="font-size: 13px; color: #475569;">Revisión manual de bloques de 500 llamadas para mapear motivos reales y depurar falsos positivos.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col_s2:
        # Se agrega la advertencia visual clara de "Pendiente de mejora técnica"
        st.markdown(
            """
            <div class="step-card" style="border: 1px dashed #F59E0B; background-color: #FFFBEB;">
                <div class="step-num" style="color: #D97706;">02</div>
                <div class="step-title">Diarizar Llamada</div>
                <p style="font-size: 13px; color: #475569;">Separación de audio por interlocutor para procesar solo el discurso del estudiante.</p>
                <span style="font-size: 11px; background-color: #FEF3C7; color: #B45309; padding: 3px 8px; border-radius: 4px; font-weight: 700; display: inline-block; margin-top: 6px;">⚠️ Pendiente por mejorar</span>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col_s3:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-num">03</div>
                <div class="step-title">Modelo Semántico</div>
                <p style="font-size: 13px; color: #475569;">Implementación de Transformer NLP que analiza el significado conceptual y no solo palabras clave.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col_s4:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-num">04</div>
                <div class="step-title">Optimizar en AWS</div>
                <p style="font-size: 13px; color: #475569;">Despliegue automático en la nube descartando audios sin valor evaluable comercial.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# --- PESTAÑA 3: NUEVA MATRIZ SEMÁNTICA ---
with tab_matriz:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="box-title"><i class="fa-solid fa-folder-open"></i> Nueva Matriz de Clasificación</div>',
        unsafe_allow_html=True,
    )

    col_reales, col_operativas = st.columns(2)

    with col_reales:
        st.markdown(
            """
            <div style="background-color: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 4px solid #EF4444; margin-bottom: 10px;">
                <strong style="color: #991B1B; font-size: 15px;"><i class="fa-solid fa-circle-xmark"></i> OBJECIONES REALES DE VENTA (5)</strong>
            </div>
            <div class="list-item"><strong>💼 Competencia:</strong> Prospecto ya matriculado en otra entidad o comparando ofertas activamente.</div>
            <div class="list-item"><strong>💵 Económica:</strong> Objeción explícita por falta de presupuesto, costos altos o problemas financieros.</div>
            <div class="list-item"><strong>👎 No Interesado/a:</strong> Manifiesta desinterés directo en los programas académicos ofrecidos.</div>
            <div class="list-item"><strong>👥 Terceros / Familia:</strong> La decisión de compra final depende de padres, pareja, jefe, etc.</div>
            <div class="list-item"><strong>⏳ Tiempo / Flexibilidad:</strong> Incompatibilidad de horarios de trabajo/estudio confirmados.</div>
        """,
            unsafe_allow_html=True,
        )

    with col_operativas:
        st.markdown(
            """
            <div style="background-color: #ECFDF5; padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 10px;">
                <strong style="color: #065F46; font-size: 15px;"><i class="fa-solid fa-circle-check"></i> CASOS OPERATIVOS / NO OBJECIÓN (7)</strong>
            </div>
            <div class="list-item"><strong>📟 Buzón de voz:</strong> Contestador automático. Sin contacto humano real.</div>
            <div class="list-item"><strong>❌ Datos erróneos:</strong> Número equivocado o formularios falsificados.</div>
            <div class="list-item"><strong>✅ Ninguna:</strong> Conversación comercial fluida que finaliza de forma correcta sin incidentes.</div>
            <div class="list-item"><strong>⌛ Sin tiempo:</strong> El prospecto solicita reagendar de inmediato por falta de tiempo para atender.</div>
            <div class="list-item"><strong>🚗 Horario incómodo:</strong> En curso de actividad personal (manejando, almorzando, etc.).</div>
            <div class="list-item"><strong>🏢 Trabajo ocupado:</strong> Laborando activamente o en reunión empresarial.</div>
            <div class="list-item"><strong>📄 Trámite / Reintegro:</strong> Estudiantes antiguos solicitando procesos administrativos.</div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# --- PESTAÑA 4: CRONOGRAMA DE ACTUALIZACIÓN DEL MODELO ---
with tab_modelo:
    # Aviso ejecutivo destacado sobre las 2 semanas requeridas
    st.markdown(
        """
        <div class="alert-banner">
            <div class="alert-title"><i class="fa-solid fa-circle-info"></i> Requerimiento Crítico de Procesamiento</div>
            <p style="margin: 0; font-size: 14px; color: #78350F; line-height: 1.5;">
                Para asimilar el volumen masivo acumulado, depurar el ruido comercial y ejecutar el reentrenamiento optimizado del modelo semántico utilizando <strong>la data acumulada de todo el año</strong>, el equipo requiere exactamente de una ventana de desarrollo de <strong>dos (2) semanas</strong> de actualización técnica en staging antes de producción.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="box-title"><i class="fa-solid fa-calendar-week"></i> Planificación Técnica (Bloque Dedicado)</div>',
        unsafe_allow_html=True,
    )

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown(
            """
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 18px; border-radius: 8px;">
                <strong style="color: #1E3A8A; font-size: 15px;"><i class="fa-solid fa-clock-rotate-left"></i> SEMANA 1: Data Pipeline</strong>
                <ul style="font-size: 13.5px; color: #475569; margin-top: 10px; padding-left: 20px; line-height: 1.6;">
                    <li>Ingesta masiva y ETL del consolidado histórico anual de audios.</li>
                    <li>Balanceo de etiquetas minoritarias y depuración de registros duplicados.</li>
                    <li>Construcción de los nuevos datasets balanceados de prueba y validación.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_w2:
        st.markdown(
            """
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 18px; border-radius: 8px;">
                <strong style="color: #1E3A8A; font-size: 15px;"><i class="fa-solid fa-rocket"></i> SEMANA 2: Calibración & QA</strong>
                <ul style="font-size: 13.5px; color: #475569; margin-top: 10px; padding-left: 20px; line-height: 1.6;">
                    <li>Reentrenamiento algorítmico del modelo Transformer y optimización de hiperparámetros.</li>
                    <li>Evaluación en staging de métricas de precisión frente al modelo base de producción.</li>
                    <li>Despliegue automático a producción sin interrupción del servicio comercial.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
