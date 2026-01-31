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

.step {
    font-weight: 700;
    margin-bottom: 10px;
}

.xml-box {
    background: #ecf9f1;
    border-left: 5px solid #2ecc71;
    padding: 12px;
    border-radius: 8px;
}

.json-box {
    background: #eef5fb;
    border-left: 5px solid #3498db;
    padding: 12px;
    border-radius: 8px;
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
# SESSION STATE INIT
# ==============================
for key, value in {
    "content": "",
    "file_type": None,
    "validated": False,
    "has_errors": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

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

    # 1️⃣ HEADER
    try:
        st.image("images/codex3-V2.png", use_column_width=True)
    except:
        pass

    st.markdown('<h1 class="main-title">Codex Validateur XML/JSON</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Configs DayZ propres & lisibles</p><div class="dayz-tag">🎮 Communauté FR</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # 2️⃣ UPLOAD
    st.markdown("### 1️⃣ Dépôt du fichier")

    if not st.session_state.validated:
        uploaded = st.file_uploader("📂 Glisse ton fichier XML ou JSON", type=["xml", "json"])
        if uploaded:
            st.session_state.content = uploaded.read().decode("utf-8")
            st.session_state.file_type = uploaded.name.split(".")[-1].lower()
    else:
        st.success("📁 Fichier chargé — étape verrouillée")

    # 3️⃣ BOUTON VALIDATION
    if st.session_state.file_type and not st.session_state.validated:
        st.markdown("### 2️⃣ Validation")

        if st.session_state.file_type == "xml":
            st.markdown("<div class='xml-box'>📄 Fichier XML détecté</div>", unsafe_allow_html=True)
            if st.button("✅ Valider le XML"):
                valid, msg, formatted, highlighted = validate_xml(st.session_state.content)
                st.session_state.validated = True
                st.session_state.has_errors = not valid
                st.session_state.result = (valid, msg, formatted, highlighted)

        elif st.session_state.file_type == "json":
            st.markdown("<div class='json-box'>📄 Fichier JSON détecté</div>", unsafe_allow_html=True)
            if st.button("✅ Valider le JSON"):
                valid, msg, formatted, highlighted = validate_json(st.session_state.content)
                st.session_state.validated = True
                st.session_state.has_errors = not valid
                st.session_state.result = (valid, msg, formatted, highlighted)

    # 4️⃣ RÉSULTAT + APERÇU
    if st.session_state.validated:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown("### 3️⃣ Résultat & aperçu")

        valid, msg, formatted, highlighted = st.session_state.result

        if valid:
            st.markdown(f"<div class='success-box'>{msg}</div>", unsafe_allow_html=True)
            st.code(formatted, language=st.session_state.file_type)
        else:
            st.markdown(f"<div class='error-box'>{msg}</div>", unsafe_allow_html=True)
            st.code(highlighted, language=st.session_state.file_type)

    # 5️⃣ ACTIONS FINALES
    if st.session_state.validated:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown("### 🛠️ Actions")

        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.has_errors:
                if st.button("🔧 Corriger automatiquement"):
                    st.session_state.content = auto_correct(st.session_state.content)
                    st.session_state.validated = False
                    st.rerun()

        with col2:
            if st.button("♻️ Réinitialiser"):
                st.session_state.clear()
                st.rerun()

    # FOOTER
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">Par EpSy ❤️ | Codex DayZ FR</div>', unsafe_allow_html=True)

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()
