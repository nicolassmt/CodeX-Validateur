"""
Codex Validateur XML/JSON
Outil pédagogique de validation et correction
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
import re

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex Validateur XML/JSON",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
* { font-family: Inter, sans-serif; }

.error {
    background: linear-gradient(135deg, #fa709a, #fee140);
    padding: 20px;
    border-radius: 14px;
}

.solution {
    background: linear-gradient(135deg, #84fab0, #8fd3f4);
    padding: 20px;
    border-radius: 14px;
}

.codebox textarea {
    font-family: Consolas, monospace;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #718096;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
for key, value in {
    "content": "",
    "filename": "",
    "filetype": None,
    "error_info": None,
    "highlighted": "",
    "corrected": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==============================
# UTILS
# ==============================
def highlight_error_with_lines(content, error_line=None):
    """Ajoute numéros de ligne + surlignage pédagogique"""
    lines = content.splitlines()
    output = []

    for idx, line in enumerate(lines, start=1):
        prefix = f"{idx:>4} | "
        if error_line == idx:
            output.append(f"{prefix}🔴 ERREUR ICI → {line}")
        else:
            output.append(prefix + line)

    return "\n".join(output)

def extract_error_info(err):
    if isinstance(err, json.JSONDecodeError):
        return {
            "type": "json",
            "line": err.lineno,
            "column": err.colno,
            "message": err.msg
        }
    elif isinstance(err, ET.ParseError):
        return {
            "type": "xml",
            "line": err.position[0],
            "column": err.position[1],
            "message": "Structure XML invalide (balise mal fermée ou mal imbriquée)"
        }
    else:
        return {
            "type": "unknown",
            "line": "?",
            "column": "?",
            "message": str(err)
        }

def validate_json(content):
    try:
        json.loads(content)
        return None
    except json.JSONDecodeError as e:
        return extract_error_info(e)

def validate_xml(content):
    try:
        ET.fromstring(content)
        return None
    except ET.ParseError as e:
        return extract_error_info(e)

def auto_correct(content):
    corrected = re.sub(r',\s*([}\]])', r'\1', content)
    corrected = corrected.replace("'", '"')
    corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
    return corrected

# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("🎮 Codex Validateur XML / JSON")
st.subheader("Comprendre, corriger et fiabiliser tes fichiers DayZ")

# ==============================
# UPLOAD
# ==============================
uploaded = st.file_uploader(
    "📤 Dépose ton fichier XML ou JSON",
    type=["xml", "json"]
)

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1]
    st.session_state.error_info = None

# ==============================
# VALIDATION
# ==============================
if st.session_state.filename:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Valider XML") and st.session_state.filetype == "xml":
            err = validate_xml(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error_with_lines(
                    st.session_state.content, err["line"]
                )

    with col2:
        if st.button("Valider JSON") and st.session_state.filetype == "json":
            err = validate_json(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error_with_lines(
                    st.session_state.content, err["line"]
                )

# ==============================
# RÉSULTAT
# ==============================
if st.session_state.error_info:
    e = st.session_state.error_info

    st.markdown(f"""
<div class="error">
<h4>❌ Erreur détectée</h4>
<b>📍 Localisation :</b> Ligne {e["line"]}, Colonne {e["column"]}<br>
<b>🧠 Description :</b> {e["message"]}
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="solution">
<h4>💡 Comment corriger</h4>
<ul>
<li>Contrôle les balises ouvrantes / fermantes</li>
<li>Vérifie l’imbrication des blocs</li>
<li>Assure-toi qu’aucune balise n’est oubliée</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.text_area(
        "🔍 Code avec repères pédagogiques",
        value=st.session_state.highlighted,
        height=420
    )

# ==============================
# CORRECTION
# ==============================
if st.session_state.error_info:
    if st.button("🔧 Corriger automatiquement"):
        st.session_state.corrected = auto_correct(st.session_state.content)
        st.session_state.content = st.session_state.corrected
        st.session_state.error_info = None
        st.session_state.highlighted = ""
        st.success("✅ Correction automatique appliquée")

# ==============================
# DOWNLOAD
# ==============================
if st.session_state.corrected:
    st.download_button(
        "⬇️ Télécharger le fichier corrigé",
        data=st.session_state.corrected,
        file_name=st.session_state.filename,
        mime="text/plain"
    )

# ==============================
# RESET
# ==============================
if st.button("🗑️ Réinitialiser"):
    st.session_state.clear()
    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown(
    '<div class="footer">Codex Validateur – EpSy ❤️ | DayZ FR</div>',
    unsafe_allow_html=True
)
