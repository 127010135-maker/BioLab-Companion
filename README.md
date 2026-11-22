# BioLab Companion

An educational Streamlit application containing four biotechnology laboratory calculation tools:
1. PCR master mix volume calculator
2. Agarose gel preparation calculator
3. Serial dilution calculator
4. Molarity / solution preparation calculator

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Run in Google Colab
1. Upload/extract the project folder in Colab.
2. Change directory into `BioLab_Companion`.
3. Install dependencies:
   `!pip install -r requirements.txt`
4. Start Streamlit in the background:
   `!streamlit run app.py &`
5. Use a supported tunnel service to expose port 8501, following that service's current instructions.

## Important
This is an educational calculation aid, not a substitute for laboratory SOPs. Confirm all inputs, units, reagent stock concentrations, and outputs before experimental use.
