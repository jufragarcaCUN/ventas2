import streamlit as st

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
    .videos-app {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 2px;
    }
    .header-sub {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 25px;
    }
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
        margin-bottom: 20px;
    }
    .section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .premium-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 5px;
        font-size: 13.5px;
    }
    .premium-table th {
        background-color: #F8FAFC;
        color: #475569;
        font-weight: 700;
        text-align: left;
        padding: 10px 14px;
        border-bottom: 2px solid #E2E8F0;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.05em;
    }
    .premium-table td {
        padding: 12px 14px;
        border-bottom: 1px solid #F1F5F9;
        color: #334155;
        line-height: 1.4;
    }
    .premium-table tr:last-child td {
        border-bottom: none;
    }
    .premium-table tr:hover td {
        background-color: #F8FAFC;
    }
    .highlight-red {
        color: #EF4444;
        font-weight: 700;
    }
    .highlight-blue {
        color: #2563EB;
        font-weight: 700;
    }
    .conclusion-banner {
        background: linear-gradient(135deg, #FFFDF5 0%, #FEF3C7 100%);
        border-left: 5px solid #D97706;
        padding: 20px;
        border-radius: 10px;
        margin-top: 5px;
        border: 1px solid rgba(217, 119, 6, 0.15);
    }
    .conclusion-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 14.5px;
        font-weight: 700;
        color: #92400E;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .conclusion-text {
        font-size: 13.5px;
        color: #78350F;
        line-height: 1.5;
        margin: 0;
    }
    .spec-badge {
        font-size: 12px;
        background-color: #F1F5F9;
        color: #334155;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="videos-app">', unsafe_allow_html=True)

st.markdown(
    '<p class="header-title">Métricas de Rendimiento e Infraestructura AWS</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="header-sub">Análisis de ingesta de archivos y procesamiento de red neuronal en la arquitectura actual</p>',
    unsafe_allow_html=True,
)

col_izq, col_der = st.columns(2)

with col_izq:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">
                <i class="fa-solid fa-server" style="color: #2563EB;"></i> 
                1. Infraestructura Actual en AWS
            </div>
            <table class="premium-table">
                <thead>
                    <tr>
                        <th style="width: 40%;">Recurso</th>
                        <th style="width: 60%;">Capacidad / Detalle</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Instancia AWS</b></td>
                        <td><span class="highlight-blue">ml.t3.large</span></td>
                    </tr>
                    <tr>
                        <td><b>Procesador (vCPUs)</b></td>
                        <td>2 vCPUs (Intel Xeon o AMD EPYC según zona)</td>
                    </tr>
                    <tr>
                        <td><b>Memoria RAM</b></td>
                        <td>8 GiB</td>
                    </tr>
                    <tr>
                        <td><b>Aceleradora (GPU)</b></td>
                        <td><span class="highlight-red">No tiene</span> (Basado puramente en CPU)</td>
                    </tr>
                    <tr>
                        <td><b>Red (Rendimiento)</b></td>
                        <td>Hasta 5 Gbps</td>
                    </tr>
                    <tr>
                        <td><b>Almacenamiento</b></td>
                        <td>Basado en EBS (Amazon Elastic Block Store)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">
                <i class="fa-solid fa-cloud-arrow-up" style="color: #10B981;"></i> 
                2. Tiempos de Ingesta (Drive ➡️ S3)
            </div>
            <table class="premium-table">
                <thead>
                    <tr>
                        <th style="width: 60%;">Métrica</th>
                        <th style="width: 40%;">Valor de la Prueba</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Volumen de videos migrados</b></td>
                        <td>500 videos de docentes</td>
                    </tr>
                    <tr>
                        <td><b>Tiempo total de transferencia</b></td>
                        <td>6 horas</td>
                    </tr>
                    <tr>
                        <td><b>Tiempo promedio por video</b></td>
                        <td><span class="highlight-blue">0.72 minutos</span> (~43 segundos)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_der:
    st.markdown(
        """
        <div class="section-card" style="border: 1px solid #FCA5A5;">
            <div class="section-title" style="color: #DC2626;">
                <i class="fa-solid fa-microchip" style="color: #EF4444;"></i> 
                3. Tiempos de Procesamiento (Red Neuronal)
            </div>
            <table class="premium-table">
                <thead>
                    <tr>
                        <th style="width: 60%;">Métrica</th>
                        <th style="width: 40%;">Valor Obtenido / Proyección</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Lote de prueba ejecutado</b></td>
                        <td>15 videos</td>
                    </tr>
                    <tr>
                        <td><b>Tiempo total de ejecución</b></td>
                        <td>3 horas y 50 minutos</td>
                    </tr>
                    <tr>
                        <td><b>Tiempo de procesamiento por video</b></td>
                        <td><span class="highlight-red">15 minutos</span></td>
                    </tr>
                    <tr style="background-color: #FFF5F5;">
                        <td><b>Proyección lote diario (300 videos)</b></td>
                        <td><span class="highlight-red">75 horas</span> (3.1 días continuos)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="conclusion-banner">
            <div class="conclusion-title">
                <i class="fa-solid fa-lightbulb"></i> Conclusión del Equipo Técnico
            </div>
            <p class="conclusion-text">
                El cuello de botella <b>no se encuentra en la migración</b> (la cual es sumamente eficiente y toma menos de un minuto por video), sino directamente en el <b>procesamiento de la red neuronal</b>. Esto se debe a que la instancia actual (<code>ml.t3.large</code>) carece de una tarjeta gráfica dedicada (GPU).
            </p>
            <p class="conclusion-text" style="margin-top: 8px; font-weight: 600;">
                💡 Recomendación: Para garantizar tiempos de entrega viables comercialmente, es indispensable evaluar y migrar a una instancia AWS que cuente con aceleración por GPU.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
