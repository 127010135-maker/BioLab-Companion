def calculate_dilution(initial_concentration, dilution_factor, number_of_steps):
    if initial_concentration <= 0:
        raise ValueError("Initial concentration must be greater than zero.")
    if dilution_factor < 1:
        raise ValueError("Dilution factor must be at least 1.")
    if number_of_steps < 1:
        raise ValueError("Number of steps must be at least 1.")
    rows = []
    for step in range(1, int(number_of_steps) + 1):
        concentration = initial_concentration / (dilution_factor ** step)
        rows.append({
            "Step": step,
            "Cumulative dilution": f"1:{dilution_factor ** step:g}",
            "Concentration": concentration
        })
    return {"rows": rows, "final_concentration": rows[-1]["Concentration"]}
