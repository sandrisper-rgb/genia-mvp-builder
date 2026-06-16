import streamlit as st
from datetime import datetime
from io import BytesIO
import base64
import os

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="GeniA Innovation Builder",
    page_icon="🧠",
    layout="wide"
)


# =========================
# FUNCIONES VISUALES
# =========================
def image_to_base64(image_file):
    with open(image_file, "rb") as image:
        return base64.b64encode(image.read()).decode()


def add_background(image_file):
    encoded = image_to_base64(image_file)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(255,255,255,0.08), rgba(255,255,255,0.16)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background: linear-gradient(
                135deg,
                rgba(6, 42, 72, 0.58),
                rgba(14, 98, 130, 0.48),
                rgba(240, 90, 40, 0.22)
            );
            border-radius: 28px;
            padding: 2rem 2.2rem 3rem 2.2rem;
            box-shadow: 0 12px 36px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.25);
        }}

        [data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.95);
        }}

        .genia-header {{
            display: flex;
            align-items: center;
            gap: 24px;
            padding: 20px 26px;
            border-radius: 26px;
            background: linear-gradient(
                135deg,
                rgba(255,255,255,0.58),
                rgba(232,246,250,0.42)
            );
            backdrop-filter: blur(7px);
            border: 1px solid rgba(11,46,74,0.18);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            margin-bottom: 18px;
        }}

        .genia-logo-img {{
            width: 210px;
            max-width: 28vw;
            height: auto;
            object-fit: contain;
        }}

        .genia-title {{
            font-size: 40px;
            line-height: 1.05;
            font-weight: 850;
            color: #0B2E4A;
            margin: 0;
        }}

        .genia-subtitle {{
            font-size: 20px;
            color: #F05A28;
            font-weight: 750;
            margin-top: 6px;
        }}

        .genia-caption {{
            font-size: 14px;
            color: #5B667A;
            margin-top: 4px;
        }}

        .block-container h1,
        .block-container h2,
        .block-container h3,
        .block-container p,
        .block-container label,
        .block-container span {{
            color: #ffffff !important;
        }}

        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stMultiSelect label,
        .stSlider label,
        .stNumberInput label {{
            color: #ffffff !important;
            font-weight: 650;
        }}

        input, textarea {{
            background-color: rgba(255,255,255,0.68) !important;
            color: #0B2E4A !important;
        }}

        div[data-baseweb="select"] > div {{
            background-color: rgba(255,255,255,0.68) !important;
            color: #0B2E4A !important;
            border: 1px solid rgba(255,255,255,0.45) !important;
            backdrop-filter: blur(4px);
        }}

        [data-testid="stExpander"] {{
            background: rgba(255,255,255,0.56);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.45);
        }}

        [data-testid="stExpander"] p,
        [data-testid="stExpander"] div,
        [data-testid="stExpander"] span {{
            color: #0B2E4A !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            color: #ffffff !important;
            font-weight: 650;
        }}

        .stTabs [aria-selected="true"] {{
            color: #F05A28 !important;
            background: rgba(255,255,255,0.62);
            border-radius: 10px 10px 0 0;
        }}

        div[data-testid="stMetricValue"] {{
            font-size: 30px;
            color: #ffffff !important;
        }}

        div[data-testid="stMetricLabel"] {{
            color: #ffffff !important;
        }}

        .maturity-card {{
            padding: 20px 22px;
            border-radius: 22px;
            border: 2px solid rgba(0,0,0,0.08);
            background: rgba(255,255,255,0.62);
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
            margin: 12px 0 18px 0;
        }}

        .maturity-title {{
            font-size: 26px;
            font-weight: 850;
            margin-bottom: 6px;
        }}

        .maturity-text {{
            font-size: 17px;
            line-height: 1.45;
            color: #0B2E4A !important;
        }}

        .result-box {{
            background: rgba(255,255,255,0.62);
            border-radius: 18px;
            padding: 18px;
            border: 1px solid rgba(255,255,255,0.55);
            margin-top: 12px;
        }}

        .result-box p,
        .result-box li,
        .result-box h1,
        .result-box h2,
        .result-box h3,
        .result-box span,
        .result-box div {{
            color: #0B2E4A !important;
        }}
        /* Botones de descarga y botones generales */
.stDownloadButton button,
.stButton button {
    background-color: rgba(255,255,255,0.92) !important;
    color: #0B2E4A !important;
    border: 1px solid rgba(11,46,74,0.25) !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
}

.stDownloadButton button p,
.stDownloadButton button span,
.stButton button p,
.stButton button span {
    color: #0B2E4A !important;
}

.stDownloadButton button:hover,
.stButton button:hover {
    background-color: #F05A28 !important;
    color: #ffffff !important;
}

.stDownloadButton button:hover p,
.stDownloadButton button:hover span,
.stButton button:hover p,
.stButton button:hover span {
    color: #ffffff !important;
}

</style>
        </style>
        """,
        unsafe_allow_html=True
    )


if os.path.exists("fondo_bootcamp.png"):
    add_background("fondo_bootcamp.png")
else:
    st.warning("No se encontró `fondo_bootcamp.png`. La app funcionará sin fondo.")


# =========================
# HEADER CON LOGO GENIA
# =========================
if os.path.exists("logo_genia.png"):
    logo_b64 = image_to_base64("logo_genia.png")
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="genia-logo-img">'
else:
    logo_html = '<div style="font-size:48px;">🧠</div>'

st.markdown(
    f"""
    <div class="genia-header">
        <div>{logo_html}</div>
        <div>
            <div class="genia-title">Innovation Builder</div>
            <div class="genia-subtitle">Del reto clínico al MVP de IA en salud</div>
            <div class="genia-caption">Programa de Inteligencia Artificial — Los Cobos Medical Center</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("¿Qué es un MVP en salud?", expanded=True):
    st.markdown("""
    Un **MVP en salud** es la versión más simple, segura y medible de una solución de IA que permite probar
    si realmente genera valor clínico antes de invertir en un desarrollo completo.

    **Debe ser:** específico, seguro, medible, supervisado y escalable.  
    **No debe ser:** una app completa, una IA autónoma ni un reemplazo del médico.
    """)

st.divider()


# =========================
# ESTADO
# =========================
if "data" not in st.session_state:
    st.session_state.data = {}

def save(key, value):
    st.session_state.data[key] = value


# =========================
# FORMULARIO
# =========================
tabs = st.tabs([
    "1. Problema",
    "2. Usuario y flujo",
    "3. Datos e IA",
    "4. MVP",
    "5. Riesgos",
    "6. KPIs",
    "7. Piloto",
    "8. Escalamiento",
    "9. Resultado"
])

with tabs[0]:
    st.header("1. Definir el problema clínico")
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre del proyecto / equipo", value=st.session_state.data.get("nombre", ""))
        area = st.selectbox("Área clínica principal", [
            "Urgencias", "Radiología", "Patología", "Oncología", "Consulta externa",
            "Hospitalización", "Laboratorio clínico", "Gestión administrativa", "Otra"
        ])
        tipo_problema = st.selectbox("Tipo de problema", [
            "Diagnóstico", "Pronóstico", "Triage / priorización", "Seguimiento",
            "Gestión del flujo de pacientes", "Resumen de historia clínica", "Educación", "Otro"
        ])

    with col2:
        problema = st.text_area(
            "Problema clínico específico",
            placeholder="Ejemplo: Los médicos tardan demasiado en identificar pacientes con riesgo de deterioro clínico en urgencias.",
            height=130
        )
        consecuencia = st.text_area(
            "¿Qué pasa si este problema no se resuelve?",
            placeholder="Ejemplo: retrasos en la atención, mayor riesgo de eventos adversos, saturación del servicio.",
            height=100
        )

    save("nombre", nombre)
    save("area", area)
    save("tipo_problema", tipo_problema)
    save("problema", problema)
    save("consecuencia", consecuencia)

with tabs[1]:
    st.header("2. Usuario y flujo clínico")
    usuario = st.selectbox("Usuario principal", [
        "Médico general", "Especialista", "Enfermería", "Paciente", "Administrativo",
        "Radiólogo", "Patólogo", "Gestor clínico", "Otro"
    ])
    momento = st.selectbox("Momento del flujo clínico donde se usaría", [
        "Antes de la consulta", "Durante la consulta", "Después de la consulta",
        "Ingreso a urgencias", "Lectura de imágenes", "Junta médica",
        "Seguimiento ambulatorio", "Otro"
    ])
    flujo_actual = st.text_area(
        "Flujo actual sin IA",
        placeholder="Paciente → datos → médico revisa manualmente → decisión",
        height=100
    )
    flujo_mvp = st.text_area(
        "Flujo propuesto con MVP",
        placeholder="Paciente → datos → MVP alerta/resume/prioriza → médico decide",
        height=100
    )
    save("usuario", usuario)
    save("momento", momento)
    save("flujo_actual", flujo_actual)
    save("flujo_mvp", flujo_mvp)

with tabs[2]:
    st.header("3. Datos e IA")
    datos = st.multiselect("Datos necesarios", [
        "Historia clínica", "Notas médicas", "Signos vitales", "Laboratorio",
        "Imágenes médicas", "Citología / patología digital", "Medicamentos",
        "Encuestas", "Datos administrativos", "Otro"
    ])
    tecnica = st.multiselect("Técnica probable de IA", [
        "Machine Learning clásico", "Deep Learning", "Computer Vision", "NLP",
        "IA generativa", "Reglas clínicas + IA", "No definido aún"
    ])
    fuente = st.text_area(
        "Fuente de los datos",
        placeholder="Ejemplo: HIS, PACS, LIS, registros retrospectivos, formularios de captura.",
        height=80
    )
    calidad = st.slider("Calidad percibida de los datos", 1, 5, 3)
    save("datos", datos)
    save("tecnica", tecnica)
    save("fuente", fuente)
    save("calidad", calidad)

with tabs[3]:
    st.header("4. Definir el MVP")
    st.info("Regla: eliminen el 80% de las funcionalidades. El MVP debe hacer una sola cosa muy bien.")
    funcion = st.text_area("Función mínima del MVP", placeholder="Mi MVP hará solamente...", height=100)
    no_hara = st.text_area(
        "¿Qué NO hará el MVP?",
        placeholder="Ejemplo: no diagnosticará, no formulará tratamiento, no reemplazará criterio médico.",
        height=100
    )
    salida = st.selectbox("Salida principal del MVP", [
        "Alerta", "Resumen", "Priorización", "Clasificación de riesgo",
        "Recomendación supervisada", "Reporte", "Tablero de control", "Otro"
    ])
    valor = st.text_area(
        "Valor clínico esperado",
        placeholder="Ejemplo: disminuir tiempo de lectura, mejorar priorización, reducir omisiones.",
        height=80
    )
    save("funcion", funcion)
    save("no_hara", no_hara)
    save("salida", salida)
    save("valor", valor)

with tabs[4]:
    st.header("5. Riesgos y mitigación")
    riesgo = st.selectbox("Riesgo principal", [
        "Falso negativo", "Falso positivo", "Sesgo poblacional", "Sobreconfianza del usuario",
        "Datos incompletos", "Privacidad", "Falla de integración", "Otro"
    ])
    peor = st.text_area(
        "Peor escenario clínico",
        placeholder="Ejemplo: el sistema no alerta un paciente que se deteriora.",
        height=90
    )
    mitigacion = st.text_area(
        "Mitigación",
        placeholder="Ejemplo: supervisión médica, uso como apoyo, control interno, auditoría semanal.",
        height=90
    )
    seguridad = st.slider("Nivel de control del riesgo", 1, 5, 3)
    save("riesgo", riesgo)
    save("peor", peor)
    save("mitigacion", mitigacion)
    save("seguridad", seguridad)

with tabs[5]:
    st.header("6. KPIs: ¿cómo sabremos que funciona?")
    kpis = st.multiselect("Seleccionen máximo 3 KPIs principales", [
        "Tiempo ahorrado", "Concordancia con experto", "Sensibilidad",
        "Especificidad", "Tasa de falsos negativos", "Satisfacción del usuario",
        "Casos priorizados correctamente", "Reducción de errores",
        "Costo por caso", "Adherencia al uso"
    ], max_selections=3)
    meta = st.text_area(
        "Meta del piloto",
        placeholder="Ejemplo: reducir 20% el tiempo de revisión sin aumentar falsos negativos.",
        height=90
    )
    medicion = st.text_area(
        "Cómo se medirá",
        placeholder="Ejemplo: comparación antes/después, revisión por experto, encuesta de satisfacción.",
        height=90
    )
    save("kpis", kpis)
    save("meta", meta)
    save("medicion", medicion)

with tabs[6]:
    st.header("7. Plan piloto")
    lugar = st.selectbox("Lugar del piloto", [
        "Urgencias", "Radiología", "Patología", "Consulta externa",
        "Hospitalización", "Comité / junta médica", "Otro"
    ])
    duracion = st.selectbox("Duración del piloto", [
        "1 semana", "2 semanas", "4 semanas", "8 semanas", "12 semanas"
    ])
    usuarios = st.number_input("Número estimado de usuarios participantes", min_value=1, max_value=1000, value=5)
    casos = st.number_input("Número estimado de casos a evaluar", min_value=1, max_value=100000, value=50)
    criterio_stop = st.text_area(
        "Criterio de detención",
        placeholder="Ejemplo: si aumenta el tiempo, si hay evento adverso o si falla la supervisión.",
        height=80
    )
    save("lugar", lugar)
    save("duracion", duracion)
    save("usuarios", usuarios)
    save("casos", casos)
    save("criterio_stop", criterio_stop)

with tabs[7]:
    st.header("8. Escalamiento y propiedad intelectual")
    escala = st.text_area(
        "Ruta de escalamiento",
        placeholder="MVP → piloto en un servicio → integración HIS/PACS/LIS → más servicios → red clínica",
        height=100
    )
    pi = st.multiselect("¿Dónde podría estar la PI?", [
        "Software", "Algoritmo/modelo", "Dataset curado", "Flujo clínico",
        "Interfaz de usuario", "Método de validación", "Marca", "Secreto industrial"
    ])
    aliados = st.text_area(
        "Aliados necesarios",
        placeholder="Ejemplo: TI, ética, calidad, dirección médica, servicio clínico, jurídico.",
        height=80
    )
    save("escala", escala)
    save("pi", pi)
    save("aliados", aliados)


# =========================
# FUNCIONES DE SALIDA
# =========================
def maturity_score(d):
    checks = [
        bool(d.get("problema")),
        bool(d.get("usuario")),
        bool(d.get("funcion")),
        bool(d.get("no_hara")),
        bool(d.get("datos")),
        bool(d.get("riesgo")),
        bool(d.get("mitigacion")),
        bool(d.get("kpis")),
        bool(d.get("lugar")),
        bool(d.get("escala")),
    ]
    score = sum(checks) * 8
    score += int(d.get("calidad", 0)) * 2
    score += int(d.get("seguridad", 0)) * 2
    return min(score, 100)


def maturity_level(score):
    if score < 40:
        return (
            "🔴 NIVEL 1: IDEA",
            "El problema clínico está identificado, pero aún no existe un MVP claramente definido.",
            "Definir mejor la función mínima, los datos requeridos, los riesgos y los KPIs.",
            "#FDECEC",
            "#B42318"
        )
    elif score < 65:
        return (
            "🟡 NIVEL 2: PROTOTIPO",
            "Existe una solución preliminar, pero aún falta precisión en métricas, piloto o mitigación de riesgo.",
            "Reducir alcance, definir KPIs y diseñar un piloto de bajo riesgo.",
            "#FFF6D9",
            "#B76E00"
        )
    elif score < 85:
        return (
            "🟢 NIVEL 3: MVP",
            "El proyecto tiene una función mínima clara, usuario definido, KPIs y control básico de riesgo.",
            "Preparar validación inicial y recoger evidencia de impacto.",
            "#EAF8EE",
            "#1E7E34"
        )
    else:
        return (
            "🔵 NIVEL 4: LISTO PARA PILOTO CLÍNICO",
            "El MVP tiene métricas, plan piloto, mitigación de riesgos y ruta de escalamiento.",
            "Presentar a comité clínico, validar gobernanza de datos y definir integración institucional.",
            "#EAF3FF",
            "#0B5CAD"
        )


def innovation_score(d):
    impacto = (4 if d.get("problema") else 0) + (3 if d.get("valor") else 0) + (3 if d.get("kpis") else 0)
    factibilidad = (4 if d.get("funcion") else 0) + (3 if d.get("no_hara") else 0) + (3 if d.get("lugar") else 0)
    datos_score = int(d.get("calidad", 0)) * 2
    escalabilidad = (5 if d.get("escala") else 0) + (3 if d.get("aliados") else 0) + (2 if d.get("pi") else 0)
    riesgo_score = int(d.get("seguridad", 0)) * 2
    return {
        "Impacto clínico": min(impacto, 10),
        "Factibilidad": min(factibilidad, 10),
        "Datos disponibles": min(datos_score, 10),
        "Escalabilidad": min(escalabilidad, 10),
        "Control del riesgo": min(riesgo_score, 10),
    }


def build_summary(d):
    return f"""
# {d.get('nombre','MVP sin nombre')}

## Resumen ejecutivo
Este MVP se propone para el área de **{d.get('area','')}**, enfocado en **{d.get('tipo_problema','')}**.

El problema clínico identificado es: **{d.get('problema','')}**.

## Usuario principal
{d.get('usuario','')} — uso previsto en: {d.get('momento','')}.

## Función mínima
El MVP hará: **{d.get('funcion','')}**.

## Lo que NO hará
{d.get('no_hara','')}

## Datos requeridos
{', '.join(d.get('datos', []))}

## Técnica probable
{', '.join(d.get('tecnica', []))}

## Riesgo principal
{d.get('riesgo','')}

Mitigación: {d.get('mitigacion','')}

## KPIs principales
{', '.join(d.get('kpis', []))}

## Plan piloto
Lugar: {d.get('lugar','')}  
Duración: {d.get('duracion','')}  
Usuarios: {d.get('usuarios','')}  
Casos: {d.get('casos','')}

## Escalamiento
{d.get('escala','')}

## Propiedad intelectual potencial
{', '.join(d.get('pi', []))}
"""


def build_pitch(d):
    nombre = d.get("nombre", "Nuestro MVP")
    problema = d.get("problema", "un problema clínico relevante")
    usuario = d.get("usuario", "el usuario clínico")
    funcion = d.get("funcion", "una función mínima de apoyo")
    datos = ", ".join(d.get("datos", [])) or "datos clínicos disponibles"
    kpis = ", ".join(d.get("kpis", [])) or "indicadores de impacto clínico"
    riesgo = d.get("riesgo", "riesgo clínico")
    mitigacion = d.get("mitigacion", "supervisión médica y monitoreo")
    lugar = d.get("lugar", "un servicio clínico")
    duracion = d.get("duracion", "4 semanas")
    escala = d.get("escala", "escalamiento progresivo a otros servicios")

    return f"""
# Borrador de pitch de 3 minutos

## 1. Apertura
Buenos días. Somos el equipo **{nombre}** y estamos desarrollando un MVP de inteligencia artificial en salud orientado a resolver un problema concreto: **{problema}**.

## 2. Problema clínico
Hoy, este problema impacta el flujo clínico porque genera retrasos, carga operativa o riesgo de omisiones. Nuestro usuario principal es **{usuario}**, quien necesita una herramienta sencilla que apoye su trabajo sin reemplazar su criterio profesional.

## 3. Solución MVP
Nuestro Producto Mínimo Viable hará una sola cosa: **{funcion}**.

Este MVP no pretende ser una plataforma completa ni una IA autónoma. Es una solución mínima, segura y medible para probar valor clínico en condiciones reales.

## 4. Datos e IA
La solución utilizará principalmente: **{datos}**.

La salida esperada será una alerta, resumen, priorización o clasificación supervisada, siempre como apoyo a la decisión clínica.

## 5. Impacto esperado
Mediremos el éxito del MVP usando estos indicadores: **{kpis}**.

El objetivo es demostrar que la herramienta mejora el flujo clínico, reduce tiempos o aumenta la seguridad sin introducir riesgos no controlados.

## 6. Riesgo y mitigación
El principal riesgo identificado es **{riesgo}**. Para controlarlo, proponemos: **{mitigacion}**.

La decisión final siempre permanecerá en manos del profesional de salud.

## 7. Piloto y escalamiento
Proponemos iniciar un piloto en **{lugar}** durante **{duracion}**.

Si demuestra valor y seguridad, la ruta de escalamiento será: **{escala}**.

## 8. Cierre
Nuestro MVP no busca construir la solución más grande, sino la más clara, segura y medible para generar impacto real en salud.
"""


def make_pdf(d):
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("GeniA Innovation Builder - Canvas MVP", styles["Title"]))
    story.append(Spacer(1, 12))

    rows = [
        ["Campo", "Respuesta"],
        ["Proyecto", d.get("nombre", "")],
        ["Área", d.get("area", "")],
        ["Problema clínico", d.get("problema", "")],
        ["Usuario", d.get("usuario", "")],
        ["Función mínima", d.get("funcion", "")],
        ["Lo que NO hará", d.get("no_hara", "")],
        ["Datos", ", ".join(d.get("datos", []))],
        ["Riesgo", d.get("riesgo", "")],
        ["Mitigación", d.get("mitigacion", "")],
        ["KPIs", ", ".join(d.get("kpis", []))],
        ["Piloto", f"{d.get('lugar','')} | {d.get('duracion','')} | {d.get('casos','')} casos"],
        ["Escalamiento", d.get("escala", "")],
        ["PI potencial", ", ".join(d.get("pi", []))]
    ]

    table = Table(rows, colWidths=[130, 360])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B2E4A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EAF3F8")),
    ]))

    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"]
    ))
    doc.build(story)
    buffer.seek(0)
    return buffer


# =========================
# RESULTADO
# =========================
with tabs[8]:
    st.header("9. Resultado del MVP")

    d = st.session_state.data
    score = maturity_score(d)
    level_title, level_text, next_step, bg_color, text_color = maturity_level(score)

    col1, col2, col3 = st.columns(3)
    col1.metric("Madurez MVP", f"{score}/100")
    col2.metric("KPIs definidos", len(d.get("kpis", [])))
    col3.metric("Datos seleccionados", len(d.get("datos", [])))

    st.markdown(
        f"""
        <div class="maturity-card" style="background:{bg_color}; border-color:{text_color};">
            <div class="maturity-title" style="color:{text_color};">{level_title}</div>
            <div class="maturity-text"><b>Interpretación:</b> {level_text}</div>
            <div class="maturity-text"><b>Próximo paso recomendado:</b> {next_step}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🏆 Potencial de innovación")
    scores = innovation_score(d)
    total_innovation = sum(scores.values())

    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Puntaje global", f"{total_innovation}/50")
        if total_innovation < 20:
            st.warning("Potencial inicial. Requiere mayor definición.")
        elif total_innovation < 35:
            st.info("Potencial intermedio. Requiere fortalecer piloto y métricas.")
        else:
            st.success("Alto potencial para piloto institucional.")

    with c2:
        for item, value in scores.items():
            st.progress(value / 10, text=f"{item}: {value}/10")

    summary = build_summary(d)

    st.subheader("📄 Resumen del MVP")
    with st.container():
        st.markdown(f'<div class="result-box">{summary}</div>', unsafe_allow_html=True)

    st.download_button(
        "📥 Descargar resumen en Markdown",
        data=summary.encode("utf-8"),
        file_name=f"genia_mvp_{d.get('nombre','proyecto').replace(' ','_')}.md",
        mime="text/markdown"
    )

    st.subheader("🎤 Borrador automático del pitch")

    pitch = build_pitch(d)
    with st.container():
        st.markdown(f'<div class="result-box">{pitch}</div>', unsafe_allow_html=True)

    st.download_button(
        "🎤 Descargar pitch en Markdown",
        data=pitch.encode("utf-8"),
        file_name=f"pitch_{d.get('nombre','proyecto').replace(' ','_')}.md",
        mime="text/markdown"
    )

    one_slide = f"""# Pitch en una diapositiva

**Nombre del MVP:** {d.get('nombre','')}

**Problema clínico:** {d.get('problema','')}

**Usuario:** {d.get('usuario','')}

**Función mínima:** {d.get('funcion','')}

**Datos:** {', '.join(d.get('datos', []))}

**KPIs:** {', '.join(d.get('kpis', []))}

**Riesgo y mitigación:** {d.get('riesgo','')} → {d.get('mitigacion','')}

**Nivel de madurez:** {level_title} ({score}/100)

**Potencial de innovación:** {total_innovation}/50

**Piloto:** {d.get('lugar','')} durante {d.get('duracion','')}

**Escalamiento:** {d.get('escala','')}
"""

    st.download_button(
        "🖼️ Descargar pitch de 1 diapositiva",
        data=one_slide.encode("utf-8"),
        file_name=f"pitch_1_slide_{d.get('nombre','proyecto').replace(' ','_')}.md",
        mime="text/markdown"
    )

    pdf = make_pdf(d)

    if pdf:
        st.download_button(
            "📄 Descargar MVP Canvas en PDF",
            data=pdf,
            file_name=f"genia_mvp_canvas_{d.get('nombre','proyecto').replace(' ','_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.caption("Para exportar PDF instala reportlab: pip install reportlab")


# =========================
# SIDEBAR
# =========================
st.sidebar.title("Guía docente")

st.sidebar.markdown("""
**Uso en clase**

1. Cada grupo abre la app.
2. Llena las secciones 1–8.
3. Revisa madurez.
4. Descarga el Canvas.
5. Presenta pitch de 3 minutos.

**La app genera**

- Nivel de madurez
- Potencial de innovación
- Borrador de pitch de 3 minutos
- Pitch en una diapositiva
- MVP Canvas en PDF
""")
