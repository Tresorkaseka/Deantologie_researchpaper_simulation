# Architecture du Projet

## 1. Objectif de l’architecture

Ce document présente l’architecture de l’ensemble du projet du point de vue d’un flux de recherche. Le dépôt est conçu comme un pipeline scientifique reproductible dans lequel la simulation, l’interprétation, la visualisation et la publication sont reliées, mais clairement séparées.

## 2. Vue d’ensemble du système

### 2.1 Pipeline en langage simple

Ce schéma répond à la question: **« Si je lance le projet une fois, que se passe-t-il du début à la fin ? »**

```mermaid
flowchart TD
    A["Vous lancez un script (exemple: run_research_experiments.py)"] --> B["Chargement des paramètres de scénario (research_config.py)"]
    B --> C["Création du monde de simulation (EthicalOrgModel dans model.py)"]
    C --> D{"Répéter pour chaque tick"}
    D --> E["Chaque agent se déplace sur la grille"]
    E --> F["Chaque agent observe ses collègues proches"]
    F --> G["L’agent calcule un score (pairs + institution - pression)"]
    G --> H["Le LLM écrit une courte justification (couche explicative optionnelle)"]
    H --> I["L’agent peut changer de type (éthique / non éthique / neutre)"]
    I --> J["Le modèle enregistre les métriques (comptes + ratio éthique)"]
    J --> D
    D -->|fin| K["Enregistrement du lot de résultats (results/scenarios/<scenario>/...)"]
    K --> L["Résumé comparatif (scenario_summary.csv + graph_papier_recherche.png)"]
    L --> M["Lecture/écriture des documents du papier (docs/Research_Paper_Scenarios.md, ODD_Documentation.md, ...)"]
```

### 2.2 Pipeline de recherche: ODD -> Simulation -> LLM -> Résultats

C’est le flux de bout en bout le plus clair si l’on veut expliquer l’étude à quelqu’un hors du domaine:

```mermaid
flowchart LR
    IN["Entrée\nODD + question de recherche + paramètres de scénario"] --> ODD["Conception du modèle\nEntités, variables, échelles, règles de processus"]
    ODD --> SIM["Cœur de simulation\nLes agents Mesa se déplacent, observent, scorent et se mettent à jour"]
    SIM --> LLM["Couche LLM\nJustifications courtes et lisibles"]
    LLM --> OUT["Sorties\nTableaux, courbes, grilles, captures de conversation"]
    OUT --> DOC["Interprétation\nDiscussion, conclusion et rapport/PDF"]

    ODD --- O1["Pourquoi ces variables ?\nPourquoi ces seuils ?"]
    SIM --- S1["Que se passe-t-il à chaque tick ?"]
    LLM --- L1["Pourquoi l’agent a-t-il dit cela ?"]
    OUT --- R1["Qu’est-ce qui a changé dans les résultats ?"]
```

En termes simples:
- `ODD` définit la structure du modèle et la signification des nombres.
- La simulation transforme ces règles en comportement d’agents dans le temps.
- Le `LLM` ne pilote pas le modèle; il explique le contexte local de décision en texte court.
- Les sorties sont ensuite agrégées en figures et tableaux pour l’article.

### 2.3 Vue technique du système (modules)

```mermaid
flowchart TB
    subgraph RC["Couche de configuration de recherche"]
        RC1["research_config.py"]
        RC2["scenarios.py"]
    end

    subgraph SC["Cœur de simulation"]
        SC1["model.py"]
        SC2["agents.py"]
        SC3["llm_backend.py"]
    end

    subgraph OR["Couche d’orchestration"]
        OR1["run.py"]
        OR2["run_simple.py"]
        OR3["run_scenarios.py"]
        OR4["run_research_experiments.py"]
    end

    subgraph EV["Couche de production des preuves"]
        EV1["viz.py"]
        EV2["results/scenarios/scenario-slug/"]
        EV3["results/scenario_summary.csv"]
    end

    subgraph PB["Couche de publication"]
        PB1["build_full_report.py"]
        PB2["corpus de documentation docs/"]
    end

    subgraph MG["Mémoire locale et gouvernance du projet"]
        MG1["memory-bank/"]
        MG2["tasks, progress, active context"]
    end

    RC --> OR
    OR --> SC
    SC --> EV
    EV --> PB
    OR -. contexte de travail local .-> MG
```

## 3. Principes architecturaux

### 3.1 Séparation des responsabilités

Le dépôt sépare:

- les hypothèses scientifiques et les définitions de scénarios;
- la logique de simulation au niveau agent;
- l’accès LLM spécifique au fournisseur;
- la génération des figures et des rapports;
- la mémoire du projet et le suivi d’exécution.

### 3.2 Reproductibilité

Les artefacts générés sont dérivés des fichiers source et sont volontairement exclus du contrôle de version. Le dépôt est donc conçu pour publier le code source, et non des artefacts éphémères.

### 3.3 Interprétabilité

L’architecture maintient une distinction nette entre:

- la logique de simulation explicite implémentée en Python;
- la sortie textuelle interprétative générée par la couche LLM.

Cette distinction est essentielle pour la transparence méthodologique.

## 4. Architecture d’exécution

### 4.1 Principaux chemins d’exécution

| Chemin | Objectif | Point d’entrée typique |
|---|---|---|
| Validation rapide | Exécution locale à petite échelle | `run_simple.py` |
| Simulation standard | Un scénario avec graphiques | `run.py` |
| Comparaison de scénarios | Plusieurs dilemmes sur une même exécution | `run_scenarios.py` |
| Campagne de recherche complète | Expériences structurelles contrôlées avec lots d’artefacts | `run_research_experiments.py` |
| Exploration interactive | Inspection via navigateur | `vis_server.py` |

### 4.2 Flux de données à l’exécution

```mermaid
flowchart TD
    ENV[".env / variables d’environnement"] --> LLM["llm_backend.py"]
    LLM <--> PROVIDER["Fournisseur LLM choisi"]
    LLM --> MODEL["model.py"]
    MODEL <--> AGENTS["agents.py"]
    MODEL --> VIZ["viz.py + métriques/journaux sauvegardés"]
    VIZ --> RESULTS["results/"]
```

### 4.3 Ce qui se passe à l’intérieur d’un tick

```mermaid
sequenceDiagram
    autonumber
    participant Runner as run_research_experiments.py
    participant Model as EthicalOrgModel (model.py)
    participant Sched as RandomActivation (Mesa)
    participant Agent as ProfessionalAgent (agents.py)
    participant LLM as LLM backend (llm_backend.py)
    participant DC as DataCollector (Mesa)

    Runner->>Model: step()
    Model->>Sched: step() (ordre aléatoire des agents)
    loop pour chaque agent
        Sched->>Agent: step()
        Agent->>Agent: move()
        Agent->>Agent: observe neighbors (radius 2 or 3)
        Agent->>Agent: compute_score()
        Agent->>LLM: ask_llm(context prompt)
        LLM-->>Agent: "ETHICAL ..." or "UNETHICAL ..."
        Agent->>Agent: update_type(score + noise, text)
    end
    Model->>DC: collect metrics (counts + ratios)
```

## 5. Architecture de recherche

La campagne de recherche est organisée autour de lots de scénarios.

```mermaid
flowchart TD
    SPEC["Spécification d’expérience"] --> RUN["Exécution du scénario"]
    RUN --> M1["metrics.csv"]
    RUN --> M2["interpretation.txt"]
    RUN --> M3["conversation_log.txt"]
    RUN --> M4["metrics.png"]
    RUN --> M5["grid_initial.png"]
    RUN --> M6["grid_final.png"]
    RUN --> M7["conversation_snapshot.png"]
    RUN --> CROSS["Comparaison inter-scénarios"]
    CROSS --> C1["scenario_summary.csv"]
    CROSS --> C2["graph_papier_recherche.png"]
```

Cette structure rend chaque scénario audit-able comme un lot de preuves indépendant.

## 6. Architecture de la documentation

### 6.1 Documents sources

Le dossier `docs/` sert maintenant plusieurs publics:

- `Execution_Guide.md` pour l’onboarding opérationnel;
- `Maintenance_et_Lancement.md` pour les procédures de relance et de maintenance;
- `ODD_Documentation.md` pour la description formelle du modèle;
- `Code_Architecture.md` pour la structure au niveau code et les interactions entre fonctions;
- `Project_Architecture.md` pour la vue globale du système.

### 6.2 Chemin de publication

```mermaid
flowchart TD
    SRC["Docs rédigés à la main + rapports générés"] --> DOCS["Corpus de documentation docs/"]
    DOCS --> REVIEW["Publication GitHub et revue externe"]
```

## 7. Architecture LLM agnostique au fournisseur

Le dépôt est conçu pour que les utilisateurs futurs puissent choisir le fournisseur qui correspond à leurs contraintes institutionnelles, financières ou méthodologiques.

### 7.1 Contrat

Le code de simulation attend seulement:

- un identifiant de modèle;
- une clé API;
- un libellé de fournisseur optionnel;
- une base URL compatible optionnelle.

### 7.2 Encapsulation

Toute la logique côté fournisseur est contenue dans `llm_backend.py`. Cela réduit le couplage et empêche le noyau de simulation de dépendre d’un SDK ou d’un fournisseur unique.

## 8. Topologie du dépôt

```text
/
|- agents.py
|- model.py
|- llm_backend.py
|- research_config.py
|- run*.py
|- viz.py
|- build_full_report.py
|- docs/
|  |- Execution_Guide.md
|  |- Maintenance_et_Lancement.md
|  |- ODD_Documentation.md
|  |- Code_Architecture.md
|  |- Project_Architecture.md
|- memory-bank/
|  |- projectbrief.md
|  |- productContext.md
|  |- activeContext.md
|  |- systemPatterns.md
|  |- techContext.md
|  |- progress.md
|  |- tasks/
|- results/              généré localement, ignoré par git
```

## 9. Pourquoi cette architecture soutient la qualité scientifique

Cette structure est adaptée à un travail orienté recherche parce qu’elle soutient:

- des définitions de scénarios traçables;
- une séparation claire entre les hypothèses du modèle et les sorties narratives;
- une génération reproductible des preuves;
- une revue indépendante des figures, journaux et rapports;
- une documentation prête à publier sans polluer le dépôt avec des fichiers générés.

## 10. Ordre de lecture recommandé

Pour un nouveau lecteur ou évaluateur, l’ordre recommandé est:

1. `README.md`
2. `docs/Project_Architecture.md`
3. `docs/Code_Architecture.md`
4. `docs/ODD_Documentation.md`
5. `docs/Execution_Guide.md`

Cette séquence va de la compréhension stratégique au détail d’implémentation, puis à la pratique d’exécution.

