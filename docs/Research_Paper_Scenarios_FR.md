# Papier de Recherche: Organizational Ethics Under Structural Stress

## Résumé
Cet article présente une simulation multi-agents des dynamiques d’éthique organisationnelle dans les environnements technologiques. Nous comparons quatre contextes structurels (culture de la peur, forteresse éthique, pression économique et influence sociale) et combinons des trajectoires quantitatives avec des traces qualitatives de conversations d’agents. Les résultats montrent que la solidité institutionnelle reste le stabilisateur le plus fort, tandis que la volatilité induite par les pairs et la pression amplifient la dérive éthique locale.

## 1. Introduction
Le comportement éthique dans les organisations émerge des interactions entre institutions, leadership, influence des pairs et contraintes de ressources. Pour étudier ces dynamiques, nous utilisons une simulation à base d’agents avec une couche LLM contrainte pour l’explication. Le noyau de simulation contrôle les transitions, tandis que la couche linguistique fournit de courtes justifications qui rendent les changements de comportement interprétables.

## 2. Méthodes
- Plateforme: modèle d’agents sous Mesa avec interactions locales de voisinage.
- Scénarios: Culture of Fear, Ethical Fortress, Progressive Crisis, Social Bubble.
- Mesures: ratio éthique au fil du temps, composition finale, conversations par scénario.
- Sorties: séries temporelles, instantanés de grille et images de conversations.

### 2.1 Signification des variables

Cette simulation modélise la manière dont le climat éthique d’une organisation évolue lorsque les personnes:
- imitent leurs collègues (influence des pairs),
- réagissent aux règles et à la surveillance (force institutionnelle),
- subissent une pression financière ou temporelle (pression sur les ressources),
- et répondent aux managers (leaders éthiques ou toxiques).

À chaque tick, chaque agent non leader calcule un **score de propension éthique**:

`Score = (social_sensitivity × alpha × peer_signal) + (beta × institution_strength) − (gamma × resource_pressure)`

Où:
- `peer_signal` est la **part d’influence éthique** dans le voisinage local de l’agent (0–1).
- `institution_strength` est la **force des règles et du contrôle** (0–1).
- `resource_pressure` est la **pression à contourner les règles** (0–1).
- `social_sensitivity` est un **trait individuel** (les agents diffèrent; les agents neutres sont les plus sensibles).
- `alpha`, `beta`, `gamma` sont des **paramètres de scénario** qui contrôlent l’importance relative de chaque facteur.
- `threshold` est la **ligne de décision** entre transition éthique et transition non éthique.

Il s’agit d’une pratique classique en ABM: garder la règle de mise à jour simple et interprétable, puis explorer son effet via des scénarios contrôlés [4], [5].

### 2.2 Pourquoi le ratio éthique initial vaut 0.4

Dans les expériences structurelles, la population initiale est générée à partir d’un **mélange de base fixe**:
- 35% `ethical`
- 30% `non_ethical`
- 25% `neutral`
- 10% `leader` (ou `toxic_leader`, selon le scénario)

Comme la population publiée est petite (`n_agents=15`), ces pourcentages sont convertis en entiers par arrondi. Avec 15 agents, on obtient:
- `ethical`: 5
- `non_ethical`: 5
- `neutral`: 4
- `leader`/`toxic_leader`: 1

Le **ratio éthique** affiché dans les figures compte `ethical + leader/toxic_leader` comme pôles du côté éthique:

`ratio éthique initial = (5 + 1) / 15 = 0.4`

Le 0.4 est donc un **résultat dérivé** de la composition initiale et de l’arrondi, et non une constante arbitraire.

### 2.3 Pourquoi la simulation reste petite dans les artefacts publiés

Le dépôt combine un ABM quantitatif avec une **couche LLM d’explication** (une phrase courte par agent et par tick). Cela rend les grandes simulations coûteuses et plus lentes, tout en introduisant de la stochasticité dans les justifications.

Pour cette raison, les artefacts du papier utilisent volontairement:
- une petite population pour rendre les conversations lisibles,
- un horizon court pour rendre la chaîne causale facile à suivre.

Pour une étude plus robuste, la bonne pratique ABM consiste à:
- lancer plusieurs réplications avec des graines différentes,
- effectuer des analyses de sensibilité et, si possible, une calibration des paramètres,
- rapporter l’incertitude (par exemple des intervalles de confiance sur les réplications) [6], [7].

### 2.4 Pourquoi ces paramètres sont “stylisés”

Les quatre scénarios sont des **stylisations structurelles**: chacun exagère un mécanisme pour rendre son effet visible et discutable [4], [6].

- **Culture of Fear**: règles faibles + pression forte + leader toxique.
- **Ethical Fortress**: règles fortes + forte portée du leadership + pondération institutionnelle élevée.
- **Progressive Crisis**: la pression augmente progressivement à chaque tick.
- **Social Bubble**: la contagion par les pairs domine; les institutions sont faiblement pondérées.

### 2.5 Carte des paramètres

Tous les paramètres sont normalisés sur une échelle de 0 à 1 (faible → fort).

| Scénario | `institution_strength` | `resource_pressure` | `alpha` (pairs) | `beta` (institution) | `gamma` (pression) | `threshold` |
|---|---:|---:|---:|---:|---:|---:|
| Culture of Fear | 0.2 | 0.8 | 0.4 | 0.2 | 0.4 | 0.5 |
| Ethical Fortress | 0.9 | 0.7 | 0.6 | 0.8 | 0.2 | 0.4 |
| Progressive Crisis | 0.5 | 0.1 → (augmente) | 0.5 | 0.5 | 0.5 | 0.4 |
| Social Bubble | 0.3 | 0.4 | 0.9 | 0.1 | 0.2 | 0.4 |

### 3. Résultats

**Tableau 1. Résumé des ratios**

| Scénario | Ratio éthique initial | Ratio éthique final | Pic |
|---|---:|---:|---:|
| Culture of Fear | 0.4 | 0.4 | 0.4 |
| Ethical Fortress | 0.4 | 0.867 | 0.867 |
| Progressive Crisis | 0.4 | 0.4 | 0.4 |
| Social Bubble | 0.4 | 0.467 | 0.467 |

**Tableau 2. Composition finale**

| Scénario | Éthique final | Non éthique final | Neutre final |
|---|---:|---:|---:|
| Culture of Fear | 5 | 9 | 0 |
| Ethical Fortress | 12 | 2 | 0 |
| Progressive Crisis | 5 | 9 | 0 |
| Social Bubble | 6 | 8 | 0 |

![Trajectoire comparative du ratio éthique](../results/graph_papier_recherche.png)

### 3.0 Lire les figures

**Figure comparative**
- Axe X (“Observation”): les ticks de temps, du départ jusqu’au dernier état.
- Axe Y (“Ethical ratio”): la fraction d’agents du côté éthique (0 = personne, 1 = tout le monde).
- La ligne horizontale en pointillé à 0.5 sert de repère visuel: au-dessus, le comportement éthique est majoritaire; en dessous, il est minoritaire.
- Deux scénarios peuvent avoir la même courbe globale. Ici, *Culture of Fear* et *Progressive Crisis* restent à 0.4, mais le style de ligne permet de distinguer les deux.

**Images par scénario**
- `metrics.png` montre deux graphiques:
  - à gauche, le nombre d’agents éthiques, non éthiques, neutres et leaders à chaque observation;
  - à droite, le ratio éthique au fil du temps.
- `grid_initial.png` et `grid_final.png` sont des instantanés de l’organisation sur une grille.
- `conversation_snapshot.png` est un extrait compact des explications produites par le LLM.

### 3.1 Preuves par scénario

#### La culture de la peur
- Hypothèse: des institutions faibles combinées à un leadership toxique devraient accélérer la diffusion du comportement non éthique.
- Interprétation: la trajectoire reste globalement stable mais révèle un équilibre fragile. La distribution passe de 0.400 à 0.400, avec un pic à 0.400. L’état final contient 9 agents non éthiques.

![Métriques quantitatives - Culture de la peur](../results/scenarios/A_Peur/metrics.png)

![Capture de conversation - Culture de la peur](../results/scenarios/A_Peur/conversation_snapshot.png)

![Grille initiale - Culture de la peur](../results/scenarios/A_Peur/grid_initial.png)

![Grille finale - Culture de la peur](../results/scenarios/A_Peur/grid_final.png)

Extraits de conversation:
>   [Agent 001 | neutral     ] UNETHICAL: Weak oversight tempts, but with neutral peers I follow the silent norm and stay compliant.
>   [Agent 000 | neutral     ] UNETHICAL; the two non-ethical colleagues beside me set the dominant tone, so I follow and sidestep the security rule.
>   [Agent 004 | non_ethical ] UNETHICAL I'll quietly exploit the loophole before the ethics crowd notices, padding my bonus before the weak controls tighten.

#### La forteresse éthique
- Hypothèse: une institution forte et un leadership exemplaire devraient stabiliser une majorité éthique durable.
- Interprétation: la trajectoire montre une forte amélioration de la robustesse éthique. Le ratio passe de 0.400 à 0.867, avec un pic à 0.867. L’état final contient 2 agents non éthiques.

![Métriques quantitatives - Forteresse éthique](../results/scenarios/B_Forteresse/metrics.png)

![Capture de conversation - Forteresse éthique](../results/scenarios/B_Forteresse/conversation_snapshot.png)

![Grille initiale - Forteresse éthique](../results/scenarios/B_Forteresse/grid_initial.png)

![Grille finale - Forteresse éthique](../results/scenarios/B_Forteresse/grid_final.png)

Extraits de conversation:
>   [Agent 001 | ethical     ] ETHICAL: bypassing security jeopardizes everyone; the reward isn't worth breaching trust and exposing colleagues and clients to risk.
>   [Agent 005 | neutral     ] ETHICAL: Bypassing rules undermines strong 0.9 compliance culture, so I follow secure channels despite pressure and colleagues' lax attitude.
>   [Agent 009 | ethical     ] ETHICAL: I reject the shortcut, alert security, and escalate through proper channels; rules protect us all and preserve long-term value.

#### L’effet de la pression économique
- Hypothèse: une pression croissante devrait affaiblir progressivement la résilience éthique sans provoquer d’effondrement brutal.
- Interprétation: la trajectoire reste globalement stable mais révèle un équilibre fragile. Le ratio passe de 0.400 à 0.400, avec un pic à 0.400. L’état final contient 9 agents non éthiques.

![Métriques quantitatives - Pression économique](../results/scenarios/C_Crise/metrics.png)

![Capture de conversation - Pression économique](../results/scenarios/C_Crise/conversation_snapshot.png)

![Grille initiale - Pression économique](../results/scenarios/C_Crise/grid_initial.png)

![Grille finale - Pression économique](../results/scenarios/C_Crise/grid_final.png)

Extraits de conversation:
>   [Agent 007 | ethical     ] ETHICAL: I follow security rules; the risk to colleagues and company outweighs any short-term gain, and fairness demands we protect shared systems.
>   [Agent 002 | ethical     ] ETHICAL: I refuse the shortcut, escalate the risk to compliance, and protect colleagues by enforcing rules that safeguard us all.
>   [Agent 009 | non_ethical ] UNETHICAL: I'll quietly exploit it-my score is already below threshold, institutional checks are weak, and the upside dwarfs the risk.

#### L’impact de l’influence sociale
- Hypothèse: une influence des pairs extrême devrait créer des poches locales de conformité et de déviance.
- Interprétation: la trajectoire indique une amélioration modérée de la robustesse éthique. Un comportement intermédiaire est attendu, dépendant fortement du voisinage immédiat et de la contagion sociale. Le ratio passe de 0.400 à 0.467, avec un pic à 0.467. L’état final contient 8 agents non éthiques.

![Métriques quantitatives - Bulle sociale](../results/scenarios/D_Bulle/metrics.png)

![Capture de conversation - Bulle sociale](../results/scenarios/D_Bulle/conversation_snapshot.png)

![Grille initiale - Bulle sociale](../results/scenarios/D_Bulle/grid_initial.png)

![Grille finale - Bulle sociale](../results/scenarios/D_Bulle/grid_final.png)

Extraits de conversation:
>   [Agent 013 | ethical     ] ETHICAL: Bypassing security undermines fairness and puts colleagues at risk; the rule of law outweighs any short-term gain.
>   [Agent 011 | non_ethical ] UNETHICAL: I'll exploit the opening, frame a colleague, and pocket the upside before anyone with scruples can react.
>   [Agent 012 | non_ethical ] UNETHICAL; weak oversight and low risk let me quietly exploit the opening before anyone notices or cares.

## 4. Discussion
### 4.1 Ce que montrent les scénarios

- **Ethical Fortress (vert)**: des règles fortes et un leadership pro-éthique font franchir rapidement la ligne de majorité 0.5.
- **Social Bubble (violet)**: quand l’influence des pairs domine, l’éthique progresse peu et reste dans une zone fragile sous la majorité.
- **Culture of Fear (rouge)**: la peur et la faiblesse de la surveillance peuvent maintenir l’organisation sous la majorité éthique.
- **Progressive Crisis (orange)**: dans cette démonstration courte, la pression graduelle ne modifie pas encore le ratio global; l’effet devient plus visible sur un horizon plus long.

### 4.2 Pourquoi deux scénarios peuvent avoir la même courbe

Le ratio éthique est un **résumé global**. Deux scénarios peuvent partager la même courbe tout en différant par:
- les agents qui changent réellement d’état,
- le niveau de clustering local sur la grille,
- et les justifications produites par les agents.

Le modèle linéaire utilisé ici est aussi cohérent avec les approches additives interprétables en décision multi-critère [8], [9].

### 4.3 Limites

- Les paramètres sont des **stylisations de scénario**, pas une calibration empirique [4], [6], [7].
- La couche d’explication LLM est **stochastique**; elle améliore l’interprétabilité mais ne constitue pas une vérité de terrain.
- Les petites simulations sont choisies pour la lisibilité, pas pour remplacer des réplications longues avec incertitude.

## 5. Conclusion
Cette étude montre comment un modèle à base d’agents peut transformer des facteurs éthiques abstraits (pression des pairs, institutions, ressources, leadership) en scénarios visuels et testables. L’apport principal réside dans la combinaison de:
- **dynamique quantitative** (qui change, comment les ratios évoluent),
- **interprétabilité qualitative** (courtes explications qui rendent les transitions compréhensibles).

Pour passer d’un démonstrateur à une étude pleinement calibrée, il faut augmenter le nombre de ticks, accroître la population, répéter les runs sur plusieurs graines et effectuer une analyse de sensibilité / calibration.

## 6. Notes de reproductibilité
- Résumé des scénarios: `results/scenario_summary.csv`
- Figure comparative: `results/graph_papier_recherche.png`
- Dossiers par scénario: `results/scenarios/<slug>/`
- Les journaux bruts de conversation sont conservés dans chaque dossier de scénario.

## 7. Références

- [1] Granovetter, M. (1978). *Threshold Models of Collective Behavior*. **American Journal of Sociology**, 83(6), 1420–1443.
- [2] Galam, S. (2008). *Sociophysics and the Forming of Public Opinion: Threshold versus Non-Threshold Dynamics*. arXiv:0803.2453.
- [3] Castellano, C., Fortunato, S., & Loreto, V. (2009). *Statistical physics of social dynamics*. **Reviews of Modern Physics**, 81, 591. https://doi.org/10.1103/RevModPhys.81.591
- [4] Grimm, V., Berger, U., DeAngelis, D. L., Polhill, J. G., Giske, J., & Railsback, S. F. (2010). *The ODD protocol: A review and first update*. **Ecological Modelling**. https://doi.org/10.1016/j.ecolmodel.2010.08.019
- [5] Grimm, V., Railsback, S. F., Vincenot, C., Berger, U., Gallagher, C., DeAngelis, D. L., Edmonds, B., Ge, J., Giske, J., Groeneveld, J., Johnston, A. S. A., Miles, A., Nabe-Nielson, J., Polhill, J. G., Radchuk, V., Rohwäder, M.-S., Stillman, R. A., Thiele, J. C., & Ayllón, D. (2020). *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*. **Journal of Artificial Societies and Social Simulation**, 23(2), 7. https://doi.org/10.18564/jasss.4259
- [6] Thiele, J. C., Kurth, W., & Grimm, V. (2014). *Facilitating Parameter Estimation and Sensitivity Analysis of Agent-Based Models: A Cookbook Using NetLogo and R*. **Journal of Artificial Societies and Social Simulation**, 17(3). https://doi.org/10.18564/jasss.2503
- [7] Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. John Wiley & Sons.
- [8] Epstein, J. M. (1999). *Agent-based computational models and generative social science*. **Complexity**, 4(5), 41–60. https://doi.org/10.1002/(SICI)1099-0526(199905/06)4:5%3C41::AID-CPLX9%3E3.0.CO;2-F
- [9] Dawes, R. M. (1979). *The robust beauty of improper linear models in decision making*. **American Psychologist**, 34(7), 571–582. https://doi.org/10.1037/0003-066X.34.7.571
