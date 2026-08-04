from pathlib import Path

source = Path("/mnt/data/Pasted text(13).txt")
target = Path("/mnt/data/genia_streamlit_multiusuario_mvp_integrado.py")

code = source.read_text(encoding="utf-8")

old_block = '''with tabs[4]:
    st.header("5. Diseñar el MVP")
    st.info("El MVP debe hacer una sola cosa útil, verificable y segura.")
    funcion = st.text_area("Función mínima", placeholder="Mi MVP hará solamente...", height=85)
    no_hara = st.text_area("¿Qué NO hará?", placeholder="No diagnosticará, no formulará tratamiento, no reemplazará criterio profesional.", height=85)
    c1, c2 = st.columns(2)
    with c1:
        entrada_mvp = st.text_area("Entrada", height=75)
        procesamiento_mvp = st.text_area("Procesamiento mínimo", height=75)
        salida = st.selectbox("Salida principal", ["Alerta","Resumen","Priorización","Clasificación de riesgo","Pronóstico","Extracción estructurada","Recomendación supervisada","Reporte","Tablero","Otro"])
    with c2:
        salida_visible = st.text_area("¿Qué verá exactamente el usuario?", height=75)
        accion_usuario = st.text_area("¿Qué hará el usuario después?", height=75)
        valor = st.text_area("Valor clínico u operativo esperado", height=75)
    for k, v in {"funcion":funcion,"no_hara":no_hara,"entrada_mvp":entrada_mvp,"procesamiento_mvp":procesamiento_mvp,"salida":salida,"salida_visible":salida_visible,"accion_usuario":accion_usuario,"valor":valor}.items(): save(k,v)
'''

new_block = '''with tabs[4]:
    st.header("5. Diseñar el MVP")
    st.info("El MVP debe hacer una sola cosa útil, verificable y segura.")
    funcion = st.text_area(
        "Función mínima",
        placeholder="Mi MVP hará solamente...",
        height=85,
        value=st.session_state.data.get("funcion", "")
    )
    no_hara = st.text_area(
        "¿Qué NO hará?",
        placeholder="No diagnosticará, no formulará tratamiento, no reemplazará criterio profesional.",
        height=85,
        value=st.session_state.data.get("no_hara", "")
    )

    c1, c2 = st.columns(2)
    with c1:
        entrada_mvp = st.text_area(
            "Entrada",
            height=75,
            value=st.session_state.data.get("entrada_mvp", "")
        )
        procesamiento_mvp = st.text_area(
            "Procesamiento mínimo",
            height=75,
            value=st.session_state.data.get("procesamiento_mvp", "")
        )
        opciones_salida = [
            "Alerta","Resumen","Priorización","Clasificación de riesgo","Pronóstico",
            "Extracción estructurada","Recomendación supervisada","Reporte","Tablero","Otro"
        ]
        salida_actual = st.session_state.data.get("salida", "Alerta")
        salida = st.selectbox(
            "Salida principal",
            opciones_salida,
            index=opciones_salida.index(salida_actual) if salida_actual in opciones_salida else 0
        )
    with c2:
        salida_visible = st.text_area(
            "¿Qué verá exactamente el usuario?",
            height=75,
            value=st.session_state.data.get("salida_visible", "")
        )
        accion_usuario = st.text_area(
            "¿Qué hará el usuario después?",
            height=75,
            value=st.session_state.data.get("accion_usuario", "")
        )
        valor = st.text_area(
            "Valor clínico u operativo esperado",
            height=75,
            value=st.session_state.data.get("valor", "")
        )

    st.subheader("Integración, interoperabilidad y operación")

    c3, c4 = st.columns(2)

    with c3:
        integracion_mvp = st.multiselect(
            "¿Con qué sistemas deberá integrarse el MVP?",
            [
                "Historia clínica electrónica (HCE / HIS)",
                "Sistema de laboratorio clínico (LIS)",
                "Sistema de imágenes médicas (PACS / RIS)",
                "ERP o sistema administrativo",
                "Repositorio documental",
                "API externa",
                "Dispositivo médico o wearable",
                "No requiere integración inicial",
                "Otro"
            ],
            default=st.session_state.data.get("integracion_mvp", [])
        )

        interoperabilidad_hce = st.multiselect(
            "Interoperabilidad con la historia clínica electrónica",
            [
                "HL7 FHIR",
                "HL7 v2",
                "DICOM",
                "SNOMED CT",
                "LOINC",
                "CIE-10 / ICD-10",
                "OMOP Common Data Model",
                "openEHR",
                "API institucional",
                "Formato institucional propio",
                "No definida",
                "No aplica"
            ],
            default=st.session_state.data.get("interoperabilidad_hce", [])
        )

        modalidad_cargue = st.multiselect(
            "Modalidad de cargue de datos",
            [
                "Carga manual por formulario",
                "Carga de archivo CSV / Excel",
                "Carga de documentos PDF",
                "Integración automática mediante API",
                "Conexión directa a base de datos",
                "Intercambio HL7 / FHIR",
                "Carga desde PACS / DICOM",
                "Captura en tiempo real desde dispositivos",
                "Carga por lotes",
                "Otra"
            ],
            default=st.session_state.data.get("modalidad_cargue", [])
        )

    with c4:
        opciones_frecuencia = [
            "En tiempo real",
            "Cada hora",
            "Diaria",
            "Semanal",
            "Mensual",
            "Por evento clínico",
            "Por cada nuevo registro",
            "Carga única para el MVP",
            "A demanda",
            "No definida"
        ]
        frecuencia_actual = st.session_state.data.get(
            "frecuencia_actualizacion",
            "No definida"
        )
        frecuencia_actualizacion = st.selectbox(
            "Periodicidad o frecuencia de actualización de los datos",
            opciones_frecuencia,
            index=opciones_frecuencia.index(frecuencia_actual)
            if frecuencia_actual in opciones_frecuencia else 9
        )

        opciones_inversion = [
            "No definido",
            "Menos de COP $5 millones",
            "COP $5–10 millones",
            "COP $10–20 millones",
            "COP $20–50 millones",
            "Más de COP $50 millones"
        ]
        inversion_actual = st.session_state.data.get(
            "rango_inversion",
            "No definido"
        )
        rango_inversion = st.selectbox(
            "Rango estimado de inversión para el MVP",
            opciones_inversion,
            index=opciones_inversion.index(inversion_actual)
            if inversion_actual in opciones_inversion else 0
        )

        detalle_integracion = st.text_area(
            "Detalle adicional de integración o cargue",
            placeholder=(
                "Ejemplo: inicialmente se cargará un archivo CSV semanal; "
                "en una fase posterior se integrará con la HCE mediante FHIR."
            ),
            height=120,
            value=st.session_state.data.get("detalle_integracion", "")
        )

    for k, v in {
        "funcion": funcion,
        "no_hara": no_hara,
        "entrada_mvp": entrada_mvp,
        "procesamiento_mvp": procesamiento_mvp,
        "salida": salida,
        "salida_visible": salida_visible,
        "accion_usuario": accion_usuario,
        "valor": valor,
        "integracion_mvp": integracion_mvp,
        "interoperabilidad_hce": interoperabilidad_hce,
        "modalidad_cargue": modalidad_cargue,
        "frecuencia_actualizacion": frecuencia_actualizacion,
        "rango_inversion": rango_inversion,
        "detalle_integracion": detalle_integracion
    }.items():
        save(k, v)
'''

if old_block not in code:
    raise RuntimeError("No se encontró el bloque original de la sección 5. MVP.")

code = code.replace(old_block, new_block)

# Incorporar los nuevos campos al resumen.
old_summary = '''**Acción del usuario:** {d.get('accion_usuario','')}

## Seguridad'''
new_summary = '''**Acción del usuario:** {d.get('accion_usuario','')}  
**Integraciones previstas:** {', '.join(d.get('integracion_mvp',[])) or 'No definidas'}  
**Interoperabilidad con HCE:** {', '.join(d.get('interoperabilidad_hce',[])) or 'No definida'}  
**Modalidad de cargue:** {', '.join(d.get('modalidad_cargue',[])) or 'No definida'}  
**Frecuencia de actualización:** {d.get('frecuencia_actualizacion','')}  
**Rango de inversión:** {d.get('rango_inversion','')}  
**Detalle de integración:** {d.get('detalle_integracion','')}

## Seguridad'''
if old_summary not in code:
    raise RuntimeError("No se encontró el punto de inserción del resumen.")
code = code.replace(old_summary, new_summary)

# Incorporar los nuevos campos al PDF.
old_rows = '''rows=[["Campo","Respuesta"],["Proyecto",d.get("nombre","")],["Problema",d.get("problema","")],["Usuario",d.get("usuario","")],["Variable objetivo",d.get("variable_objetivo","")],["Función mínima",d.get("funcion","")],["Línea base",d.get("linea_base","")],["Riesgo",d.get("riesgo","")],["Mitigación",d.get("mitigacion","")],["KPIs",", ".join(d.get("kpis",[]))],["Piloto",f"{d.get('lugar','')} | {d.get('duracion','')} | {d.get('casos','')} casos"]]'''
new_rows = '''rows=[
        ["Campo","Respuesta"],
        ["Proyecto",d.get("nombre","")],
        ["Problema",d.get("problema","")],
        ["Usuario",d.get("usuario","")],
        ["Variable objetivo",d.get("variable_objetivo","")],
        ["Función mínima",d.get("funcion","")],
        ["Integraciones",", ".join(d.get("integracion_mvp",[]))],
        ["Interoperabilidad HCE",", ".join(d.get("interoperabilidad_hce",[]))],
        ["Modalidad de cargue",", ".join(d.get("modalidad_cargue",[]))],
        ["Frecuencia",d.get("frecuencia_actualizacion","")],
        ["Rango de inversión",d.get("rango_inversion","")],
        ["Línea base",d.get("linea_base","")],
        ["Riesgo",d.get("riesgo","")],
        ["Mitigación",d.get("mitigacion","")],
        ["KPIs",", ".join(d.get("kpis",[]))],
        ["Piloto",f"{d.get('lugar','')} | {d.get('duracion','')} | {d.get('casos','')} casos"]
    ]'''
if old_rows not in code:
    raise RuntimeError("No se encontró la tabla del PDF.")
code = code.replace(old_rows, new_rows)

# Incorporar los nuevos campos al elevator pitch.
old_pitch_lines = '''                f"Acción del usuario: {d.get('accion_usuario','') or 'Por definir'}",
                f"Línea base: {d.get('linea_base','') or 'Por definir'}",
            ],'''
new_pitch_lines = '''                f"Acción del usuario: {d.get('accion_usuario','') or 'Por definir'}",
                f"Línea base: {d.get('linea_base','') or 'Por definir'}",
                f"Integración: {', '.join(d.get('integracion_mvp',[])) or 'Por definir'}",
                f"Interoperabilidad HCE: {', '.join(d.get('interoperabilidad_hce',[])) or 'Por definir'}",
                f"Cargue y actualización: {', '.join(d.get('modalidad_cargue',[])) or 'Por definir'} | {d.get('frecuencia_actualizacion','Por definir')}",
                f"Inversión estimada: {d.get('rango_inversion','Por definir')}",
            ],'''
if old_pitch_lines not in code:
    raise RuntimeError("No se encontró el bloque del elevator pitch.")
code = code.replace(old_pitch_lines, new_pitch_lines)

# Incorporar una referencia breve en el Canvas visual.
old_canvas_mvp = '''        (
            "MVP",
            f"{clean_value(d.get('funcion'))}\\n"
            f"Salida: {clean_value(d.get('salida_visible'))}"
        ),'''
new_canvas_mvp = '''        (
            "MVP",
            f"{clean_value(d.get('funcion'))}\\n"
            f"Salida: {clean_value(d.get('salida_visible'))}\\n"
            f"Integración: {clean_value(', '.join(d.get('integracion_mvp', [])), 'No definida')}\\n"
            f"Frecuencia: {clean_value(d.get('frecuencia_actualizacion'))}"
        ),'''
if old_canvas_mvp not in code:
    raise RuntimeError("No se encontró el bloque MVP del Canvas.")
code = code.replace(old_canvas_mvp, new_canvas_mvp)

target.write_text(code, encoding="utf-8")

print(f"Archivo creado correctamente: {target}")
print(f"Tamaño: {target.stat().st_size:,} bytes")
