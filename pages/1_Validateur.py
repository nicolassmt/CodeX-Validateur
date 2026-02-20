"""
Codex Suite - Module Validateur ULTIME
Validation automatique + Pédagogie + Auto-correction
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
}

.warning-item {
    background: rgba(251, 191, 36, 0.1);
    border-left: 3px solid #fbbf24;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
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
    <p>Uploadez n'importe quel fichier de configuration DayZ (XML ou JSON). Le système détecte automatiquement le type, valide la syntaxe ET les règles métier, localise les erreurs avec précision et propose des corrections automatiques.</p>
</div>
""", unsafe_allow_html=True)

# Upload de fichier
uploaded_file = st.file_uploader(
    "Choisissez un fichier",
    type=['xml', 'json'],
    help="17+ types supportés : types.xml, events.xml, cfggameplay.json, etc."
)

if uploaded_file:
    # Lire le contenu
    content = uploaded_file.read().decode('utf-8')
    filename = uploaded_file.name
    
    # Bouton de validation
    if st.button("🚀 Valider le fichier", type="primary"):
        with st.spinner("Analyse en cours..."):
            # Validation avec le système ULTIME fusionné
            result = validator.validate(content, filename)
            
            # Stocker dans session state
            st.session_state.validation_result = result

# Afficher les résultats
if 'validation_result' in st.session_state:
    result = st.session_state.validation_result
    
    # ═══════════════════════════════════════════════════════
    # RÉSUMÉ
    # ═══════════════════════════════════════════════════════
    
    if result.valid:
        st.markdown(f"""
        <div class="result-box success">
            <h2 style="color: #00D4FF; margin: 0;">✅ Fichier Valide</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                Type détecté : <strong>{result.file_type or 'Inconnu'}</strong> ({result.format.upper()})
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
    
    # ═══════════════════════════════════════════════════════
    # PÉDAGOGIE (si erreur de syntaxe)
    # ═══════════════════════════════════════════════════════
    
    if not result.valid and result.pedagogy:
        pedagogy = result.pedagogy
        
        st.markdown(f"""
        <div class="pedagogy-box">
            <h4>💡 {pedagogy.get('title', 'Explication')}</h4>
            <p><strong>Problème :</strong> {pedagogy.get('message_novice', '')}</p>
            <p><strong>Solution :</strong> {pedagogy.get('solution', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Exemples avant/après
        if pedagogy.get('example_before') or pedagogy.get('example_after'):
            col1, col2 = st.columns(2)
            
            with col1:
                if pedagogy.get('example_before'):
                    st.markdown("**❌ Avant (incorrect) :**")
                    st.code(pedagogy['example_before'], language=result.format)
            
            with col2:
                if pedagogy.get('example_after'):
                    st.markdown("**✅ Après (correct) :**")
                    st.code(pedagogy['example_after'], language=result.format)
    
    # ═══════════════════════════════════════════════════════
    # CORRECTION AUTOMATIQUE
    # ═══════════════════════════════════════════════════════
    
    if result.corrected_content:
        st.markdown("""
        <div class="correction-box">
            <h3 style="color: #22c55e; margin: 0 0 12px 0;">✨ Correction Automatique Disponible</h3>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">
                Les corrections suivantes ont été appliquées :
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        for correction in result.applied_corrections:
            st.success(f"✓ {correction}")
        
        st.code(result.corrected_content, language=result.format)
        
        st.download_button(
            label="💾 Télécharger le fichier corrigé",
            data=result.corrected_content,
            file_name=f"corrigé_{uploaded_file.name}",
            mime="text/plain",
            type="primary"
        )
    
    # ═══════════════════════════════════════════════════════
    # ONGLETS DÉTAILS
    # ═══════════════════════════════════════════════════════
    
    tab1, tab2, tab3, tab4 = st.tabs(["❌ Erreurs", "⚠️ Avertissements", "📄 Formaté", "ℹ️ Informations"])
    
    with tab1:
        if result.errors:
            for idx, error in enumerate(result.errors, 1):
                line = error.get('line', '?')
                message = error.get('message', 'Erreur inconnue')
                
                # Localisation précise si disponible
                if result.real_error_line:
                    real_line = result.real_error_line.get('real_line', line)
                    reason = result.real_error_line.get('reason', '')
                    if real_line != line:
                        st.info(f"🎯 **Localisation précise :** {reason}")
                        line = real_line
                
                st.markdown(f"""
                <div class="error-item">
                    <strong>Erreur #{idx} - Ligne {line}</strong><br>
                    {message}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Aucune erreur de syntaxe détectée ! ✅")
    
    with tab2:
        if result.warnings:
            for idx, warning in enumerate(result.warnings, 1):
                line = warning.get('line', '?')
                message = warning.get('message', 'Avertissement inconnu')
                suggestion = warning.get('suggestion', '')
                
                st.markdown(f"""
                <div class="warning-item">
                    <strong>Avertissement #{idx}</strong> {f'- Ligne {line}' if line != '?' else ''}<br>
                    {message}<br>
                    <small style="color: rgba(255,255,255,0.6);">{suggestion}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun avertissement.")
    
    with tab3:
        if result.formatted_content:
            st.subheader("📄 Fichier Formaté")
            st.code(result.formatted_content, language=result.format)
            
            st.download_button(
                label="💾 Télécharger formaté",
                data=result.formatted_content,
                file_name=f"formaté_{uploaded_file.name}",
                mime="text/plain"
            )
        else:
            st.info("Formatage non disponible pour ce fichier.")
    
    with tab4:
        st.json({
            'Type de fichier': result.file_type or 'Inconnu',
            'Format': result.format,
            'Confiance de détection': f"{result.confidence:.0%}",
            'Nombre d\'erreurs': len(result.errors),
            'Nombre d\'avertissements': len(result.warnings),
            'Validateur utilisé': result.metadata.get('validator', 'Détection seule'),
            'Correction auto disponible': result.corrected_content is not None
        })

st.markdown('</div>', unsafe_allow_html=True)
