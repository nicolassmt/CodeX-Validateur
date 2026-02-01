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
.error {background: linear-gradient(135deg,#fa709a,#fee140);padding:20px;border-radius:14px;}
.solution {background: linear-gradient(135deg,#84fab0,#8fd3f4);padding:20px;border-radius:14px;}
.code {background:#f7fafc;padding:15px;border-radius:10px;font-family:monospace;font-size:13px;white-space:pre;}
.footer {text-align:center;margin-top:40px;color:#718096;}
.bad {color:red;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
for k in ["content","filename","filetype","error","display"]:
    st.session_state.setdefault(k, None)

# ==============================
# UTILS
# ==============================
def number_lines(content, error_line=None):
    out = []
    for i, line in enumerate(content.splitlines(), 1):
        prefix = f"{i:4} | "
        if i == error_line:
            out.append(f"{prefix}🔴 {line}")
        else:
            out.append(prefix + line)
    return "\n".join(out)

def find_unclosed_tags(xml):
    stack = []
    for i, line in enumerate(xml.splitlines(), 1):
        for tag in re.findall(r"<(/?)(\w+)", line):
            if tag[0] == "":
                stack.append((tag[1], i))
            else:
                if stack and stack[-1][0] == tag[1]:
                    stack.pop()
    return stack

# ==============================
# HEADER
# ==============================
st.title("🎮 Codex Validateur XML / JSON")
st.subheader("Comprendre et corriger les erreurs de structure DayZ")

# ==============================
# UPLOAD
# ==============================
uploaded = st.file_uploader("📤 Dépose ton fichier XML ou JSON", type=["xml","json"])
if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1]

# ==============================
# VALIDATION BUTTONS
# ==============================
if st.session_state.filename:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Valider XML", disabled=st.session_state.filetype!="xml"):
            try:
                ET.fromstring(st.session_state.content)
                st.success("XML valide 🎉")
            except ET.ParseError as e:
                unclosed = find_unclosed_tags(st.session_state.content)
                st.session_state.error = {
                    "line": e.position[0],
                    "msg": str(e),
                    "unclosed": unclosed
                }

    with col2:
        if st.button("✅ Valider JSON", disabled=st.session_state.filetype!="json"):
            try:
                json.loads(st.session_state.content)
                st.success("JSON valide 🎉")
            except json.JSONDecodeError as e:
                st.session_state.error = {
                    "line": e.lineno,
                    "msg": e.msg
                }

# ==============================
# RESULT
# ==============================
if st.session_state.error:
    e = st.session_state.error

    st.markdown(f"""
<div class="error">
<h4>❌ Erreur détectée</h4>
<b>Ligne :</b> {e["line"]}<br>
<b>Description :</b> {e["msg"]}
</div>
""", unsafe_allow_html=True)

    if "unclosed" in e and e["unclosed"]:
        tag, line = e["unclosed"][-1]
        st.markdown(f"""
<div class="solution">
<h4>💡 Analyse pédagogique</h4>
La balise <b>&lt;{tag}&gt;</b> ouverte à la ligne <b>{line}</b> n’a jamais été fermée.<br>
XML détecte donc l’erreur seulement à la fin du fichier.
</div>
""", unsafe_allow_html=True)

    st.markdown("🔎 **Code analysé (lignes numérotées)**")
    st.markdown(
        f"<div class='code'>{number_lines(st.session_state.content, e['line'])}</div>",
        unsafe_allow_html=True
    )

# ==============================
# FOOTER
# ==============================
st.markdown('<div class="footer">Codex Validateur – EpSy ❤️ | DayZ FR</div>', unsafe_allow_html=True)
