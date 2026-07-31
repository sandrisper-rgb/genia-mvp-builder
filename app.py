from pathlib import Path
import html
import re
import py_compile

src = Path("/mnt/data/Pasted text(11).txt")
code = src.read_text(encoding="utf-8")

# 1) Strengthen CSS for result boxes, inputs and buttons.
old_css = """.result-box,.maturity-card {{ background:rgba(255,255,255,.68); border-radius:18px; padding:18px; margin-top:12px; }}
        .result-box *,.maturity-card * {{ color:#0B2E4A!important; }}
        .stDownloadButton button,.stButton button {{ background:#fff!important; color:#0B2E4A!important; font-weight:700!important; border-radius:12px!important; }}"""

new_css = """.result-box,.maturity-card {{
            background:rgba(255,255,255,.96)!important;
            border-radius:18px;
            padding:20px;
            margin-top:12px;
            border:1px solid rgba(11,46,74,.20);
            box-shadow:0 6px 18px rgba(0,0,0,.12);
        }}
        .result-box,.result-box *,.maturity-card,.maturity-card * {{
            color:#0B2E4A!important;
        }}
        .result-box {{
            white-space:pre-wrap;
            font-size:16px;
            line-height:1.55;
            overflow-wrap:anywhere;
        }}
        textarea {{
            background-color:rgba(255,255,255,.96)!important;
            color:#0B2E4A!important;
            -webkit-text-fill-color:#0B2E4A!important;
        }}
        .stDownloadButton button,.stButton button {{
            background:#fff!important;
            color:#0B2E4A!important;
            font-weight:700!important;
            border-radius:12px!important;
            border:1px solid rgba(11,46,74,.25)!important;
        }}
        .stDownloadButton button p,
        .stDownloadButton button span,
        .stButton button p,
        .stButton button span {{
            color:#0B2E4A!important;
            -webkit-text-fill-color:#0B2E4A!important;
        }}
        .stDownloadButton button:hover,.stButton button:hover {{
            background:#F05A28!important;
            color:#fff!important;
        }}
        .stDownloadButton button:hover p,
        .stDownloadButton button:hover span,
        .stButton button:hover p,
        .stButton button:hover span {{
            color:#fff!important;
            -webkit-text-fill-color:#fff!important;
        }}"""

if old_css not in code:
    raise ValueError("No encontré el bloque CSS esperado.")
code = code.replace(old_css, new_css)

# 2) Import html for safe rendering.
code = code.replace("import base64\nimport os\nimport re\n", "import base64\nimport html\nimport os\nimport re\n")

# 3) Replace summary rendering and add visible pitch box.
old_result = """    summary=build_summary(d,score,level,innovation,blockers)
    st.subheader("Resumen del MVP"); st.markdown(f'<div class="result-box">{summary}</div>',unsafe_allow_html=True)
    filename=safe_filename(d.get("nombre"))
    st.download_button("📥 Descargar resumen en Markdown",summary.encode("utf-8"),file_name=f"genia_mvp_{filename}.md",mime="text/markdown")
    pitch=f\"\"\"# Pitch de 3 minutos\\n\\nSomos el equipo **{d.get('nombre','')}**. El problema es **{d.get('problema','')}**. Nuestro usuario es **{d.get('usuario','')}** y buscamos apoyar **{d.get('decision','')}**. El MVP hará **{d.get('funcion','')}** y se comparará contra **{d.get('linea_base','')}**. Mediremos **{', '.join(d.get('kpis',[]))}**. El principal riesgo es **{d.get('riesgo','')}**, mitigado mediante **{d.get('mitigacion','')}**. Proponemos un piloto en **{d.get('lugar','')}** durante **{d.get('duracion','')}**.\\n\"\"\"
    st.download_button("🎤 Descargar pitch",pitch.encode("utf-8"),file_name=f"pitch_{filename}.md",mime="text/markdown")
"""

new_result = """    summary=build_summary(d,score,level,innovation,blockers)
    st.subheader("Resumen del MVP")
    summary_html = html.escape(summary)
    st.markdown(
        f'<div class="result-box">{summary_html}</div>',
        unsafe_allow_html=True
    )

    filename=safe_filename(d.get("nombre"))
    st.download_button(
        "📥 Descargar resumen en Markdown",
        summary.encode("utf-8"),
        file_name=f"genia_mvp_{filename}.md",
        mime="text/markdown"
    )

    pitch=f\"\"\"# Pitch de 3 minutos

Somos el equipo **{d.get('nombre','')}**.

El problema es **{d.get('problema','')}**.

Nuestro usuario es **{d.get('usuario','')}** y buscamos apoyar **{d.get('decision','')}**.

El MVP hará **{d.get('funcion','')}** y se comparará contra **{d.get('linea_base','')}**.

Mediremos **{', '.join(d.get('kpis',[]))}**.

El principal riesgo es **{d.get('riesgo','')}**, mitigado mediante **{d.get('mitigacion','')}**.

Proponemos un piloto en **{d.get('lugar','')}** durante **{d.get('duracion','')}**.
\"\"\"

    st.subheader("Pitch de 3 minutos")
    pitch_html = html.escape(pitch)
    st.markdown(
        f'<div class="result-box">{pitch_html}</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        "🎤 Descargar pitch",
        pitch.encode("utf-8"),
        file_name=f"pitch_{filename}.md",
        mime="text/markdown"
    )
"""

if old_result not in code:
    raise ValueError("No encontré el bloque de resultados esperado.")
code = code.replace(old_result, new_result)

out = Path("/mnt/data/app_corregido_resultados.py")
out.write_text(code, encoding="utf-8")
py_compile.compile(str(out), doraise=True)

print(f"Archivo creado y validado: {out}")
