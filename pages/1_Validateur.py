"""
Codex Suite - Module Validateur
Validation automatique de tous les fichiers DayZ
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.validator import validator

# ═══════════════════════════════════════════════════════
# CONFIG PAGE
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Codex - Validateur",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# CSS UNIFIÉ
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #000000; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.header-container {
    width: 100%;
    margin: 0 0 40px 0;
    padding: 0;
}
.header-container img {
    width: 100%;
    height: auto;
    display: block;
}

.content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 30px;
}

.page-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 40px;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

.info-box {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 30px;
}

.info-box h3 {
    color: #00D4FF;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

.info-box p {
    color: rgba(255, 255, 255, 0.85);
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.result-box {
    background: rgba(0, 25, 50, 0.55);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
}

.result-box.success {
    border-color: rgba(0, 212, 255, 0.6);
    background: rgba(0, 50, 75, 0.4);
}

.result-box.error {
    border-color: rgba(239, 68, 68, 0.6);
    background: rgba(75, 0, 0, 0.4);
}

.error-item {
    background: rgba(239, 68, 68, 0.1);
    border-left: 3px solid #ef4444;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
}

.warning-item {
    background: rgba(251, 191, 36, 0.1);
    border-left: 3px solid #fbbf24;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000;
    border: none;
    border-radius: 14px;
    padding: 16px 32px;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 5px 18px rgba(0, 212, 255, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HEADER IMAGE
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="header-container">
    <img src="https://raw.githubusercontent.com/EpSyDev/codex-validateur/main/assets/images/codex_header.png" alt="CODEX">
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# CONTENU PRINCIPAL
# ═══════════════════════════════════════════════════════

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">📝 Validateur de Fichiers DayZ</h1>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <h3>🎯 Validation Automatique</h3>
    <p>Uploadez n'importe quel fichier de configuration DayZ (XML ou JSON). Le système détecte automatiquement le type de fichier et applique les règles de validation appropriées.</p>
</div>
""", unsafe_allow_html=True)

# Upload de fichier
uploaded_file = st.file_uploader(
    "Choisissez un fichier",
    type=['xml', 'json'],
    help="Formats supportés : XML (types, events, globals...) et JSON (cfggameplay, cfgeffectarea...)"
)

if uploaded_file:
    # Lire le contenu
    content = uploaded_file.read().decode('utf-8')
    filename = uploaded_file.name
    
    # Bouton de validation
    if st.button("🚀 Valider le fichier", type="primary"):
        with st.spinner("Analyse en cours..."):
            # Validation
            result = validator.validate(content, filename)
            
            # Stocker dans session state
            st.session_state.validation_result = result

# Afficher les résultats
if 'validation_result' in st.session_state:
    result = st.session_state.validation_result
    
    # Résumé
    if result.valid:
        st.markdown(f"""
        <div class="result-box success">
            <h2 style="color: #00D4FF; margin: 0;">✅ Fichier Valide</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                Type détecté : <strong>{result.file_type}</strong> ({result.format.upper()})
                <br>Confiance : {result.confidence:.0%}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-box error">
            <h2 style="color: #ef4444; margin: 0;">❌ Erreurs Détectées</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                {len(result.errors)} erreur(s) trouvée(s)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Onglets pour détails
    tab1, tab2, tab3 = st.tabs(["❌ Erreurs", "⚠️ Avertissements", "ℹ️ Informations"])
    
    with tab1:
        if result.errors:
            for idx, error in enumerate(result.errors, 1):
                st.markdown(f"""
                <div class="error-item">
                    <strong>Erreur #{idx}</strong><br>
                    {error.get('message', 'Erreur inconnue')}<br>
                    <small style="color: rgba(255,255,255,0.6);">{error.get('suggestion', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Aucune erreur détectée ! ✅")
    
    with tab2:
        if result.warnings:
            for idx, warning in enumerate(result.warnings, 1):
                st.markdown(f"""
                <div class="warning-item">
                    <strong>Avertissement #{idx}</strong><br>
                    {warning.get('message', 'Avertissement inconnu')}<br>
                    <small style="color: rgba(255,255,255,0.6);">{warning.get('suggestion', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun avertissement.")
    
    with tab3:
        st.json({
            'Type de fichier': result.file_type,
            'Format': result.format,
            'Confiance': f"{result.confidence:.0%}",
            'Nombre d\'erreurs': len(result.errors),
            'Nombre d\'avertissements': len(result.warnings),
            'Validateur': result.metadata.get('validator', 'N/A')
        })

st.markdown('</div>', unsafe_allow_html=True)
