# 📄 EVENTS.XML - Documentation Complète

## 📋 Vue d'ensemble

### Informations générales
- **Nom du fichier** : `events.xml`
- **Rôle** : Gestion des événements dynamiques (animaux, zombies infectés, crashs, véhicules, objets statiques)
- **Emplacement** : `mpmissions/[nom_mission]/db/events.xml`
- **Version DayZ** : 1.28
- **Priorité** : ⭐⭐⭐ CRITIQUE
- **Fréquence de modification** : ÉLEVÉE
- **Nombre d'events** : 58 events dans la version vanilla
- **Fichier lié** : `cfgeventspawns.xml` (positions géographiques des events)

### Impact sur le serveur
- ✅ Contrôle les spawns d'ANIMAUX (vaches, cerfs, ours, loups, etc.)
- ✅ Gère les hordes de ZOMBIES INFECTÉS dynamiques (militaires, ville, etc.)
- ✅ Définit les EVENTS STATIQUES (crash d'hélico, convoi militaire, voiture de police)
- ✅ Configure les VÉHICULES persistants
- ✅ Gère les spawns de RESSOURCES naturelles (fruits, champignons, pierres)

### Redémarrage requis
- ❌ Modifications prises en compte au **prochain restart** du serveur
- ⚠️ Pas de hot-reload possible

---

## 🏗️ Structure XML

### Structure racine
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<events>
    <event name="NomEvent">
        <!-- Configuration de l'event -->
    </event>
    <event name="AutreEvent">
        <!-- Configuration de l'event -->
    </event>
    <!-- ... 58 events au total ... -->
</events>
```

### Structure d'un élément `<event>`

```xml
<event name="StaticHeliCrash">
    <!-- SPAWN CONTROL -->
    <nominal>3</nominal>              <!-- Nombre simultané cible -->
    <min>2</min>                      <!-- Nombre minimum garanti -->
    <max>4</max>                      <!-- Nombre maximum autorisé -->
    <lifetime>7200</lifetime>         <!-- Durée de vie en minutes -->
    <restock>7200</restock>           <!-- Temps avant respawn -->
    
    <!-- RADIUS CONTROL -->
    <saferadius>500</saferadius>      <!-- Rayon de sécurité (distance joueur) -->
    <distanceradius>500</distanceradius>  <!-- Rayon de distance entre events -->
    <cleanupradius>100</cleanupradius>    <!-- Rayon de cleanup -->
    
    <!-- FLAGS -->
    <flags 
        deletable="0"                 <!-- Peut être supprimé -->
        init_random="0"               <!-- Init aléatoire au démarrage -->
        remove_damaged="1"            <!-- Retirer si endommagé -->
    />
    
    <!-- POSITION & LIMIT -->
    <position>fixed</position>        <!-- Type de positionnement -->
    <limit>mixed</limit>              <!-- Type de limite de spawn -->
    <active>1</active>                <!-- Event activé (1) ou non (0) -->
    
    <!-- CHILDREN (objets spawnés) -->
    <children>
        <child 
            lootmax="10" 
            lootmin="5" 
            max="1" 
            min="1" 
            type="UH1H_Wreck"
        />
    </children>
</event>
```

---

## 📊 Balises détaillées

### 🔴 BALISES OBLIGATOIRES

#### `name` (attribut de `<event>`)
- **Type** : String (texte)
- **Obligatoire** : ✅ OUI
- **Description** : Nom unique de l'event
- **Format** : Sensible à la casse, sans espaces
- **Conventions de nommage** :
  - `Animal*` : Animaux (AnimalBear, AnimalWolf)
  - `Infected*` : Zombies infectés (InfectedArmy, InfectedCity)
  - `Static*` : Events statiques (StaticHeliCrash, StaticMilitaryConvoy)
  - `Vehicle*` : Véhicules (VehicleSedan02, VehicleTruck01)
  - `Trajectory*` : Ressources naturelles (TrajectoryApple, TrajectoryStones)

**Exemples :**
```xml
<event name="StaticHeliCrash">
<event name="AnimalBear">
<event name="InfectedArmy">
<event name="VehicleSedan02">
```

---

#### `<nominal>`
- **Type** : Integer (nombre entier)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 250
- **Description** : Nombre cible d'instances simultanées de cet event sur la map
- **Règle métier** : `min` ≤ `nominal` ≤ `max`

**Comportement :**
- Si nominal = 0 → Event désactivé (mais peut être réactivé avec active=1)
- Si nominal = 1 → 1 seul event actif à la fois
- Si nominal = 50 → Jusqu'à 50 instances simultanées

**Exemples par type :**
```xml
<!-- Event unique (crash hélico) -->
<nominal>3</nominal>

<!-- Animaux moyens (cerfs) -->
<nominal>9</nominal>

<!-- Hordes de zombies -->
<nominal>50</nominal>

<!-- Véhicules -->
<nominal>8</nominal>

<!-- Ressources naturelles abondantes -->
<nominal>140</nominal>
```

---

#### `<min>`
- **Type** : Integer
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 250
- **Description** : Nombre MINIMUM garanti d'instances actives
- **Règle métier** : `min` ≤ `nominal` ≤ `max`

**Comportement :**
- Si le nombre descend sous `min`, le système force un respawn
- `min = 0` → Pas de garantie minimale

**Stratégies :**
```xml
<!-- Event garanti (toujours présent) -->
<nominal>3</nominal>
<min>2</min>

<!-- Event optionnel (peut être absent) -->
<nominal>5</nominal>
<min>0</min>

<!-- Event constant (toujours au max) -->
<nominal>50</nominal>
<min>50</min>
```

---

#### `<max>`
- **Type** : Integer
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 250
- **Description** : Nombre MAXIMUM autorisé d'instances actives
- **Règle métier** : `min` ≤ `nominal` ≤ `max`

**Comportement :**
- Le système ne dépassera JAMAIS cette limite
- Utile pour éviter la saturation

**Exemples :**
```xml
<!-- Contrôle strict (peu de variation) -->
<nominal>3</nominal>
<min>2</min>
<max>4</max>

<!-- Large variation possible -->
<nominal>50</nominal>
<min>25</min>
<max>250</max>
```

---

#### `<lifetime>`
- **Type** : Integer (minutes pour animaux/events, secondes pour autres)
- **Obligatoire** : ✅ OUI
- **Plage** : 1 à 7200 (dépend du type)
- **Description** : Durée de vie de l'event avant despawn automatique

**⚠️ ATTENTION - Unité variable :**
- **Animaux** : En MINUTES (180 = 3 heures)
- **Zombies infectés** : En MINUTES (3 = 3 minutes)
- **Events statiques** : En MINUTES (7200 = 5 jours)
- **Véhicules** : En MINUTES (300 = 5 heures)
- **Ressources naturelles** : En MINUTES (180 = 3 heures)

**Valeurs typiques :**
```xml
<!-- Zombies (courte durée) -->
<lifetime>3</lifetime>  <!-- 3 minutes -->

<!-- Animaux (durée moyenne) -->
<lifetime>180</lifetime>  <!-- 3 heures -->

<!-- Véhicules (durée longue) -->
<lifetime>300</lifetime>  <!-- 5 heures -->

<!-- Events statiques (très longue) -->
<lifetime>7200</lifetime>  <!-- 5 jours -->
```

---

#### `<restock>`
- **Type** : Integer (minutes ou secondes selon contexte)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 7200
- **Description** : Temps minimum avant qu'un nouvel event puisse spawn
- **Valeur spéciale** : 0 = respawn immédiat si sous le nominal

**Stratégies :**
```xml
<!-- Respawn immédiat (animaux, zombies) -->
<restock>0</restock>

<!-- Respawn contrôlé (events rares) -->
<restock>7200</restock>  <!-- 5 jours -->
```

---

#### `<saferadius>`
- **Type** : Integer (mètres)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 1000
- **Description** : Rayon de sécurité autour des joueurs (event ne spawn pas si joueur trop proche)

**Comportement :**
- 0 = Pas de distance minimale (peut spawn près des joueurs)
- Valeur élevée = Event spawn loin des joueurs

**Exemples :**
```xml
<!-- Peut spawn près des joueurs -->
<saferadius>0</saferadius>

<!-- Spawn à distance moyenne -->
<saferadius>200</saferadius>

<!-- Spawn très loin des joueurs -->
<saferadius>500</saferadius>
```

---

#### `<distanceradius>`
- **Type** : Integer (mètres)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 1000
- **Description** : Distance minimale entre deux instances du même event

**Comportement :**
- 0 = Pas de distance minimale entre events
- Valeur élevée = Events bien espacés sur la map

**Exemples :**
```xml
<!-- Events peuvent être proches -->
<distanceradius>20</distanceradius>

<!-- Events moyennement espacés -->
<distanceradius>100</distanceradius>

<!-- Events très espacés -->
<distanceradius>500</distanceradius>
```

---

#### `<cleanupradius>`
- **Type** : Integer (mètres)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 200
- **Description** : Rayon dans lequel l'event peut être nettoyé (despawn forcé)

**Comportement :**
- Plus petit = Cleanup agressif
- Plus grand = Event persiste plus longtemps

**Exemples :**
```xml
<!-- Cleanup rapide -->
<cleanupradius>25</cleanupradius>

<!-- Cleanup moyen -->
<cleanupradius>100</cleanupradius>

<!-- Cleanup lent -->
<cleanupradius>200</cleanupradius>
```

---

#### `<flags>` (attributs multiples)
- **Type** : Boolean (0 ou 1)
- **Obligatoire** : ✅ OUI
- **Description** : Drapeaux de comportement de l'event

**Attributs disponibles :**

**`deletable`** (0 ou 1)
- 0 = Event ne peut PAS être supprimé par le système
- 1 = Event peut être supprimé si conditions réunies
- **Recommandé** : 0 (pour événements importants)

**`init_random`** (0 ou 1)
- 0 = Events spawnent selon les règles normales au démarrage
- 1 = Events ont une position aléatoire à l'init
- **Recommandé** : 0 (comportement standard)

**`remove_damaged`** (0 ou 1)
- 0 = Event persiste même si endommagé
- 1 = Event est retiré s'il est trop endommagé
- **Utilisation** : 1 pour animaux/véhicules, 0 pour objets statiques

**Configuration typique :**
```xml
<!-- Animaux (retirés si tués) -->
<flags deletable="0" init_random="0" remove_damaged="1"/>

<!-- Events statiques (persistent) -->
<flags deletable="0" init_random="0" remove_damaged="0"/>

<!-- Zombies dynamiques (retirés si tués) -->
<flags deletable="0" init_random="0" remove_damaged="1"/>
```

---

#### `<position>`
- **Type** : Enum (liste fixe)
- **Obligatoire** : ✅ OUI
- **Quantité** : 1 seule valeur
- **Description** : Mode de positionnement de l'event

**Valeurs autorisées :**

**`fixed`** - Position fixe
- Event spawn à des positions prédéfinies dans `cfgeventspawns.xml`
- **Utilisation** : Crashs d'hélico, convois, véhicules, animaux
- **Exemples** : StaticHeliCrash, AnimalBear, VehicleSedan02

**`player`** - Position dynamique relative au joueur
- Event spawn autour du joueur (dans les radius définis)
- **Utilisation** : Zombies dynamiques, ressources naturelles
- **Exemples** : InfectedArmy, TrajectoryApple

**`uniform`** - Position uniforme sur toute la map
- Event peut spawn n'importe où (rare)
- **Utilisation** : Peu utilisé en vanilla

**Exemples :**
```xml
<!-- Event à position fixe (crash hélico) -->
<position>fixed</position>

<!-- Event dynamique autour du joueur (zombies) -->
<position>player</position>
```

---

#### `<limit>`
- **Type** : Enum (liste fixe)
- **Obligatoire** : ✅ OUI
- **Quantité** : 1 seule valeur
- **Description** : Mode de limitation du spawn des children

**Valeurs autorisées :**

**`mixed`** - Mélange aléatoire
- Plusieurs types de children peuvent spawner ensemble
- Quantités respectent les min/max de chaque child
- **Utilisation** : Véhicules (variantes couleurs), ressources multiples
- **Exemple** : VehicleSedan02 (noir, gris, rouge au hasard)

**`parent`** - Limite au niveau parent
- La limite s'applique à l'event parent, pas aux children
- **Utilisation** : Events avec un seul type de child

**`child`** - Limite au niveau child
- Chaque child a sa propre limite individuelle
- **Utilisation** : Animaux (variantes de la même espèce)
- **Exemple** : AnimalCow (vaches brunes, tachetées, blanches)

**`custom`** - Limite personnalisée
- Comportement spécial défini par le jeu
- **Utilisation** : Zombies infectés, certains animaux

**Exemples :**
```xml
<!-- Véhicules (variantes couleurs mélangées) -->
<limit>mixed</limit>

<!-- Animaux (plusieurs variantes possibles) -->
<limit>child</limit>

<!-- Zombies (hordes dynamiques) -->
<limit>custom</limit>
```

---

#### `<active>`
- **Type** : Boolean (0 ou 1)
- **Obligatoire** : ✅ OUI
- **Description** : Active ou désactive l'event

**Valeurs :**
- **1** = Event ACTIVÉ (spawn normalement)
- **0** = Event DÉSACTIVÉ (ne spawn pas)

**Usage :**
```xml
<!-- Event actif -->
<active>1</active>

<!-- Event désactivé (saisonnier par exemple) -->
<active>0</active>
```

**⚠️ Différence avec nominal=0 :**
- `nominal=0` + `active=1` → Event peut spawner mais nominal cible = 0
- `nominal>0` + `active=0` → Event complètement désactivé

---

#### `<children>` (conteneur)
- **Type** : Conteneur de `<child>`
- **Obligatoire** : ✅ OUI
- **Quantité** : 1 à plusieurs children
- **Description** : Objets/entités qui spawnent avec cet event

**Structure d'un `<child>` :**
```xml
<child 
    lootmax="10"      <!-- Loot maximum dans l'objet (0 = pas de loot) -->
    lootmin="5"       <!-- Loot minimum dans l'objet -->
    max="1"           <!-- Nombre maximum de cet objet -->
    min="1"           <!-- Nombre minimum de cet objet -->
    type="UH1H_Wreck" <!-- Classname de l'objet -->
/>
```

**Attributs du `<child>` :**

**`type`** (obligatoire)
- **Type** : String
- **Description** : Classname de l'objet/entité à spawner
- **Exemples** : 
  - Animaux : `Animal_UrsusArctos` (ours)
  - Zombies : `ZmbM_SoldierNormal` (zombie militaire)
  - Véhicules : `CivilianSedan` (berline)
  - Objets : `UH1H_Wreck` (épave hélico)

**`min`** (obligatoire)
- **Type** : Integer
- **Plage** : 0 à 100
- **Description** : Nombre minimum de cet objet à spawner
- **Cas spéciaux** :
  - min=0 : Objet optionnel
  - min=100 : Objet spawn toujours (zombies, animaux rares)

**`max`** (obligatoire)
- **Type** : Integer
- **Plage** : 0 à 100
- **Description** : Nombre maximum de cet objet à spawner
- **Règle** : max ≥ min

**`lootmin`** (obligatoire)
- **Type** : Integer
- **Plage** : 0 à 10
- **Description** : Quantité minimale de loot dans l'objet (si applicable)
- **0** = Pas de loot

**`lootmax`** (obligatoire)
- **Type** : Integer
- **Plage** : 0 à 10
- **Description** : Quantité maximale de loot dans l'objet
- **Règle** : lootmax ≥ lootmin

**Exemples de children :**

```xml
<!-- Crash d'hélico avec loot -->
<children>
    <child lootmax="10" lootmin="5" max="1" min="1" type="UH1H_Wreck"/>
</children>

<!-- Horde de zombies (plusieurs types) -->
<children>
    <child lootmax="5" lootmin="0" max="0" min="30" type="ZmbM_PatrolNormal_Autumn"/>
    <child lootmax="5" lootmin="0" max="0" min="10" type="ZmbM_PatrolNormal_Flat"/>
    <child lootmax="5" lootmin="0" max="0" min="20" type="ZmbM_SoldierNormal"/>
</children>

<!-- Animaux (variantes) -->
<children>
    <child lootmax="0" lootmin="0" max="1" min="0" type="Animal_BosTaurusF_Brown"/>
    <child lootmax="0" lootmin="0" max="1" min="0" type="Animal_BosTaurusF_Spotted"/>
    <child lootmax="0" lootmin="0" max="1" min="0" type="Animal_BosTaurusF_White"/>
</children>

<!-- Véhicules (variantes couleurs) -->
<children>
    <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
    <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
    <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
</children>

<!-- Ressources naturelles (sans loot) -->
<children>
    <child lootmax="0" lootmin="0" max="0" min="0" type="Apple"/>
</children>
```

---

## 📋 Liste complète des events vanilla

### 🦊 Animaux ambiants (Ambient)
```
AmbientFox       - Renards
AmbientHare      - Lièvres
AmbientHen       - Poules
```

### 🐻 Animaux sauvages (Animal)
```
AnimalBear       - Ours
AnimalCow        - Vaches
AnimalDeer       - Cerfs
AnimalGoat       - Chèvres
AnimalPig        - Cochons
AnimalRoeDeer    - Chevreuils
AnimalSheep      - Moutons
AnimalWildBoar   - Sangliers
AnimalWolf       - Loups
```

### 🧟 Zombies infectés dynamiques (Infected)
```
InfectedArmy         - Zombies militaires
InfectedArmyHard     - Zombies militaires difficiles
InfectedCity         - Zombies de ville
InfectedCityTier1    - Zombies de ville (Tier 1)
InfectedFirefighter  - Zombies pompiers
InfectedIndustrial   - Zombies industriels
InfectedMedic        - Zombies médicaux
InfectedNBC          - Zombies NBC (combinaison)
InfectedNBCYellow    - Zombies NBC jaune
InfectedPolice       - Zombies policiers
InfectedPoliceHard   - Zombies policiers difficiles
InfectedPrisoner     - Zombies prisonniers
InfectedReligious    - Zombies religieux
InfectedSanta        - Zombies Père Noël (événement)
InfectedSolitude     - Zombies isolés
InfectedVillage      - Zombies de village
InfectedVillageTier1 - Zombies de village (Tier 1)
```

### 🚁 Events statiques (Static)
```
StaticAirplaneCrate      - Caisse d'avion
StaticBonfire            - Feu de camp
StaticChristmasTree      - Sapin de Noël
StaticContaminatedArea   - Zone contaminée
StaticFridgeTest         - Test frigo
StaticHeliCrash          - Crash d'hélicoptère
StaticMilitaryConvoy     - Convoi militaire
StaticPoliceCar          - Voiture de police
StaticPoliceSituation    - Situation policière
StaticSantaCrash         - Crash du Père Noël
StaticTrain              - Train
```

### 🍎 Ressources naturelles (Trajectory)
```
TrajectoryApple      - Pommes
TrajectoryCanina     - Baies de canina
TrajectoryConiferous - Champignons (conifères)
TrajectoryDeciduous  - Champignons (feuillus)
TrajectoryHumus      - Champignons (humus)
TrajectoryPear       - Poires
TrajectoryPlum       - Prunes
TrajectorySambucus   - Baies de sureau
TrajectoryStones     - Pierres
```

### 🚗 Véhicules (Vehicle)
```
VehicleBoat              - Bateaux
VehicleCivilianSedan     - Berline civile
VehicleHatchback02       - Berline compacte
VehicleOffroad02         - 4x4
VehicleOffroadHatchback  - Berline tout-terrain
VehicleSedan02           - Berline
VehicleTruck01           - Camion
```

### 📦 Autres
```
ItemPlanks - Planches
Loot       - Loot générique
```

---

## ⚠️ Règles métier et validations

### Règle 1 : `min` ≤ `nominal` ≤ `max`
```xml
<!-- ✅ CORRECT -->
<nominal>50</nominal>
<min>25</min>
<max>250</max>

<!-- ❌ ERREUR -->
<nominal>10</nominal>
<min>20</min>    <!-- min > nominal -->
<max>5</max>     <!-- max < nominal -->
```

---

### Règle 2 : `lifetime` > 0
```xml
<!-- ✅ CORRECT -->
<lifetime>180</lifetime>

<!-- ❌ ERREUR -->
<lifetime>0</lifetime>
<lifetime>-10</lifetime>
```

---

### Règle 3 : `active` doit être 0 ou 1
```xml
<!-- ✅ CORRECT -->
<active>1</active>
<active>0</active>

<!-- ❌ ERREUR -->
<active>true</active>
<active>2</active>
```

---

### Règle 4 : Flags doivent être 0 ou 1
```xml
<!-- ✅ CORRECT -->
<flags deletable="0" init_random="0" remove_damaged="1"/>

<!-- ❌ ERREUR -->
<flags deletable="yes" init_random="2"/>
```

---

### Règle 5 : `position` valide
```xml
<!-- ✅ CORRECT -->
<position>fixed</position>
<position>player</position>
<position>uniform</position>

<!-- ❌ ERREUR -->
<position>random</position>
<position>custom</position>
```

---

### Règle 6 : `limit` valide
```xml
<!-- ✅ CORRECT -->
<limit>mixed</limit>
<limit>parent</limit>
<limit>child</limit>
<limit>custom</limit>

<!-- ❌ ERREUR -->
<limit>all</limit>
<limit>none</limit>
```

---

### Règle 7 : Children valides
```xml
<!-- ✅ CORRECT -->
<child lootmax="10" lootmin="5" max="3" min="1" type="Item"/>

<!-- ❌ ERREUR -->
<child lootmax="5" lootmin="10" max="1" min="3" type="Item"/>
<!-- lootmin > lootmax ET min > max -->
```

---

## 💡 Exemples complets commentés

### Exemple 1 : Crash d'hélicoptère
```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>              <!-- 3 crashs simultanés max -->
    <min>2</min>                      <!-- Au moins 2 garantis -->
    <max>4</max>                      <!-- Max 4 en même temps -->
    <lifetime>7200</lifetime>         <!-- 5 jours de durée de vie -->
    <restock>7200</restock>           <!-- 5 jours avant respawn -->
    <saferadius>500</saferadius>      <!-- Spawn loin des joueurs -->
    <distanceradius>500</distanceradius>  <!-- Crashs bien espacés -->
    <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="0"/>
    <position>fixed</position>        <!-- Positions fixes sur map -->
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child 
            lootmax="10"              <!-- 5 à 10 items de loot -->
            lootmin="5" 
            max="1"                   <!-- 1 épave -->
            min="1" 
            type="UH1H_Wreck"         <!-- Hélico UH-1H -->
        />
    </children>
</event>
```

---

### Exemple 2 : Horde de zombies militaires
```xml
<event name="InfectedArmy">
    <nominal>50</nominal>             <!-- 50 hordes actives -->
    <min>25</min>                     <!-- Au moins 25 -->
    <max>250</max>                    <!-- Max 250 -->
    <lifetime>3</lifetime>            <!-- 3 minutes de vie -->
    <restock>0</restock>              <!-- Respawn immédiat -->
    <saferadius>100</saferadius>      <!-- Spawn à 100m des joueurs -->
    <distanceradius>50</distanceradius>
    <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>player</position>       <!-- Spawn autour des joueurs -->
    <limit>custom</limit>
    <active>1</active>
    <children>
        <!-- Plusieurs types de zombies militaires -->
        <child lootmax="5" lootmin="0" max="0" min="30" type="ZmbM_PatrolNormal_Autumn"/>
        <child lootmax="5" lootmin="0" max="0" min="10" type="ZmbM_PatrolNormal_Flat"/>
        <child lootmax="5" lootmin="0" max="0" min="20" type="ZmbM_SoldierNormal"/>
    </children>
</event>
```

---

### Exemple 3 : Animaux (ours)
```xml
<event name="AnimalBear">
    <nominal>0</nominal>              <!-- Désactivé par défaut -->
    <min>2</min>
    <max>2</max>
    <lifetime>180</lifetime>          <!-- 3 heures -->
    <restock>0</restock>
    <saferadius>200</saferadius>
    <distanceradius>0</distanceradius>
    <cleanupradius>0</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>custom</limit>
    <active>1</active>
    <children>
        <child 
            lootmax="0"               <!-- Pas de loot (animal vivant) -->
            lootmin="0" 
            max="1" 
            min="1" 
            type="Animal_UrsusArctos" <!-- Ours brun -->
        />
    </children>
</event>
```

---

### Exemple 4 : Véhicule (berline)
```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>          <!-- 5 heures -->
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>              <!-- Variantes aléatoires -->
    <active>1</active>
    <children>
        <!-- 3 variantes de couleur -->
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

---

## 🎯 Cas d'usage et stratégies

### Stratégie 1 : Augmenter les crashs d'hélico
```xml
<!-- AVANT (vanilla) -->
<nominal>3</nominal>
<min>2</min>
<max>4</max>

<!-- APRÈS (serveur avec plus de loot) -->
<nominal>5</nominal>
<min>4</min>
<max>6</max>
```

---

### Stratégie 2 : Désactiver un event
```xml
<!-- Méthode 1 : Via active -->
<active>0</active>

<!-- Méthode 2 : Via nominal (moins propre) -->
<nominal>0</nominal>
<min>0</min>
<max>0</max>
```

---

### Stratégie 3 : Augmenter les véhicules
```xml
<!-- AVANT -->
<nominal>8</nominal>

<!-- APRÈS -->
<nominal>15</nominal>
<max>20</max>
```

---

### Stratégie 4 : Réduire les zombies dynamiques
```xml
<!-- AVANT -->
<nominal>50</nominal>
<min>25</min>

<!-- APRÈS (serveur PvP) -->
<nominal>20</nominal>
<min>10</min>
```

---

## 🔍 Erreurs courantes et solutions

### Erreur 1 : Events ne spawnent pas
**Causes :**
- `active=0` → Event désactivé
- `nominal=0` → Aucune instance cible
- Positions manquantes dans `cfgeventspawns.xml`

**Solution :**
```xml
<active>1</active>
<nominal>3</nominal>  <!-- > 0 -->
```

---

### Erreur 2 : Trop d'events simultanés
**Cause :** `max` trop élevé

**Solution :**
```xml
<max>10</max>  <!-- Au lieu de 250 -->
```

---

### Erreur 3 : Events despawnent trop vite
**Cause :** `lifetime` trop court

**Solution :**
```xml
<lifetime>7200</lifetime>  <!-- Au lieu de 180 -->
```

---

## 📊 Valeurs de référence vanilla

### Crashs d'hélico
- nominal: 3
- lifetime: 7200 (5 jours)
- loot: 5-10 items

### Animaux
- Cerfs: nominal=9, lifetime=180 (3h)
- Ours: nominal=0 (désactivé), lifetime=180
- Loups: nominal=8, lifetime=180

### Véhicules
- Berlines: nominal=8, lifetime=300 (5h)
- 4x4: nominal=3, lifetime=300

### Zombies
- Hordes militaires: nominal=50, lifetime=3 (3min)
- Hordes ville: nominal=50, lifetime=3

---

## 🛠️ Fichiers liés

### `cfgeventspawns.xml`
- Définit les positions géographiques des events `position=fixed`
- Chaque event a ses propres zones de spawn
- **FICHIER SPÉCIFIQUE PAR MAP** (Chernarus, Livonia, Sakhal)

### Interaction
```
events.xml                cfgeventspawns.xml
----------                ------------------
<event name="StaticHeliCrash">    <event name="HeliCrash">
  <position>fixed</position>        <pos x="..." z="..." />
</event>                            </event>
```

---

## ✅ Checklist de validation Codex

### Syntaxe XML
- [ ] Fichier commence par `<?xml version="1.0"?>`
- [ ] Balise racine `<events>` présente
- [ ] Toutes les balises fermées

### Structure des events
- [ ] Chaque `<event>` a un attribut `name` unique
- [ ] Toutes les balises obligatoires présentes

### Valeurs numériques
- [ ] `min` ≤ `nominal` ≤ `max`
- [ ] `lifetime` > 0
- [ ] `active` est 0 ou 1
- [ ] Flags sont 0 ou 1

### Énumérations
- [ ] `<position>` utilise fixed/player/uniform
- [ ] `<limit>` utilise mixed/parent/child/custom

### Children
- [ ] Chaque child a min, max, lootmin, lootmax, type
- [ ] `lootmin` ≤ `lootmax`
- [ ] `min` ≤ `max`

---

**📝 Document créé par Codex - L'outil pour la communauté DayZ FR**
**Version : 1.0 - Basé sur DayZ 1.28**
**Dernière mise à jour : 2025**

---

## 🎯 Prochaines étapes

1. ✅ Documentation events.xml complétée
2. 📄 Prochains fichiers à documenter :
   - zombie_territories.xml (spécifique par map)
   - cfgeconomycore.xml
   - globals.xml

**Félicitations ! Tu as maintenant la documentation COMPLÈTE d'events.xml ! 🎉**
