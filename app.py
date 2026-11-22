import streamlit as st
import pandas as pd
from modules.pcr_calculator import calculate_pcr
from modules.agarose_calculator import calculate_agarose
from modules.dilution_calculator import calculate_dilution
from modules.buffer_calculator import calculate_molarity, calculate_buffer

st.set_page_config(page_title="BioLab Companion", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.main {background-color: #f7fafc;}
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.5rem; border-radius: 16px; background: linear-gradient(120deg,#e0f2fe,#ecfdf5);}
.small-note {color: #52606d; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧬 BioLab Companion</h1><p>Interactive calculators for common biotechnology laboratory preparations.</p></div>', unsafe_allow_html=True)
st.caption("Educational support tool. Always verify calculations against your laboratory SOP, reagent datasheets, and supervisor instructions.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a calculator", [
        "Home", "PCR Master Mix", "Agarose Gel", "Serial Dilution",
        "Molarity & Solution Preparation"
    ])
    st.divider()
    st.caption("BioLab Companion | Python + Streamlit")

if page == "Home":
    st.subheader("Welcome!")
    st.write("BioLab Companion brings frequently used laboratory calculations together in one simple interface.")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**PCR Master Mix**\n\nCalculate reagent volumes for multiple reactions, including an optional pipetting overage.")
        st.info("**Agarose Gel Preparation**\n\nCalculate agarose mass for a selected gel percentage and buffer volume.")
    with c2:
        st.info("**Serial Dilution**\n\nCalculate concentrations across successive dilution steps.")
        st.info("**Molarity & Solution Preparation**\n\nCalculate solute mass from molecular weight, target molarity, and final volume.")
    st.subheader("How to use")
    st.write("1. Select a calculator from the sidebar.\n2. Enter values with the units shown.\n3. Select **Calculate**.\n4. Review the result, formula, and notes before preparing anything in the laboratory.")
    st.warning("The calculators do not replace experimental protocols. Check stock concentrations, reagent compatibility, and local safety procedures.")

elif page == "PCR Master Mix":
    st.subheader("PCR Master Mix Calculator")
    st.write("Enter the volume of each component for **one reaction**. The calculator scales the values to the required number of reactions.")
    n = st.number_input("Number of reactions (including controls)", min_value=1, max_value=500, value=10, step=1)
    overage = st.number_input("Extra volume / overage (%)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)
    st.markdown("**Per-reaction reagent volumes (µL)**")
    defaults = {"PCR master mix": 10.0, "Forward primer": 1.0, "Reverse primer": 1.0, "Template DNA": 2.0, "Nuclease-free water": 5.0}
    cols = st.columns(2)
    vals = {}
    for i, (name, default) in enumerate(defaults.items()):
        with cols[i % 2]:
            vals[name] = st.number_input(name, min_value=0.0, value=default, step=0.5, key=f"pcr_{name}")
    if st.button("Calculate PCR volumes", type="primary"):
        try:
            result = calculate_pcr(n, overage, vals)
            st.success(f"Prepare a total master mix volume of {result['master_mix_total']:.2f} µL (excluding template DNA).")
            df = pd.DataFrame(result["rows"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.metric("Total reaction volume", f"{result['reaction_volume']:.2f} µL")
            st.info("Formula: total reagent volume = per-reaction volume × number of reactions × (1 + overage/100).")
            st.caption("Template DNA is listed separately in the table and excluded from the combined master-mix total by default.")
            st.download_button("Download PCR calculation (CSV)", df.to_csv(index=False).encode("utf-8"), "pcr_calculation.csv", "text/csv")
        except ValueError as e:
            st.error(str(e))

elif page == "Agarose Gel":
    st.subheader("Agarose Gel Preparation Calculator")
    percent = st.number_input("Desired agarose concentration (% w/v)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    volume = st.number_input("Final buffer volume (mL)", min_value=1.0, max_value=2000.0, value=50.0, step=5.0)
    if st.button("Calculate agarose quantity", type="primary"):
        try:
            result = calculate_agarose(percent, volume)
            st.success(f"Weigh **{result['agarose_g']:.3f} g** agarose.")
            st.metric("Agarose required", f"{result['agarose_g']:.3f} g")
            st.write(f"Prepare approximately {volume:.1f} mL of the selected electrophoresis buffer, then dissolve the agarose according to your laboratory protocol.")
            st.info("Formula: agarose (g) = concentration (% w/v) × volume (mL) ÷ 100.")
            st.caption("For example, 1% w/v means 1 g agarose per 100 mL solution.")
        except ValueError as e:
            st.error(str(e))

elif page == "Serial Dilution":
    st.subheader("Serial Dilution Calculator")
    initial = st.number_input("Initial concentration", min_value=0.000001, value=1000.0, format="%.6f")
    unit = st.selectbox("Concentration unit", ["µg/mL", "mg/mL", "ng/µL", "mol/L", "CFU/mL", "Other"])
    factor = st.number_input("Dilution factor at each step (e.g. 10 for a 1:10 dilution)", min_value=1.0, max_value=1000000.0, value=10.0, step=1.0)
    steps = st.number_input("Number of dilution steps", min_value=1, max_value=20, value=5, step=1)
    sample_volume = st.number_input("Sample volume transferred at each step (µL)", min_value=0.1, value=100.0, step=10.0)
    diluent_volume = st.number_input("Diluent volume in each tube (µL)", min_value=0.0, value=900.0, step=10.0)
    if st.button("Calculate dilution series", type="primary"):
        try:
            result = calculate_dilution(initial, factor, steps)
            df = pd.DataFrame(result["rows"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(f"Concentration after {steps} steps: {result['final_concentration']:.6g} {unit}")
            st.info("Formula: Cₙ = C₀ ÷ (dilution factor)ⁿ.")
            if diluent_volume > 0:
                actual_factor = (sample_volume + diluent_volume) / sample_volume
                st.caption(f"Your entered transfer and diluent volumes produce a per-step dilution factor of {actual_factor:.4g}:1. The concentration table above uses the dilution factor entered separately.")
                if abs(actual_factor - factor) > max(0.01, factor * 0.01):
                    st.warning("The entered volumes do not match the selected dilution factor. Adjust them if you intend to prepare that exact dilution.")
            st.download_button("Download dilution series (CSV)", df.to_csv(index=False).encode("utf-8"), "serial_dilution.csv", "text/csv")
        except ValueError as e:
            st.error(str(e))

elif page == "Molarity & Solution Preparation":
    st.subheader("Molarity and Solution Preparation")
    mode = st.radio("Calculation type", ["Mass required to prepare a solution", "Molarity from known mass"], horizontal=True)
    mw = st.number_input("Molecular weight (g/mol)", min_value=0.000001, value=58.44, format="%.6f")
    if mode == "Mass required to prepare a solution":
        molarity = st.number_input("Target molarity (mol/L)", min_value=0.000001, value=0.1, format="%.6f")
        volume_ml = st.number_input("Final solution volume (mL)", min_value=0.1, value=100.0, step=10.0)
        if st.button("Calculate required mass", type="primary"):
            try:
                result = calculate_molarity(mw, molarity, volume_ml)
                st.success(f"Required solute mass: **{result['mass_g']:.4f} g**")
                st.info("Formula: mass (g) = molarity (mol/L) × volume (L) × molecular weight (g/mol).")
            except ValueError as e:
                st.error(str(e))
    else:
        mass = st.number_input("Solute mass (g)", min_value=0.000001, value=0.5844, format="%.6f")
        volume_ml = st.number_input("Final solution volume (mL)", min_value=0.1, value=100.0, step=10.0, key="known_vol")
        if st.button("Calculate molarity", type="primary"):
            try:
                result = calculate_buffer(mass, mw, volume_ml)
                st.success(f"Calculated molarity: **{result['molarity']:.6f} mol/L**")
                st.info("Formula: molarity (mol/L) = mass (g) ÷ [molecular weight (g/mol) × volume (L)].")
            except ValueError as e:
                st.error(str(e))

st.divider()
st.caption("BioLab Companion is an educational calculator. Confirm all outputs independently before laboratory use.")
