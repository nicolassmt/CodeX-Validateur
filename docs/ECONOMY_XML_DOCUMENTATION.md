# 📄 ECONOMY.XML (CFGECONOMYCORE.XML) - Documentation Complète

## 📋 Vue d'ensemble

### Informations générales
- **Nom du fichier** : `economy.xml` (aussi appelé `cfgeconomycore.xml`)
- **Rôle** : Configuration du système économique global du serveur (ce qui persiste, ce qui respawn)
- **Emplacement** : `mpmissions/[nom_mission]/db/economy.xml`
- **Version DayZ** : 1.28
- **Priorité** : ⭐⭐⭐ CRITIQUE (détermine le comportement de TOUT le serveur)
- **Fréquence de modification** : FAIBLE (configuration une fois pour toutes)
- **Taille** : **10 lignes** (mais impact ÉNORME !)

### Impact sur le serveur
- ✅ Contrôle si les items PERSISTENT après restart
- ✅ Détermine si les animaux/zombies/véhicules RESPAWNENT
- ✅ Gère la SAUVEGARDE des objets dans la base de données
- ✅ Active/désactive des systèmes entiers (randoms, custom)
- ✅ **C'EST LE CERVEAU ÉCONOMIQUE DU SERVEUR**

### Redémarrage requis
- ✅ Modifications prises en compte au **prochain restart** du serveur
- ⚠️ **ATTENTION** : Mal configurer ce fichier peut CASSER votre serveur !

---

## 🏗️ Structure XML

### Structure complète
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

### Vue simplifiée
```xml
<economy>
    <!-- Chaque ligne contrôle un système -->
    <SYSTEME init="?" load="?" respawn="?" save="?"/>
</economy>
```

---

## 📊 Les 8 systèmes économiques

### 🎯 Vue d'ensemble

| Système | Description | Vanilla Config |
|---------|-------------|----------------|
| `dynamic` | Items de loot dynamique | `1 1 1 1` |
| `animals` | Animaux sauvages | `1 0 1 0` |
| `zombies` | Zombies infectés | `1 0 1 0` |
| `vehicles` | Véhicules | `1 1 1 1` |
| `randoms` | Spawns aléatoires | `0 0 1 0` |
| `custom` | Système custom/mods | `0 0 0 0` |
| `building` | Constructions joueurs | `1 1 0 1` |
| `player` | Joueurs | `1 1 1 1` |

---

## 🔧 Les 4 attributs (FLAGS)

Chaque système a 4 attributs (flags) qui contrôlent son comportement :

### `init` - Initialisation
- **Valeurs** : `0` ou `1`
- **Description** : Active (1) ou désactive (0) le système à l'INIT du serveur (premier démarrage)
- **Quand** : Au PREMIER démarrage du serveur (base de données vide)

**Comportement :**
- `init="1"` → Le système démarre et spawn ses entités initiales
- `init="0"` → Le système ne démarre PAS au premier boot

**Exemple :**
```xml
<!-- Au premier démarrage, des animaux vont spawner -->
<animals init="1" ... />

<!-- Au premier démarrage, pas de randoms -->
<randoms init="0" ... />
```

---

### `load` - Chargement
- **Valeurs** : `0` ou `1`
- **Description** : Charge (1) ou non (0) les données SAUVEGARDÉES depuis la base de données
- **Quand** : À chaque RESTART du serveur (après le premier)

**Comportement :**
- `load="1"` → Restaure les entités sauvegardées (véhicules, bases, items)
- `load="0"` → Ne restaure PAS les entités (respawn à zéro)

**Cas d'usage :**
```xml
<!-- Les véhicules persistent entre restarts -->
<vehicles init="1" load="1" ... />

<!-- Les animaux NE persistent PAS (respawn frais) -->
<animals init="1" load="0" ... />
```

**⚠️ ATTENTION :**
- `load="0"` = **PERTE TOTALE** des entités de ce système à chaque restart !
- Les joueurs peuvent perdre leurs bases si `building load="0"` !

---

### `respawn` - Respawn
- **Valeurs** : `0` ou `1`
- **Description** : Active (1) ou désactive (0) le RESPAWN automatique des entités
- **Quand** : En continu pendant que le serveur tourne

**Comportement :**
- `respawn="1"` → Les entités respawnent selon les règles (types.xml, events.xml)
- `respawn="0"` → Aucun respawn (les entités ne reviennent jamais)

**Exemples :**
```xml
<!-- Les items de loot respawnent -->
<dynamic init="1" load="1" respawn="1" ... />

<!-- Les constructions NE respawnent PAS (logique !) -->
<building init="1" load="1" respawn="0" ... />
```

**Cas extrême :**
```xml
<!-- Serveur "one life" - plus de loot après pillage initial -->
<dynamic init="1" load="1" respawn="0" save="1"/>
```

---

### `save` - Sauvegarde
- **Valeurs** : `0` ou `1`
- **Description** : Sauvegarde (1) ou non (0) les entités dans la base de données
- **Quand** : Périodiquement pendant que le serveur tourne

**Comportement :**
- `save="1"` → Les entités sont sauvegardées en BDD (persistent au restart si load="1")
- `save="0"` → Les entités NE sont PAS sauvegardées (volatiles)

**Logique :**
```xml
<!-- Sauvegarder les véhicules (sinon ils disparaissent) -->
<vehicles ... save="1"/>

<!-- Ne PAS sauvegarder les animaux (ils respawnent) -->
<animals ... save="0"/>
```

**⚠️ Impact performance :**
- `save="1"` = Écritures régulières en BDD (charge serveur)
- `save="0"` = Pas d'écriture (meilleure performance, mais pas de persistence)

---

## 🎯 Documentation des 8 systèmes

### 1️⃣ `<dynamic>` - Items de loot dynamique

**Configuration vanilla :**
```xml
<dynamic init="1" load="1" respawn="1" save="1"/>
```

**Rôle :**
- Gère TOUS les items de `types.xml`
- Armes, vêtements, nourriture, outils, munitions, etc.
- C'est le CŒUR du système de loot

**Explication des flags :**
- `init="1"` → Au démarrage, spawn les items selon types.xml
- `load="1"` → Restaure les items sauvegardés (items dans bases, véhicules)
- `respawn="1"` → Les items respawnent selon nominal/restock
- `save="1"` → Les items sont sauvegardés (persistent entre restarts)

**⚠️ Configuration critique :**
```xml
<!-- ✅ CORRECT - Configuration standard -->
<dynamic init="1" load="1" respawn="1" save="1"/>

<!-- ⚠️ DANGEREUX - Pas de respawn = map vide après pillage -->
<dynamic init="1" load="1" respawn="0" save="1"/>

<!-- ❌ DESTRUCTEUR - Pas de load = perte de TOUT le loot sauvegardé -->
<dynamic init="1" load="0" respawn="1" save="1"/>
```

**Impact joueurs :**
- `respawn="0"` → Plus de loot = serveur mort en 2h
- `load="0"` → Bases vidées à chaque restart = ragequit communauté

---

### 2️⃣ `<animals>` - Animaux sauvages

**Configuration vanilla :**
```xml
<animals init="1" load="0" respawn="1" save="0"/>
```

**Rôle :**
- Gère les animaux de `events.xml` (cerfs, ours, loups, vaches, etc.)
- Position : events avec `position="fixed"`

**Explication des flags :**
- `init="1"` → Spawn des animaux au démarrage
- `load="0"` → **NE restaure PAS** les animaux sauvegardés (respawn frais)
- `respawn="1"` → Les animaux respawnent selon events.xml
- `save="0"` → Les animaux **NE sont PAS sauvegardés** (volatiles)

**Logique :**
- Les animaux sont **volatiles** (ne persistent pas)
- Ils respawnent frais à chaque restart
- **Pas de sauvegarde** = meilleure performance

**Modifications possibles :**
```xml
<!-- Désactiver les animaux complètement -->
<animals init="0" load="0" respawn="0" save="0"/>

<!-- Sauvegarder les animaux (inhabituel) -->
<animals init="1" load="1" respawn="1" save="1"/>
```

---

### 3️⃣ `<zombies>` - Zombies infectés

**Configuration vanilla :**
```xml
<zombies init="1" load="0" respawn="1" save="0"/>
```

**Rôle :**
- Gère les zombies de `zombie_territories.xml` ET `events.xml`
- Zombies statiques ET hordes dynamiques

**Explication des flags :**
- `init="1"` → Spawn des zombies au démarrage
- `load="0"` → **NE restaure PAS** les zombies (respawn frais)
- `respawn="1"` → Les zombies respawnent en continu
- `save="0"` → Les zombies **NE sont PAS sauvegardés**

**Logique :**
- Les zombies sont **volatiles** (comme les animaux)
- Ils respawnent frais à chaque restart
- **Pas de sauvegarde** = évite la surcharge BDD

**Modifications possibles :**
```xml
<!-- Serveur sans zombies (PvP pur) -->
<zombies init="0" load="0" respawn="0" save="0"/>

<!-- Zombies qui persistent (très inhabituel) -->
<zombies init="1" load="1" respawn="1" save="1"/>
```

---

### 4️⃣ `<vehicles>` - Véhicules

**Configuration vanilla :**
```xml
<vehicles init="1" load="1" respawn="1" save="1"/>
```

**Rôle :**
- Gère les véhicules de `events.xml`
- Voitures, camions, bateaux, etc.

**Explication des flags :**
- `init="1"` → Spawn des véhicules au démarrage
- `load="1"` → **Restaure** les véhicules sauvegardés (position, état, inventaire)
- `respawn="1"` → Les véhicules respawnent selon events.xml
- `save="1"` → Les véhicules **SONT sauvegardés** (persistent)

**Logique :**
- Les véhicules **PERSISTENT** entre restarts
- Position, état mécanique, inventaire sauvegardés
- Respawn seulement si détruits/despawnés

**⚠️ Configuration critique :**
```xml
<!-- ✅ CORRECT - Véhicules persistent -->
<vehicles init="1" load="1" respawn="1" save="1"/>

<!-- ❌ PERTE VÉHICULES - Ne persistent pas -->
<vehicles init="1" load="0" respawn="1" save="0"/>
```

**Impact joueurs :**
- `load="0"` + `save="0"` → Tous les véhicules réinitialisés à chaque restart
- Joueurs perdent leurs véhicules réparés = frustration

---

### 5️⃣ `<randoms>` - Spawns aléatoires

**Configuration vanilla :**
```xml
<randoms init="0" load="0" respawn="1" save="0"/>
```

**Rôle :**
- Gère les spawns aléatoires (système peu utilisé en vanilla)
- Peut être utilisé par des mods/configs custom

**Explication des flags :**
- `init="0"` → **DÉSACTIVÉ** au démarrage
- `load="0"` → Ne charge rien
- `respawn="1"` → Respawn activé (si system activé)
- `save="0"` → Pas de sauvegarde

**Logique vanilla :**
- **SYSTÈME DÉSACTIVÉ** par défaut
- Peut être activé pour configs custom

**Activation :**
```xml
<!-- Activer les randoms -->
<randoms init="1" load="0" respawn="1" save="0"/>
```

---

### 6️⃣ `<custom>` - Système custom/mods

**Configuration vanilla :**
```xml
<custom init="0" load="0" respawn="0" save="0"/>
```

**Rôle :**
- Système réservé pour les **MODS** et configs custom
- Non utilisé en vanilla

**Explication des flags :**
- `init="0"` → **COMPLÈTEMENT DÉSACTIVÉ**
- `load="0"` → Ne charge rien
- `respawn="0"` → Pas de respawn
- `save="0"` → Pas de sauvegarde

**Logique :**
- **SYSTÈME DORMANT** en vanilla
- À activer selon besoins mods

**Activation pour mods :**
```xml
<!-- Activer pour un mod -->
<custom init="1" load="1" respawn="1" save="1"/>
```

---

### 7️⃣ `<building>` - Constructions joueurs

**Configuration vanilla :**
```xml
<building init="1" load="1" respawn="0" save="1"/>
```

**Rôle :**
- Gère TOUTES les constructions des joueurs
- Bases, tentes, barils, coffres, murs, tours, etc.

**Explication des flags :**
- `init="1"` → Système actif au démarrage
- `load="1"` → **RESTAURE** toutes les bases sauvegardées
- `respawn="0"` → Les bases **NE respawnent PAS** (logique !)
- `save="1"` → Les bases **SONT sauvegardées**

**Logique :**
- Les bases **PERSISTENT** entre restarts
- **Crucial pour la survie** des joueurs
- `respawn="0"` = les bases ne réapparaissent pas magiquement

**⚠️ Configuration ULTRA-CRITIQUE :**
```xml
<!-- ✅ CORRECT - Bases persistent -->
<building init="1" load="1" respawn="0" save="1"/>

<!-- ❌ CATASTROPHE - Perte de TOUTES les bases -->
<building init="1" load="0" respawn="0" save="0"/>

<!-- ❌ ABSURDE - Bases respawnent (doublon) -->
<building init="1" load="1" respawn="1" save="1"/>
```

**Impact joueurs :**
- `load="0"` → **TOUTES LES BASES SUPPRIMÉES** à chaque restart
- `save="0"` → Bases ne persistent pas
- → **EXODE MASSIF DES JOUEURS** garanti

---

### 8️⃣ `<player>` - Joueurs

**Configuration vanilla :**
```xml
<player init="1" load="1" respawn="1" save="1"/>
```

**Rôle :**
- Gère les **JOUEURS** et leurs données
- Position, inventaire, santé, statuts, etc.

**Explication des flags :**
- `init="1"` → Système joueurs actif
- `load="1"` → **RESTAURE** les données joueurs sauvegardées
- `respawn="1"` → Respawn activé (système de spawn joueur)
- `save="1"` → Les données joueurs **SONT sauvegardées**

**Logique :**
- Les joueurs **PERSISTENT** entre restarts
- Position, inventaire, santé restaurés
- **Essentiel** pour l'expérience joueur

**⚠️ NE JAMAIS MODIFIER (sauf serveurs très spéciaux) :**
```xml
<!-- ✅ TOUJOURS garder cette config -->
<player init="1" load="1" respawn="1" save="1"/>

<!-- ❌ WIPE JOUEURS à chaque restart -->
<player init="1" load="0" respawn="1" save="0"/>
```

**Impact :**
- `load="0"` ou `save="0"` → Les joueurs **PERDENT TOUT** à chaque restart
- → Serveur MORT en 1 jour

---

## 📋 Configurations par type de serveur

### 🎮 Serveur Vanilla Standard
```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```
**Usage :** Configuration par défaut, équilibrée

---

### 🔫 Serveur PvP (sans zombies)
```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="0" load="0" respawn="0" save="0"/>  <!-- DÉSACTIVÉ -->
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```
**Usage :** PvP pur, focus combat joueurs

---

### 🏕️ Serveur Base-Building intensif
```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="1" load="1" respawn="1" save="1"/>  <!-- ACTIVÉ pour mods -->
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```
**Usage :** Avec mods de construction

---

### 🧟 Serveur Hardcore Zombies
```xml
<economy>
    <dynamic init="1" load="1" respawn="0" save="1"/>  <!-- Peu de loot -->
    <animals init="0" load="0" respawn="0" save="0"/>  <!-- Pas d'animaux -->
    <zombies init="1" load="0" respawn="1" save="0"/>  <!-- Zombies actifs -->
    <vehicles init="0" load="0" respawn="0" save="0"/>  <!-- Pas de véhicules -->
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```
**Usage :** Survie extrême

---

### 🔄 Serveur "Fresh Start" (wipe régulier)
```xml
<economy>
    <dynamic init="1" load="0" respawn="1" save="0"/>  <!-- Pas de persistence -->
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="0" respawn="1" save="0"/>  <!-- Véhicules reset -->
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="0" respawn="0" save="0"/>  <!-- Bases reset -->
    <player init="1" load="1" respawn="1" save="1"/>  <!-- Joueurs persistent quand même -->
</economy>
```
**Usage :** Reset journalier/hebdomadaire

---

## ⚠️ Règles de validation

### Règle 1 : Valeurs binaires (0 ou 1)
```xml
<!-- ✅ CORRECT -->
<dynamic init="1" load="1" respawn="1" save="1"/>

<!-- ❌ ERREUR -->
<dynamic init="true" load="yes" respawn="on" save="1"/>
<dynamic init="2" load="1" respawn="1" save="1"/>
```

**Validation :** Tous les attributs doivent être `0` ou `1`

---

### Règle 2 : Cohérence load/save
```xml
<!-- ⚠️ INCOHÉRENT -->
<vehicles init="1" load="1" respawn="1" save="0"/>
<!-- load="1" mais save="0" = rien à charger ! -->

<!-- ✅ COHÉRENT -->
<vehicles init="1" load="1" respawn="1" save="1"/>
<!-- OU -->
<animals init="1" load="0" respawn="1" save="0"/>
```

**Logique :**
- Si `load="1"`, alors généralement `save="1"` (sinon rien à charger)
- Si `save="0"`, alors généralement `load="0"` (pas de données)

**Exception valide :**
```xml
<!-- Valide : charge l'init mais ne sauvegarde pas -->
<system init="1" load="1" respawn="0" save="0"/>
```

---

### Règle 3 : Building respawn
```xml
<!-- ❌ ABSURDE -->
<building init="1" load="1" respawn="1" save="1"/>
<!-- Les bases NE doivent PAS respawner ! -->

<!-- ✅ CORRECT -->
<building init="1" load="1" respawn="0" save="1"/>
```

**Validation :** `building` doit TOUJOURS avoir `respawn="0"`

---

### Règle 4 : Player toujours actif
```xml
<!-- ❌ DANGEREUX -->
<player init="0" load="0" respawn="0" save="0"/>
<!-- Serveur cassé, joueurs ne peuvent pas se connecter ! -->

<!-- ✅ CORRECT -->
<player init="1" load="1" respawn="1" save="1"/>
```

**Validation :** `player` doit TOUJOURS être `1 1 1 1` (sauf cas très spéciaux)

---

## 🎯 Impact des configurations

### Tableau de décision

| Config | Items | Animaux | Zombies | Véhicules | Bases | Joueurs |
|--------|-------|---------|---------|-----------|-------|---------|
| **Vanilla** | Persistent | Respawn | Respawn | Persistent | Persistent | Persistent |
| **PvP Pur** | Persistent | Respawn | OFF | Persistent | Persistent | Persistent |
| **Hardcore** | Fresh | OFF | Respawn | OFF | Persistent | Persistent |
| **Wipe Daily** | Fresh | Respawn | Respawn | Fresh | Fresh | Persistent |

---

## 💡 Cas d'usage et stratégies

### Stratégie 1 : Performance optimale
```xml
<!-- Désactiver ce qui n'est pas utilisé -->
<randoms init="0" load="0" respawn="0" save="0"/>
<custom init="0" load="0" respawn="0" save="0"/>

<!-- Animaux/zombies sans sauvegarde (moins de charge BDD) -->
<animals init="1" load="0" respawn="1" save="0"/>
<zombies init="1" load="0" respawn="1" save="0"/>
```

**Résultat :** Serveur plus léger, moins d'écritures BDD

---

### Stratégie 2 : Wipe du loot sans affecter les joueurs
```xml
<!-- Items reset -->
<dynamic init="1" load="0" respawn="1" save="0"/>

<!-- Véhicules reset -->
<vehicles init="1" load="0" respawn="1" save="0"/>

<!-- Bases et joueurs PERSISTENT -->
<building init="1" load="1" respawn="0" save="1"/>
<player init="1" load="1" respawn="1" save="1"/>
```

**Résultat :** Fresh loot, mais les joueurs gardent leurs bases et persos

---

### Stratégie 3 : Serveur événementiel (reset complet)
```xml
<!-- TOUT reset sauf les joueurs -->
<dynamic init="1" load="0" respawn="1" save="0"/>
<animals init="1" load="0" respawn="1" save="0"/>
<zombies init="1" load="0" respawn="1" save="0"/>
<vehicles init="1" load="0" respawn="1" save="0"/>
<building init="1" load="0" respawn="0" save="0"/>  <!-- Bases reset -->

<!-- Joueurs persistent (gardent leur progression) -->
<player init="1" load="1" respawn="1" save="1"/>
```

**Usage :** Événements, tournois, compétitions

---

## 🔍 Erreurs courantes et solutions

### Erreur 1 : Bases disparaissent à chaque restart
**Symptôme :** Les joueurs reconstruisent tout après chaque restart

**Cause :**
```xml
<building init="1" load="0" respawn="0" save="0"/>
```

**Solution :**
```xml
<building init="1" load="1" respawn="0" save="1"/>
```

---

### Erreur 2 : Véhicules réinitialisés
**Symptôme :** Véhicules réparés reviennent à l'état initial

**Cause :**
```xml
<vehicles init="1" load="0" respawn="1" save="0"/>
```

**Solution :**
```xml
<vehicles init="1" load="1" respawn="1" save="1"/>
```

---

### Erreur 3 : Trop de charge serveur/BDD
**Symptôme :** Serveur lag, BDD surchargée

**Cause :** Trop de sauvegardes actives

**Solution :**
```xml
<!-- Ne pas sauvegarder ce qui n'a pas besoin de persister -->
<animals init="1" load="0" respawn="1" save="0"/>
<zombies init="1" load="0" respawn="1" save="0"/>
```

---

### Erreur 4 : Joueurs perdent tout
**Symptôme :** Joueurs se reconnectent nus

**Cause :**
```xml
<player init="1" load="0" respawn="1" save="0"/>
```

**Solution :**
```xml
<!-- NE JAMAIS TOUCHER -->
<player init="1" load="1" respawn="1" save="1"/>
```

---

## ✅ Checklist de validation Codex

### Syntaxe XML
- [ ] Fichier commence par `<?xml version="1.0"?>`
- [ ] Balise racine `<economy>` présente
- [ ] 8 systèmes présents (dynamic, animals, zombies, vehicles, randoms, custom, building, player)
- [ ] Toutes les balises auto-fermantes (`/>`)

### Valeurs
- [ ] Tous les attributs sont 0 ou 1
- [ ] Pas de valeurs textuelles (true/false/yes/no)

### Cohérence
- [ ] `building` a `respawn="0"` (bases ne respawnent pas)
- [ ] `player` a tous les flags à 1 (sauf config spéciale)
- [ ] Si `load="1"`, généralement `save="1"`

### Sécurité
- [ ] `building` sauvegarde activée (sinon perte bases)
- [ ] `player` sauvegarde activée (sinon perte joueurs)
- [ ] `vehicles` sauvegarde activée si véhicules importants

---

## 📊 Résumé visuel

```
INIT    LOAD    RESPAWN    SAVE
 ↓       ↓        ↓         ↓
Au     Charge   Respawn   Sauvegarde
1er    données  actif     en BDD
boot   BDD      pendant   pendant
                jeu       jeu

Exemples :
┌─────────┬──────┬──────┬─────────┬──────┬─────────────┐
│ Système │ init │ load │ respawn │ save │ Résultat    │
├─────────┼──────┼──────┼─────────┼──────┼─────────────┤
│ dynamic │  1   │  1   │    1    │  1   │ Persistent  │
│ animals │  1   │  0   │    1    │  0   │ Volatiles   │
│ zombies │  1   │  0   │    1    │  0   │ Volatiles   │
│ vehicle │  1   │  1   │    1    │  1   │ Persistent  │
│ randoms │  0   │  0   │    1    │  0   │ Désactivé   │
│ custom  │  0   │  0   │    0    │  0   │ Désactivé   │
│ building│  1   │  1   │    0    │  1   │ Persistent  │
│ player  │  1   │  1   │    1    │  1   │ Persistent  │
└─────────┴──────┴──────┴─────────┴──────┴─────────────┘
```

---

## 🎓 Comprendre les interactions

### Scénario : Restart du serveur

**État initial :** Serveur tourne avec joueurs actifs

**Au restart :**

1. **Arrêt serveur**
   - Systèmes avec `save="1"` → Données écrites en BDD
   - Systèmes avec `save="0"` → Données perdues

2. **Démarrage serveur**
   - Systèmes avec `load="1"` → Restaure depuis BDD
   - Systèmes avec `load="0"` → Repart à zéro

3. **Pendant le jeu**
   - Systèmes avec `respawn="1"` → Respawn actif
   - Systèmes avec `respawn="0"` → Pas de respawn

**Exemple concret :**

```xml
<animals init="1" load="0" respawn="1" save="0"/>
```

- **Avant restart** : 50 cerfs sur la map
- **Au restart** : `save="0"` → Cerfs disparus
- **Après restart** : `load="0"` → Pas de restore, respawn frais
- **Résultat** : Nouveaux cerfs spawnent selon events.xml

---

**📝 Document créé par CodeX - L'outil pour la communauté DayZ FR**
**Version : 1.0 - Basé sur DayZ 1.28**
**Dernière mise à jour : 2025**
