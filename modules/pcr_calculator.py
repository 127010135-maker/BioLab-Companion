def calculate_pcr(number_of_reactions, overage_percent, reagent_volumes):
    if number_of_reactions < 1:
        raise ValueError("Number of reactions must be at least 1.")
    if overage_percent < 0:
        raise ValueError("Overage cannot be negative.")
    if not reagent_volumes or any(v < 0 for v in reagent_volumes.values()):
        raise ValueError("Enter non-negative reagent volumes.")
    if any(v == 0 for v in reagent_volumes.values()):
        # Zero is allowed for optional components, so no error is raised.
        pass
    multiplier = number_of_reactions * (1 + overage_percent / 100)
    rows = []
    total_all = 0.0
    total_master = 0.0
    for reagent, per_rxn in reagent_volumes.items():
        total = per_rxn * multiplier
        rows.append({
            "Reagent": reagent,
            "Per reaction (µL)": round(per_rxn, 4),
            "Total to prepare (µL)": round(total, 4)
        })
        total_all += per_rxn
        if reagent.strip().lower() not in {"template dna", "template"}:
            total_master += total
    return {
        "rows": rows,
        "reaction_volume": total_all,
        "master_mix_total": total_master
    }
