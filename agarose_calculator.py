def calculate_agarose(concentration_percent, volume_ml):
    if concentration_percent <= 0 or volume_ml <= 0:
        raise ValueError("Concentration and volume must be greater than zero.")
    mass_g = concentration_percent * volume_ml / 100
    return {"agarose_g": mass_g}
