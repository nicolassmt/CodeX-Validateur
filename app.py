"""
Codex Validateur XML/JSON
L'outil indispensable pour vérifier vos fichiers de configuration DayZ
Créé par EpSy pour la communauté francophone DayZ
VERSION ULTIME - Images cliquables + Surlignage erreurs + Correction en place
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from pathlib import Path

# =============================
# CONFIGURATION PAGE
# =============================
st.set_page_config(
    page_title="Codex Validateur XML/JSON",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# STYLE CSS
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
.block-container { background-color: #ffffff; border-radius: 20px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }

.main-title { color: #2d3748; font-size: 2.5em; font-weight: 700; margin: 10px 0; }
.subtitle { color: #718096; font-size: 1.1em; margin-bottom: 10px; }
.dayz-tag { display:inline-block; background:linear-gradient(135deg,#667eea,#764ba2); color:white; padding:8px 20px; border-radius:20px; font-weight:600; }

.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    font-family: Consolas, monospace;
    font-size: 14px;
}

.success-box {
    background: linear-gradient(135deg,#84fab0,#8fd3f4);
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
}

.error-box {
    background: linear-gradient(135deg,#fa709a,#fee140);
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
}

.suggestion-box {
    background: linear-gradient(135deg,#ffecd2,#fcb69f);
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
}

.separator {
    height: 3px;
    background: linear-gradient(90deg,#667eea,#764ba2);
    margin: 30px 0;
    border-radius: 2px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #718096;
}

.discord-link {
    display:inline-block;
    background:#5865F2;
    color:white;
    padding:12px 30px;
    border-radius:25px;
    text-decoration:none;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# =============================
# OUTILS
# =============================
def highlight_error_line(content, error=None):
    lines = content.splitlines()
    if hasattr(error, "lineno") and 1 <= error.lineno <= len(lines):
        idx = error.lineno - 1
        lines[idx] = f"🔴 ERREUR ICI >>> {lines[idx]}"
    return "\n".join(lines)

def analyze_xml_error(error):
    suggestions = []
    msg = str(error).lower()
    if "mismatched" in msg:
        suggestions.append("Balise ouverte / fermée incorrecte")
    if "not well-formed" in msg:
        suggestions.append("Caractère non échappé (& → &amp;)")
    return suggestions

def analyze_json_error(content, error):
    suggestions = []
    if error.lineno:
        suggestions.append(f"Ligne {error.lineno}: {content.splitlines()[error.lineno-1]}")
    msg = str(error).lower()
    if "comma" in msg:
        suggestions.append("Virgule en trop ou manquante")
    if "brace" in msg or "bracket" in msg:
        suggestions.append("Accolade ou crochet non fermé")
    return suggestions

def validate_xml(content):
    try:
        ET.fromstring(content)
        pretty = minidom.parseString(content).toprettyxml(indent="  ")
        pretty = "\n".join(l for l in pretty.splitlines() if l.strip())
        return True, "XML valide ✅", pretty, None, []
    except ET.ParseError as e:
        return False, str(e), None, highlight_error_line(content, e), analyze_xml_error(e)

def validate_json(content):
    try:
        data = json.loads(content)
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return True, "JSON valide ✅", pretty, None, []
    except json.JSONDecodeError as e:
        return False, str(e), None, highlight_error_line(content, e), analyze_json_error(content, e)

def auto_correct(content):
    corrected = content
    fixes = []

    if content.strip().startswith(("{", "[")):
        if "'" in corrected:
            corrected = corrected.replace("'", '"')
            fixes.append("Guillemets simples remplacés")
        corrected = re.sub(r",\s*([}\]])", r"\1", corrected)

    corrected = re.sub(r"&(?!(amp|lt|gt|quot|apos);)", "&amp;", corrected)

    return corrected, fixes

# =============================
# APP
# =============================
def main():

    if "content" not in st.session_state:
        st.session_state.content = ""

    if "filename" not in st.session_state:
        st.session_state.filename = "fichier.txt"

    # HEADER LOGO SÉCURISÉ
    logo = Path("images/codex3-V2.png")
    if logo.exists():
        st.image(str(logo), use_container_width=True)
    else:
        st.warning("⚠️ Logo introuvable : images/codex3-V2.png")

    st.markdown("<h1 class='main-title'>Codex Validateur XML / JSON</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Configs DayZ claires, propres et sans stress</p>", unsafe_allow_html=True)
    st.markdown("<div class='dayz-tag'>🎮 Communauté DayZ FR</div>", unsafe_allow_html=True)
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    # ACTIONS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("images/xml.png", use_container_width=True)
        if st.button("Valider XML"):
            st.session_state.action = "xml"

    with col2:
        st.image("images/json.png", use_container_width=True)
        if st.button("Valider JSON"):
            st.session_state.action = "json"

    with col3:
        st.image("images/auto_corriger.png", use_container_width=True)
        if st.button("Auto-corriger"):
            st.session_state.action = "correct"

    with col4:
        st.image("images/effacer.png", use_container_width=True)
        if st.button("Effacer"):
            st.session_state.action = "clear"

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("📤 Charger un fichier", type=["xml", "json", "txt"])
    if uploaded:
        st.session_state.content = uploaded.read().decode("utf-8")
        st.session_state.filename = uploaded.name

    st.session_state.content = st.text_area(
        "📝 Contenu du fichier",
        value=st.session_state.content,
        height=350
    )

    if "action" in st.session_state:
        action = st.session_state.action
        content = st.session_state.content

        if action == "clear":
            st.session_state.content = ""
            st.session_state.filename = "fichier.txt"
            st.rerun()

        if action == "correct" and content.strip():
            corrected, fixes = auto_correct(content)
            st.session_state.content = corrected
            st.success("Correction appliquée ✅")
            if fixes:
                st.write(", ".join(fixes))

        if action in ("xml", "json") and content.strip():
            if action == "xml":
                valid, msg, pretty, highlight, sugg = validate_xml(content)
            else:
                valid, msg, pretty, highlight, sugg = validate_json(content)

            if valid:
                st.markdown(f"<div class='success-box'>{msg}</div>", unsafe_allow_html=True)
                st.code(pretty, language=action)
            else:
                st.markdown(f"<div class='error-box'>{msg}</div>", unsafe_allow_html=True)
                for s in sugg:
                    st.markdown(f"<div class='suggestion-box'>💡 {s}</div>", unsafe_allow_html=True)
                st.code(highlight, language=action)

        del st.session_state.action
        st.rerun()

    st.markdown("""
    <div class="separator"></div>
    <div class="footer">
        <a class="discord-link" href="https://discord.gg/CQR6KTJ63C">💬 Discord CodeX</a>
        <p>Créé par EpSy ❤️</p>
    </div>
    """, unsafe_allow_html=True)

# =============================
if __name__ == "__main__":
    main()
