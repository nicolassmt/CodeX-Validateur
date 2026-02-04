"""
Codex Suite - Module Documentation
Recueil pédagogique des fichiers de configuration DayZ
"""

import streamlit as st
from pathlib import Path

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex - Documentation",
    page_icon="📚",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
* { font-family: Inter, sans-serif; }

.doc-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 30px;
    border-radius: 16px;
    margin-bottom: 30px;
}

.doc-content {
    line-height: 1.8;
    font-size: 16px;
}

.doc-content h1, .doc-content h2, .doc-content h3 {
    color: #1f2937;
    margin-top: 30px;
    margin-bottom: 15px;
}

.doc-content code {
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
}

.doc-content pre {
    background: #1f2937;
    color: #f9fafb;
    padding: 20px;
    border-radius: 10px;
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("📚 Documentation DayZ")
st.subheader("Apprends à maîtriser les fichiers de configuration")

# Bouton retour
if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("app.py")

st.markdown("---")

# ==============================
# INTRO
# ==============================
st.markdown("""
<div class="doc-header">
    <h2>🎯 5 fichiers essentiels documentés</h2>
    <p>
        Documentation exhaustive, exemples concrets, et bonnes pratiques pour
        configurer ton serveur DayZ comme un pro.
    </p>
    <p><strong>170+ pages</strong> de documentation en français 🇫🇷</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# TABS DOCUMENTATION
# ==============================
doc_tabs = st.tabs([
    "📄 types.xml",
    "🚁 events.xml", 
    "💰 economy.xml",
    "🌐 globals.xml",
    "💬 messages.xml"
])

# Fonction helper pour charger les docs
def load_doc(filename):
    """Charge un fichier de documentation"""
    doc_path = Path("docs") / filename
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ Documentation `{filename}` non trouvée. Assure-toi que le fichier est dans le dossier `docs/`."

# ==============================
# TAB 1 : TYPES.XML
# ==============================
with doc_tabs[0]:
    st.markdown("## 📄 types.xml - Gestion des items et du loot")
    
    st.info("""
    **Ce fichier contrôle :**
    - Tous les items du jeu (1917 items vanilla)
    - Quantités de spawn (nominal, min, max)
    - Où ils apparaissent (<usage>, <value>)
    - Leur durée de vie (lifetime)
    - Leurs catégories et tiers
    """)
    
    with st.expander("📖 Voir la documentation complète (40 pages)"):
        content = load_doc("TYPES_XML_DOCUMENTATION.md")
        st.markdown(content)

# ==============================
# TAB 2 : EVENTS.XML
# ==============================
with doc_tabs[1]:
    st.markdown("## 🚁 events.xml - Événements dynamiques")
    
    st.info("""
    **Ce fichier contrôle :**
    - Crashs d'hélicoptères
    - Convois militaires
    - Animaux sauvages (ours, loups, cerfs)
    - Zombies infectés spéciaux
    - Véhicules spawnables
    """)
    
    with st.expander("📖 Voir la documentation complète (45 pages)"):
        content = load_doc("EVENTS_XML_DOCUMENTATION.md")
        st.markdown(content)

# ==============================
# TAB 3 : ECONOMY.XML
# ==============================
with doc_tabs[2]:
    st.markdown("## 💰 economy.xml - Économie globale")
    
    st.info("""
    **Ce fichier contrôle :**
    - 8 systèmes économiques (dynamic, animals, zombies, vehicles, etc.)
    - Flags de persistence (init, load, respawn, save)
    - **CRITIQUE** : Configuration incorrecte = perte de données !
    """)
    
    st.warning("⚠️ **ATTENTION** : Ce fichier est critique ! Une mauvaise config peut faire disparaître les bases joueurs ou les véhicules.")
    
    with st.expander("📖 Voir la documentation complète (35 pages)"):
        content = load_doc("ECONOMY_XML_DOCUMENTATION.md")
        st.markdown(content)

# ==============================
# TAB 4 : GLOBALS.XML
# ==============================
with doc_tabs[3]:
    st.markdown("## 🌐 globals.xml - Variables serveur")
    
    st.info("""
    **Ce fichier contrôle :**
    - 31 variables globales du serveur
    - Limites (AnimauxMax, ZombiesMax)
    - Timers de cleanup
    - Durabilité du loot
    - Flags de bases (refresh frequency)
    - Comportements serveur
    """)
    
    with st.expander("📖 Voir la documentation complète (50 pages)"):
        content = load_doc("GLOBALS_XML_DOCUMENTATION.md")
        st.markdown(content)

# ==============================
# TAB 5 : MESSAGES.XML
# ==============================
with doc_tabs[4]:
    st.markdown("## 💬 messages.xml - Messages automatiques")
    
    st.info("""
    **Ce fichier contrôle :**
    - Messages de bienvenue
    - Annonces périodiques
    - Restarts automatiques programmés
    - Comptes à rebours
    - Messages à la connexion
    """)
    
    with st.expander("📖 Voir la documentation complète (30 pages)"):
        content = load_doc("MESSAGES_XML_DOCUMENTATION.md")
        st.markdown(content)

# ==============================
# TÉLÉCHARGEMENT
# ==============================
st.markdown("---")
st.markdown("## 💾 Télécharger toute la documentation")

st.markdown("""
Tu peux télécharger l'intégralité de la documentation en PDF ou consulter 
les fichiers markdown sur GitHub :

- 📄 **PDF complet** : [Télécharger](lien_vers_pdf) *(à venir)*
- ⭐ **GitHub** : [Voir sur GitHub](https://github.com/EpSyDev/codex-validateur/tree/main/docs)
""")

# ==============================
# GUIDE DE DÉMARRAGE
# ==============================
st.markdown("---")
st.markdown("## 🚀 Guide de démarrage rapide")

quick_col1, quick_col2 = st.columns(2)

with quick_col1:
    st.markdown("""
    ### Pour débuter
    
    1. **Commence par globals.xml**
       - Plus simple
       - Variables claires
       - Impact direct
    
    2. **Puis types.xml**
       - Ajuste le loot
       - Teste progressivement
    
    3. **Enfin events.xml et economy.xml**
       - Plus complexes
       - Nécessitent de la compréhension
    """)

with quick_col2:
    st.markdown("""
    ### Ressources externes
    
    - 📺 [Wiki officiel DayZ](https://community.bistudio.com/wiki/DayZ:Server_Configuration)
    - 💬 [Discord Codex](https://discord.gg/CQR6KTJ63C)
    - 🎥 [Tutoriels YouTube](lien_youtube) *(à venir)*
    - 📝 [Forum communauté](lien_forum) *(à venir)*
    """)

# ==============================
# FAQ
# ==============================
st.markdown("---")
st.markdown("## ❓ FAQ")

with st.expander("📁 Où placer ces fichiers sur mon serveur ?"):
    st.markdown("""
    Ces fichiers vont dans :
    ```
    mpmissions/[nom_de_ta_mission]/db/
    ├── types.xml
    ├── events.xml
    ├── economy.xml  (ou cfgeconomycore.xml)
    ├── globals.xml
    └── messages.xml
    ```
    """)

with st.expander("🔄 Dois-je redémarrer le serveur après modification ?"):
    st.markdown("""
    - **types.xml, events.xml, economy.xml, globals.xml** : ✅ Restart OBLIGATOIRE
    - **messages.xml** : ❌ Pas de restart nécessaire (hot-reload selon version)
    """)

with st.expander("⚠️ Comment éviter de casser mon serveur ?"):
    st.markdown("""
    1. **TOUJOURS faire une sauvegarde** avant de modifier
    2. **Valider la syntaxe** avec le Validateur Codex
    3. **Tester sur un serveur local** avant prod
    4. **Modifier petit à petit** (pas tout en même temps)
    5. **Lire la documentation** de chaque variable avant modification
    """)

with st.expander("📊 Quels fichiers ont le plus d'impact ?"):
    st.markdown("""
    Par ordre d'importance :
    
    1. **economy.xml** 🔴 CRITIQUE
       - Peut faire perdre toutes les bases
    
    2. **types.xml** 🟠 IMPORTANT
       - Définit tout le loot
    
    3. **globals.xml** 🟡 MODÉRÉ
       - Affecte les performances
    
    4. **events.xml** 🟢 FAIBLE
       - Zombies et events
    
    5. **messages.xml** ⚪ COSMÉTIQUE
       - Juste des messages
    """)
