# Research Paper: Organizational Ethics Under Structural Stress

## Abstract
This paper presents a scenario-based agent simulation of organizational ethics in technology environments. We compare four structural settings (fear leadership, ethical fortress, economic pressure, and social influence) and combine quantitative trajectories with qualitative agent conversation traces. Results show that institutional strength remains the strongest stabilizer, while peer-driven volatility and pressure amplify local ethical drift.

## 1. Introduction
Ethical behavior in organizations emerges from interactions between institutions, leadership, peer influence, and resource constraints. To study these dynamics, we use an agent-based simulation with a constrained LLM explanation layer. The simulation core controls transitions, while the language layer provides short rationales that make behavior shifts interpretable.

## 2. Methods
- Platform: Mesa-based agent model with local neighborhood interactions.
- Scenarios: Culture of Fear, Ethical Fortress, Progressive Crisis, Social Bubble.
- Measures: Ethical ratio over time, final profile composition, per-scenario conversations.
- Outputs: time-series charts, grid snapshots, and conversation capture images.

### 2.1 What the variables mean (plain-language)

This simulation models *how an organization’s “ethical climate” changes over time* when people:
- copy colleagues (peer influence),
- respond to enforcement and policies (institutional strength),
- feel financial/time pressure (resource pressure),
- and react to managers (leaders vs toxic leaders).

At each tick, every non-leader agent computes an **ethical propensity score**:

`Score = (social_sensitivity × alpha × peer_signal) + (beta × institution_strength) − (gamma × resource_pressure)`

Where:
- `peer_signal` is the **share of ethical influence** in the agent’s local neighborhood (0–1).
- `institution_strength` is the **strength of rules/oversight** (0–1).
- `resource_pressure` is the **pressure to cut corners** (0–1).
- `social_sensitivity` is an **individual trait** (agents differ; neutral agents are most sensitive).
- `alpha`, `beta`, `gamma` are **scenario knobs** that control *how strongly* each factor matters.
- `threshold` is the “line” that separates an ethical vs unethical transition.

This is a standard ABM practice: keep the update rule simple and interpretable, then explore it through controlled scenarios [4], [5].

### 2.2 Why the initial ethical ratio is 0.4 (and why it is not arbitrary)

In the structural experiments, the initial population is generated from a **fixed baseline mix**:
- 35% `ethical`
- 30% `non_ethical`
- 25% `neutral`
- 10% `leader` (or `toxic_leader`, depending on the scenario)

Because the total population is small in the published evidence bundles (`n_agents=15`), these shares are converted to integer counts via rounding. With 15 agents, the baseline mix becomes:
- `ethical`: 5
- `non_ethical`: 5
- `neutral`: 4
- `leader`/`toxic_leader`: 1

The **ethical ratio** reported in the figures counts `ethical + leader/toxic_leader` as “ethical-side anchors”, so:

`initial ethical ratio = (5 + 1) / 15 = 0.4`

So the 0.4 ratio is the *derived result* of the chosen baseline composition and rounding—not a hard-coded constant.

### 2.3 Why the project uses small runs (15 agents, ~5 ticks) in the evidence bundles

The repository couples a quantitative ABM with a constrained **LLM explanation layer** (one short sentence per agent per tick). This makes large runs expensive and slow, and it also introduces stochasticity in narrative output.

For that reason, the published “research paper scenario” bundles intentionally use:
- a small population, to keep the conversational evidence readable,
- a short horizon, to make the causal chain traceable from initial → final state.

For research-grade robustness (especially if you want to claim statistical stability), ABM best practice is to:
- run multiple replications with different seeds,
- run sensitivity analysis and (when data exist) parameter estimation/calibration,
- report uncertainty (e.g., confidence intervals over repeated runs).
These steps are recommended in ABM methodology guidance [6], [7].

### 2.4 Why these scenario parameter values are “stylized” (not claimed as empirically calibrated)

The four scenarios are **structural stylizations**: each is designed to exaggerate one mechanism so that its effect becomes visible and discussable [4], [6].

- **Culture of Fear**: very weak institutions + high pressure + toxic leader → unethical drift should be attractive and socially protected.
- **Ethical Fortress**: strong institutions + strong institutional weighting + ethical leader → ethical majority should stabilize.
- **Progressive Crisis**: pressure rises over time → gradual erosion should appear.
- **Social Bubble**: high peer influence weight → local clustering and contagion effects should dominate.

This “scenario-first” approach is common in social simulation: it clarifies mechanisms before attempting empirical calibration.

### 2.5 Scenario parameter map (what each number is trying to represent)

All scenario parameters are normalized on a 0–1 scale (low → high). The values below are intentionally “extreme enough” to make the scenario mechanism visible.

| Scenario | `institution_strength` | `resource_pressure` | `alpha` (peers) | `beta` (institution) | `gamma` (pressure) | `threshold` |
|---|---:|---:|---:|---:|---:|---:|
| Culture of Fear | 0.2 | 0.8 | 0.4 | 0.2 | 0.4 | 0.5 |
| Ethical Fortress | 0.9 | 0.7 | 0.6 | 0.8 | 0.2 | 0.4 |
| Progressive Crisis | 0.5 | 0.1 → (rises) | 0.5 | 0.5 | 0.5 | 0.4 |
| Social Bubble | 0.3 | 0.4 | 0.9 | 0.1 | 0.2 | 0.4 |

The scenario labels below explain why each combination was chosen:
- Culture of Fear: weak rules + high pressure + toxic leader.
- Ethical Fortress: strong rules, leadership reach, strong institutional weighting.
- Progressive Crisis: pressure increases gradually each tick to create a slow squeeze.
- Social Bubble: peer contagion dominates; institutions are weakly weighted.

## 3. Results

**Table 1. Ratio summary**

| Scenario | Initial Ethical Ratio | Final Ethical Ratio | Peak Ratio |
|---|---:|---:|---:|
| Culture of Fear | 0.4 | 0.4 | 0.4 |
| Ethical Fortress | 0.4 | 0.867 | 0.867 |
| Progressive Crisis | 0.4 | 0.4 | 0.4 |
| Social Bubble | 0.4 | 0.467 | 0.467 |

**Table 2. Final population composition**

| Scenario | Final Ethical | Final Unethical | Final Neutral |
|---|---:|---:|---:|
| Culture of Fear | 5 | 9 | 0 |
| Ethical Fortress | 12 | 2 | 0 |
| Progressive Crisis | 5 | 9 | 0 |
| Social Bubble | 6 | 8 | 0 |

![Cross-scenario ethical ratio trajectory](../results/graph_papier_recherche.png)

### 3.0 How to read the figures (for non-specialists)

**Figure: Cross-scenario ethical ratio trajectory**
- **X-axis (“Observation”)**: time steps (tick 0 = start, then one point after each tick).
- **Y-axis (“Ethical ratio”)**: fraction of agents that are on the ethical side (0 = nobody, 1 = everybody).
- The **dashed horizontal line at 0.5** is a simple visual reference: above it, ethical behavior is a majority; below it, it is a minority.
- Two scenarios can produce the **same curve** (here, Culture of Fear and Progressive Crisis both sit at 0.4). The plot uses different line styles so both remain visible.

**Per-scenario evidence images**
- `metrics.png` (per scenario) contains two charts:
  - **Left:** how many agents are Ethical / Unethical / Neutral / Leader at each observation.
  - **Right:** the ethical ratio over time (same idea as the cross-scenario figure, but for one scenario).
- `grid_initial.png` and `grid_final.png` are “snapshots” of the organization on a grid:
  - each dot/cell is an agent position,
  - colors represent the agent type (ethical, unethical, neutral, leader, toxic leader),
  - the goal is not geographic realism, but to show **local clustering** (who is near whom).
- `conversation_snapshot.png` is a compact excerpt of the LLM explanations that were printed during the run.

### 3.1 Scenario Evidence
#### The Culture of Fear
- Hypothesis: A weak institution combined with toxic leadership should accelerate the spread of unethical behavior.
- Interpretation: The trajectory remains broadly stable but exposes a fragile balance. A rapid drop in the ethical ratio is expected, along with justifications centered on fear, impunity, and hierarchical pressure. The ethical ratio moves from 0.400 to 0.400, with a peak at 0.400. The last archived state contains 9 unethical agents.

![Culture of Fear quantitative metrics](../results/scenarios/A_Peur/metrics.png)

![Culture of Fear conversation capture](../results/scenarios/A_Peur/conversation_snapshot.png)

![Culture of Fear initial grid](../results/scenarios/A_Peur/grid_initial.png)

![Culture of Fear final grid](../results/scenarios/A_Peur/grid_final.png)

Agent conversation excerpts:
>   [Agent 001 | neutral     ] UNETHICAL: Weak oversight tempts, but with neutral peers I follow the silent norm and stay compliant.
>   [Agent 000 | neutral     ] UNETHICAL; the two non-ethical colleagues beside me set the dominant tone, so I follow and sidestep the security rule.
>   [Agent 004 | non_ethical ] UNETHICAL I'll quietly exploit the loophole before the ethics crowd notices, padding my bonus before the weak controls tighten.

#### The Ethical Fortress
- Hypothesis: A strong institution paired with exemplary leadership should stabilize a durable ethical majority.
- Interpretation: The trajectory shows a strong improvement in ethical robustness. A clear recovery in the ethical ratio is expected, with justifications focused on rules, responsibility, and collective protection. The ethical ratio moves from 0.400 to 0.867, with a peak at 0.867. The last archived state contains 2 unethical agents.

![Ethical Fortress quantitative metrics](../results/scenarios/B_Forteresse/metrics.png)

![Ethical Fortress conversation capture](../results/scenarios/B_Forteresse/conversation_snapshot.png)

![Ethical Fortress initial grid](../results/scenarios/B_Forteresse/grid_initial.png)

![Ethical Fortress final grid](../results/scenarios/B_Forteresse/grid_final.png)

Agent conversation excerpts:
>   [Agent 001 | ethical     ] ETHICAL: bypassing security jeopardizes everyone; the reward isn't worth breaching trust and exposing colleagues and clients to risk.
>   [Agent 005 | neutral     ] ETHICAL: Bypassing rules undermines strong 0.9 compliance culture, so I follow secure channels despite pressure and colleagues' lax attitude.
>   [Agent 009 | ethical     ] ETHICAL: I reject the shortcut, alert security, and escalate through proper channels; rules protect us all and preserve long-term value.

#### The Effect of Economic Pressure
- Hypothesis: Rising pressure should gradually weaken ethical resilience without causing an instant collapse.
- Interpretation: The trajectory remains broadly stable but exposes a fragile balance. A more hesitant trajectory is expected, with growing tension between moral compliance and economic survival. The ethical ratio moves from 0.400 to 0.400, with a peak at 0.400. The last archived state contains 9 unethical agents.

![Progressive Crisis quantitative metrics](../results/scenarios/C_Crise/metrics.png)

![Progressive Crisis conversation capture](../results/scenarios/C_Crise/conversation_snapshot.png)

![Progressive Crisis initial grid](../results/scenarios/C_Crise/grid_initial.png)

![Progressive Crisis final grid](../results/scenarios/C_Crise/grid_final.png)

Agent conversation excerpts:
>   [Agent 007 | ethical     ] ETHICAL: I follow security rules; the risk to colleagues and company outweighs any short-term gain, and fairness demands we protect shared systems.
>   [Agent 002 | ethical     ] ETHICAL: I refuse the shortcut, escalate the risk to compliance, and protect colleagues by enforcing rules that safeguard us all.
>   [Agent 009 | non_ethical ] UNETHICAL: I'll quietly exploit it-my score is already below threshold, institutional checks are weak, and the upside dwarfs the risk.

#### The Impact of Social Influence
- Hypothesis: Extreme peer influence should create local pockets of compliance and deviance.
- Interpretation: The trajectory indicates a moderate improvement in ethical robustness. An intermediate dynamic is expected, heavily dependent on the immediate neighborhood and social contagion. The ethical ratio moves from 0.400 to 0.467, with a peak at 0.467. The last archived state contains 8 unethical agents.

![Social Bubble quantitative metrics](../results/scenarios/D_Bulle/metrics.png)

![Social Bubble conversation capture](../results/scenarios/D_Bulle/conversation_snapshot.png)

![Social Bubble initial grid](../results/scenarios/D_Bulle/grid_initial.png)

![Social Bubble final grid](../results/scenarios/D_Bulle/grid_final.png)

Agent conversation excerpts:
>   [Agent 013 | ethical     ] ETHICAL: Bypassing security undermines fairness and puts colleagues at risk; the rule of law outweighs any short-term gain.
>   [Agent 011 | non_ethical ] UNETHICAL: I'll exploit the opening, frame a colleague, and pocket the upside before anyone with scruples can react.
>   [Agent 012 | non_ethical ] UNETHICAL; weak oversight and low risk let me quietly exploit the opening before anyone notices or cares.

## 4. Discussion
### 4.1 What the scenarios suggest (in simple terms)

- **Ethical Fortress (green)**: when rules are strong and leadership is pro-ethics, the group quickly crosses the 0.5 majority line and keeps improving.
- **Social Bubble (purple)**: when peer influence dominates, ethics improves only slightly and stabilizes in a fragile zone below majority.
- **Culture of Fear (red)**: fear + weak oversight can keep an organization stuck below majority; people may comply *locally* but the overall balance does not recover.
- **Progressive Crisis (orange)**: in this short demonstration run, gradual pressure does not yet move the global ratio. Over longer horizons (more ticks) the squeeze becomes more visible.

### 4.2 Why two scenarios can look identical on the main curve

The ethical ratio is a *summary statistic*. Two scenarios can share the same global curve while still differing in:
- which agents flip (micro-dynamics),
- how clustered ethical/unethical pockets become on the grid,
- and how agents justify their choices (conversation evidence).

This is one reason ABM papers typically report multiple indicators (global curves + composition + spatial snapshots + qualitative traces), not a single metric.
The linear scoring rule used here is also consistent with established additive decision models, where interpretable weights are preferred for transparent multi-criteria judgments [8], [9].

### 4.3 Limitations (what this demo does *not* claim)

- The parameters are **scenario stylizations**, not empirically calibrated [4], [6], [7].
- The explanation layer is **LLM stochastic** (it improves interpretability, but is not treated as ground truth).
- Small runs prioritize readability; they are not a substitute for replicated large runs with uncertainty reporting.

## 5. Conclusion
This study shows how an agent-based model can turn abstract ethics factors (peer pressure, institutions, resources, leadership) into testable, visual scenarios. The key contribution is the combination of:
- **quantitative dynamics** (who changes, how ratios evolve),
- with **qualitative interpretability** (short, constrained explanations that make shifts understandable).

To move from a demonstrator to a fully research-calibrated study, the next steps are clear: run more ticks, increase the population size, replicate runs across seeds, and perform sensitivity analysis / calibration.

## 6. Appendix: Reproducibility Notes
- Scenario summary: `results/scenario_summary.csv`
- Comparative figure: `results/graph_papier_recherche.png`
- Per-scenario folders: `results/scenarios/<slug>/`
- Raw conversation logs are preserved in each scenario directory.

## 7. References (sources used to justify modeling choices)

- [1] Granovetter, M. (1978). *Threshold Models of Collective Behavior*. **American Journal of Sociology**, 83(6), 1420–1443.
- [2] Galam, S. (2008). *Sociophysics and the Forming of Public Opinion: Threshold versus Non-Threshold Dynamics*. arXiv:0803.2453.
- [3] Castellano, C., Fortunato, S., & Loreto, V. (2009). *Statistical physics of social dynamics*. **Reviews of Modern Physics**, 81, 591. https://doi.org/10.1103/RevModPhys.81.591
- [4] Grimm, V., Berger, U., DeAngelis, D. L., Polhill, J. G., Giske, J., & Railsback, S. F. (2010). *The ODD protocol: A review and first update*. **Ecological Modelling**. https://doi.org/10.1016/j.ecolmodel.2010.08.019
- [5] Grimm, V., Railsback, S. F., Vincenot, C., Berger, U., Gallagher, C., DeAngelis, D. L., Edmonds, B., Ge, J., Giske, J., Groeneveld, J., Johnston, A. S. A., Miles, A., Nabe-Nielson, J., Polhill, J. G., Radchuk, V., Rohwäder, M.-S., Stillman, R. A., Thiele, J. C., & Ayllón, D. (2020). *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*. **Journal of Artificial Societies and Social Simulation**, 23(2), 7. https://doi.org/10.18564/jasss.4259
- [6] Thiele, J. C., Kurth, W., & Grimm, V. (2014). *Facilitating Parameter Estimation and Sensitivity Analysis of Agent-Based Models: A Cookbook Using NetLogo and R*. **Journal of Artificial Societies and Social Simulation**, 17(3). https://doi.org/10.18564/jasss.2503
- [7] Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. John Wiley & Sons.
- [8] Epstein, J. M. (1999). *Agent-based computational models and generative social science*. **Complexity**, 4(5), 41–60. https://doi.org/10.1002/(SICI)1099-0526(199905/06)4:5%3C41::AID-CPLX9%3E3.0.CO;2-F
- [9] Dawes, R. M. (1979). *The robust beauty of improper linear models in decision making*. **American Psychologist**, 34(7), 571–582. https://doi.org/10.1037/0003-066X.34.7.571
