"""
Codex Suite - HYBRID LIGHT + GALACTIC HEADER
Black × Glacier Blue + Header spatial
Créé par EpSy
"""

import streamlit as st

st.set_page_config(
    page_title="Codex Suite",
    page_icon="images/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Image horizon spatial encodée en base64
HORIZON_IMAGE = "/9j/4AAQSkZJRgABAQEBLAEsAAD/4QBWRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAITAAMAAAABAAEAAAAAAAAAAAEsAAAAAQAAASwAAAAB/+0ALFBob3Rvc2hvcCAzLjAAOEJJTQQEAAAAAAAPHAFaAAMbJUccAQAA"  # Tronqué pour exemple

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Orbitron:wght@700;900&display=swap');

* {{ 
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: #000000;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* ═══════════════════════════════════════════════════════
   HEADER GALACTIQUE (NOUVEAU)
   ═══════════════════════════════════════════════════════ */

.galactic-header {{
    background-image: url('data:image/jpeg;base64,{HORIZON_IMAGE}');
    background-size: cover;
    background-position: center bottom;
    padding: 60px 20px 50px 20px;
    text-align: center;
    position: relative;
    border-bottom: 2px solid #00D4FF;
    margin-bottom: 40px;
    overflow: hidden;
}}

.galactic-header::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, 
        rgba(0,0,0,0.9) 0%, 
        rgba(0,0,0,0.6) 40%, 
        rgba(0,0,0,0.85) 100%);
    z-index: 1;
}}

.galactic-header::after {{
    content: '';
    position: absolute;
    bottom: -2px; left: 0; right: 0;
    height: 2px;
    background: #00D4FF;
    box-shadow: 0 0 15px #00D4FF, 0 0 30px rgba(0, 212, 255, 0.5);
    z-index: 3;
}}

.galactic-logo {{
    font-family: 'Michroma', 'Orbitron', monospace;
    font-weight: 900;
    font-size: 84px;
    letter-spacing: 24px;
    color: #FFFFFF;
    text-transform: uppercase;
    margin: 0; padding: 0;
    position: relative;
    z-index: 2;
    line-height: 1;
    text-shadow: 
        0 0 10px rgba(255, 255, 255, 1),
        0 0 20px #00D4FF,
        0 0 40px #00D4FF,
        0 0 60px rgba(0, 212, 255, 0.6);
    animation: logo-pulse 4s ease-in-out infinite;
}}

@keyframes logo-pulse {{
    0%, 100% {{
        text-shadow: 
            0 0 10px rgba(255, 255, 255, 1),
            0 0 20px #00D4FF,
            0 0 40px #00D4FF,
            0 0 60px rgba(0, 212, 255, 0.6);
    }}
    50% {{
        text-shadow: 
            0 0 15px rgba(255, 255, 255, 1),
            0 0 30px #00D4FF,
            0 0 60px #00D4FF,
            0 0 90px rgba(0, 212, 255, 0.8);
    }}
}}

.galactic-tagline {{
    font-family: 'Michroma', sans-serif;
    font-weight: normal;
    font-size: 13px;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: rgba(0, 212, 255, 0.9);
    margin-top: 20px;
    position: relative;
    z-index: 2;
    text-shadow: 0 0 8px rgba(184, 230, 255, 0.6);
}}

@media (max-width: 768px) {{
    .galactic-logo {{ font-size: 52px; letter-spacing: 14px; }}
    .galactic-tagline {{ font-size: 10px; letter-spacing: 3px; }}
}}

/* ═══════════════════════════════════════════════════════
   TON CSS ACTUEL (CONSERVÉ)
   ═══════════════════════════════════════════════════════ */

/* HERO */
.hero-box {{
    text-align: center;
    padding: 50px 20px 45px 20px;  /* Padding réduit car header au-dessus */
}}

.hero-title {{
    font-size: 76px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF 0%, #38BDF8 50%, #0EA5E9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
    letter-spacing: -2px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3));
}}

.hero-sub {{
    font-size: 22px;
    color: rgba(0, 212, 255, 0.9);
    margin-bottom: 45px;
}}

.pill {{
    display: inline-block;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00D4FF;
    padding: 11px 22px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    margin: 5px;
    transition: all 0.3s ease;
}}

.pill:hover {{
    background: rgba(0, 212, 255, 0.15);
    border-color: rgba(0, 212, 255, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 212, 255, 0.25);
}}

/* MODULES */
.modules-wrapper {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 30px;
}}

.section-title {{
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 50px;
}}

.card {{
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.6) 0%, rgba(0, 15, 30, 0.7) 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 26px;
    padding: 42px 32px;
    text-align: center;
    transition: all 0.4s ease;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}}

.card:hover {{
    transform: translateY(-8px);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 15px 40px rgba(0, 212, 255, 0.25);
}}

.card-icon {{
    font-size: 64px;
    margin-bottom: 24px;
    transition: transform 0.3s ease;
}}

.card:hover .card-icon {{
    transform: scale(1.08);
}}

.card-title {{
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 16px;
}}

.card-text {{
    color: rgba(0, 212, 255, 0.8);
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 24px;
}}

.card-list {{
    text-align: left;
    margin-top: 22px;
    padding-top: 22px;
    border-top: 1px solid rgba(0, 212, 255, 0.12);
}}

.list-line {{
    color: #00D4FF;
    font-size: 13px;
    margin: 10px 0;
    padding-left: 20px;
}}

.list-line::before {{
    content: '→';
    position: absolute;
    margin-left: -20px;
}}

/* STATS */
.stats-section {{
    background: rgba(0, 0, 0, 0.4);
    border-top: 1px solid rgba(0, 212, 255, 0.2);
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
    padding: 70px 30px;
    margin: 90px 0;
}}

.stat {{
    text-align: center;
    padding: 32px 22px;
    background: rgba(0, 25, 50, 0.4);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 18px;
    transition: all 0.3s ease;
}}

.stat:hover {{
    border-color: rgba(0, 212, 255, 0.4);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
}}

.stat-num {{
    font-size: 50px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}}

.stat-label {{
    color: rgba(0, 212, 255, 0.7);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}}

/* ROADMAP */
.roadmap {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 70px 30px;
}}

.roadmap-card {{
    background: rgba(0, 25, 50, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 22px;
    padding: 42px;
    transition: all 0.3s ease;
}}

.roadmap-card:hover {{
    border-color: rgba(0, 212, 255, 0.35);
    box-shadow: 0 6px 25px rgba(0, 212, 255, 0.15);
}}

.roadmap-title {{
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 26px;
}}

.roadmap-item {{
    color: #64748b;
    font-size: 15px;
    margin: 13px 0;
    padding-left: 30px;
}}

.roadmap-item.done {{
    color: #00D4FF;
}}

.roadmap-item.wip {{
    color: #fbbf24;
}}

.roadmap-item.done::before {{
    content: '✓ ';
}}

.roadmap-item.wip::before {{
    content: '⟳ ';
}}

/* FOOTER */
.footer {{
    text-align: center;
    padding: 65px 30px 45px 30px;
    margin-top: 90px;
    border-top: 1px solid rgba(0, 212, 255, 0.2);
}}

.footer-brand {{
    font-size: 21px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 12px;
}}

.footer-text {{
    color: #64748b;
    font-size: 13px;
    margin: 8px 0;
}}

.footer-link {{
    color: #00D4FF;
    text-decoration: none;
    margin: 0 16px;
    font-size: 13px;
    font-weight: 600;
    transition: color 0.3s ease;
}}

.footer-link:hover {{
    color: #38BDF8;
}}

/* BUTTONS */
.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000;
    border: none;
    border-radius: 13px;
    padding: 15px 30px;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.25);
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 212, 255, 0.35);
}}

@media (max-width: 768px) {{
    .hero-title {{ font-size: 50px; }}
    .hero-sub {{ font-size: 18px; }}
}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HEADER GALACTIQUE (NOUVEAU)
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="galactic-header">
    <h1 class="galactic-logo">CODEX</h1>
    <p class="galactic-tagline">
        Serveur de Soutien et d'Entraide à la Communauté DayZ Francophone
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TON CONTENU ACTUEL (CONSERVÉ)
# ═══════════════════════════════════════════════════════

# HERO
st.markdown("""
<div class="hero-box">
    <h1 class="hero-title">CODEX SUITE</h1>
    <p class="hero-sub">La boîte à outils ultime pour DayZ</p>
    <div>
        <span class="pill">🔍 VALIDATION AUTO</span>
        <span class="pill">🗺️ ÉDITEUR VISUEL</span>
        <span class="pill">📚 DOCUMENTATION</span>
        <span class="pill">🇫🇷 100% FRANÇAIS</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ... Le reste de ton code (modules, stats, roadmap, footer)
