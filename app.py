"""
Codex Validateur XML/JSON
Outil pédagogique de validation et correction
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier modules au path Python
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from modules.validator import validate
from modules.locator import locate_real_error
from modules.comparator import compare_before_after, compare_side_by_side
from modules.corrector import auto_correct, can_auto_correct, suggest_manual_fixes


# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex Validateur XML/JSON",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==============================
# CSS
# ==============================
st.markdown("""
<style>
* { font-family: Inter, sans-serif; }

.block {
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
}

.identification { 
    background: linear-gradient(135deg, #667eea, #764ba2); 
    color: white; 
}

.localisation { 
    background: linear-gradient(135deg, #f6d365, #fda085); 
    color: #7c2d12;
}

.description { 
    background: linear-gradient(135deg, #fa709a, #fee140); 
    color: #7f1d1d;
}

.solution { 
    background: linear-gradient(135deg, #84fab0, #8fd3f4); 
    color: #065f46;
}

.success-block {
    background: linear-gradient(135deg, #a8edea, #fed6e3);
    padding: 20px;
    border-radius: 14px;
    margin: 20px 0;
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 2px solid #e5e7eb;
    color: #6b7280;
}

/* Scroll pour le code analysé */
.code-scroll {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 10px;
    background: #f9fafb;
}

/* Alerte post-correction */
.correction-alert {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #78350f;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
    font-size: 1.1em;
    font-weight: 600;
    text-align: center;
    border: 3px solid #f59e0b;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}
</style>
""", unsafe_allow_html=True)


# ==============================
# SESSION STATE
# ==============================
defaults = {
    "content": "",
    "filename": "",
    "filetype": None,
    "validation_result": None,
    "corrected_content": None,
    "show_comparison": False,
    "user_level": "novice",
    "correction_applied": False,
    "just_corrected": False  # Nouveau flag pour message visible
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("🎮 Codex Validateur XML / JSON")
st.subheader("Comprendre, corriger et fiabiliser tes fichiers DayZ")

# Sélecteur de niveau utilisateur
col_level_1, col_level_2, col_level_3 = st.columns([1, 1, 2])
with col_level_1:
    user_level = st.radio(
        "Ton niveau :",
        ["novice", "modder"],
        index=0 if st.session_state.user_level == "novice" else 1,
        horizontal=True
    )
    st.session_state.user_level = user_level

st.markdown("---")


# ==============================
# UPLOAD
# ==============================
uploaded = st.file_uploader(
    "📤 Dépose ton fichier XML ou JSON",
    type=["xml", "json"],
    help="Fichiers DayZ acceptés : cfgweather.xml, cfgeventsapawns.xml, types.xml, cfggameplay.json, etc."
)

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1].lower()
    st.session_state.validation_result = None
    st.session_state.corrected_content = None
    st.session_state.show_comparison = False
    st.session_state.correction_applied = False
    st.session_state.just_corrected = False


# ==============================
# ZONE DE TEXTE (si pas de fichier uploadé)
# ==============================
if not uploaded:
    st.markdown("### ✏️ Ou colle ton code directement ici")
    
    col_type_1, col_type_2 = st.columns(2)
    with col_type_1:
        manual_type = st.selectbox(
            "Type de fichier",
            ["xml", "json"],
            help="Sélectionne le type de ton code"
        )
    
    content_input = st.text_area(
        "Code",
        value=st.session_state.content,
        height=300,
        placeholder="Colle ton code XML ou JSON ici..."
    )
    
    if content_input != st.session_state.content:
        st.session_state.content = content_input
        st.session_state.filetype = manual_type
        st.session_state.filename = f"code_colle.{manual_type}"
        st.session_state.validation_result = None
        st.session_state.corrected_content = None
        st.session_state.show_comparison = False
        st.session_state.correction_applied = False
        st.session_state.just_corrected = False

st.markdown("---")


# ==============================
# ALERTE POST-CORRECTION (FIX 3)
# ==============================
if st.session_state.just_corrected:
    st.markdown("""
    <div class="correction-alert">
        ✅ CORRECTION EFFECTUÉE ! 
        <br>
        👇 Remonte voir la comparaison avant/après ci-dessous 👇
    </div>
    """, unsafe_allow_html=True)
    st.session_state.just_corrected = False  # Reset pour ne pas réafficher


# ==============================
# BOUTONS D'ACTION
# ==============================
if st.session_state.content:
    st.markdown("### 🎯 Actions disponibles")
    
    col_btn_1, col_btn_2, col_btn_3, col_btn_4 = st.columns(4)
    
    with col_btn_1:
        if st.button("🔍 Valider", use_container_width=True, type="primary"):
            with st.spinner("Validation en cours..."):
                result = validate(st.session_state.content, st.session_state.filetype)
                st.session_state.validation_result = result
                st.session_state.show_comparison = False
    
    with col_btn_2:
        # Bouton correction : actif uniquement si validation échouée
        can_correct = (
            st.session_state.validation_result and 
            not st.session_state.validation_result["valid"]
        )
        
        if st.button("🔧 Auto-corriger", use_container_width=True, disabled=not can_correct, key="btn_correct_top"):
            with st.spinner("Correction en cours..."):
                correction = auto_correct(
                    st.session_state.content, 
                    st.session_state.filetype
                )
                
                if correction["has_changes"]:
                    st.session_state.corrected_content = correction["corrected"]
                    st.session_state.show_comparison = True
                    st.session_state.just_corrected = True  # FIX 3 : Flag pour afficher l'alerte
                    st.success(f"✅ {len(correction['applied_corrections'])} correction(s) appliquée(s)")
                    st.rerun()
                else:
                    st.info("ℹ️ Aucune correction automatique possible pour cette erreur")
    
    with col_btn_3:
        if st.button("🗑️ Réinitialiser", use_container_width=True):
            for key in defaults.keys():
                st.session_state[key] = defaults[key]
            st.rerun()
    
    with col_btn_4:
        # FIX 4 : Bouton télécharger actif si validation OK OU correction appliquée
        download_enabled = (
            (st.session_state.validation_result and st.session_state.validation_result["valid"]) or
            st.session_state.correction_applied
        )
        
        if download_enabled:
            download_content = st.session_state.content
            download_filename = st.session_state.filename
            
            if st.session_state.correction_applied:
                name_parts = st.session_state.filename.rsplit(".", 1)
                if len(name_parts) == 2:
                    download_filename = f"{name_parts[0]}_corrige.{name_parts[1]}"
                else:
                    download_filename = f"{st.session_state.filename}_corrige"
            
            st.download_button(
                "💾 Télécharger",
                data=download_content,
                file_name=download_filename,
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.button("💾 Télécharger", use_container_width=True, disabled=True, help="Valide d'abord ton fichier")

st.markdown("---")


# ==============================
# COMPARAISON AVANT/APRÈS (affichée EN PREMIER si dispo)
# ==============================
if st.session_state.show_comparison and st.session_state.corrected_content:
    st.markdown("### 🔄 Comparaison avant / après correction")
    
    comparison = compare_side_by_side(
        st.session_state.content,
        st.session_state.corrected_content
    )
    
    col_comp_1, col_comp_2 = st.columns(2)
    
    with col_comp_1:
        st.markdown("**❌ Avant**")
        before_code = "\n".join([
            f"{'🔴 ' if changed else '   '}{content}"
            for num, content, changed in comparison["before_lines"]
        ])
        st.code(before_code, language=st.session_state.filetype, line_numbers=True)
    
    with col_comp_2:
        st.markdown("**✅ Après**")
        after_code = "\n".join([
            f"{'✅ ' if changed else '   '}{content}"
            for num, content, changed in comparison["after_lines"]
        ])
        st.code(after_code, language=st.session_state.filetype, line_numbers=True)
    
    # Bouton pour appliquer la correction
    col_apply_1, col_apply_2, col_apply_3 = st.columns([1, 1, 2])
    
    with col_apply_1:
        if st.button("✅ Appliquer la correction", use_container_width=True, type="primary"):
            st.session_state.content = st.session_state.corrected_content
            st.session_state.corrected_content = None
            st.session_state.validation_result = None
            st.session_state.show_comparison = False
            st.session_state.correction_applied = True  # FIX 4 : Marquer comme corrigé
            st.success("✅ Correction appliquée ! Tu peux maintenant re-valider ou télécharger le fichier.")
            st.rerun()
    
    with col_apply_2:
        if st.button("❌ Annuler", use_container_width=True):
            st.session_state.corrected_content = None
            st.session_state.show_comparison = False
            st.rerun()
    
    st.markdown("---")


# ==============================
# AFFICHAGE DES RÉSULTATS
# ==============================
if st.session_state.validation_result:
    result = st.session_state.validation_result
    
    # ==============================
    # CAS 1 : FICHIER VALIDE
    # ==============================
    if result["valid"]:
        st.markdown("""
        <div class="success-block">
            <h3>✅ Nickel ! Ton fichier est parfait !</h3>
            <p>Aucune erreur détectée. Le fichier est prêt pour DayZ.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🎨 Code formaté")
        st.code(result["formatted"], language=result["file_type"], line_numbers=True)
    
    # ==============================
    # CAS 2 : FICHIER AVEC ERREUR
    # ==============================
    else:
        error = result["error"]
        matched = error["matched"]
        
        # Niveau de message selon utilisateur
        if matched:
            if st.session_state.user_level == "novice":
                message_user = matched["message_novice"]
            else:
                message_user = matched["message_modder"]
        else:
            message_user = error["message_brut"]
        
        # ==============================
        # FIX 1 : ORDRE LOGIQUE - D'ABORD LOCALISATION + EXTRAIT
        # ==============================
        
        # Calcul de la vraie ligne (smart locate pour XML)
        reported_line = error["line"]
        real_line = reported_line
        confidence = None
        reason = None
        
        if result["file_type"] == "xml":
            location = locate_real_error(st.session_state.content, reported_line)
            real_line = location["real_line"]
            confidence = location["confidence"]
            reason = location["reason"]
        
        # ==============================
        # BLOC 1 : LOCALISATION (en premier pour visuel immédiat)
        # ==============================
        if result["file_type"] == "xml" and real_line != reported_line:
            st.markdown(f"""
            <div class="block localisation">
                <h4>📍 Localisation de l'erreur</h4>
                <p><strong>🎯 Ligne probable :</strong> {real_line} (confiance : {confidence})</p>
                <p><strong>Colonne :</strong> {error["column"]}</p>
                <p><strong>💡 Explication :</strong> {reason}</p>
                <p style="font-size: 0.9em; margin-top: 10px;">
                    <em>Note : Le parseur indiquait ligne {reported_line}, mais l'analyse a identifié la cause réelle plus haut.</em>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="block localisation">
                <h4>📍 Localisation de l'erreur</h4>
                <p><strong>Ligne :</strong> {real_line}</p>
                <p><strong>Colonne :</strong> {error["column"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 2 : EXTRAIT RÉEL (juste après la localisation)
        # ==============================
        st.markdown("#### 📝 Extrait autour de l'erreur")
        
        lines = st.session_state.content.splitlines()
        start_line = max(1, real_line - 3)
        end_line = min(len(lines), real_line + 3)
        
        extract_lines = []
        for i in range(start_line, end_line + 1):
            line_content = lines[i - 1] if i <= len(lines) else ""
            if i == real_line:
                extract_lines.append(f"🔴 LIGNE {i} → {line_content}")
            else:
                extract_lines.append(f"   LIGNE {i}   {line_content}")
        
        extract_code = "\n".join(extract_lines)
        st.code(extract_code, language=result["file_type"])
        
        # ==============================
        # BLOC 3 : IDENTIFICATION
        # ==============================
        st.markdown(f"""
        <div class="block identification">
            <h4>🧩 Identification</h4>
            <p><strong>Type de fichier :</strong> {result["file_type"].upper()}</p>
            <p><strong>Erreur détectée :</strong> {matched["titre"] if matched else "Erreur de syntaxe"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 4 : DESCRIPTION
        # ==============================
        st.markdown(f"""
        <div class="block description">
            <h4>🧠 Description de l'erreur</h4>
            <p>{message_user}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==============================
        # FIX 2 : SOLUTION PLUS DIRECTIVE
        # ==============================
        if matched:
            can_auto = can_auto_correct(matched)
            
            if can_auto:
                st.markdown(f"""
                <div class="block solution">
                    <h4>💡 Solution</h4>
                    <p>✅ <strong>Cette erreur peut être corrigée automatiquement !</strong></p>
                    
                    <p><strong>👉 Action immédiate :</strong></p>
                    <ol>
                        <li>Clique sur le bouton <strong>"🔧 Auto-corriger"</strong> (en haut de la page ou ci-dessous)</li>
                        <li>Compare l'avant/après qui s'affichera</li>
                        <li>Clique sur <strong>"✅ Appliquer"</strong> si la correction te convient</li>
                        <li>Re-valide le fichier pour confirmer qu'il n'y a plus d'erreur</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Suggestions manuelles
                suggestions = suggest_manual_fixes(
                    st.session_state.content,
                    result["file_type"],
                    matched
                )
                
                steps_html = "".join([f"<li>{step}</li>" for step in suggestions["manual_steps"]])
                
                st.markdown(f"""
                <div class="block solution">
                    <h4>💡 Solution</h4>
                    <p>⚠️ <strong>Cette erreur nécessite une correction manuelle.</strong></p>
                    
                    <p><strong>👉 Étapes à suivre :</strong></p>
                    <ol>
                        {steps_html}
                        <li>Modifie ton fichier selon ces indications</li>
                        <li>Re-charge le fichier corrigé dans l'outil</li>
                        <li>Clique sur <strong>"🔍 Valider"</strong> pour vérifier</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 5 : CODE COMPLET (avec scroll)
        # ==============================
        st.markdown("#### 📄 Code complet analysé")
        
        highlighted_lines = []
        for i, line in enumerate(lines, start=1):
            if i == real_line:
                highlighted_lines.append(f"🔴 → {line}")
            else:
                highlighted_lines.append(f"     {line}")
        
        highlighted_code = "\n".join(highlighted_lines)
        
        st.markdown('<div class="code-scroll">', unsafe_allow_html=True)
        st.code(highlighted_code, language=result["file_type"], line_numbers=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Exemple de la DB en expander
        if matched and matched.get("exemple_avant"):
            with st.expander("💡 Voir un exemple de correction similaire"):
                col_ex_1, col_ex_2 = st.columns(2)
                
                with col_ex_1:
                    st.markdown("**❌ Avant (incorrect)**")
                    st.code(matched["exemple_avant"], language=result["file_type"])
                
                with col_ex_2:
                    st.markdown("**✅ Après (correct)**")
                    st.code(matched["exemple_après"], language=result["file_type"])
        
        # ==============================
        # BOUTON AUTO-CORRIGER EN BAS
        # ==============================
        if matched and can_auto_correct(matched):
            st.markdown("---")
            col_bottom_btn = st.columns([1, 2, 1])[1]
            
            with col_bottom_btn:
                if st.button("🔧 Auto-corriger maintenant", use_container_width=True, type="primary", key="btn_correct_bottom"):
                    with st.spinner("Correction en cours..."):
                        correction = auto_correct(
                            st.session_state.content, 
                            st.session_state.filetype
                        )
                        
                        if correction["has_changes"]:
                            st.session_state.corrected_content = correction["corrected"]
                            st.session_state.show_comparison = True
                            st.session_state.just_corrected = True  # FIX 3 : Flag pour alerte
                            st.rerun()
                        else:
                            st.info("ℹ️ Aucune correction automatique possible")


# ==============================
# FOOTER
# ==============================
st.markdown(
    """
    <div class="footer">
        <p><strong>Codex Validateur XML/JSON</strong></p>
        <p>Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
        <p><a href="https://discord.gg/CQR6KTJ63C" target="_blank">💬 Rejoindre le Discord</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
