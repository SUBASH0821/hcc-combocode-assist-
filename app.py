import io
import json

import pandas as pd
import streamlit as st

from coding_engine import analyze_note, analyze_batch

st.set_page_config(
    page_title="HCC ComboCode Assist",
    page_icon="🩺",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.8rem; max-width: 1250px;}
    .hero {
        padding: 1.4rem;
        border-radius: 14px;
        background: linear-gradient(120deg, #102a43, #176b70);
        color: white;
        margin-bottom: 1.2rem;
    }
    .hero h1 {color: white; margin-bottom: .3rem;}
    .hero p {color: #e2f5f4; margin-bottom: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>HCC ComboCode Assist</h1>
      <p>Clinical documentation review · Combination-code candidates ·
      HCC coding workflow</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "EDUCATIONAL PROTOTYPE — Not a validated coding system. "
    "Never enter identifiable patient information. Do not use demo rules "
    "to select final billing codes, determine HCC eligibility, or submit claims."
)

with st.sidebar:
    st.header("Review settings")
    fiscal_year = st.selectbox(
        "Encounter fiscal year",
        ["2027", "2026", "2025"],
        index=0,
    )
    st.caption(
        "Selecting a year does not load that year's official code set. "
        "Verify code validity and HCC mappings against official files."
    )
    st.divider()
    st.markdown("### Workflow")
    st.markdown(
        "1. Enter a synthetic note\n"
        "2. Review evidence and warnings\n"
        "3. Confirm coding against official sources\n"
        "4. Export review findings"
    )

tab_single, tab_batch, tab_about = st.tabs(
    ["📝 Note review", "📂 Batch review", "ℹ️ Method and limitations"]
)

with tab_single:
    st.subheader("Clinical documentation review")
    st.write(
        "Enter a fictional clinical note. The engine searches a limited set "
        "of concepts and returns candidates for human review."
    )

    demo_note = (
        "Assessment: Type 2 diabetes mellitus with documented diabetic "
        "neuropathy. Hypertension is also documented. Provider assessment "
        "and applicable coding instructions require review."
    )

    note = st.text_area(
        "Clinical note",
        value=demo_note,
        height=170,
        help="Use fictional or properly de-identified text only.",
    )

    if st.button("Analyze documentation", type="primary"):
        candidates = analyze_note(note)

        st.subheader("Review findings")
        st.caption(
            f"Selected encounter fiscal year: {fiscal_year}. "
            "No official codebook is connected in this prototype."
        )

        for i, item in enumerate(candidates, start=1):
            with st.container(border=True):
                st.markdown(f"**{i}. {item.concept}**")
                st.info(item.status)

                st.markdown("**Evidence terms detected**")
                if item.evidence:
                    st.write(", ".join(item.evidence))
                else:
                    st.write("No demo evidence terms detected.")

                st.markdown("**Why review is needed**")
                st.write(item.explanation)

                st.markdown("**Validation checklist**")
                for detail in item.missing_details:
                    st.checkbox(
                        detail,
                        key=f"single_{i}_{detail}",
                    )

                decision = st.radio(
                    "Reviewer disposition",
                    [
                        "Pending review",
                        "Supported after official verification",
                        "Not supported",
                        "Provider clarification needed",
                    ],
                    key=f"decision_{i}",
                )
                st.caption(f"Reviewer disposition: {decision}")

        st.caption(
            "A candidate is not a final diagnosis code. The checkboxes "
            "record local UI review only; this prototype does not maintain "
            "an audit database."
        )

with tab_batch:
    st.subheader("Batch note review")
    st.write(
        "Upload a CSV containing `note_id` and `note` columns. "
        "Use synthetic notes only."
    )

    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        key="batch_upload",
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded, dtype=str).fillna("")
            required = {"note_id", "note"}

            if not required.issubset(df.columns):
                st.error("CSV must contain columns named note_id and note.")
            elif len(df) > 500:
                st.error("Demo limit: 500 rows per upload.")
            else:
                st.dataframe(df.head(20), use_container_width=True)

                if st.button("Analyze uploaded notes", type="primary"):
                    pairs = list(zip(df["note_id"], df["note"]))
                    results = analyze_batch(pairs)
                    result_df = pd.DataFrame(results)

                    st.session_state["batch_results"] = result_df
                    st.success(
                        f"Review generated for {len(df)} notes. "
                        "These are candidates, not final codes."
                    )

        except Exception as exc:
            st.error(f"Could not read the CSV: {exc}")

    if "batch_results" in st.session_state:
        result_df = st.session_state["batch_results"]
        st.subheader("Batch review findings")
        st.dataframe(result_df, use_container_width=True)

        csv_data = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download review results CSV",
            data=csv_data,
            file_name="hcc_combo_review_results.csv",
            mime="text/csv",
        )

with tab_about:
    st.subheader("What this version can and cannot do")

    st.markdown(
        """
        **Can do**
        - Search for a small number of illustrative diagnosis concepts.
        - Display matched text concepts and review prompts.
        - Process a synthetic-note CSV.
        - Export candidate review findings.

        **Cannot do**
        - Guarantee 100% coding accuracy.
        - Reliably interpret all clinical negation, temporality, or causality.
        - Determine a final ICD-10-CM code or billable specificity.
        - Validate inclusion, exclusion, sequencing, or "code first" rules.
        - Calculate a valid CMS-HCC category or risk score.
        - Replace official coding guidance or a qualified coder.

        **Production roadmap**
        1. Import licensed/authorized official ICD-10-CM files by fiscal year.
        2. Add a validated terminology and clinical NLP pipeline.
        3. Integrate official CMS-HCC mappings and model software for the
           correct payment year.
        4. Build an auditable human-review workflow.
        5. Evaluate precision, recall, exact-code accuracy, and false
           positive rates against expert-adjudicated records.
        """
    )

    st.markdown("### Official reference sources")
    st.markdown(
        "- [CDC ICD-10-CM resources](https://www.cdc.gov/nchs/icd/icd-10-cm/)\n"
        "- [CMS ICD-10 files and guidelines](https://www.cms.gov/medicare/coding-billing/icd-10-codes)\n"
        "- [CMS HCC model mappings](https://www.cms.gov/medicare/payment/medicare-advantage-rates-statistics/risk-adjustment)"
    )

st.divider()
st.caption(
    "HCC ComboCode Assist · Demonstration only · "
    "Human verification is mandatory."
)

