"""
Codex Suite - Module Validateur FINAL
Validation XML/JSON avec pédagogie et auto-correction
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import de l'ancien système qui fonctionne
from modules.validator import validate

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

.pedagogy-box {
    background: rgba(0, 100, 150, 0.15);
    border-left: 4px solid #00D4FF;
    padding: 20px;
    margin: 16px 0;
    border-radius: 8px;
}

.pedagogy-box h4 {
    color: #00D4FF;
    margin: 0 0 12px 0;
    font-size: 18px;
}

.pedagogy-box p {
    color: rgba(255, 255, 255, 0.9);
    margin: 8px 0;
    line-height: 1.6;
}

.error-item {
    background: rgba(239, 68, 68, 0.1);
    border-left: 3px solid #ef4444;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.9);
}

.warning-item {
    background: rgba(251, 191, 36, 0.1);
    border-left: 3px solid #fbbf24;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.9);
}

.correction-box {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
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
    <h3>🎯 Validation Intelligente</h3>
    <p>Uploadez n'importe quel fichier de configuration DayZ (XML ou JSON). Le système détecte le type, localise précisément les erreurs et propose des corrections automatiques avec messages pédagogiques en français.</p>
</div>
""", unsafe_allow_html=True)

# Upload de fichier
uploaded_file = st.file_uploader(
    "Choisissez un fichier",
    type=['xml', 'json'],
    help="Types supportés : types.xml, events.xml, globals.xml, cfggameplay.json, etc."
)

if uploaded_file:
    # Lire le contenu
    content = uploaded_file.read().decode('utf-8')
    filename = uploaded_file.name
    
    # Déterminer le type de fichier
    file_type = "json" if filename.lower().endswith('.json') else "xml"
    
    # Bouton de validation
    if st.button("🚀 Valider le fichier", type="primary"):
        with st.spinner("Analyse en cours..."):
            # Validation avec l'ancien système qui fonctionne
            result = validate(content, file_type)
            
            # Stocker dans session state
            st.session_state.validation_result = result

# Afficher les résultats
if 'validation_result' in st.session_state:
    result = st.session_state.validation_result
    
    # Vérifier que result est valide
    if not result:
        st.error("❌ Erreur lors de la validation")
        st.stop()
    
    # ═══════════════════════════════════════════════════════
    # RÉSUMÉ
    # ═══════════════════════════════════════════════════════
    
    if result.get("valid", False):
        dayz_type = result.get("dayz_type", "Fichier DayZ")
        st.markdown(f"""
        <div class="result-box success">
            <h2 style="color: #00D4FF; margin: 0;">✅ Fichier Valide</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                Type détecté : <strong>{dayz_type or 'Inconnu'}</strong> ({result.get("file_type", "unknown").upper()})
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-box error">
            <h2 style="color: #ef4444; margin: 0;">❌ Erreurs Détectées</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                Erreur de syntaxe trouvée
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # PÉDAGOGIE (si erreur avec matching)
    # ═══════════════════════════════════════════════════════
    
    if not result.get("valid", False) and result.get("error") and result.get("error", {}).get("matched"):
        matched = result["error"]["matched"]
        
        st.markdown(f"""
        <div class="pedagogy-box">
            <h4>💡 {matched.get('title', 'Explication')}</h4>
            <p><strong>Pour les débutants :</strong><br>{matched.get('message_novice', '')}</p>
            <p><strong>Pour les moddeurs :</strong><br>{matched.get('message_modder', '')}</p>
            <p><strong>Solution :</strong><br>{matched.get('solution', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Exemples avant/après
        if matched.get('example_before') or matched.get('example_after'):
            col1, col2 = st.columns(2)
            
            with col1:
                if matched.get('example_before'):
                    st.markdown("**❌ Avant (incorrect) :**")
                    st.code(matched['example_before'], language=result.get("file_type", "text"))
            
            with col2:
                if matched.get('example_after'):
                    st.markdown("**✅ Après (correct) :**")
                    st.code(matched['example_after'], language=result.get("file_type", "text"))
    
    # ═══════════════════════════════════════════════════════
    # LOCALISATION PRÉCISE (si disponible)
    # ═══════════════════════════════════════════════════════
    
    if not result.get("valid", False) and result.get("error"):
        error = result["error"]
        
        st.markdown("### 🎯 Localisation de l'Erreur")
        
        # Ligne reportée par le parseur
        reported_line = error.get("line", "?")
        
        st.markdown(f"""
        <div class="error-item">
            <strong>Ligne signalée par le parseur :</strong> {reported_line}<br>
            <strong>Colonne :</strong> {error.get("column", "?")}<br>
            <strong>Message brut :</strong> {error.get("message_brut", "Erreur inconnue")}
        </div>
        """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # CORRECTION AUTOMATIQUE
    # ═══════════════════════════════════════════════════════
    
    if result.get("corrected"):
        st.markdown("""
        <div class="correction-box">
            <h3 style="color: #22c55e; margin: 0 0 12px 0;">✨ Correction Automatique Disponible</h3>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">
                Le fichier a été corrigé automatiquement !
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code(result["corrected"], language=result.get("file_type", "text"))
        
        st.download_button(
            label="💾 Télécharger le fichier corrigé",
            data=result["corrected"],
            file_name=f"corrigé_{uploaded_file.name}",
            mime="text/plain",
            type="primary"
        )
    
    # ═══════════════════════════════════════════════════════
    # ONGLETS DÉTAILS
    # ═══════════════════════════════════════════════════════
    
    tab1, tab2, tab3 = st.tabs(["📄 Formaté", "⚠️ Avertissements Sémantiques", "ℹ️ Informations"])
    
    with tab1:
        if result.get("formatted"):
            st.subheader("📄 Fichier Formaté")
            st.code(result["formatted"], language=result.get("file_type", "text"))
            
            st.download_button(
                label="💾 Télécharger formaté",
                data=result["formatted"],
                file_name=f"formaté_{uploaded_file.name}",
                mime="text/plain"
            )
        else:
            st.info("Formatage non disponible (erreur de syntaxe).")
    
    with tab2:
        if result.get("semantic_warnings"):
            st.markdown("### ⚠️ Avertissements Sémantiques")
            for warning in result["semantic_warnings"]:
                severity = warning.get("severity", "warning")
                message = warning.get("message", "")
                line = warning.get("line", 0)
                
                if severity == "error":
                    st.markdown(f"""
                    <div class="error-item">
                        <strong>Ligne {line}</strong><br>
                        {message}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="warning-item">
                        <strong>Ligne {line}</strong><br>
                        {message}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Aucun avertissement sémantique.")
    
    with tab3:
        info_data = {
            'Type de fichier': result.get('dayz_type') or 'Inconnu',
            'Format': result.get("file_type", "unknown").upper(),
            'Fichier valide': '✅ Oui' if result.get("valid", False) else '❌ Non',
            'Correction auto disponible': '✅ Oui' if result.get("corrected") else '❌ Non',
            'Formatage disponible': '✅ Oui' if result.get("formatted") else '❌ Non'
        }
        
        if result.get("semantic_warnings"):
            info_data['Avertissements sémantiques'] = len(result["semantic_warnings"])
        
        st.json(info_data)

st.markdown('</div>', unsafe_allow_html=True)
