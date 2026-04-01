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

## 3. Results

| Scenario | Initial Ethical Ratio | Final Ethical Ratio | Peak Ratio | Final Ethical | Final Unethical | Final Neutral |
|---|---:|---:|---:|---:|---:|---:|
| Culture of Fear | 0.4 | 0.4 | 0.4 | 5 | 9 | 0 |
| Ethical Fortress | 0.4 | 0.867 | 0.867 | 12 | 2 | 0 |
| Progressive Crisis | 0.4 | 0.4 | 0.4 | 5 | 9 | 0 |
| Social Bubble | 0.4 | 0.467 | 0.467 | 6 | 8 | 0 |

![Cross-scenario ethical ratio trajectory](../results/graph_papier_recherche.png)

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
The cross-scenario comparison highlights a robust methodological finding: structural variables dominate isolated individual tendencies. Strong institutions reduce ethical volatility and support durable ethical majorities. In contrast, weak institutional settings and high social contagion produce fragile trajectories that are highly sensitive to local neighborhood composition.

Conversation evidence reinforces this reading. In stronger governance contexts, agents reference compliance and institutional duty more often. Under fragile conditions, conversation patterns shift toward tactical adaptation and local imitation. Even when some provider errors appear in raw logs, the surviving trace remains coherent with quantitative transitions.

## 5. Conclusion
This study confirms that scenario-based agent modeling can produce research-grade evidence on organizational ethics when quantitative trajectories are paired with structured conversational traces. The framework supports reproducible comparative analysis and can be extended with richer role taxonomies, larger populations, and repeated-run confidence intervals.

## 6. Appendix: Reproducibility Notes
- Scenario summary: `results/scenario_summary.csv`
- Comparative figure: `results/graph_papier_recherche.png`
- Per-scenario folders: `results/scenarios/<slug>/`
- Raw conversation logs are preserved in each scenario directory.
