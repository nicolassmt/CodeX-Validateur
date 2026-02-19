"""
Codex Suite - VERSION FINALE
Police Sawah chargée en base64 depuis assets/fonts/
Créé par EpSy
"""

import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Codex Suite",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Chargement de la police Sawah en base64 ───────────────────────────────────
def load_font_b64(path: str) -> str:
    """Lit un fichier de police et retourne son contenu encodé en base64."""
    font_path = Path(__file__).parent / path
    if font_path.exists():
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

# ─── Sélection du meilleur format disponible ──────────────────────────────────
FONT_CANDIDATES = [
    ("assets/fonts/Sawah_PersonalUseOnly.woff2", "woff2"),
    ("assets/fonts/Sawah_PersonalUseOnly.woff",  "woff"),
    ("assets/fonts/Sawah_PersonalUseOnly.ttf",   "truetype"),
]

# ─── DEBUG TEMPORAIRE : affiche les chemins cherchés ──────────────────────────
for font_file, fmt in FONT_CANDIDATES:
    font_path = Path(__file__).parent / font_file
    st.write(f"🔍 `{font_file}` → existe : **{font_path.exists()}** | path : `{font_path}`")

# Priorité : woff2 > woff > ttf  (choisit le premier fichier trouvé)
FONT_CANDIDATES = [
    ("assets/fonts/Sawah_PersonalUseOnly.woff2", "woff2"),
    ("assets/fonts/Sawah_PersonalUseOnly.woff",  "woff"),
    ("assets/fonts/Sawah_PersonalUseOnly.ttf",   "truetype"),
]

font_face_block = ""
for font_file, fmt in FONT_CANDIDATES:
    b64 = load_font_b64(font_file)
    if b64:
        font_face_block = f"""
@font-face {{
    font-family: 'Sawah';
    src: url('data:font/{fmt};base64,{b64}') format('{fmt}');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}}"""
        break  # premier format trouvé suffit

# ═══════════════════════════════════════════════════════
# CSS PARTIE 1 : Imports + Font Face
# ═══════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Orbitron:wght@700;900&display=swap');

{font_face_block}

* {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: #000000; }}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# CSS PARTIE 2 : Tous les autres styles
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
.galactic-header {
    background: linear-gradient(180deg, #000000 0%, #0A1628 50%, #000000 100%);
    padding: 90px 20px 70px 20px;
    text-align: center;
    border-bottom: 2px solid #00D4FF;
    margin-bottom: 60px;
    box-shadow: 0 5px 30px rgba(0, 212, 255, 0.4);
}

.galactic-logo {
    font-family: 'Sawah', 'Michroma', monospace !important;
    font-weight: normal !important;
    font-size: 200px !important;
    letter-spacing: 45px !important;
    color: #FFFFFF !important;
    text-transform: uppercase !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 0.9 !important;
    text-shadow: 
        0 0 20px rgba(255, 255, 255, 1),
        0 0 40px #00D4FF,
        0 0 70px #00D4FF,
        0 0 100px rgba(0, 212, 255, 0.8),
        0 0 130px rgba(0, 212, 255, 0.6);
    animation: logo-pulse 2s ease-in-out infinite;
}

@keyframes logo-pulse {
    0%, 100% {
        text-shadow: 
            0 0 15px rgba(255, 255, 255, 1),
            0 0 30px #00D4FF,
            0 0 50px #00D4FF,
            0 0 70px rgba(0, 212, 255, 0.7);
    }
    50% {
        text-shadow: 
            0 0 20px rgba(255, 255, 255, 1),
            0 0 40px #00D4FF,
            0 0 70px #00D4FF,
            0 0 100px rgba(0, 212, 255, 0.9),
            0 0 130px rgba(0, 212, 255, 0.6);
    }
}

.galactic-tagline {
    font-family: 'Michroma', sans-serif;
    font-weight: normal;
    font-size: 16px;
    letter-spacing: 8px;
    text-transform: uppercase;
    color: rgba(0, 212, 255, 0.95);
    margin-top: 30px;
    line-height: 1.6;
    text-shadow: 0 0 10px rgba(184, 230, 255, 0.7);
}

.modules-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 30px 80px 30px;
}

.section-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 55px;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

.card {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 26px;
    padding: 44px 34px;
    text-align: center;
    transition: all 0.4s ease;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    height: 100%;
}

.card:hover {
    transform: translateY(-10px);
    border-color: rgba(0, 212, 255, 0.6);
    box-shadow: 0 18px 45px rgba(0, 212, 255, 0.3);
}

.card-icon { font-size: 68px; margin-bottom: 26px; transition: transform 0.3s ease; }
.card:hover .card-icon { transform: scale(1.12); }
.card-title { font-size: 28px; font-weight: 800; color: #FFFFFF; margin-bottom: 18px; }
.card-text { color: rgba(0, 212, 255, 0.85); font-size: 15px; line-height: 1.7; margin-bottom: 26px; }
.card-list { text-align: left; margin-top: 24px; padding-top: 24px; border-top: 1px solid rgba(0, 212, 255, 0.15); }
.list-line { color: #00D4FF; font-size: 13px; margin: 11px 0; padding-left: 22px; position: relative; }
.list-line::before { content: '→'; position: absolute; left: 0; }

.stats-section {
    background: rgba(0, 0, 0, 0.5);
    border-top: 1px solid rgba(0, 212, 255, 0.25);
    border-bottom: 1px solid rgba(0, 212, 255, 0.25);
    padding: 75px 30px;
    margin: 100px 0;
}

.stat {
    text-align: center;
    padding: 36px 24px;
    background: rgba(0, 25, 50, 0.45);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    transition: all 0.3s ease;
}

.stat:hover {
    border-color: rgba(0, 212, 255, 0.45);
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(0, 212, 255, 0.25);
}

.stat-num {
    font-size: 54px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}

.stat-label {
    color: rgba(0, 212, 255, 0.75);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.roadmap { max-width: 1200px; margin: 0 auto; padding: 75px 30px; }
.roadmap-card { background: rgba(0, 25, 50, 0.55); border: 1px solid rgba(0, 212, 255, 0.25); border-radius: 24px; padding: 44px; transition: all 0.3s ease; }
.roadmap-card:hover { border-color: rgba(0, 212, 255, 0.4); box-shadow: 0 8px 30px rgba(0, 212, 255, 0.2); }
.roadmap-title { font-size: 26px; font-weight: 800; color: #FFFFFF; margin-bottom: 28px; }
.roadmap-item { color: #64748b; font-size: 15px; margin: 14px 0; padding-left: 32px; position: relative; }
.roadmap-item.done { color: #00D4FF; }
.roadmap-item.wip { color: #fbbf24; }
.roadmap-item.done::before { content: '✓ '; position: absolute; left: 0; }
.roadmap-item.wip::before { content: '⟳ '; position: absolute; left: 0; }

.footer { text-align: center; padding: 70px 30px 50px 30px; margin-top: 100px; border-top: 1px solid rgba(0, 212, 255, 0.25); }
.footer-brand { font-size: 22px; font-weight: 800; color: #FFFFFF; margin-bottom: 14px; }
.footer-text { color: #64748b; font-size: 13px; margin: 10px 0; }
.footer-link { color: #00D4FF; text-decoration: none; margin: 0 18px; font-size: 13px; font-weight: 600; transition: color 0.3s ease; }
.footer-link:hover { color: #38BDF8; }

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

@media (max-width: 1200px) {
    .galactic-logo { font-size: 120px !important; letter-spacing: 32px !important; }
    .galactic-tagline { font-size: 14px; letter-spacing: 6px; }
}

@media (max-width: 768px) {
    .galactic-logo { font-size: 80px !important; letter-spacing: 20px !important; }
    .galactic-tagline { font-size: 11px; letter-spacing: 4px; }
    .section-title { font-size: 32px; }
}

@media (max-width: 480px) {
    .galactic-logo { font-size: 50px !important; letter-spacing: 12px !important; }
    .galactic-tagline { font-size: 9px; letter-spacing: 3px; }
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="galactic-header">
    <h1 class="galactic-logo">CODEX</h1>
    <p class="galactic-tagline">
        Serveur de Soutien et d'Entraide à la Communauté DayZ Francophone
    </p>
</div>
""", unsafe_allow_html=True)

# ─── MODULES ───────────────────────────────────────────────────────────────────
st.markdown('<div class="modules-wrapper"><h2 class="section-title">🚀 Modules disponibles</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📝</div>
        <div class="card-title">Validateur</div>
        <div class="card-text">Valide et corrige automatiquement tes fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-line">Détection erreurs</div>
            <div class="list-line">Correction automatique</div>
            <div class="list-line">Validation sémantique</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🚀 Ouvrir", key="v"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🗺️</div>
        <div class="card-title">Carte Interactive</div>
        <div class="card-text">Édite visuellement les spawns zombies sur les cartes DayZ</div>
        <div class="card-list">
            <div class="list-line">Chernarus</div>
            <div class="list-line">Livonia</div>
            <div class="list-line">Sakhal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🗺️ Ouvrir", key="m"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📚</div>
        <div class="card-title">Documentation</div>
        <div class="card-text">Apprends à maîtriser les fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-line">types.xml</div>
            <div class="list-line">events.xml</div>
            <div class="list-line">economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("📖 Ouvrir", key="d"):
        st.switch_page("pages/3_Documentation.py")

st.markdown('</div>', unsafe_allow_html=True)

# ─── STATS ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="stats-section"><h2 class="section-title">📊 Codex en chiffres</h2>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat"><div class="stat-num">13+</div><div class="stat-label">Validateurs</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat"><div class="stat-num">100%</div><div class="stat-label">Auto</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat"><div class="stat-num">3</div><div class="stat-label">Maps</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat"><div class="stat-num">170+</div><div class="stat-label">Docs</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── ROADMAP ───────────────────────────────────────────────────────────────────
st.markdown('<div class="roadmap"><h2 class="section-title">🛣️ Roadmap</h2>', unsafe_allow_html=True)

r1, r2 = st.columns(2, gap="large")
with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">✅ Disponible</div>
        <div class="roadmap-item done">13 Validateurs complets</div>
        <div class="roadmap-item done">Correction automatique</div>
        <div class="roadmap-item done">Validation sémantique</div>
        <div class="roadmap-item done">Documentation complète</div>
        <div class="roadmap-item done">Carte Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">🚧 En cours</div>
        <div class="roadmap-item wip">Calibration Chernarus</div>
        <div class="roadmap-item wip">Calibration Sakhal</div>
        <div class="roadmap-item wip">Éditeur types.xml</div>
        <div class="roadmap-item wip">Templates prêts</div>
        <div class="roadmap-item wip">Chatbot IA</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-brand">CODEX SUITE v3.0</div>
    <p class="footer-text">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div style="margin-top: 24px;">
        <a href="https://discord.gg/CQR6KTJ63C" class="footer-link">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" class="footer-link">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-link">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
