"""
codex_theme.py
Module pour charger le thème galactique CodeX dans Streamlit
"""

import streamlit as st
from pathlib import Path
import base64


def load_css():
    """Charge le CSS custom depuis assets/style.css avec image encodée"""
    css_file = Path(__file__).parent / "assets" / "style.css"
    image_file = Path(__file__).parent / "assets" / "images" / "horizon-spatial.png"
    
    if not css_file.exists():
        st.warning(f"⚠️ Fichier CSS non trouvé : {css_file}")
        return
    
    # Lire le CSS
    with open(css_file) as f:
        css_content = f.read()
    
    # Encoder l'image en base64 si elle existe
    if image_file.exists():
        with open(image_file, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            # Remplacer le chemin de l'image par la version base64
            css_content = css_content.replace(
                "url('./images/horizon-spatial.png')",
                f"url('data:image/png;base64,{img_data}')"
            )
    else:
        st.warning(f"⚠️ Image non trouvée : {image_file}")
    
    # Injecter le CSS
    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)


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
