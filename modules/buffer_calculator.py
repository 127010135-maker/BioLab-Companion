def calculate_molarity(molecular_weight, target_molarity, volume_ml):
    if molecular_weight <= 0 or target_molarity <= 0 or volume_ml <= 0:
        raise ValueError("Molecular weight, molarity, and volume must be greater than zero.")
    volume_l = volume_ml / 1000
    mass_g = target_molarity * volume_l * molecular_weight
    return {"mass_g": mass_g}

def calculate_buffer(mass_g, molecular_weight, volume_ml):
    if mass_g <= 0 or molecular_weight <= 0 or volume_ml <= 0:
        raise ValueError("Mass, molecular weight, and volume must be greater than zero.")
    volume_l = volume_ml / 1000
    molarity = mass_g / (molecular_weight * volume_l)
    return {"molarity": molarity}
