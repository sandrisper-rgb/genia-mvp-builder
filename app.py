
import streamlit as st
from datetime import datetime
from io import BytesIO
import pandas as pd

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

st.set_page_config(
    page_title="GeniA MVP Builder",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.main {background-color: #f7f9fc;}
.block-container {padding-top: 2rem;}
div[data-testid="stMetricValue"] {font-size: 28px;}
.card {
    padding: 1.2rem;
    border-radius: 18px;
    background-color: white;
    border: 1px solid #d9e2ef;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
}
.small-note {font-size: 0.9rem; color: #5b667a;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 GeniA MVP Builder")
st.caption("Programa de Inteligencia Artificial — Los Cobos Medical Center")
st.markdown("### Del reto clínico a un Producto Mínimo Viable en salud")

with st.expander("¿Qué es un MVP en salud?", expanded=True):
    st.markdown("""
    Un **MVP en salud** es la versión más simple, segura y medible de una solución de IA que permite probar
    si realmente genera valor clínico antes de invertir en un desarrollo completo.

    **Debe ser:** específico, seguro, medible, supervisado y escalable.  
    **No debe ser:** una app completa, una IA autónoma ni un reemplazo del médico.
    """)

st.divider()

if "data" not in st.session_state:
    st.session_state.data = {}

def save(key, value):
    st.session_state.data[key] = value

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
    for k, v in {
        "nombre": nombre, "area": area, "tipo_problema": tipo_problema,
        "problema": problema, "consecuencia": consecuencia
    }.items():
        save(k, v)

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
    flujo_actual = st.text_area("Flujo actual sin IA", placeholder="Paciente → datos → médico revisa manualmente → decisión", height=100)
    flujo_mvp = st.text_area("Flujo propuesto con MVP", placeholder="Paciente → datos → MVP alerta/resume/prioriza → médico decide", height=100)
    save("usuario", usuario); save("momento", momento); save("flujo_actual", flujo_actual); save("flujo_mvp", flujo_mvp)

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
    fuente = st.text_area("Fuente de los datos", placeholder="Ejemplo: HIS, PACS, LIS, registros retrospectivos, formularios de captura.", height=80)
    calidad = st.slider("Calidad percibida de los datos", 1, 5, 3)
    save("datos", datos); save("tecnica", tecnica); save("fuente", fuente); save("calidad", calidad)

with tabs[3]:
    st.header("4. Definir el MVP")
    st.info("Regla: eliminen el 80% de las funcionalidades. El MVP debe hacer una sola cosa muy bien.")
    funcion = st.text_area("Función mínima del MVP", placeholder="Mi MVP hará solamente...", height=100)
    no_hara = st.text_area("¿Qué NO hará el MVP?", placeholder="Ejemplo: no diagnosticará, no formulará tratamiento, no reemplazará criterio médico.", height=100)
    salida = st.selectbox("Salida principal del MVP", [
        "Alerta", "Resumen", "Priorización", "Clasificación de riesgo",
        "Recomendación supervisada", "Reporte", "Tablero de control", "Otro"
    ])
    valor = st.text_area("Valor clínico esperado", placeholder="Ejemplo: disminuir tiempo de lectura, mejorar priorización, reducir omisiones.", height=80)
    save("funcion", funcion); save("no_hara", no_hara); save("salida", salida); save("valor", valor)

with tabs[4]:
    st.header("5. Riesgos y mitigación")
    riesgo = st.selectbox("Riesgo principal", [
        "Falso negativo", "Falso positivo", "Sesgo poblacional", "Sobreconfianza del usuario",
        "Datos incompletos", "Privacidad", "Falla de integración", "Otro"
    ])
    peor = st.text_area("Peor escenario clínico", placeholder="Ejemplo: el sistema no alerta un paciente que se deteriora.", height=90)
    mitigacion = st.text_area("Mitigación", placeholder="Ejemplo: supervisión médica, uso como apoyo, control interno, auditoría semanal.", height=90)
    seguridad = st.slider("Nivel de control del riesgo", 1, 5, 3)
    save("riesgo", riesgo); save("peor", peor); save("mitigacion", mitigacion); save("seguridad", seguridad)

with tabs[5]:
    st.header("6. KPIs: ¿cómo sabremos que funciona?")
    kpis = st.multiselect("Seleccionen máximo 3 KPIs principales", [
        "Tiempo ahorrado", "Concordancia con experto", "Sensibilidad",
        "Especificidad", "Tasa de falsos negativos", "Satisfacción del usuario",
        "Casos priorizados correctamente", "Reducción de errores",
        "Costo por caso", "Adherencia al uso"
    ], max_selections=3)
    meta = st.text_area("Meta del piloto", placeholder="Ejemplo: reducir 20% el tiempo de revisión sin aumentar falsos negativos.", height=90)
    medicion = st.text_area("Cómo se medirá", placeholder="Ejemplo: comparación antes/después, revisión por experto, encuesta de satisfacción.", height=90)
    save("kpis", kpis); save("meta", meta); save("medicion", medicion)

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
    criterio_stop = st.text_area("Criterio de detención", placeholder="Ejemplo: si el control interno falla, si aumenta el tiempo, si hay evento adverso.", height=80)
    save("lugar", lugar); save("duracion", duracion); save("usuarios", usuarios); save("casos", casos); save("criterio_stop", criterio_stop)

with tabs[7]:
    st.header("8. Escalamiento y propiedad intelectual")
    escala = st.text_area("Ruta de escalamiento", placeholder="MVP → piloto en un servicio → integración HIS/PACS/LIS → más servicios → red clínica", height=100)
    pi = st.multiselect("¿Dónde podría estar la PI?", [
        "Software", "Algoritmo/modelo", "Dataset curado", "Flujo clínico",
        "Interfaz de usuario", "Método de validación", "Marca", "Secreto industrial"
    ])
    aliados = st.text_area("Aliados necesarios", placeholder="Ejemplo: TI, ética, calidad, dirección médica, servicio clínico, jurídico.", height=80)
    save("escala", escala); save("pi", pi); save("aliados", aliados)

def maturity_score(d):
    score = 0
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
    score += sum(checks) * 8
    score += int(d.get("calidad", 0)) * 2
    score += int(d.get("seguridad", 0)) * 2
    return min(score, 100)

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

def make_pdf(d):
    if not REPORTLAB_AVAILABLE:
        return None
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("GeniA MVP Builder - Canvas de Producto Mínimo Viable", styles["Title"]))
    story.append(Spacer(1, 12))
    rows = [
        ["Campo", "Respuesta"],
        ["Proyecto", d.get("nombre","")],
        ["Área", d.get("area","")],
        ["Problema clínico", d.get("problema","")],
        ["Usuario", d.get("usuario","")],
        ["Función mínima", d.get("funcion","")],
        ["Lo que NO hará", d.get("no_hara","")],
        ["Datos", ", ".join(d.get("datos", []))],
        ["Riesgo", d.get("riesgo","")],
        ["Mitigación", d.get("mitigacion","")],
        ["KPIs", ", ".join(d.get("kpis", []))],
        ["Piloto", f"{d.get('lugar','')} | {d.get('duracion','')} | {d.get('casos','')} casos"],
        ["Escalamiento", d.get("escala","")],
        ["PI potencial", ", ".join(d.get("pi", []))]
    ]
    table = Table(rows, colWidths=[130, 360])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0B2E4A")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,1), (0,-1), colors.HexColor("#EAF3F8")),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    doc.build(story)
    buffer.seek(0)
    return buffer

with tabs[8]:
    st.header("9. Resultado del MVP")
    d = st.session_state.data
    score = maturity_score(d)
    col1, col2, col3 = st.columns(3)
    col1.metric("Madurez MVP", f"{score}/100")
    col2.metric("KPIs definidos", len(d.get("kpis", [])))
    col3.metric("Datos seleccionados", len(d.get("datos", [])))

    if score < 50:
        st.warning("El MVP todavía está muy amplio o incompleto. Revisen problema, función mínima, riesgo y KPIs.")
    elif score < 80:
        st.info("Buen avance. Ajusten métricas, riesgos y plan piloto antes del pitch.")
    else:
        st.success("MVP listo para pitch y discusión de escalamiento.")

    summary = build_summary(d)
    st.markdown(summary)

    st.download_button(
        "📥 Descargar resumen en Markdown",
        data=summary.encode("utf-8"),
        file_name=f"genia_mvp_{d.get('nombre','proyecto').replace(' ','_')}.md",
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

st.sidebar.title("Guía docente")
st.sidebar.markdown("""
**Uso en clase**
1. Cada grupo abre la app.
2. Llena las secciones 1–8.
3. Revisa madurez.
4. Descarga el Canvas.
5. Presenta pitch de 3 minutos.

**Pitch final**
- Problema
- Usuario
- MVP
- Datos
- KPIs
- Riesgo
- Piloto
- Escalamiento
""")
