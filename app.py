from pathlib import Path
import textwrap, py_compile

script = r'''
import streamlit as st
from datetime import datetime
from io import BytesIO
import base64
import os
import re

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="GeniA Innovation Builder",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# FUNCIONES VISUALES
# ============================================================
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
                rgba(6, 42, 72, 0.62),
                rgba(14, 98, 130, 0.50),
                rgba(240, 90, 40, 0.22)
            );
            border-radius: 28px;
            padding: 2rem 2.2rem 3rem 2.2rem;
            box-shadow: 0 12px 36px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.25);
        }}

        [data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.96);
        }}

        .genia-header {{
            display: flex;
            align-items: center;
            gap: 24px;
            padding: 20px 26px;
            border-radius: 26px;
            background: linear-gradient(
                135deg,
                rgba(255,255,255,0.60),
                rgba(232,246,250,0.44)
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
        .stNumberInput label,
        .stRadio label,
        .stCheckbox label {{
            color: #ffffff !important;
            font-weight: 650;
        }}

        input, textarea {{
            background-color: rgba(255,255,255,0.72) !important;
            color: #0B2E4A !important;
        }}

        div[data-baseweb="select"] > div {{
            background-color: rgba(255,255,255,0.72) !important;
            color: #0B2E4A !important;
            border: 1px solid rgba(255,255,255,0.45) !important;
            backdrop-filter: blur(4px);
        }}

        [data-testid="stExpander"] {{
            background: rgba(255,255,255,0.58);
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
            background: rgba(255,255,255,0.64);
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

        .stDownloadButton button,
        .stButton button {{
            background-color: rgba(255,255,255,0.94) !important;
            color: #0B2E4A !important;
            border: 1px solid rgba(11,46,74,0.25) !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
        }}

        .stDownloadButton button p,
        .stDownloadButton button span,
        .stButton button p,
        .stButton button span {{
            color: #0B2E4A !important;
        }}

        .stDownloadButton button:hover,
        .stButton button:hover {{
            background-color: #F05A28 !important;
            color: #ffffff !important;
        }}

        .stDownloadButton button:hover p,
        .stDownloadButton button:hover span,
        .stButton button:hover p,
        .stButton button:hover span {{
            color: #ffffff !important;
        }}

        .small-note {{
            background: rgba(255,255,255,0.64);
            border-left: 5px solid #F05A28;
            padding: 12px 14px;
            border-radius: 10px;
            margin: 8px 0 14px 0;
        }}

        .small-note p {{
            color: #0B2E4A !important;
            margin: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


if os.path.exists("fondo_bootcamp.png"):
    add_background("fondo_bootcamp.png")
else:
    st.warning("No se encontró `fondo_bootcamp.png`. La app funcionará sin fondo.")


# ============================================================
# HEADER
# ============================================================
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

with st.expander("¿Qué es un MVP de IA en salud?", expanded=True):
    st.markdown("""
    Un **MVP de IA en salud** es la versión más simple, segura y medible de una solución que permite comprobar
    si genera valor clínico u operativo antes de invertir en un desarrollo completo.

    **Debe ser:** específico, verificable, medible, supervisado y limitado a un caso de uso.  
    **No debe ser:** una plataforma completa, una IA autónoma ni un reemplazo del profesional.
    """)

st.divider()


# ============================================================
# ESTADO
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = {}


def save(key, value):
    st.session_state.data[key] = value


def safe_filename(text):
    text = (text or "proyecto").strip()
    text = re.sub(r"[^A-Za-z0-9_-]+", "_", text)
    return text.strip("_") or "proyecto"


# ============================================================
# FORMULARIO
# ============================================================
tabs = st.tabs([
    "1. Problema",
    "2. Usuario y flujo",
    "3. Variable objetivo",
    "4. Datos e IA",
    "5. MVP",
    "6. Riesgos",
    "7. Validación y KPIs",
    "8. Piloto",
    "9. Escalamiento",
    "10. Resultado"
])


with tabs[0]:
    st.header("1. Definir el problema")
    st.markdown(
        '<div class="small-note"><p>Primero definan el problema; no comiencen por el algoritmo.</p></div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input(
            "Nombre del proyecto / equipo",
            value=st.session_state.data.get("nombre", "")
        )
        area = st.selectbox(
            "Área principal",
            [
                "Urgencias", "Radiología", "Patología", "Oncología",
                "Consulta externa", "Hospitalización", "Laboratorio clínico",
                "Farmacia", "Gestión administrativa", "Salud pública", "Otra"
            ]
        )
        tipo_problema = st.selectbox(
            "Tipo de problema",
            [
                "Diagnóstico", "Pronóstico", "Triage / priorización",
                "Seguimiento", "Gestión del flujo de pacientes",
                "Extracción de información", "Resumen de historia clínica",
                "Planeación de demanda", "Educación", "Otro"
            ]
        )

    with col2:
        problema = st.text_area(
            "Problema específico",
            placeholder=(
                "Ejemplo: Los médicos tardan demasiado en identificar pacientes "
                "con riesgo de deterioro clínico en urgencias."
            ),
            height=125
        )
        evidencia_problema = st.text_area(
            "¿Qué evidencia demuestra que el problema existe?",
            placeholder=(
                "Ejemplo: tiempos de atención, auditorías, eventos adversos, "
                "entrevistas, indicadores institucionales."
            ),
            height=95
        )
        consecuencia = st.text_area(
            "¿Qué pasa si no se resuelve?",
            placeholder=(
                "Ejemplo: retrasos, sobrecarga, omisiones, mayor estancia o costos."
            ),
            height=95
        )

    save("nombre", nombre)
    save("area", area)
    save("tipo_problema", tipo_problema)
    save("problema", problema)
    save("evidencia_problema", evidencia_problema)
    save("consecuencia", consecuencia)


with tabs[1]:
    st.header("2. Usuario, decisión y flujo")

    col1, col2 = st.columns(2)

    with col1:
        usuario = st.selectbox(
            "Usuario principal",
            [
                "Médico general", "Especialista", "Enfermería", "Paciente",
                "Administrativo", "Radiólogo", "Patólogo", "Farmacéutico",
                "Gestor clínico", "Equipo de calidad", "Otro"
            ]
        )
        momento = st.selectbox(
            "Momento del flujo",
            [
                "Antes de la consulta", "Durante la consulta",
                "Después de la consulta", "Ingreso a urgencias",
                "Durante hospitalización", "Antes del egreso",
                "Lectura de imágenes", "Junta médica",
                "Seguimiento ambulatorio", "Gestión operativa", "Otro"
            ]
        )
        decision = st.text_area(
            "¿Qué decisión o acción apoyará?",
            placeholder=(
                "Ejemplo: priorizar valoración, solicitar revisión, "
                "seleccionar casos para seguimiento."
            ),
            height=100
        )

    with col2:
        flujo_actual = st.text_area(
            "Flujo actual sin IA",
            placeholder="Paciente → datos → revisión manual → decisión",
            height=95
        )
        flujo_mvp = st.text_area(
            "Flujo propuesto con MVP",
            placeholder="Datos → MVP → resultado verificable → profesional decide",
            height=95
        )
        responsable_final = st.text_input(
            "Responsable de la decisión final",
            placeholder="Ejemplo: médico tratante, radiólogo, químico farmacéutico"
        )

    save("usuario", usuario)
    save("momento", momento)
    save("decision", decision)
    save("flujo_actual", flujo_actual)
    save("flujo_mvp", flujo_mvp)
    save("responsable_final", responsable_final)


with tabs[2]:
    st.header("3. Variable objetivo y alcance")

    tarea_ia = st.selectbox(
        "Tarea principal del MVP",
        [
            "Predecir un evento", "Clasificar", "Priorizar",
            "Extraer información", "Resumir", "Pronosticar demanda",
            "Detectar una anomalía", "Recomendar bajo supervisión", "Otra"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        variable_objetivo = st.text_area(
            "Variable objetivo o resultado principal",
            placeholder=(
                "Ejemplo: reingreso hospitalario no programado dentro de 30 días."
            ),
            height=95
        )
        definicion_positiva = st.text_area(
            "Definición exacta del caso positivo o resultado correcto",
            placeholder=(
                "Ejemplo: nueva hospitalización no programada en la misma institución "
                "dentro de los 30 días posteriores al egreso."
            ),
            height=105
        )
        unidad_analisis = st.selectbox(
            "Unidad de análisis",
            [
                "Paciente", "Consulta", "Hospitalización", "Imagen",
                "Documento", "Medicamento", "Día", "Servicio", "Otra"
            ]
        )

    with col2:
        horizonte = st.text_input(
            "Horizonte temporal",
            placeholder="Ejemplo: 24 horas, 7 días, 30 días"
        )
        poblacion = st.text_area(
            "Población objetivo",
            placeholder=(
                "Ejemplo: adultos hospitalizados próximos al egreso."
            ),
            height=95
        )
        exclusion = st.text_area(
            "Casos fuera del alcance",
            placeholder=(
                "Ejemplo: menores de edad, gestantes, pacientes sin información mínima."
            ),
            height=95
        )

    save("tarea_ia", tarea_ia)
    save("variable_objetivo", variable_objetivo)
    save("definicion_positiva", definicion_positiva)
    save("unidad_analisis", unidad_analisis)
    save("horizonte", horizonte)
    save("poblacion", poblacion)
    save("exclusion", exclusion)


with tabs[3]:
    st.header("4. Datos, línea base y técnica de IA")

    datos = st.multiselect(
        "Datos necesarios",
        [
            "Historia clínica", "Notas médicas", "Signos vitales",
            "Laboratorio", "Imágenes médicas",
            "Citología / patología digital", "Medicamentos",
            "Encuestas", "Datos administrativos",
            "Series temporales", "Datos externos", "Otro"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        fuente = st.text_area(
            "Fuente de los datos",
            placeholder="Ejemplo: HIS, PACS, LIS, registros retrospectivos.",
            height=85
        )
        disponibilidad = st.selectbox(
            "Disponibilidad real de los datos",
            [
                "No confirmada", "Parcial", "Disponible sin depurar",
                "Disponible y depurada", "Disponible y lista para análisis"
            ]
        )
        volumen = st.number_input(
            "Número aproximado de registros disponibles",
            min_value=0,
            max_value=10000000,
            value=0,
            step=10
        )
        calidad = st.slider("Calidad percibida de los datos", 1, 5, 3)

    with col2:
        etiqueta = st.text_area(
            "¿Cómo se obtiene la etiqueta o verdad de referencia?",
            placeholder=(
                "Ejemplo: diagnóstico confirmado, revisión por experto, "
                "registro administrativo, consenso clínico."
            ),
            height=85
        )
        linea_base = st.text_area(
            "Línea base de comparación",
            placeholder=(
                "Ejemplo: revisión manual, regla clínica, promedio histórico, "
                "regresión logística."
            ),
            height=85
        )
        tecnica = st.multiselect(
            "Técnica probable de IA",
            [
                "Reglas clínicas", "Regresión logística",
                "Machine Learning clásico", "Gradient Boosting",
                "Deep Learning", "Computer Vision", "NLP",
                "IA generativa", "Series temporales",
                "Reglas + IA", "No definido aún"
            ]
        )

    save("datos", datos)
    save("fuente", fuente)
    save("disponibilidad", disponibilidad)
    save("volumen", volumen)
    save("calidad", calidad)
    save("etiqueta", etiqueta)
    save("linea_base", linea_base)
    save("tecnica", tecnica)


with tabs[4]:
    st.header("5. Diseñar el MVP")
    st.info("Regla: el MVP debe hacer una sola cosa útil, verificable y segura.")

    funcion = st.text_area(
        "Función mínima",
        placeholder="Mi MVP hará solamente...",
        height=90
    )
    no_hara = st.text_area(
        "¿Qué NO hará?",
        placeholder=(
            "Ejemplo: no diagnosticará, no formulará tratamiento, "
            "no reemplazará el criterio profesional."
        ),
        height=90
    )

    col1, col2 = st.columns(2)

    with col1:
        entrada_mvp = st.text_area(
            "Entrada del MVP",
            placeholder="Formulario, archivo, imagen, nota clínica, datos del HIS.",
            height=85
        )
        procesamiento_mvp = st.text_area(
            "Procesamiento mínimo",
            placeholder="Validación → limpieza → modelo → regla de seguridad.",
            height=85
        )
        salida = st.selectbox(
            "Salida principal",
            [
                "Alerta", "Resumen", "Priorización",
                "Clasificación de riesgo", "Pronóstico",
                "Extracción estructurada", "Recomendación supervisada",
                "Reporte", "Tablero", "Otro"
            ]
        )

    with col2:
        salida_visible = st.text_area(
            "¿Qué verá exactamente el usuario?",
            placeholder=(
                "Ejemplo: riesgo bajo/medio/alto, variables relevantes y advertencia."
            ),
            height=85
        )
        accion_usuario = st.text_area(
            "¿Qué hará el usuario después?",
            placeholder=(
                "Ejemplo: revisar, confirmar, corregir, escalar o priorizar."
            ),
            height=85
        )
        valor = st.text_area(
            "Valor esperado",
            placeholder=(
                "Ejemplo: reducir tiempo, mejorar priorización, disminuir omisiones."
            ),
            height=85
        )

    save("funcion", funcion)
    save("no_hara", no_hara)
    save("entrada_mvp", entrada_mvp)
    save("procesamiento_mvp", procesamiento_mvp)
    save("salida", salida)
    save("salida_visible", salida_visible)
    save("accion_usuario", accion_usuario)
    save("valor", valor)


with tabs[5]:
    st.header("6. Riesgos, supervisión y gobernanza")

    riesgo = st.selectbox(
        "Riesgo principal",
        [
            "Falso negativo", "Falso positivo", "Sesgo poblacional",
            "Sobreconfianza del usuario", "Datos incompletos",
            "Privacidad", "Falla de integración", "Alucinación",
            "Uso fuera de alcance", "Otro"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        peor = st.text_area(
            "Peor escenario",
            placeholder="Ejemplo: el sistema no alerta un caso que se deteriora.",
            height=90
        )
        mitigacion = st.text_area(
            "Mitigación",
            placeholder=(
                "Ejemplo: supervisión humana, umbral conservador, auditoría, "
                "doble lectura."
            ),
            height=90
        )
        seguridad = st.slider("Nivel estimado de control del riesgo", 1, 5, 3)

    with col2:
        supervisor = st.text_input(
            "¿Quién revisará la salida?",
            placeholder="Ejemplo: médico tratante, especialista, auditor"
        )
        baja_confianza = st.text_area(
            "¿Qué hará el sistema con baja confianza o datos insuficientes?",
            placeholder=(
                "Ejemplo: abstenerse, mostrar advertencia, solicitar revisión."
            ),
            height=90
        )
        correccion_usuario = st.selectbox(
            "¿El usuario puede corregir o rechazar el resultado?",
            ["No definido", "Sí", "No"]
        )

    privacidad = st.multiselect(
        "Controles de datos y gobernanza previstos",
        [
            "Anonimización / seudonimización", "Control de acceso",
            "Registro de auditoría", "Consentimiento o base legal",
            "Aprobación institucional", "Comité de ética",
            "Evaluación de seguridad", "Plan de gestión de incidentes"
        ]
    )

    save("riesgo", riesgo)
    save("peor", peor)
    save("mitigacion", mitigacion)
    save("seguridad", seguridad)
    save("supervisor", supervisor)
    save("baja_confianza", baja_confianza)
    save("correccion_usuario", correccion_usuario)
    save("privacidad", privacidad)


with tabs[6]:
    st.header("7. Validación y KPIs")

    validaciones = st.multiselect(
        "Tipos de validación previstos",
        [
            "Validación técnica interna",
            "Validación con expertos",
            "Prueba de usabilidad",
            "Validación clínica retrospectiva",
            "Validación prospectiva",
            "Evaluación operativa",
            "Evaluación de sesgo",
            "Evaluación de calibración"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        kpis = st.multiselect(
            "Seleccionen máximo 4 KPIs",
            [
                "Tiempo ahorrado", "Concordancia con experto",
                "Sensibilidad", "Especificidad", "Precisión",
                "AUPRC", "AUROC", "F1", "Calibración",
                "Tasa de falsos negativos", "Satisfacción del usuario",
                "Casos priorizados correctamente", "Reducción de errores",
                "Costo por caso", "Adherencia al uso",
                "MAE / RMSE", "WAPE / MAPE"
            ],
            max_selections=4
        )
        meta = st.text_area(
            "Meta cuantificable",
            placeholder=(
                "Ejemplo: reducir 20% el tiempo sin aumentar falsos negativos."
            ),
            height=85
        )

    with col2:
        medicion = st.text_area(
            "Cómo se medirá",
            placeholder=(
                "Ejemplo: comparación antes/después, revisión por experto."
            ),
            height=85
        )
        muestra_validacion = st.number_input(
            "Número estimado de casos para validación inicial",
            min_value=0,
            max_value=1000000,
            value=0,
            step=10
        )
        criterio_avance = st.text_area(
            "Criterio para avanzar al piloto",
            placeholder=(
                "Ejemplo: sensibilidad ≥ 90%, usabilidad ≥ 80% y ausencia de eventos críticos."
            ),
            height=85
        )

    save("validaciones", validaciones)
    save("kpis", kpis)
    save("meta", meta)
    save("medicion", medicion)
    save("muestra_validacion", muestra_validacion)
    save("criterio_avance", criterio_avance)


with tabs[7]:
    st.header("8. Plan piloto")

    col1, col2 = st.columns(2)

    with col1:
        lugar = st.selectbox(
            "Lugar del piloto",
            [
                "Urgencias", "Radiología", "Patología",
                "Consulta externa", "Hospitalización",
                "Farmacia", "Comité / junta médica",
                "Gestión administrativa", "Otro"
            ]
        )
        duracion = st.selectbox(
            "Duración",
            ["1 semana", "2 semanas", "4 semanas", "8 semanas", "12 semanas"]
        )
        usuarios = st.number_input(
            "Usuarios participantes",
            min_value=1,
            max_value=1000,
            value=5
        )

    with col2:
        casos = st.number_input(
            "Casos a evaluar",
            min_value=1,
            max_value=100000,
            value=50
        )
        criterio_stop = st.text_area(
            "Criterio de detención",
            placeholder=(
                "Ejemplo: evento adverso, pérdida de datos, incremento del tiempo."
            ),
            height=85
        )
        responsable_piloto = st.text_input(
            "Responsable del piloto",
            placeholder="Nombre o rol institucional"
        )

    save("lugar", lugar)
    save("duracion", duracion)
    save("usuarios", usuarios)
    save("casos", casos)
    save("criterio_stop", criterio_stop)
    save("responsable_piloto", responsable_piloto)


with tabs[8]:
    st.header("9. Escalamiento y propiedad intelectual")

    escala = st.text_area(
        "Ruta de escalamiento",
        placeholder=(
            "MVP → validación → piloto → integración → nuevos servicios."
        ),
        height=95
    )
    pi = st.multiselect(
        "¿Dónde podría estar la propiedad intelectual?",
        [
            "Software", "Algoritmo / modelo", "Dataset curado",
            "Flujo clínico", "Interfaz", "Método de validación",
            "Marca", "Secreto industrial"
        ]
    )
    aliados = st.text_area(
        "Aliados necesarios",
        placeholder=(
            "TI, ética, calidad, dirección médica, servicio clínico, jurídico."
        ),
        height=85
    )
    integracion = st.multiselect(
        "Integraciones futuras",
        ["HIS", "PACS", "LIS", "ERP", "API", "Repositorio documental", "Otra"]
    )

    save("escala", escala)
    save("pi", pi)
    save("aliados", aliados)
    save("integracion", integracion)


# ============================================================
# FUNCIONES DE EVALUACIÓN
# ============================================================
def has_text(d, key, min_len=8):
    return len(str(d.get(key, "")).strip()) >= min_len


def maturity_score(d):
    score = 0

    # Problema y usuario: 18
    score += 4 if has_text(d, "problema", 20) else 0
    score += 3 if has_text(d, "evidencia_problema", 12) else 0
    score += 3 if has_text(d, "decision", 12) else 0
    score += 3 if has_text(d, "flujo_mvp", 12) else 0
    score += 3 if has_text(d, "responsable_final", 3) else 0
    score += 2 if has_text(d, "consecuencia", 12) else 0

    # Variable objetivo: 16
    score += 5 if has_text(d, "variable_objetivo", 12) else 0
    score += 4 if has_text(d, "definicion_positiva", 12) else 0
    score += 3 if has_text(d, "horizonte", 2) else 0
    score += 2 if has_text(d, "poblacion", 8) else 0
    score += 2 if has_text(d, "exclusion", 8) else 0

    # Datos y línea base: 18
    score += 3 if d.get("datos") else 0
    score += 3 if has_text(d, "fuente", 8) else 0
    score += 4 if d.get("disponibilidad") in [
        "Disponible sin depurar",
        "Disponible y depurada",
        "Disponible y lista para análisis"
    ] else 0
    score += 2 if int(d.get("volumen", 0)) > 0 else 0
    score += 3 if has_text(d, "etiqueta", 8) else 0
    score += 3 if has_text(d, "linea_base", 8) else 0

    # MVP: 16
    score += 4 if has_text(d, "funcion", 12) else 0
    score += 3 if has_text(d, "no_hara", 10) else 0
    score += 2 if has_text(d, "entrada_mvp", 6) else 0
    score += 2 if has_text(d, "salida_visible", 8) else 0
    score += 3 if has_text(d, "accion_usuario", 8) else 0
    score += 2 if has_text(d, "valor", 8) else 0

    # Seguridad: 16
    score += 3 if has_text(d, "peor", 8) else 0
    score += 4 if has_text(d, "mitigacion", 10) else 0
    score += 2 if has_text(d, "supervisor", 3) else 0
    score += 3 if has_text(d, "baja_confianza", 8) else 0
    score += 2 if d.get("correccion_usuario") == "Sí" else 0
    score += 2 if len(d.get("privacidad", [])) >= 2 else 0

    # Validación y piloto: 16
    score += 3 if len(d.get("validaciones", [])) >= 2 else 0
    score += 3 if len(d.get("kpis", [])) >= 2 else 0
    score += 3 if has_text(d, "meta", 8) else 0
    score += 3 if has_text(d, "criterio_avance", 8) else 0
    score += 2 if int(d.get("muestra_validacion", 0)) > 0 else 0
    score += 2 if has_text(d, "criterio_stop", 8) else 0

    return min(score, 100)


def maturity_level(score, d):
    blockers = []

    if not has_text(d, "variable_objetivo", 12):
        blockers.append("variable objetivo")
    if not has_text(d, "linea_base", 8):
        blockers.append("línea base")
    if not has_text(d, "mitigacion", 10):
        blockers.append("mitigación")
    if not has_text(d, "criterio_avance", 8):
        blockers.append("criterio de avance")
    if len(d.get("validaciones", [])) < 2:
        blockers.append("plan de validación")

    if score < 40:
        return (
            "🔴 NIVEL 1: IDEA",
            "El problema existe, pero el MVP todavía no está suficientemente definido.",
            "Definir variable objetivo, usuario, función mínima, datos y riesgos.",
            "#FDECEC",
            "#B42318",
            blockers
        )
    elif score < 65:
        return (
            "🟡 NIVEL 2: PROTOTIPO CONCEPTUAL",
            "La solución tiene estructura inicial, pero aún no demuestra viabilidad suficiente.",
            "Precisar datos, línea base, validación y supervisión humana.",
            "#FFF6D9",
            "#B76E00",
            blockers
        )
    elif score < 85 or blockers:
        return (
            "🟢 NIVEL 3: MVP DEFINIDO",
            "El proyecto tiene un MVP coherente y puede avanzar a validación inicial.",
            "Completar los elementos bloqueantes antes de declarar preparación para piloto.",
            "#EAF8EE",
            "#1E7E34",
            blockers
        )
    else:
        return (
            "🔵 NIVEL 4: CANDIDATO A PILOTO",
            "El MVP cuenta con problema, objetivo, línea base, validación, seguridad y plan de piloto.",
            "Revisión institucional, gobernanza de datos y aprobación formal antes de ejecutarlo.",
            "#EAF3FF",
            "#0B5CAD",
            blockers
        )


def innovation_score(d):
    impacto = (
        (4 if has_text(d, "problema", 20) else 0)
        + (3 if has_text(d, "valor", 8) else 0)
        + (3 if has_text(d, "meta", 8) else 0)
    )
    factibilidad = (
        (3 if has_text(d, "funcion", 12) else 0)
        + (2 if has_text(d, "linea_base", 8) else 0)
        + (3 if d.get("disponibilidad") in [
            "Disponible sin depurar",
            "Disponible y depurada",
            "Disponible y lista para análisis"
        ] else 0)
        + (2 if int(d.get("volumen", 0)) > 0 else 0)
    )
    datos_score = (
        min(int(d.get("calidad", 0)) * 2, 6)
        + (2 if has_text(d, "etiqueta", 8) else 0)
        + (2 if has_text(d, "fuente", 8) else 0)
    )
    escalabilidad = (
        (4 if has_text(d, "escala", 8) else 0)
        + (3 if has_text(d, "aliados", 8) else 0)
        + (2 if d.get("pi") else 0)
        + (1 if d.get("integracion") else 0)
    )
    riesgo_score = (
        (3 if has_text(d, "mitigacion", 10) else 0)
        + (2 if has_text(d, "baja_confianza", 8) else 0)
        + (2 if has_text(d, "supervisor", 3) else 0)
        + (2 if len(d.get("privacidad", [])) >= 2 else 0)
        + (1 if d.get("correccion_usuario") == "Sí" else 0)
    )

    return {
        "Impacto": min(impacto, 10),
        "Factibilidad": min(factibilidad, 10),
        "Datos": min(datos_score, 10),
        "Escalabilidad": min(escalabilidad, 10),
        "Control del riesgo": min(riesgo_score, 10),
    }


def project_recommendations(d):
    recs = []

    if not has_text(d, "variable_objetivo", 12):
        recs.append("Definir una variable objetivo concreta y medible.")
    if not has_text(d, "definicion_positiva", 12):
        recs.append("Precisar cómo se determina un caso positivo o correcto.")
    if not has_text(d, "linea_base", 8):
        recs.append("Definir una línea base antes de comparar modelos avanzados.")
    if d.get("disponibilidad") in ["No confirmada", "Parcial"]:
        recs.append("Confirmar acceso, permisos, calidad y volumen real de datos.")
    if not has_text(d, "baja_confianza", 8):
        recs.append("Diseñar el comportamiento ante baja confianza o datos incompletos.")
    if len(d.get("validaciones", [])) < 2:
        recs.append("Incluir al menos validación técnica y validación con usuarios o expertos.")
    if not has_text(d, "criterio_avance", 8):
        recs.append("Establecer un criterio cuantificable para avanzar al piloto.")
    if not has_text(d, "criterio_stop", 8):
        recs.append("Definir cuándo detener el piloto por seguridad o desempeño.")
    if d.get("correccion_usuario") != "Sí":
        recs.append("Permitir que el profesional revise, corrija o rechace la salida.")

    if not recs:
        recs.append("El proyecto está bien estructurado; el siguiente paso es la revisión institucional.")

    return recs[:7]


def build_summary(d, score, level_title, total_innovation, blockers):
    recs = project_recommendations(d)
    blockers_text = ", ".join(blockers) if blockers else "Ninguno identificado"
    recs_text = "\n".join([f"- {x}" for x in recs])

    return f"""
# {d.get('nombre', 'MVP sin nombre')}

## Resumen ejecutivo
Área: **{d.get('area', '')}**  
Tipo de problema: **{d.get('tipo_problema', '')}**

**Problema:** {d.get('problema', '')}

**Evidencia del problema:** {d.get('evidencia_problema', '')}

**Usuario principal:** {d.get('usuario', '')}

**Decisión apoyada:** {d.get('decision', '')}

## Variable objetivo
**Tarea:** {d.get('tarea_ia', '')}  
**Resultado principal:** {d.get('variable_objetivo', '')}  
**Definición:** {d.get('definicion_positiva', '')}  
**Horizonte:** {d.get('horizonte', '')}  
**Unidad de análisis:** {d.get('unidad_analisis', '')}  
**Población:** {d.get('poblacion', '')}

## Datos y método
**Datos:** {', '.join(d.get('datos', []))}  
**Fuente:** {d.get('fuente', '')}  
**Disponibilidad:** {d.get('disponibilidad', '')}  
**Volumen estimado:** {d.get('volumen', '')}  
**Verdad de referencia:** {d.get('etiqueta', '')}  
**Línea base:** {d.get('linea_base', '')}  
**Técnicas probables:** {', '.join(d.get('tecnica', []))}

## MVP
**Función mínima:** {d.get('funcion', '')}  
**Lo que no hará:** {d.get('no_hara', '')}  
**Entrada:** {d.get('entrada_mvp', '')}  
**Procesamiento:** {d.get('procesamiento_mvp', '')}  
**Salida:** {d.get('salida_visible', '')}  
**Acción del usuario:** {d.get('accion_usuario', '')}

## Seguridad
**Riesgo principal:** {d.get('riesgo', '')}  
**Peor escenario:** {d.get('peor', '')}  
**Mitigación:** {d.get('mitigacion', '')}  
**Supervisor:** {d.get('supervisor', '')}  
**Baja confianza:** {d.get('baja_confianza', '')}  
**Gobernanza:** {', '.join(d.get('privacidad', []))}

## Validación
**Tipos de validación:** {', '.join(d.get('validaciones', []))}  
**KPIs:** {', '.join(d.get('kpis', []))}  
**Meta:** {d.get('meta', '')}  
**Criterio de avance:** {d.get('criterio_avance', '')}

## Piloto
Lugar: {d.get('lugar', '')}  
Duración: {d.get('duracion', '')}  
Usuarios: {d.get('usuarios', '')}  
Casos: {d.get('casos', '')}  
Criterio de detención: {d.get('criterio_stop', '')}

## Escalamiento
{d.get('escala', '')}

## Evaluación automática
**Madurez:** {level_title} ({score}/100)  
**Potencial de innovación:** {total_innovation}/50  
**Elementos bloqueantes:** {blockers_text}

## Recomendaciones
{recs_text}
"""


def build_pitch(d):
    nombre = d.get("nombre", "Nuestro MVP")
    problema = d.get("problema", "un problema relevante")
    usuario = d.get("usuario", "el usuario")
    decision = d.get("decision", "una decisión")
    funcion = d.get("funcion", "una función mínima")
    variable = d.get("variable_objetivo", "un resultado medible")
    datos = ", ".join(d.get("datos", [])) or "datos disponibles"
    linea_base = d.get("linea_base", "el proceso actual")
    kpis = ", ".join(d.get("kpis", [])) or "indicadores técnicos y de impacto"
    riesgo = d.get("riesgo", "un riesgo relevante")
    mitigacion = d.get("mitigacion", "supervisión profesional")
    lugar = d.get("lugar", "un servicio")
    duracion = d.get("duracion", "4 semanas")
    escala = d.get("escala", "escalamiento progresivo")

    return f"""
# Borrador de pitch de 3 minutos

## 1. Apertura
Somos el equipo **{nombre}** y trabajamos sobre el siguiente problema: **{problema}**.

## 2. Usuario y decisión
Nuestro usuario principal es **{usuario}**. La solución busca apoyar esta decisión o acción:
**{decision}**.

## 3. Resultado que queremos lograr
El MVP se enfocará en **{variable}**.

## 4. Solución mínima
El MVP hará una sola cosa: **{funcion}**.

No es una plataforma completa ni una IA autónoma. Es una solución limitada, verificable y supervisada.

## 5. Datos y línea base
Utilizará: **{datos}**.

Se comparará contra: **{linea_base}**.

## 6. Evaluación
Mediremos su desempeño y utilidad mediante: **{kpis}**.

## 7. Seguridad
El principal riesgo es **{riesgo}**. La mitigación propuesta es: **{mitigacion}**.

La decisión final permanecerá en manos del profesional responsable.

## 8. Piloto y escalamiento
Proponemos un piloto en **{lugar}** durante **{duracion}**.

Si demuestra valor y seguridad, la ruta será: **{escala}**.

## 9. Cierre
Nuestro MVP no busca ser la solución más grande, sino la más clara, segura y medible para demostrar impacto real.
"""


def make_pdf(d, score, level_title, total_innovation, blockers):
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CenterTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0B2E4A")
    ))
    styles.add(ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#F05A28"),
        spaceBefore=8,
        spaceAfter=6
    ))

    story = [
        Paragraph("GeniA Innovation Builder", styles["CenterTitle"]),
        Paragraph("Canvas de MVP de IA en salud", styles["Heading2"]),
        Spacer(1, 10)
    ]

    def p(text):
        return Paragraph(str(text or "").replace("\n", "<br/>"), styles["BodyText"])

    rows = [
        ["Campo", "Respuesta"],
        ["Proyecto", d.get("nombre", "")],
        ["Área", d.get("area", "")],
        ["Problema", d.get("problema", "")],
        ["Usuario", d.get("usuario", "")],
        ["Decisión", d.get("decision", "")],
        ["Variable objetivo", d.get("variable_objetivo", "")],
        ["Horizonte", d.get("horizonte", "")],
        ["Función mínima", d.get("funcion", "")],
        ["Lo que no hará", d.get("no_hara", "")],
        ["Datos", ", ".join(d.get("datos", []))],
        ["Línea base", d.get("linea_base", "")],
        ["Riesgo", d.get("riesgo", "")],
        ["Mitigación", d.get("mitigacion", "")],
        ["KPIs", ", ".join(d.get("kpis", []))],
        ["Piloto", f"{d.get('lugar','')} | {d.get('duracion','')} | {d.get('casos','')} casos"],
        ["Madurez", f"{level_title} ({score}/100)"],
        ["Innovación", f"{total_innovation}/50"],
        ["Bloqueantes", ", ".join(blockers) if blockers else "Ninguno"]
    ]

    pdf_rows = [[p(cell) for cell in row] for row in rows]

    table = Table(pdf_rows, colWidths=[125, 365], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B2E4A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#666666")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EAF3F8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    story.append(table)
    story.append(PageBreak())
    story.append(Paragraph("Recomendaciones", styles["Section"]))

    for rec in project_recommendations(d):
        story.append(Paragraph(f"• {rec}", styles["BodyText"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["BodyText"]
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ============================================================
# RESULTADO
# ============================================================
with tabs[9]:
    st.header("10. Resultado del MVP")

    d = st.session_state.data
    score = maturity_score(d)
    (
        level_title,
        level_text,
        next_step,
        bg_color,
        text_color,
        blockers
    ) = maturity_level(score, d)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Madurez", f"{score}/100")
    col2.metric("KPIs", len(d.get("kpis", [])))
    col3.metric("Datos", len(d.get("datos", [])))
    col4.metric("Validaciones", len(d.get("validaciones", [])))

    st.markdown(
        f"""
        <div class="maturity-card" style="background:{bg_color}; border-color:{text_color};">
            <div class="maturity-title" style="color:{text_color};">{level_title}</div>
            <div class="maturity-text"><b>Interpretación:</b> {level_text}</div>
            <div class="maturity-text"><b>Próximo paso:</b> {next_step}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if blockers:
        st.warning("Elementos bloqueantes: " + ", ".join(blockers))
    else:
        st.success("No se identificaron elementos bloqueantes principales.")

    st.subheader("🏆 Potencial de innovación")
    scores = innovation_score(d)
    total_innovation = sum(scores.values())

    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Puntaje global", f"{total_innovation}/50")
        if total_innovation < 20:
            st.warning("Potencial inicial. Requiere mayor definición.")
        elif total_innovation < 35:
            st.info("Potencial intermedio. Fortalecer datos, validación o escalamiento.")
        else:
            st.success("Alto potencial para validación institucional.")

    with c2:
        for item, value in scores.items():
            st.progress(value / 10, text=f"{item}: {value}/10")

    st.subheader("🧭 Recomendaciones automáticas")
    for rec in project_recommendations(d):
        st.write(f"• {rec}")

    summary = build_summary(
        d, score, level_title, total_innovation, blockers
    )

    st.subheader("📄 Resumen del MVP")
    st.markdown(
        f'<div class="result-box">{summary}</div>',
        unsafe_allow_html=True
    )

    filename = safe_filename(d.get("nombre", "proyecto"))

    st.download_button(
        "📥 Descargar resumen en Markdown",
        data=summary.encode("utf-8"),
        file_name=f"genia_mvp_{filename}.md",
        mime="text/markdown"
    )

    st.subheader("🎤 Borrador del pitch")
    pitch = build_pitch(d)

    st.markdown(
        f'<div class="result-box">{pitch}</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        "🎤 Descargar pitch en Markdown",
        data=pitch.encode("utf-8"),
        file_name=f"pitch_{filename}.md",
        mime="text/markdown"
    )

    one_slide = f"""# Pitch en una diapositiva

**Nombre:** {d.get('nombre','')}

**Problema:** {d.get('problema','')}

**Usuario y decisión:** {d.get('usuario','')} → {d.get('decision','')}

**Variable objetivo:** {d.get('variable_objetivo','')}

**Función mínima:** {d.get('funcion','')}

**Datos y línea base:** {', '.join(d.get('datos', []))} | {d.get('linea_base','')}

**KPIs:** {', '.join(d.get('kpis', []))}

**Riesgo y mitigación:** {d.get('riesgo','')} → {d.get('mitigacion','')}

**Madurez:** {level_title} ({score}/100)

**Potencial de innovación:** {total_innovation}/50

**Piloto:** {d.get('lugar','')} durante {d.get('duracion','')}

**Escalamiento:** {d.get('escala','')}
"""

    st.download_button(
        "🖼️ Descargar pitch de 1 diapositiva",
        data=one_slide.encode("utf-8"),
        file_name=f"pitch_1_slide_{filename}.md",
        mime="text/markdown"
    )

    pdf = make_pdf(
        d, score, level_title, total_innovation, blockers
    )

    if pdf:
        st.download_button(
            "📄 Descargar MVP Canvas en PDF",
            data=pdf,
            file_name=f"genia_mvp_canvas_{filename}.pdf",
            mime="application/pdf"
        )
    else:
        st.caption("Para exportar PDF instala reportlab: pip install reportlab")


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Guía docente")

st.sidebar.markdown("""
**Uso en clase**

1. Cada grupo abre la app.
2. Completa las secciones 1–9.
3. Revisa madurez y bloqueantes.
4. Ajusta su propuesta.
5. Descarga el Canvas.
6. Presenta un pitch de 3 minutos.

**La app genera**

- Nivel de madurez
- Elementos bloqueantes
- Potencial de innovación
- Recomendaciones
- Resumen del MVP
- Pitch de 3 minutos
- Pitch en una diapositiva
- Canvas en PDF

**Principio central**

El algoritmo no es el MVP.  
El MVP integra problema, usuario, datos, salida, acción, validación y seguridad.
""")

st.sidebar.divider()

if st.sidebar.button("Reiniciar formulario"):
    st.session_state.data = {}
    st.rerun()
'''

path = Path("/mnt/data/genia_innovation_builder_actualizado.py")
path.write_text(script, encoding="utf-8")
py_compile.compile(str(path), doraise=True)

print(f"Archivo creado y validado: {path}")
print(f"Tamaño: {path.stat().st_size:,} bytes")
