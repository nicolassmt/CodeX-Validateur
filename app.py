"""
Codex Validateur XML/JSON
Outil de validation pour fichiers DayZ
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from pathlib import Path

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.block-container {
    background-color: #ffffff;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.main-title { font-size: 2.5em; font-weight: 700; color: #2d3748; }
.subtitle { color: #718096; margin-bottom: 10px; }

.dayz-tag {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 8px 20px;
    border-radius: 20px;
    font-weight: 600;
}

.separator {
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 2px;
    margin: 30px 0;
}

.success-box {
    background: linear-gradient(135deg, #84fab0, #8fd3f4);
    padding: 20px;
    border-radius: 15px;
}

.error-box {
    background: linear-gradient(135deg, #fa709a, #fee140);
    padding: 20px;
    border-radius: 15px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #718096;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE SAFE INIT
# ==============================
if "content" not in st.session_state:
    st.session_state["content"] = ""

if "filename" not in st.session_state:
    st.session_state["filename"] = "fichier.txt"

if "action" not in st.session_state:
    st.session_state["action"] = None

# ==============================
# UTILS
# ==============================
def highlight_error_line(content, error):
    lines = content.splitlines()
    if hasattr(error, "lineno") and 1 <= error.lineno <= len(lines):
        i = error.lineno - 1
        lines[i] = f"🔴 ERREUR ICI → {lines[i]}"
    return "\n".join(lines)

def validate_xml(content):
    try:
        ET.fromstring(content)
        pretty = minidom.parseString(content).toprettyxml(indent="  ")
        return True, "✅ XML valide", pretty, ""
    except ET.ParseError as e:
        return False, f"❌ Erreur XML : {e}", "", highlight_error_line(content, e)

def validate_json(content):
    try:
        data = json.loads(content)
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return True, "✅ JSON valide", pretty, ""
    except json.JSONDecodeError as e:
        return False, f"❌ Erreur JSON ligne {e.lineno}", "", highlight_error_line(content, e)

def auto_correct(content):
    corrected = content.replace("'", '"')
    corrected = re.sub(r',\s*([}\]])', r'\1', corrected)
    corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
    return corrected

# ==============================
# MAIN
# ==============================
def main():

    # HEADER
    try:
        st.image("images/codex3-V2.png", use_column_width=True)
    except:
        pass

    st.markdown('<h1 class="main-title">Codex Validateur XML/JSON</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Configs DayZ propres & lisibles</p><div class="dayz-tag">🎮 Communauté FR</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # ACTIONS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("XML"): st.session_state["action"] = "xml"
    with col2:
        if st.button("JSON"): st.session_state["action"] = "json"
    with col3:
        if st.button("🔧 Corriger"): st.session_state["action"] = "correct"
    with col4:
        if st.button("🗑️ Clear"): st.session_state["action"] = "clear"

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # UPLOAD
    uploaded = st.file_uploader("📤 Dépose ton fichier", type=["xml", "json", "txt"])
    if uploaded:
        st.session_state["content"] = uploaded.read().decode("utf-8")
        st.session_state["filename"] = uploaded.name

    st.session_state["content"] = st.text_area(
        "📝 Ton fichier",
        value=st.session_state["content"],
        height=350
    )

    # LOGIQUE ACTION
    action = st.session_state["action"]
    content = st.session_state["content"]

    if action == "clear":
        st.session_state.clear()
        st.rerun()

    if action in ("xml", "json") and content.strip():
        valid, msg, formatted, highlighted = (
            validate_xml(content) if action == "xml" else validate_json(content)
        )

        if valid:
            st.markdown(f'<div class="success-box">{msg}</div>', unsafe_allow_html=True)
            st.code(formatted, language=action)
        else:
            st.markdown(f'<div class="error-box">{msg}</div>', unsafe_allow_html=True)
            st.code(highlighted, language=action)

    if action == "correct" and content.strip():
        corrected = auto_correct(content)
        st.session_state["content"] = corrected
        st.success("✅ Correction appliquée")
        st.rerun()

    st.session_state["action"] = None

    # FOOTER
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">Par EpSy ❤️ | Discord DayZ FR</div>', unsafe_allow_html=True)

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()
