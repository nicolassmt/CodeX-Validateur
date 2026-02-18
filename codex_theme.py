"""
codex_theme.py
Module pour charger le thème galactique CodeX dans Streamlit
"""

import streamlit as st
from pathlib import Path


def load_css():
    """Charge le CSS custom depuis assets/style.css"""
    css_file = Path(__file__).parent / "assets" / "style.css"
    
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Fichier CSS non trouvé : {css_file}")


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
    Initialise le thème complet CodeX
    À appeler au début de chaque page
    """
    # Configuration de la page
    st.set_page_config(
        page_title="CodeX Suite",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Charger le CSS
    load_css()
    
    # Afficher le header
    render_header()


# ═══════════════════════════════════════════════════════
# EXEMPLE D'UTILISATION
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    # Initialiser le thème
    init_theme()
    
    # Contenu de ta page
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
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier",
        type=["xml", "json"],
        help="Types supportés : XML, JSON"
    )
    
    if uploaded_file:
        st.success(f"✅ Fichier chargé : {uploaded_file.name}")
        
        if st.button("🚀 Valider le fichier"):
            st.balloons()
            st.success("✨ Validation réussie !")
