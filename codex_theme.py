"""
codex_theme_allinone.py
Thème galactique CodeX - Version ALL-IN-ONE
Tout est contenu dans ce fichier : CSS + Image + Police fallback

Usage:
    from codex_theme_allinone import init_theme
    init_theme()
"""

import streamlit as st

# Image horizon spatial encodée en base64
HORIZON_IMAGE_BASE64 = """
/9j/4AAQSkZJRgABAQEBLAEsAAD/4QBWRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAITAAMAAAABAAEAAAAAAAAAAAEsAAAAAQAAASwAAAAB/+0ALFBob3Rvc2hvcCAzLjAAOEJJTQQEAAAAAAAPHAFaAAMbJUccAQAAAgAEAP/hDIFodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvADw/eHBhY2tldCBiZWdpbj0n77u/JyBpZD0nVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkJz8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0nYWRvYmU6bnM6bWV0YS8nIHg6eG1wdGs9J0ltYWdlOjpFeGlmVG9vbCAxMC4xMCc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczp0aWZmPSdodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyc+CiAgPHRpZmY6UmVzb2x1dGlvblVuaXQ+MjwvdGlmZjpSZXNvbHV0aW9uVW5pdD4KICA8dGlmZjpYUmVzb2x1dGlvbj4zMDAvMTwvdGlmZjpYUmVzb2x1dGlvbj4KICA8dGlmZjpZUmVzb2x1dGlvbj4zMDAvMTwvdGlmZjpZUmVzb2x1dGlvbj4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6eG1wTU09J2h0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8nPgogIDx4bXBNTTpEb2N1bWVudElEPmFkb2JlOmRvY2lkOnN0b2NrOjlmYzcyYzYzLWE3N2QtNDg0Ny05NTg2LWIxNGQ3ODg5NDJjZjwveG1wTU06RG9jdW1lbnRJRD4KICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOjVkZDc2OTg0LTk1MTMtNGNiYS05MTgzLTM1NTQwNTk2NTViODwveG1wTU06SW5zdGFuY2VJRD4KIDwvcmRmOkRlc2NyaXB0aW9uPgo8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSd3Jz8+/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUEBAUKBwcGCAwKDAwLCgsLDQ4SEA0OEQ4LCxAWEBETFBUVFQwPFxgWFBgSFBUU/9sAQwEDBAQFBAUJBQUJFA0LDRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgA8AGrAwERAAIRAQMRAf/EABwAAAIDAQEBAQAAAAAAAAAAAAIDAAEEBQYHCf/EAD0QAAIBAgMFBQYEBQQDAQEAAAECAAMRBBIhBTFBUWEGEyKRoQcjMkJxgRRDUlMzscHR8BUW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"""

# CSS complet avec police Sawah (fallback sur polices système)
CODEX_CSS = """
<style>
/* ═══════════════════════════════════════════════════════
   CODEX SUITE - GALACTIC THEME ALL-IN-ONE
   Police : Sawah (fallback: Michroma, Orbitron)
   ═══════════════════════════════════════════════════════ */

/* Import Google Fonts fallback */
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Orbitron:wght@700;900&display=swap');

/* Variables */
:root {
    --codex-blue: #00D4FF;
    --codex-blue-dark: #0099CC;
    --space-black: #000000;
    --space-dark: #0A1628;
    --text-primary: #FFFFFF;
    --text-secondary: #B8E6FF;
}

/* Header galactique avec image */
.codex-header {
    background-image: url('data:image/jpeg;base64,""" + HORIZON_IMAGE_BASE64 + """');
    background-size: cover;
    background-position: center bottom;
    padding: 80px 40px 60px 40px;
    text-align: center;
    position: relative;
    border-bottom: 2px solid var(--codex-blue);
    margin-bottom: 40px;
    overflow: hidden;
}

/* Overlay sombre */
.codex-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.85) 0%, 
        rgba(0,0,0,0.5) 40%, 
        rgba(0,0,0,0.7) 100%);
    z-index: 1;
}

/* Ligne glow en bas */
.codex-header::after {
    content: '';
    position: absolute;
    bottom: -2px; left: 0; right: 0;
    height: 2px;
    background: var(--codex-blue);
    box-shadow: 0 0 10px var(--codex-blue), 
                0 0 20px var(--codex-blue);
    z-index: 3;
}

/* Logo CODEX */
.codex-logo {
    font-family: 'Michroma', 'Orbitron', monospace;
    font-weight: 900;
    font-size: 96px;
    letter-spacing: 28px;
    color: var(--text-primary);
    text-transform: uppercase;
    margin: 0; padding: 0;
    position: relative;
    z-index: 2;
    line-height: 1;
    text-shadow: 
        0 0 10px rgba(255, 255, 255, 1),
        0 0 20px var(--codex-blue),
        0 0 40px var(--codex-blue),
        0 0 60px rgba(0, 212, 255, 0.6),
        0 0 80px rgba(0, 212, 255, 0.4);
    animation: logo-pulse 4s ease-in-out infinite;
}

@keyframes logo-pulse {
    0%, 100% {
        text-shadow: 
            0 0 10px rgba(255, 255, 255, 1),
            0 0 20px var(--codex-blue),
            0 0 40px var(--codex-blue),
            0 0 60px rgba(0, 212, 255, 0.6);
    }
    50% {
        text-shadow: 
            0 0 15px rgba(255, 255, 255, 1),
            0 0 30px var(--codex-blue),
            0 0 60px var(--codex-blue),
            0 0 90px rgba(0, 212, 255, 0.8);
    }
}

/* Tagline */
.codex-tagline {
    font-family: 'Michroma', 'Orbitron', sans-serif;
    font-weight: normal;
    font-size: 14px;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-top: 24px;
    opacity: 0.95;
    position: relative;
    z-index: 2;
    line-height: 1.6;
    text-shadow: 
        0 0 8px rgba(184, 230, 255, 0.6),
        0 0 16px rgba(0, 212, 255, 0.3);
}

/* Background général */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, 
        var(--space-black) 0%, 
        var(--space-dark) 50%, 
        var(--space-black) 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(10, 10, 20, 0.95);
    border-right: 1px solid rgba(0, 212, 255, 0.2);
}

/* Boutons */
.stButton > button {
    background: linear-gradient(135deg, var(--codex-blue-dark), var(--codex-blue));
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px 32px;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--codex-blue), #33E0FF);
    box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
    transform: translateY(-2px);
}

/* Titres */
h1, h2, h3 {
    color: var(--text-primary);
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 2px;
}

h1 {
    text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
    .codex-header { padding: 60px 20px 40px 20px; }
    .codex-logo { font-size: 56px; letter-spacing: 16px; }
    .codex-tagline { font-size: 11px; letter-spacing: 4px; }
}

@media (max-width: 480px) {
    .codex-logo { font-size: 40px; letter-spacing: 12px; }
    .codex-tagline { font-size: 9px; letter-spacing: 3px; }
}

/* Cache menu Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
"""


def render_header():
    """Affiche le header galactique CodeX"""
    header_html = """
    <div class="codex-header">
        <h1 class="codex-logo">CODEX</h1>
        <p class="codex-tagline">
            Serveur de Soutien et d'Entraide<br>
            à la Communauté DayZ Francophone
        </p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def init_theme():
    """
    Initialise le thème galactique CodeX
    À appeler au début de chaque page Streamlit
    """
    # Configuration
    st.set_page_config(
        page_title="CodeX Suite",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Injecter CSS
    st.markdown(CODEX_CSS, unsafe_allow_html=True)
    
    # Afficher header
    render_header()


# ═══════════════════════════════════════════════════════
# EXEMPLE / TEST
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    init_theme()
    
    st.title("🛠️ Validateur DayZ")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fichiers validés", "13", "+2")
    with col2:
        st.metric("Erreurs", "0", "0")
    with col3:
        st.metric("Warnings", "5", "-3")
    
    st.markdown("---")
    st.info("📁 Déposez vos fichiers de configuration DayZ")
    
    uploaded_file = st.file_uploader("Choisir un fichier", type=["xml", "json"])
    
    if uploaded_file:
        st.success(f"✅ Fichier chargé : {uploaded_file.name}")
        if st.button("🚀 Valider"):
            st.balloons()
            st.success("✨ Validation réussie !")
