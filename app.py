"""
Codex Suite - Page d'accueil
La boîte à outils DayZ francophone
Créé par EpSy
"""

import streamlit as st

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex Suite - Accueil",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CSS CUSTOM
# ==============================
st.markdown("""
<style>
* { 
    font-family: Inter, sans-serif; 
}

/* Cards modules */
.module-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
    border: 2px solid #e5e7eb;
}

.module-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    border-color: #667eea;
}

.module-icon {
    font-size: 64px;
    margin-bottom: 20px;
}

.module-title {
    font-size: 24px;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 15px;
}

.module-description {
    color: #6b7280;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.hero-section {
    text-align: center;
    padding: 40px 0;
    margin-bottom: 40px;
}

.hero-title {
    font-size: 48px;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 20px;
    color: #6b7280;
    margin-bottom: 30px;
}

.footer {
    text-align: center;
    margin-top: 80px;
    padding-top: 40px;
    border-top: 2px solid #e5e7eb;
    color: #6b7280;
}

.feature-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    margin: 5px;
}

/* Sidebar custom */
.css-1d391kg {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("### 🎮 Navigation")
    st.markdown("Utilise le menu ci-dessus pour naviguer entre les modules")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    **Codex Suite** v2.0
    
    Suite d'outils pour la communauté DayZ francophone.
    
    Développé avec ❤️ par **EpSy**
    """)
    
    st.markdown("---")
    
    st.markdown("### 💬 Communauté")
    st.markdown("[💬 Discord](https://discord.gg/CQR6KTJ63C)")
    st.markdown("[⭐ GitHub](https://github.com/EpSyDev/codex-validateur)")

# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

# Hero section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🎮 Codex Suite</h1>
    <p class="hero-subtitle">La boîte à outils complète pour DayZ</p>
    <div>
        <span class="feature-badge">🔍 Validation</span>
        <span class="feature-badge">🗺️ Éditeur visuel</span>
        <span class="feature-badge">📚 Documentation</span>
        <span class="feature-badge">🇫🇷 100% Français</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# MODULES CARDS
# ==============================
st.markdown("## 🚀 Choisis ton module")
st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">📝</div>
        <div class="module-title">Validateur XML/JSON</div>
        <div class="module-description">
            Valide et corrige automatiquement tes fichiers de configuration DayZ.
            <br><br>
            ✅ Détection erreurs<br>
            ✅ Correction auto<br>
            ✅ Validation sémantique
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("🚀 Ouvrir le Validateur", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🗺️</div>
        <div class="module-title">Carte Interactive</div>
        <div class="module-description">
            Édite visuellement les spawns sur les cartes DayZ.
            <br><br>
            🗺️ Chernarus<br>
            🗺️ Livonia<br>
            🗺️ Sakhal
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("🗺️ Ouvrir la Carte", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">📚</div>
        <div class="module-title">Documentation</div>
        <div class="module-description">
            Apprends à maîtriser les fichiers de configuration DayZ.
            <br><br>
            📄 types.xml<br>
            🚁 events.xml<br>
            💰 economy.xml<br>
            🌐 globals.xml<br>
            💬 messages.xml
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("📖 Lire la Documentation", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Documentation.py")

# ==============================
# STATISTIQUES (optionnel)
# ==============================
st.markdown("---")
st.markdown("## 📊 Codex en chiffres")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Fichiers supportés", "5+")

with stat_col2:
    st.metric("Corrections auto", "100%")

with stat_col3:
    st.metric("Maps disponibles", "3")

with stat_col4:
    st.metric("Documentation", "170+ pages")

# ==============================
# ROADMAP (optionnel)
# ==============================
st.markdown("---")
st.markdown("## 🛣️ Roadmap")

roadmap_col1, roadmap_col2 = st.columns(2)

with roadmap_col1:
    st.markdown("""
    ### ✅ Disponible maintenant
    - ✅ Validateur XML/JSON complet
    - ✅ Correction automatique
    - ✅ Validation sémantique
    - ✅ Documentation exhaustive
    """)

with roadmap_col2:
    st.markdown("""
    ### 🚧 En développement
    - 🗺️ Éditeur visuel Chernarus
    - 🗺️ Éditeur visuel Livonia
    - 🗺️ Éditeur visuel Sakhal
    - 🎨 Templates préconfigurés
    """)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer">
    <p><strong>Codex Suite</strong> v2.0</p>
    <p>Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <p>
        <a href="https://discord.gg/CQR6KTJ63C" target="_blank">💬 Discord</a> •
        <a href="https://github.com/EpSyDev/codex-validateur" target="_blank">⭐ GitHub</a> •
        <a href="mailto:contact@exemple.com">📧 Contact</a>
    </p>
</div>
""", unsafe_allow_html=True)
