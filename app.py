"""
Codex Suite - Page d'accueil
La boîte à outils DayZ francophone
Créé par EpSy

🎨 REDESIGN v3.0 - Dark Premium Edition
"""

import streamlit as st

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex Suite - Accueil",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS CUSTOM - DARK PREMIUM
# ==============================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

/* GLOBAL STYLES */
* { 
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
}

/* Main app background */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 10, 0.95);
    border-right: 1px solid rgba(102, 126, 234, 0.2);
}

[data-testid="stSidebar"] * {
    color: #e5e5e5 !important;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 80px 20px 60px 20px;
    position: relative;
    overflow: hidden;
}

.hero-glow {
    position: absolute;
    top: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 800px;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.3) 0%, transparent 70%);
    filter: blur(80px);
    z-index: 0;
    pointer-events: none;
}

.hero-title {
    font-size: 72px;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff 0%, #667eea 50%, #ff00ea 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
    letter-spacing: -2px;
    position: relative;
    z-index: 1;
    text-shadow: 0 0 40px rgba(102, 126, 234, 0.5);
}

.hero-subtitle {
    font-size: 24px;
    color: #b8b8b8;
    font-weight: 300;
    margin-bottom: 40px;
    position: relative;
    z-index: 1;
}

.feature-badges {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.feature-badge {
    background: rgba(102, 126, 234, 0.15);
    border: 1px solid rgba(102, 126, 234, 0.3);
    color: #00d4ff;
    padding: 12px 24px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 600;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.feature-badge:hover {
    background: rgba(102, 126, 234, 0.25);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

/* Module Cards */
.modules-section {
    padding: 40px 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.section-title {
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    margin-bottom: 50px;
}

.module-card {
    background: rgba(26, 26, 46, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 24px;
    padding: 40px 30px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.module-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4ff, #667eea, #ff00ea);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.module-card:hover::before {
    opacity: 1;
}

.module-card:hover {
    transform: translateY(-8px);
    border-color: rgba(102, 126, 234, 0.5);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    background: rgba(26, 26, 46, 0.8);
}

.module-icon {
    font-size: 72px;
    margin-bottom: 25px;
    filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4));
}

.module-title {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 15px;
}

.module-description {
    color: #b8b8b8;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 25px;
}

.module-features {
    text-align: left;
    margin-top: 20px;
}

.feature-item {
    color: #00d4ff;
    font-size: 14px;
    margin: 8px 0;
    padding-left: 20px;
    position: relative;
}

.feature-item::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #667eea;
}

/* Stats Section */
.stats-section {
    background: rgba(10, 10, 10, 0.5);
    border-top: 1px solid rgba(102, 126, 234, 0.2);
    border-bottom: 1px solid rgba(102, 126, 234, 0.2);
    padding: 60px 20px;
    margin: 80px 0;
}

.stat-card {
    text-align: center;
    padding: 30px;
    background: rgba(26, 26, 46, 0.4);
    border: 1px solid rgba(102, 126, 234, 0.15);
    border-radius: 16px;
    backdrop-filter: blur(10px);
}

.stat-number {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #667eea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.stat-label {
    color: #b8b8b8;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Roadmap Section */
.roadmap-section {
    max-width: 1200px;
    margin: 0 auto;
    padding: 60px 20px;
}

.roadmap-card {
    background: rgba(26, 26, 46, 0.5);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 20px;
    padding: 40px;
    backdrop-filter: blur(10px);
}

.roadmap-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 25px;
}

.roadmap-item {
    color: #b8b8b8;
    font-size: 16px;
    margin: 15px 0;
    padding-left: 30px;
    position: relative;
}

.roadmap-item.done {
    color: #00d4ff;
}

.roadmap-item.wip {
    color: #ff9500;
}

.roadmap-item::before {
    position: absolute;
    left: 0;
    font-size: 18px;
}

.roadmap-item.done::before {
    content: '✓';
    color: #00d4ff;
}

.roadmap-item.wip::before {
    content: '⟳';
    color: #ff9500;
}

/* Footer */
.footer {
    text-align: center;
    padding: 60px 20px 40px 20px;
    margin-top: 80px;
    border-top: 1px solid rgba(102, 126, 234, 0.2);
}

.footer-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
}

.footer-text {
    color: #6b7280;
    font-size: 14px;
    margin: 8px 0;
}

.footer-links {
    margin-top: 20px;
}

.footer-link {
    color: #00d4ff;
    text-decoration: none;
    margin: 0 15px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.footer-link:hover {
    color: #667eea;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 48px;
    }
    
    .hero-subtitle {
        font-size: 18px;
    }
    
    .module-title {
        font-size: 22px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div class="hero-section">
    <div class="hero-glow"></div>
    <h1 class="hero-title">CODEX SUITE</h1>
    <p class="hero-subtitle">La boîte à outils ultime pour DayZ</p>
    <div class="feature-badges">
        <span class="feature-badge">🔍 Validation automatique</span>
        <span class="feature-badge">🗺️ Éditeur visuel</span>
        <span class="feature-badge">📚 Documentation complète</span>
        <span class="feature-badge">🇫🇷 100% Français</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================
# MODULES SECTION
# ==============================
st.markdown('<div class="modules-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Choisis ton module</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">📝</div>
        <div class="module-title">Validateur</div>
        <div class="module-description">
            Valide et corrige automatiquement tes fichiers de configuration DayZ
        </div>
        <div class="module-features">
            <div class="feature-item">Détection erreurs</div>
            <div class="feature-item">Correction automatique</div>
            <div class="feature-item">Validation sémantique</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("🚀 Ouvrir le Validateur", key="btn_validator"):
        st.switch_page("pages/1_📝_Validateur.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🗺️</div>
        <div class="module-title">Carte Interactive</div>
        <div class="module-description">
            Édite visuellement les spawns zombies sur les cartes DayZ
        </div>
        <div class="module-features">
            <div class="feature-item">Chernarus</div>
            <div class="feature-item">Livonia</div>
            <div class="feature-item">Sakhal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("🗺️ Ouvrir la Carte", key="btn_map"):
        st.switch_page("pages/2_🗺️_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">📚</div>
        <div class="module-title">Documentation</div>
        <div class="module-description">
            Apprends à maîtriser les fichiers de configuration DayZ
        </div>
        <div class="module-features">
            <div class="feature-item">types.xml</div>
            <div class="feature-item">events.xml</div>
            <div class="feature-item">economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("📖 Documentation", key="btn_docs"):
        st.switch_page("pages/3_📚_Documentation.py")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# STATS SECTION
# ==============================
st.markdown("""
<div class="stats-section">
    <h2 class="section-title">Codex en chiffres</h2>
""", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">5+</div>
        <div class="stat-label">Fichiers supportés</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">Corrections auto</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">Maps disponibles</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">170+</div>
        <div class="stat-label">Pages de doc</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# ROADMAP SECTION
# ==============================
st.markdown('<div class="roadmap-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Roadmap</h2>', unsafe_allow_html=True)

roadmap_col1, roadmap_col2 = st.columns(2, gap="large")

with roadmap_col1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">✅ Disponible</div>
        <div class="roadmap-item done">Validateur XML/JSON complet</div>
        <div class="roadmap-item done">Correction automatique</div>
        <div class="roadmap-item done">Validation sémantique</div>
        <div class="roadmap-item done">Documentation exhaustive</div>
        <div class="roadmap-item done">Carte interactive Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with roadmap_col2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">🚧 En développement</div>
        <div class="roadmap-item wip">Calibration Chernarus</div>
        <div class="roadmap-item wip">Calibration Sakhal</div>
        <div class="roadmap-item wip">Édition drag & drop</div>
        <div class="roadmap-item wip">Templates préconfigurés</div>
        <div class="roadmap-item wip">Export multi-format</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer">
    <div class="footer-title">CODEX SUITE v3.0</div>
    <p class="footer-text">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div class="footer-links">
        <a href="https://discord.gg/CQR6KTJ63C" target="_blank" class="footer-link">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" target="_blank" class="footer-link">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-link">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
