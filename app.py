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
    max-height: 380px;
    overflow-y: auto;
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
for key, default in {
    "content": "",
    "filename": "",
    "filetype": None,
    "error_info": None,
    "display_code": "",
    "analysis_done": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ==============================
# UTILS
# ==============================
def highlight_error(content, line):
    lines = content.splitlines()
    if 1 <= line <= len(lines):
        lines[line - 1] = "🔴 ERREUR ICI → " + lines[line - 1]
    return "\n".join(lines)

def extract_error_info(err):
    if isinstance(err, json.JSONDecodeError):
        return {
            "type": "json",
            "line": err.lineno,
            "column": err.colno,
            "message": err.msg
        }
    if isinstance(err, ET.ParseError):
        return {
            "type": "xml",
            "line": err.position[0],
            "column": err.position[1],
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
    content = re.sub(r',\s*([}\]])', r'\1', content)
    content = content.replace("'", '"')
    content = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', content)
    return content

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
uploaded = st.file_uploader("📤 Dépose ton fichier XML ou JSON", type=["xml", "json"])

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1].lower()
    st.session_state.error_info = None
    st.session_state.analysis_done = False

# ==============================
# VALIDATION
# ==============================
if st.session_state.filename:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🟩 Valider XML") and st.session_state.filetype == "xml":
            err = validate_xml(st.session_state.content)
            st.session_state.analysis_done = True
            if err:
                st.session_state.error_info = err
                st.session_state.display_code = highlight_error(
                    st.session_state.content, err["line"]
                )
            else:
                st.success("✅ XML valide")
                st.session_state.display_code = st.session_state.content

    with col2:
        if st.button("🟦 Valider JSON") and st.session_state.filetype == "json":
            err = validate_json(st.session_state.content)
            st.session_state.analysis_done = True
            if err:
                st.session_state.error_info = err
                st.session_state.display_code = highlight_error(
                    st.session_state.content, err["line"]
                )
            else:
                st.success("✅ JSON valide")
                st.session_state.display_code = st.session_state.content

# ==============================
# RÉSULTAT
# ==============================
if st.session_state.analysis_done:

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
<h4>💡 Solution</h4>
<ul>
<li>Vérifie la ligne indiquée</li>
<li>Supprime les virgules finales</li>
<li>Vérifie les balises ou caractères spéciaux</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.text_area(
        "🔍 Code analysé",
        value=st.session_state.display_code,
        height=380,
        key="codebox"
    )

    # ==============================
    # ACTIONS POST-ANALYSE
    # ==============================
    colA, colB = st.columns(2)

    with colA:
        if st.button("🔧 Corriger automatiquement"):
            st.session_state.content = auto_correct(st.session_state.content)
            st.session_state.display_code = st.session_state.content
            st.session_state.error_info = None
            st.success("✅ Correction appliquée")

    with colB:
        if st.button("🗑️ Réinitialiser"):
            st.session_state.clear()
            st.rerun()

    st.download_button(
        "⬇️ Télécharger le fichier corrigé",
        data=st.session_state.content,
        file_name=st.session_state.filename,
        mime="text/plain"
    )
    st.info("ℹ️ Le fichier téléchargé devra garder le nom d’origine pour DayZ")

# ==============================
# FOOTER
# ==============================
st.markdown('<div class="footer">Codex Validateur – EpSy ❤️ | DayZ FR</div>', unsafe_allow_html=True)
