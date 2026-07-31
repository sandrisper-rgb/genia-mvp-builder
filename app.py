import base64
import os
import re
import textwrap
from datetime import datetime
from io import BytesIO

import streamlit as st

# Librerías opcionales
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    PPTX_AVAILABLE = True
except Exception:
    PPTX_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


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
def image_to_base64(path: str) -> str:
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode()


def add_background(path: str) -> None:
    encoded = image_to_base64(path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(255,255,255,.08), rgba(255,255,255,.16)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background: linear-gradient(
                135deg,
                rgba(6,42,72,.62),
                rgba(14,98,130,.50),
                rgba(240,90,40,.22)
            );
            border-radius: 28px;
            padding: 2rem 2.2rem 3rem;
            box-shadow: 0 12px 36px rgba(0,0,0,.25);
            border: 1px solid rgba(255,255,255,.25);
        }}

        [data-testid="stSidebar"] {{
            background: rgba(255,255,255,.96);
        }}

        .genia-header {{
            display:flex;
            align-items:center;
            gap:24px;
            padding:20px 26px;
            border-radius:26px;
            background:linear-gradient(135deg, rgba(255,255,255,.60), rgba(232,246,250,.44));
            border:1px solid rgba(11,46,74,.18);
            box-shadow:0 8px 24px rgba(0,0,0,.12);
            margin-bottom:18px;
        }}

        .genia-logo-img {{
            width:210px;
            max-width:28vw;
            height:auto;
            object-fit:contain;
        }}

        .genia-title {{
            font-size:40px;
            line-height:1.05;
            font-weight:850;
            color:#0B2E4A;
            margin:0;
        }}

        .genia-subtitle {{
            font-size:20px;
            color:#F05A28;
            font-weight:750;
            margin-top:6px;
        }}

        .genia-caption {{
            font-size:14px;
            color:#5B667A;
            margin-top:4px;
        }}

        .block-container h1,
        .block-container h2,
        .block-container h3,
        .block-container p,
        .block-container label,
        .block-container span {{
            color:#FFFFFF !important;
        }}

        input, textarea {{
            background-color:rgba(255,255,255,.95) !important;
            color:#0B2E4A !important;
            -webkit-text-fill-color:#0B2E4A !important;
        }}

        div[data-baseweb="select"] > div {{
            background-color:rgba(255,255,255,.95) !important;
            color:#0B2E4A !important;
        }}

        [data-testid="stExpander"] {{
            background:rgba(255,255,255,.58);
            border-radius:14px;
        }}

        [data-testid="stExpander"] * {{
            color:#0B2E4A !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            color:#FFFFFF !important;
            font-weight:650;
        }}

        .stTabs [aria-selected="true"] {{
            color:#F05A28 !important;
            background:rgba(255,255,255,.62);
            border-radius:10px 10px 0 0;
        }}

        .result-card {{
            background:#0B2E4A !important;
            color:#FFFFFF !important;
            border-radius:18px;
            padding:18px;
            border:1px solid rgba(255,255,255,.15);
            box-shadow:0 6px 18px rgba(0,0,0,.12);
            margin-top:12px;
        }}

        .result-card * {{
            color:#FFFFFF !important;
        }}

        .maturity-card {{
            background:rgba(255,255,255,.94) !important;
            border-radius:18px;
            padding:18px;
            border:1px solid rgba(11,46,74,.18);
            box-shadow:0 6px 18px rgba(0,0,0,.12);
            margin-top:12px;
        }}

        .maturity-card * {{
            color:#0B2E4A !important;
        }}

        .stDownloadButton button,
        .stButton button {{
            background:#FFFFFF !important;
            color:#0B2E4A !important;
            font-weight:700 !important;
            border-radius:12px !important;
            border:1px solid rgba(11,46,74,.25) !important;
        }}

        .stDownloadButton button p,
        .stDownloadButton button span,
        .stButton button p,
        .stButton button span {{
            color:#0B2E4A !important;
            -webkit-text-fill-color:#0B2E4A !important;
        }}

        .stDownloadButton button:hover,
        .stButton button:hover {{
            background:#F05A28 !important;
        }}

        .stDownloadButton button:hover p,
        .stDownloadButton button:hover span,
        .stButton button:hover p,
        .stButton button:hover span {{
            color:#FFFFFF !important;
            -webkit-text-fill-color:#FFFFFF !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


if os.path.exists("fondo_bootcamp.png"):
    add_background("fondo_bootcamp.png")

if os.path.exists("logo_genia.png"):
    logo = f'<img src="data:image/png;base64,{image_to_base64("logo_genia.png")}" class="genia-logo-img">'
else:
    logo = '<div style="font-size:48px;">🧠</div>'

st.markdown(
    f"""
    <div class="genia-header">
        <div>{logo}</div>
        <div>
            <div class="genia-title">Innovation Builder</div>
            <div class="genia-subtitle">Del reto clínico al MVP de IA en salud</div>
            <div class="genia-caption">Programa de Inteligencia Artificial — Los Cobos Medical Center</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("¿Qué es un MVP de IA en salud?", expanded=True):
    st.markdown("""
    Un **MVP de IA en salud** es la versión más simple, segura y medible de una solución
    que permite comprobar si genera valor clínico u operativo antes de invertir en un desarrollo completo.

    **Debe ser:** específico, verificable, medible, supervisado y limitado a un caso de uso.  
    **No debe ser:** una plataforma completa, una IA autónoma ni un reemplazo del profesional.
    """)


# ============================================================
# ESTADO
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = {}


def save(key, value):
    st.session_state.data[key] = value


def text_ok(d, key, minimum=8):
    return len(str(d.get(key, "")).strip()) >= minimum


def safe_filename(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", (text or "proyecto")).strip("_") or "proyecto"


# ============================================================
# TABS
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

# ------------------------------------------------------------
# 1. PROBLEMA
# ------------------------------------------------------------
with tabs[0]:
    st.header("1. Definir el problema")

    c1, c2 = st.columns(2)
    with c1:
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
                "Seguimiento", "Gestión del flujo", "Extracción de información",
                "Resumen de historia clínica", "Planeación de demanda",
                "Educación", "Otro"
            ]
        )

    with c2:
        problema = st.text_area(
            "Problema específico",
            placeholder="Ejemplo: identificación tardía de pacientes con riesgo de deterioro.",
            height=110
        )
        evidencia_problema = st.text_area(
            "¿Qué evidencia demuestra que existe?",
            placeholder="Indicadores, auditorías, eventos, tiempos o entrevistas.",
            height=90
        )
        consecuencia = st.text_area(
            "¿Qué ocurre si no se resuelve?",
            height=80
        )

    for k, v in {
        "nombre": nombre,
        "area": area,
        "tipo_problema": tipo_problema,
        "problema": problema,
        "evidencia_problema": evidencia_problema,
        "consecuencia": consecuencia
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 2. USUARIO Y FLUJO
# ------------------------------------------------------------
with tabs[1]:
    st.header("2. Usuario, decisión y flujo")

    c1, c2 = st.columns(2)
    with c1:
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
        decision = st.text_area("¿Qué decisión o acción apoyará?", height=90)

    with c2:
        flujo_actual = st.text_area(
            "Flujo actual sin IA",
            placeholder="Datos → revisión manual → decisión",
            height=85
        )
        flujo_mvp = st.text_area(
            "Flujo propuesto con MVP",
            placeholder="Datos → MVP → resultado verificable → profesional decide",
            height=85
        )
        responsable_final = st.text_input("Responsable de la decisión final")

    for k, v in {
        "usuario": usuario,
        "momento": momento,
        "decision": decision,
        "flujo_actual": flujo_actual,
        "flujo_mvp": flujo_mvp,
        "responsable_final": responsable_final
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 3. VARIABLE OBJETIVO
# ------------------------------------------------------------
with tabs[2]:
    st.header("3. Variable objetivo y alcance")

    tarea_ia = st.selectbox(
        "Tarea principal",
        [
            "Predecir un evento", "Clasificar", "Priorizar", "Extraer información",
            "Resumir", "Pronosticar demanda", "Detectar una anomalía",
            "Recomendar bajo supervisión", "Otra"
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        variable_objetivo = st.text_area(
            "Variable objetivo o resultado principal",
            placeholder="Ejemplo: reingreso no programado dentro de 30 días.",
            height=90
        )
        definicion_positiva = st.text_area(
            "Definición exacta del resultado correcto",
            height=90
        )
        unidad_analisis = st.selectbox(
            "Unidad de análisis",
            ["Paciente", "Consulta", "Hospitalización", "Imagen", "Documento", "Medicamento", "Día", "Servicio", "Otra"]
        )

    with c2:
        horizonte = st.text_input("Horizonte temporal", placeholder="24 horas, 7 días, 30 días")
        poblacion = st.text_area("Población objetivo", height=85)
        exclusion = st.text_area("Casos fuera del alcance", height=85)

    for k, v in {
        "tarea_ia": tarea_ia,
        "variable_objetivo": variable_objetivo,
        "definicion_positiva": definicion_positiva,
        "unidad_analisis": unidad_analisis,
        "horizonte": horizonte,
        "poblacion": poblacion,
        "exclusion": exclusion
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 4. DATOS E IA
# ------------------------------------------------------------
with tabs[3]:
    st.header("4. Datos, línea base y técnica de IA")

    datos = st.multiselect(
        "Datos necesarios",
        [
            "Historia clínica", "Notas médicas", "Signos vitales", "Laboratorio",
            "Imágenes médicas", "Citología / patología digital", "Medicamentos",
            "Encuestas", "Datos administrativos", "Series temporales",
            "Datos externos", "Otro"
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        fuente = st.text_area("Fuente de los datos", height=80)
        disponibilidad = st.selectbox(
            "Disponibilidad real",
            [
                "No confirmada", "Parcial", "Disponible sin depurar",
                "Disponible y depurada", "Disponible y lista para análisis"
            ]
        )
        volumen = st.number_input(
            "Número aproximado de registros",
            min_value=0,
            max_value=10000000,
            value=0,
            step=10
        )
        calidad = st.slider("Calidad percibida", 1, 5, 3)

    with c2:
        etiqueta = st.text_area("¿Cómo se obtiene la verdad de referencia?", height=80)
        linea_base = st.text_area(
            "Línea base de comparación",
            placeholder="Revisión manual, regla clínica, promedio histórico o modelo simple.",
            height=80
        )
        tecnica = st.multiselect(
            "Técnica probable",
            [
                "Reglas clínicas", "Regresión logística", "Machine Learning clásico",
                "Gradient Boosting", "Deep Learning", "Computer Vision", "NLP",
                "IA generativa", "Series temporales", "Reglas + IA", "No definido aún"
            ]
        )

    for k, v in {
        "datos": datos,
        "fuente": fuente,
        "disponibilidad": disponibilidad,
        "volumen": volumen,
        "calidad": calidad,
        "etiqueta": etiqueta,
        "linea_base": linea_base,
        "tecnica": tecnica
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 5. MVP
# ------------------------------------------------------------
with tabs[4]:
    st.header("5. Diseñar el MVP")
    st.info("El MVP debe hacer una sola cosa útil, verificable y segura.")

    funcion = st.text_area(
        "Función mínima",
        placeholder="Mi MVP hará solamente...",
        height=85
    )
    no_hara = st.text_area(
        "¿Qué NO hará?",
        placeholder="No diagnosticará, no formulará tratamiento, no reemplazará criterio profesional.",
        height=85
    )

    c1, c2 = st.columns(2)
    with c1:
        entrada_mvp = st.text_area("Entrada", height=75)
        procesamiento_mvp = st.text_area("Procesamiento mínimo", height=75)
        salida = st.selectbox(
            "Salida principal",
            [
                "Alerta", "Resumen", "Priorización", "Clasificación de riesgo",
                "Pronóstico", "Extracción estructurada", "Recomendación supervisada",
                "Reporte", "Tablero", "Otro"
            ]
        )

    with c2:
        salida_visible = st.text_area("¿Qué verá exactamente el usuario?", height=75)
        accion_usuario = st.text_area("¿Qué hará el usuario después?", height=75)
        valor = st.text_area("Valor clínico u operativo esperado", height=75)

    for k, v in {
        "funcion": funcion,
        "no_hara": no_hara,
        "entrada_mvp": entrada_mvp,
        "procesamiento_mvp": procesamiento_mvp,
        "salida": salida,
        "salida_visible": salida_visible,
        "accion_usuario": accion_usuario,
        "valor": valor
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 6. RIESGOS
# ------------------------------------------------------------
with tabs[5]:
    st.header("6. Riesgos, supervisión y gobernanza")

    riesgo = st.selectbox(
        "Riesgo principal",
        [
            "Falso negativo", "Falso positivo", "Sesgo poblacional", "Sobreconfianza",
            "Datos incompletos", "Privacidad", "Falla de integración",
            "Alucinación", "Uso fuera de alcance", "Otro"
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        peor = st.text_area("Peor escenario", height=80)
        mitigacion = st.text_area("Mitigación", height=80)
        seguridad = st.slider("Nivel estimado de control", 1, 5, 3)

    with c2:
        supervisor = st.text_input("¿Quién revisará la salida?")
        baja_confianza = st.text_area(
            "¿Qué hará el sistema con baja confianza o datos insuficientes?",
            height=80
        )
        correccion_usuario = st.selectbox(
            "¿El usuario puede corregir o rechazar?",
            ["No definido", "Sí", "No"]
        )

    privacidad = st.multiselect(
        "Controles previstos",
        [
            "Anonimización / seudonimización", "Control de acceso",
            "Registro de auditoría", "Consentimiento o base legal",
            "Aprobación institucional", "Comité de ética",
            "Evaluación de seguridad", "Gestión de incidentes"
        ]
    )

    for k, v in {
        "riesgo": riesgo,
        "peor": peor,
        "mitigacion": mitigacion,
        "seguridad": seguridad,
        "supervisor": supervisor,
        "baja_confianza": baja_confianza,
        "correccion_usuario": correccion_usuario,
        "privacidad": privacidad
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 7. VALIDACIÓN Y KPIS
# ------------------------------------------------------------
with tabs[6]:
    st.header("7. Validación y KPIs")

    validaciones = st.multiselect(
        "Tipos de validación",
        [
            "Validación técnica interna", "Validación con expertos",
            "Prueba de usabilidad", "Validación clínica retrospectiva",
            "Validación prospectiva", "Evaluación operativa",
            "Evaluación de sesgo", "Evaluación de calibración"
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        kpis = st.multiselect(
            "Máximo 4 KPIs",
            [
                "Tiempo ahorrado", "Concordancia con experto", "Sensibilidad",
                "Especificidad", "Precisión", "AUPRC", "AUROC", "F1",
                "Calibración", "Tasa de falsos negativos", "Satisfacción del usuario",
                "Casos priorizados correctamente", "Reducción de errores",
                "Costo por caso", "Adherencia al uso", "MAE / RMSE", "WAPE / MAPE"
            ],
            max_selections=4
        )
        meta = st.text_area("Meta cuantificable", height=80)

    with c2:
        medicion = st.text_area("Cómo se medirá", height=80)
        muestra_validacion = st.number_input(
            "Casos para validación inicial",
            min_value=0,
            max_value=1000000,
            value=0,
            step=10
        )
        criterio_avance = st.text_area("Criterio para avanzar al piloto", height=80)

    for k, v in {
        "validaciones": validaciones,
        "kpis": kpis,
        "meta": meta,
        "medicion": medicion,
        "muestra_validacion": muestra_validacion,
        "criterio_avance": criterio_avance
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 8. PILOTO
# ------------------------------------------------------------
with tabs[7]:
    st.header("8. Plan piloto")

    c1, c2 = st.columns(2)
    with c1:
        lugar = st.selectbox(
            "Lugar del piloto",
            [
                "Urgencias", "Radiología", "Patología", "Consulta externa",
                "Hospitalización", "Farmacia", "Comité / junta médica",
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

    with c2:
        casos = st.number_input(
            "Casos a evaluar",
            min_value=1,
            max_value=100000,
            value=50
        )
        criterio_stop = st.text_area("Criterio de detención", height=80)
        responsable_piloto = st.text_input("Responsable del piloto")

    for k, v in {
        "lugar": lugar,
        "duracion": duracion,
        "usuarios": usuarios,
        "casos": casos,
        "criterio_stop": criterio_stop,
        "responsable_piloto": responsable_piloto
    }.items():
        save(k, v)

# ------------------------------------------------------------
# 9. ESCALAMIENTO
# ------------------------------------------------------------
with tabs[8]:
    st.header("9. Escalamiento y propiedad intelectual")

    escala = st.text_area("Ruta de escalamiento", height=90)
    pi = st.multiselect(
        "Propiedad intelectual potencial",
        [
            "Software", "Algoritmo / modelo", "Dataset curado",
            "Flujo clínico", "Interfaz", "Método de validación",
            "Marca", "Secreto industrial"
        ]
    )
    aliados = st.text_area("Aliados necesarios", height=75)
    integracion = st.multiselect(
        "Integraciones futuras",
        ["HIS", "PACS", "LIS", "ERP", "API", "Repositorio documental", "Otra"]
    )

    for k, v in {
        "escala": escala,
        "pi": pi,
        "aliados": aliados,
        "integracion": integracion
    }.items():
        save(k, v)


# ============================================================
# FUNCIONES DE EVALUACIÓN
# ============================================================
def maturity_score(d):
    score = 0
    weighted = {
        "problema": 4,
        "evidencia_problema": 3,
        "decision": 3,
        "flujo_mvp": 3,
        "responsable_final": 3,
        "variable_objetivo": 5,
        "definicion_positiva": 4,
        "horizonte": 3,
        "poblacion": 2,
        "exclusion": 2,
        "fuente": 3,
        "etiqueta": 3,
        "linea_base": 4,
        "funcion": 4,
        "no_hara": 3,
        "entrada_mvp": 2,
        "salida_visible": 2,
        "accion_usuario": 3,
        "valor": 2,
        "peor": 3,
        "mitigacion": 4,
        "supervisor": 2,
        "baja_confianza": 3,
        "meta": 3,
        "criterio_avance": 3,
        "criterio_stop": 2,
        "escala": 2
    }

    for key, points in weighted.items():
        if text_ok(d, key, 6 if points <= 2 else 8):
            score += points

    score += 3 if d.get("datos") else 0
    score += 4 if d.get("disponibilidad") in [
        "Disponible sin depurar",
        "Disponible y depurada",
        "Disponible y lista para análisis"
    ] else 0
    score += 2 if int(d.get("volumen", 0)) > 0 else 0
    score += 2 if d.get("correccion_usuario") == "Sí" else 0
    score += 2 if len(d.get("privacidad", [])) >= 2 else 0
    score += 3 if len(d.get("validaciones", [])) >= 2 else 0
    score += 3 if len(d.get("kpis", [])) >= 2 else 0
    score += 2 if int(d.get("muestra_validacion", 0)) > 0 else 0

    return min(score, 100)


def maturity_level(score, d):
    blockers = []

    for key, label in [
        ("variable_objetivo", "variable objetivo"),
        ("linea_base", "línea base"),
        ("mitigacion", "mitigación"),
        ("criterio_avance", "criterio de avance")
    ]:
        if not text_ok(d, key, 8):
            blockers.append(label)

    if len(d.get("validaciones", [])) < 2:
        blockers.append("plan de validación")

    if score < 40:
        return (
            "🔴 NIVEL 1: IDEA",
            "El problema está identificado, pero el MVP aún no está definido.",
            "Definir objetivo, datos, función mínima y riesgos.",
            blockers
        )
    if score < 65:
        return (
            "🟡 NIVEL 2: PROTOTIPO CONCEPTUAL",
            "Existe una estructura inicial, pero falta viabilidad.",
            "Fortalecer datos, línea base, validación y supervisión.",
            blockers
        )
    if score < 85 or blockers:
        return (
            "🟢 NIVEL 3: MVP DEFINIDO",
            "El MVP puede avanzar a validación inicial.",
            "Resolver elementos bloqueantes antes del piloto.",
            blockers
        )
    return (
        "🔵 NIVEL 4: CANDIDATO A PILOTO",
        "Cuenta con objetivo, datos, seguridad y validación.",
        "Realizar revisión institucional antes de ejecutarlo.",
        blockers
    )


def innovation_score(d):
    return {
        "Impacto": min(
            10,
            (4 if text_ok(d, "problema", 20) else 0) +
            (3 if text_ok(d, "valor") else 0) +
            (3 if text_ok(d, "meta") else 0)
        ),
        "Factibilidad": min(
            10,
            (3 if text_ok(d, "funcion") else 0) +
            (3 if text_ok(d, "linea_base") else 0) +
            (4 if d.get("disponibilidad") in [
                "Disponible sin depurar",
                "Disponible y depurada",
                "Disponible y lista para análisis"
            ] else 0)
        ),
        "Datos": min(
            10,
            int(d.get("calidad", 0)) * 2 + (2 if text_ok(d, "etiqueta") else 0)
        ),
        "Escalabilidad": min(
            10,
            (4 if text_ok(d, "escala") else 0) +
            (3 if text_ok(d, "aliados") else 0) +
            (2 if d.get("pi") else 0) +
            (1 if d.get("integracion") else 0)
        ),
        "Control del riesgo": min(
            10,
            (3 if text_ok(d, "mitigacion") else 0) +
            (2 if text_ok(d, "baja_confianza") else 0) +
            (2 if text_ok(d, "supervisor") else 0) +
            (2 if len(d.get("privacidad", [])) >= 2 else 0) +
            (1 if d.get("correccion_usuario") == "Sí" else 0)
        )
    }


def recommendations(d):
    recs = []
    checks = [
        ("variable_objetivo", "Definir una variable objetivo concreta y medible."),
        ("definicion_positiva", "Precisar cómo se determina el resultado correcto."),
        ("linea_base", "Definir una línea base antes de comparar modelos avanzados."),
        ("baja_confianza", "Diseñar el comportamiento ante baja confianza o datos incompletos."),
        ("criterio_avance", "Establecer un criterio cuantificable para avanzar al piloto."),
        ("criterio_stop", "Definir cuándo detener el piloto por seguridad.")
    ]
    for key, msg in checks:
        if not text_ok(d, key, 8):
            recs.append(msg)

    if d.get("disponibilidad") in ["No confirmada", "Parcial"]:
        recs.append("Confirmar acceso, permisos, calidad y volumen real de datos.")
    if len(d.get("validaciones", [])) < 2:
        recs.append("Incluir validación técnica y validación con expertos o usuarios.")
    if d.get("correccion_usuario") != "Sí":
        recs.append("Permitir que el profesional corrija o rechace la salida.")

    return recs[:7] or ["El proyecto está bien estructurado; sigue la revisión institucional."]


# ============================================================
# FUNCIONES DE CONTENIDO
# ============================================================
def build_summary(d, score, level, innovation, blockers):
    rec_text = "\n".join(f"- {r}" for r in recommendations(d))
    blockers_text = ", ".join(blockers) if blockers else "Ninguno"

    return f"""# {d.get('nombre', 'MVP sin nombre')}

## Problema
**Área:** {d.get('area', '')}
**Problema:** {d.get('problema', '')}
**Evidencia:** {d.get('evidencia_problema', '')}
**Usuario:** {d.get('usuario', '')}
**Decisión:** {d.get('decision', '')}

## Variable objetivo
**Tarea:** {d.get('tarea_ia', '')}
**Resultado:** {d.get('variable_objetivo', '')}
**Definición:** {d.get('definicion_positiva', '')}
**Horizonte:** {d.get('horizonte', '')}
**Población:** {d.get('poblacion', '')}

## Datos y línea base
**Datos:** {', '.join(d.get('datos', []))}
**Fuente:** {d.get('fuente', '')}
**Disponibilidad:** {d.get('disponibilidad', '')}
**Verdad de referencia:** {d.get('etiqueta', '')}
**Línea base:** {d.get('linea_base', '')}

## MVP
**Función mínima:** {d.get('funcion', '')}
**No hará:** {d.get('no_hara', '')}
**Entrada:** {d.get('entrada_mvp', '')}
**Salida:** {d.get('salida_visible', '')}
**Acción del usuario:** {d.get('accion_usuario', '')}

## Seguridad
**Riesgo:** {d.get('riesgo', '')}
**Mitigación:** {d.get('mitigacion', '')}
**Supervisor:** {d.get('supervisor', '')}
**Baja confianza:** {d.get('baja_confianza', '')}

## Validación y piloto
**Validaciones:** {', '.join(d.get('validaciones', []))}
**KPIs:** {', '.join(d.get('kpis', []))}
**Meta:** {d.get('meta', '')}
**Piloto:** {d.get('lugar', '')} durante {d.get('duracion', '')} con {d.get('casos', '')} casos

## Resultado automático
**Madurez:** {level} ({score}/100)
**Innovación:** {innovation}/50
**Bloqueantes:** {blockers_text}

## Recomendaciones
{rec_text}
"""


def build_pitch_slides(d, score, level, innovation):
    slide_1 = {
        "title": "1. El problema",
        "content": [
            f"Proyecto: {d.get('nombre', '')}",
            f"Área: {d.get('area', '')}",
            f"Problema: {d.get('problema', '')}",
            f"Consecuencia: {d.get('consecuencia', '')}",
            f"Evidencia: {d.get('evidencia_problema', '')}",
        ]
    }

    slide_2 = {
        "title": "2. Usuario y oportunidad",
        "content": [
            f"Usuario principal: {d.get('usuario', '')}",
            f"Momento del flujo: {d.get('momento', '')}",
            f"Decisión apoyada: {d.get('decision', '')}",
            f"Responsable final: {d.get('responsable_final', '')}",
            f"Población objetivo: {d.get('poblacion', '')}",
        ]
    }

    slide_3 = {
        "title": "3. La solución MVP",
        "content": [
            f"Variable objetivo: {d.get('variable_objetivo', '')}",
            f"Función mínima: {d.get('funcion', '')}",
            f"Entrada: {d.get('entrada_mvp', '')}",
            f"Salida visible: {d.get('salida_visible', '')}",
            f"Acción del usuario: {d.get('accion_usuario', '')}",
            f"Línea base: {d.get('linea_base', '')}",
        ]
    }

    slide_4 = {
        "title": "4. Evidencia, seguridad y métricas",
        "content": [
            f"Datos: {', '.join(d.get('datos', []))}",
            f"Técnica probable: {', '.join(d.get('tecnica', []))}",
            f"Riesgo principal: {d.get('riesgo', '')}",
            f"Mitigación: {d.get('mitigacion', '')}",
            f"KPIs: {', '.join(d.get('kpis', []))}",
            f"Meta: {d.get('meta', '')}",
        ]
    }

    slide_5 = {
        "title": "5. Piloto y llamado a la acción",
        "content": [
            f"Piloto: {d.get('lugar', '')} | {d.get('duracion', '')} | {d.get('casos', '')} casos",
            f"Responsable del piloto: {d.get('responsable_piloto', '')}",
            f"Escalamiento: {d.get('escala', '')}",
            f"Nivel de madurez: {level} ({score}/100)",
            f"Potencial de innovación: {innovation}/50",
            "Siguiente paso: validar, priorizar y preparar piloto institucional.",
        ]
    }

    return [slide_1, slide_2, slide_3, slide_4, slide_5]


def slides_to_markdown(slides):
    parts = []
    for slide in slides:
        parts.append(f"# {slide['title']}\n")
        for item in slide["content"]:
            parts.append(f"- {item}\n")
        parts.append("\n")
    return "".join(parts)


# ============================================================
# EXPORTACIÓN
# ============================================================
def make_pdf(d, summary):
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
    story = [
        Paragraph("GeniA Innovation Builder", styles["Title"]),
        Spacer(1, 12)
    ]

    rows = [
        ["Campo", "Respuesta"],
        ["Proyecto", d.get("nombre", "")],
        ["Problema", d.get("problema", "")],
        ["Usuario", d.get("usuario", "")],
        ["Variable objetivo", d.get("variable_objetivo", "")],
        ["Función mínima", d.get("funcion", "")],
        ["Línea base", d.get("linea_base", "")],
        ["Riesgo", d.get("riesgo", "")],
        ["Mitigación", d.get("mitigacion", "")],
        ["KPIs", ", ".join(d.get("kpis", []))],
        ["Piloto", f"{d.get('lugar', '')} | {d.get('duracion', '')} | {d.get('casos', '')} casos"],
    ]

    table = Table(rows, colWidths=[125, 365], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B2E4A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), .5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EAF3F8"))
    ]))

    story += [
        table,
        Spacer(1, 12),
        Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"])
    ]
    doc.build(story)
    buffer.seek(0)
    return buffer


def make_pptx(slides, project_name="pitch"):
    if not PPTX_AVAILABLE:
        return None

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for slide_data in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Fondo
        background = slide.background.fill
        background.solid()
        background.fore_color.rgb = __import__("pptx.dml.color").dml.color.RGBColor(11, 46, 74)

        # Título
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.0), Inches(0.8))
        title_tf = title_box.text_frame
        title_p = title_tf.paragraphs[0]
        title_run = title_p.add_run()
        title_run.text = slide_data["title"]
        title_run.font.size = Pt(26)
        title_run.font.bold = True
        title_run.font.color.rgb = __import__("pptx.dml.color").dml.color.RGBColor(240, 90, 40)

        # Contenido
        body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.8), Inches(5.4))
        body_tf = body_box.text_frame
        body_tf.word_wrap = True

        first = True
        for item in slide_data["content"]:
            if first:
                p = body_tf.paragraphs[0]
                first = False
            else:
                p = body_tf.add_paragraph()
            p.text = f"• {item}"
            p.level = 0
            p.font.size = Pt(18)
            p.font.color.rgb = __import__("pptx.dml.color").dml.color.RGBColor(255, 255, 255)

    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output


def make_scores_chart(scores_dict):
    if not MATPLOTLIB_AVAILABLE:
        return None

    labels = list(scores_dict.keys())
    values = list(scores_dict.values())

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, values)
    ax.set_ylim(0, 10)
    ax.set_title("Madurez / Potencial de innovación")
    ax.set_ylabel("Puntaje")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer


def wrap_lines(text, width=70):
    if not text:
        return [""]
    lines = []
    for paragraph in str(text).split("\n"):
        wrapped = textwrap.wrap(paragraph, width=width) or [""]
        lines.extend(wrapped)
    return lines


def make_canvas_png(d, score, level, innovation, blockers):
    if not PIL_AVAILABLE:
        return None

    width, height = 1600, 1100
    image = Image.new("RGB", (width, height), (11, 46, 74))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        section_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
        text_font = ImageFont.truetype("DejaVuSans.ttf", 22)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 18)
    except Exception:
        title_font = ImageFont.load_default()
        section_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Título
    draw.text((50, 30), "GeniA Innovation Builder - MVP Canvas", fill=(255, 255, 255), font=title_font)
    draw.text((50, 85), f"Proyecto: {d.get('nombre', '')}", fill=(240, 90, 40), font=section_font)

    boxes = [
        ("Problema", d.get("problema", "")),
        ("Usuario / Decisión", f"{d.get('usuario', '')}\n{d.get('decision', '')}"),
        ("Variable objetivo", d.get("variable_objetivo", "")),
        ("Datos / Línea base", f"{', '.join(d.get('datos', []))}\nLínea base: {d.get('linea_base', '')}"),
        ("MVP", f"{d.get('funcion', '')}\nSalida: {d.get('salida_visible', '')}"),
        ("Riesgo / Mitigación", f"{d.get('riesgo', '')}\n{d.get('mitigacion', '')}"),
        ("KPIs / Meta", f"{', '.join(d.get('kpis', []))}\nMeta: {d.get('meta', '')}"),
        ("Piloto / Escalamiento", f"{d.get('lugar', '')} | {d.get('duracion', '')} | {d.get('casos', '')} casos\n{d.get('escala', '')}"),
    ]

    coords = [
        (50, 140, 750, 320),
        (820, 140, 1530, 320),
        (50, 350, 750, 530),
        (820, 350, 1530, 530),
        (50, 560, 750, 740),
        (820, 560, 1530, 740),
        (50, 770, 750, 950),
        (820, 770, 1530, 950),
    ]

    for (title, content), (x1, y1, x2, y2) in zip(boxes, coords):
        draw.rounded_rectangle((x1, y1, x2, y2), radius=18, fill=(255, 255, 255), outline=(240, 90, 40), width=3)
        draw.text((x1 + 20, y1 + 15), title, fill=(11, 46, 74), font=section_font)

        y_text = y1 + 55
        for line in wrap_lines(content, width=48):
            draw.text((x1 + 20, y_text), line, fill=(11, 46, 74), font=small_font)
            y_text += 24

    footer_y = 980
    draw.rounded_rectangle((50, footer_y, 1530, 1070), radius=18, fill=(240, 90, 40))
    footer_text = (
        f"Madurez: {level} ({score}/100) | Innovación: {innovation}/50 | "
        f"Bloqueantes: {', '.join(blockers) if blockers else 'Ninguno'}"
    )
    draw.text((70, footer_y + 18), footer_text, fill=(255, 255, 255), font=section_font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


# ============================================================
# RESULTADOS
# ============================================================
with tabs[9]:
    st.header("10. Resultado del MVP")

    d = st.session_state.data
    score = maturity_score(d)
    level, interpretation, next_step, blockers = maturity_level(score, d)
    scores = innovation_score(d)
    innovation = sum(scores.values())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Madurez", f"{score}/100")
    c2.metric("Innovación", f"{innovation}/50")
    c3.metric("KPIs", len(d.get("kpis", [])))
    c4.metric("Validaciones", len(d.get("validaciones", [])))

    st.markdown(
        f"""
        <div class="maturity-card">
            <h2>{level}</h2>
            <p><b>Interpretación:</b> {interpretation}</p>
            <p><b>Próximo paso:</b> {next_step}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if blockers:
        st.warning("Elementos bloqueantes: " + ", ".join(blockers))
    else:
        st.success("No se identificaron elementos bloqueantes principales.")

    st.subheader("Potencial de innovación")
    for item, value in scores.items():
        st.progress(value / 10, text=f"{item}: {value}/10")

    st.subheader("Recomendaciones")
    for rec in recommendations(d):
        st.write("• " + rec)

    # Resumen
    summary = build_summary(d, score, level, innovation, blockers)
    st.subheader("Resumen del MVP")
    st.text_area(
        "Resumen generado",
        value=summary,
        height=360,
        key="summary_preview"
    )

    # Pitch 5 slides
    slides = build_pitch_slides(d, score, level, innovation)
    pitch_md = slides_to_markdown(slides)

    st.subheader("Elevator pitch de 5 diapositivas")
    for idx, slide in enumerate(slides, start=1):
        with st.expander(slide["title"], expanded=(idx == 1)):
            content_text = "\n".join([f"• {x}" for x in slide["content"]])
            st.text_area(
                f"Contenido {idx}",
                value=content_text,
                height=180,
                key=f"slide_preview_{idx}"
            )

    filename = safe_filename(d.get("nombre"))

    # Descargas de texto
    st.download_button(
        "📥 Descargar resumen en Markdown",
        summary.encode("utf-8"),
        file_name=f"genia_mvp_{filename}.md",
        mime="text/markdown"
    )

    st.download_button(
        "🎤 Descargar elevator pitch en Markdown",
        pitch_md.encode("utf-8"),
        file_name=f"pitch_5_slides_{filename}.md",
        mime="text/markdown"
    )

    # PPTX
    pptx_file = make_pptx(slides, filename)
    if pptx_file:
        st.download_button(
            "📊 Descargar elevator pitch en PowerPoint (.pptx)",
            pptx_file,
            file_name=f"pitch_5_slides_{filename}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        st.caption("Para exportar PowerPoint instala: pip install python-pptx")

    # PNG Chart
    chart_file = make_scores_chart(scores)
    if chart_file:
        st.download_button(
            "📈 Descargar figura de innovación (.png)",
            chart_file,
            file_name=f"innovacion_{filename}.png",
            mime="image/png"
        )
        st.image(chart_file, caption="Vista previa: figura de innovación", use_container_width=True)
    else:
        st.caption("Para exportar la figura instala: pip install matplotlib")

    # PNG Canvas
    canvas_file = make_canvas_png(d, score, level, innovation, blockers)
    if canvas_file:
        st.download_button(
            "🖼️ Descargar canvas visual del MVP (.png)",
            canvas_file,
            file_name=f"canvas_mvp_{filename}.png",
            mime="image/png"
        )
        st.image(canvas_file, caption="Vista previa: canvas visual del MVP", use_container_width=True)
    else:
        st.caption("Para exportar el canvas visual instala: pip install pillow")

    # PDF
    pdf = make_pdf(d, summary)
    if pdf:
        st.download_button(
            "📄 Descargar Canvas en PDF",
            pdf,
            file_name=f"genia_mvp_canvas_{filename}.pdf",
            mime="application/pdf"
        )
    else:
        st.caption("Para exportar PDF instala: pip install reportlab")


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Guía docente")
st.sidebar.markdown("""
1. Cada grupo completa las secciones 1–9.  
2. Revisa madurez y bloqueantes.  
3. Ajusta su propuesta.  
4. Descarga el Canvas.  
5. Presenta un pitch de 5 diapositivas.

**Principio:**  
el algoritmo no es el MVP.  
El MVP integra problema, usuario, datos, salida, acción, validación y seguridad.
""")

st.sidebar.markdown("### Librerías recomendadas")
st.sidebar.code(
    "streamlit\nreportlab\npython-pptx\npillow\nmatplotlib",
    language="text"
)

if st.sidebar.button("Reiniciar formulario"):
    st.session_state.data = {}
    st.rerun()
