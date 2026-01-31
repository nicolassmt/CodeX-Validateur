"""
Codex Validateur XML/JSON
Outil pédagogique de validation et correction
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from io import BytesIO

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

.step {
    background: #f7fafc;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 20px;
    border-left: 6px solid #667eea;
}

.code-box textarea {
    height: 380px !important;
}

.xml-btn button { background-color: #38a169 !important; color: white !important; }
.json-btn button { background-color: #3182ce !important; color: white !important; }

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
defaults = {
    "content": "",
    "filename": "",
    "type": None,
    "error": None,
    "highlighted": "",
    "corrected": "",
    "validated": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==============================
# UTILS
# ==============================
def highlight_error(content, lineno):
    lines = content.splitlines()
    if 1 <= lineno <= len(lines):
        lines[lineno - 1] = "🔴 ERREUR ICI → " + lines[lineno - 1]
    return "\n".join(lines)

def validate_json(content):
    try:
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, e

def validate_xml(content):
    try:
        ET.fromstring(content)
        return True, None
    except ET.ParseError as e:
        return False, e

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
st.subheader("L’outil français pour comprendre et corriger ses configs DayZ")

# ==============================
# ÉTAPE 1 – UPLOAD
# ==============================
st.markdown("### 1️⃣ Dépose ton fichier")

uploaded = st.file_uploader(
    "Formats acceptés : XML ou JSON",
    type=["xml", "json"],
    disabled=bool(st.session_state.filename)
)

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.type = uploaded.name.split(".")[-1]

if st.session_state.filename:
    st.success(f"📁 Fichier détecté : {st.session_state.filename}")

# ==============================
# ÉTAPE 2 – VALIDATION
# ==============================
if st.session_state.filename:
    st.markdown("### 2️⃣ Choisis le type de validation")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Valider XML", key="xml", help="Analyse XML") and st.session_state.type == "xml":
            ok, err = validate_xml(st.session_state.content)
            if not ok:
                st.session_state.error = err
                st.session_state.highlighted = highlight_error(st.session_state.content, err.position[0])
            else:
                st.session_state.validated = True

    with col2:
        if st.button("Valider JSON", key="json", help="Analyse JSON") and st.session_state.type == "json":
            ok, err = validate_json(st.session_state.content)
            if not ok:
                st.session_state.error = err
                st.session_state.highlighted = highlight_error(st.session_state.content, err.lineno)
            else:
                st.session_state.validated = True

# ==============================
# ÉTAPE 3 – RÉSULTATS
# ==============================
if st.session_state.error:
    err = st.session_state.error

    st.markdown("### 3️⃣ Résultat de la validation")

    st.markdown(f"""
<div class="error">
<h4>❌ Oups ! Il y a une erreur dans ton fichier</h4>
<b>📍 Localisation :</b><br>
Ligne : {getattr(err, 'lineno', err.position[0])}<br>
Colonne : {getattr(err, 'colno', err.position[1]) if hasattr(err, 'colno') else ''}
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="solution">
<h4>💡 Comment corriger ?</h4>
<ul>
<li>Une virgule est placée après le dernier élément</li>
<li>JSON/XML n'autorisent pas les virgules finales</li>
<li>Supprime simplement la dernière virgule</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("#### 🔍 Code concerné")
    st.text_area(
        "Aperçu avec erreur",
        value=st.session_state.highlighted,
        key="codeview",
        height=380
    )

# ==============================
# ÉTAPE 4 – CORRECTION
# ==============================
if st.session_state.error:
    st.markdown("### 4️⃣ Correction")

    if st.button("🔧 Corriger automatiquement"):
        st.session_state.corrected = auto_correct(st.session_state.content)
        st.session_state.content = st.session_state.corrected
        st.session_state.error = None
        st.session_state.highlighted = ""
        st.success("✅ Correction appliquée")

# ==============================
# ÉTAPE 5 – TÉLÉCHARGEMENT
# ==============================
if st.session_state.corrected:
    st.markdown("### 5️⃣ Télécharger le fichier corrigé")

    st.download_button(
        "⬇️ Télécharger la version corrigée",
        data=st.session_state.corrected,
        file_name=st.session_state.filename,
        mime="text/plain"
    )

    st.info("ℹ️ Pense à renommer le fichier exactement comme l’original si nécessaire.")

# ==============================
# RESET
# ==============================
st.markdown("### 6️⃣ Réinitialiser")
if st.button("🗑️ Tout recommencer"):
    st.session_state.clear()
    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown('<div class="footer">Codex Validateur – EpSy ❤️ | Communauté DayZ FR</div>', unsafe_allow_html=True)
