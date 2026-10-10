
# hcc-combocode-assist
hcc-combocode-assist helpfull for coders
HCC ComboCode Assist

An AI-assisted medical coding review prototype built with Python and Streamlit.

HCC ComboCode Assist helps medical coding students and healthcare informatics developers explore documentation concepts, possible combination-code candidates, coding specificity, and review workflows.

Features
Clinical note concept matching
Combination-code candidate flags
Documentation evidence and missing-specificity checklist
CSV batch review
Downloadable review findings
Conservative handling of some negation patterns
Automated unit tests
Streamlit deployment support
Technology
Python
Streamlit
Pandas
Pytest
Project structure
hcc-combocode-assist/
├── app.py
├── coding_engine.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   ├── demo_notes.csv
│   └── combo_rules_demo.json
└── tests/
    └── test_coding_engine.py

Run locally
Install Python 3.11 or a compatible version.
Clone your repository.
Create and activate a virtual environment.
Install dependencies.
Launch Streamlit.
git clone https://github.com/YOUR_USERNAME/hcc-combocode-assist.git
cd hcc-combocode-assist

python -m venv .venv


Activate the environment:

Windows

.venv\Scripts\activate


macOS/Linux

source .venv/bin/activate


Install and run:

pip install -r requirements.txt
streamlit run app.py


Open the local URL displayed in your terminal.

Run tests
pytest -q

Official coding references
CDC ICD-10-CM resources: https://www.cdc.gov/nchs/icd/icd-10-cm/
CMS ICD-10 files and coding guidelines: https://www.cms.gov/medicare/coding-billing/icd-10-codes
CMS HCC model mappings and software: https://www.cms.gov/medicare/payment/medicare-advantage-rates-statistics/risk-adjustment

Always verify the encounter date, applicable fiscal-year code set, tabular instructions, and relevant risk-adjustment model.

Limitations

This repository is an educational prototype, not a validated medical coding product. Its illustrative rules do not contain the complete ICD-10-CM classification or CMS-HCC mappings. It does not assign definitive billing codes, calculate valid risk scores, or guarantee accuracy.

Do not use its outputs for claim submission, payment decisions, or clinical decision-making. Use synthetic data only until appropriate privacy, security, validation, and governance requirements are satisfied.

Roadmap
Official, versioned ICD-10-CM terminology import
Official CMS-HCC mapping integration
Clinical NLP with negation and temporality handling
Documentation evidence highlighting
Reviewer audit trail
Expert-adjudicated evaluation dataset
Precision, recall, and exact-code accuracy reporting
License

MIT License. See LICENSE for terms.

Disclaimer

This project is for education and research. It is not affiliated with or endorsed by CMS, CDC, or any official coding authority.
