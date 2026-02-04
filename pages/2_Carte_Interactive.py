"""
Codex Suite - Module Carte Interactive
Éditeur visuel des spawns DayZ sur Chernarus, Livonia et Sakhal
"""

import streamlit as st

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex - Carte Interactive",
    page_icon="🗺️",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
* { font-family: Inter, sans-serif; }

.coming-soon {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 60px;
    border-radius: 20px;
    text-align: center;
    margin: 40px 0;
}

.coming-soon h2 {
    font-size: 48px;
    margin-bottom: 20px;
}

.coming-soon p {
    font-size: 20px;
    opacity: 0.9;
}

.feature-list {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 20px 0;
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

st.title("🗺️ Carte Interactive")
st.subheader("Édite visuellement les spawns sur les cartes DayZ")

# Bouton retour
if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("app.py")

st.markdown("---")

# ==============================
# TABS POUR LES 3 MAPS
# ==============================
tab1, tab2, tab3 = st.tabs(["🗺️ Chernarus", "🗺️ Livonia", "🗺️ Sakhal"])

with tab1:
    st.markdown("""
    <div class="coming-soon">
        <h2>🚧 Chernarus - En développement</h2>
        <p>L'éditeur visuel pour Chernarus arrive bientôt !</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-list">
        <h3>🎯 Fonctionnalités prévues :</h3>
        <ul>
            <li>✅ Carte interactive haute résolution de Chernarus</li>
            <li>✅ Visualisation des zones de spawn zombies</li>
            <li>✅ Cocher/décocher les spawns directement sur la carte</li>
            <li>✅ Ajuster les paramètres (smin, smax, dmin, dmax, radius)</li>
            <li>✅ Génération automatique de <code>zombie_territories.xml</code></li>
            <li>✅ Export prêt à uploader sur ton serveur</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📅 **Statut** : Phase de développement - Disponible dans une prochaine mise à jour")

with tab2:
    st.markdown("""
    <div class="coming-soon">
        <h2>🚧 Livonia - En développement</h2>
        <p>L'éditeur visuel pour Livonia arrive bientôt !</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-list">
        <h3>🎯 Fonctionnalités prévues :</h3>
        <ul>
            <li>✅ Carte interactive haute résolution de Livonia</li>
            <li>✅ Toutes les fonctionnalités de l'éditeur Chernarus</li>
            <li>✅ Zones spécifiques à Livonia (forêts, lacs, villages polonais)</li>
            <li>✅ Export <code>zombie_territories.xml</code> pour Livonia</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📅 **Statut** : Planifié après Chernarus")

with tab3:
    st.markdown("""
    <div class="coming-soon">
        <h2>🚧 Sakhal - En développement</h2>
        <p>L'éditeur visuel pour Sakhal arrive bientôt !</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-list">
        <h3>🎯 Fonctionnalités prévues :</h3>
        <ul>
            <li>✅ Carte interactive haute résolution de Sakhal</li>
            <li>✅ Toutes les fonctionnalités de l'éditeur Chernarus</li>
            <li>✅ Zones spécifiques à Sakhal (zones arctiques, installations)</li>
            <li>✅ Export <code>zombie_territories.xml</code> pour Sakhal</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📅 **Statut** : Planifié après Livonia")

# ==============================
# TIMELINE
# ==============================
st.markdown("---")
st.markdown("## 🛣️ Timeline de développement")

timeline_col1, timeline_col2, timeline_col3 = st.columns(3)

with timeline_col1:
    st.markdown("""
    ### Phase 1 : Chernarus
    - 📅 **Début** : Maintenant
    - 🎯 **Objectif** : Éditeur complet
    - ⏱️ **Durée estimée** : 2-3 semaines
    """)

with timeline_col2:
    st.markdown("""
    ### Phase 2 : Livonia
    - 📅 **Début** : Après Chernarus
    - 🎯 **Objectif** : Port sur Livonia
    - ⏱️ **Durée estimée** : 1-2 semaines
    """)

with timeline_col3:
    st.markdown("""
    ### Phase 3 : Sakhal
    - 📅 **Début** : Après Livonia
    - 🎯 **Objectif** : Port sur Sakhal
    - ⏱️ **Durée estimée** : 1-2 semaines
    """)

# ==============================
# APERÇU TECHNIQUE
# ==============================
st.markdown("---")
st.markdown("## 🔧 Aperçu technique")

st.markdown("""
L'éditeur de carte interactive utilisera :
- **Folium** ou **Plotly** pour la carte interactive
- **Image haute résolution** de chaque map
- **Zones cliquables** pour chaque spawn
- **Édition en temps réel** des paramètres
- **Génération XML** instantanée

### Exemple d'interface (mockup) :

```
┌─────────────────────────────────────────────────────┐
│  [Carte Chernarus]                                  │
│                                                      │
│  🔴 Zone Balota       [Actif ✓]  [Éditer]          │
│  🔴 Zone NWAF         [Actif ✓]  [Éditer]          │
│  ⚪ Zone Elektro      [Inactif]  [Éditer]          │
│  🔴 Zone Berezino     [Actif ✓]  [Éditer]          │
│                                                      │
│  [💾 Générer XML]  [⬇️ Télécharger]               │
└─────────────────────────────────────────────────────┘
```
""")

# ==============================
# CONTRIBUER
# ==============================
st.markdown("---")
st.markdown("## 🤝 Contribuer au développement")

st.info("""
**Tu veux participer au développement ?**

Rejoins-nous sur Discord pour :
- Tester les versions bêta
- Proposer des fonctionnalités
- Signaler des bugs
- Contribuer au code

💬 [Discord Codex](https://discord.gg/CQR6KTJ63C)
""")
