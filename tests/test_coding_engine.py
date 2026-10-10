from coding_engine import analyze_note


def test_diabetes_and_documented_neuropathy_flagged():
    results = analyze_note(
        "Type 2 diabetes mellitus with documented diabetic neuropathy."
    )
    assert any(
        "Diabetes" in result.concept
        and result.status == "REVIEW COMBINATION CANDIDATE"
        for result in results
    )


def test_diabetes_without_complication_does_not_infer_one():
    results = analyze_note("Diabetes mellitus is documented.")
    diabetes = next(
        result for result in results
        if "Diabetes" in result.concept
    )
    assert diabetes.status == "REVIEW SPECIFICITY"


def test_negated_neuropathy_is_not_positive_evidence():
    results = analyze_note(
        "Diabetes is documented. No neuropathy is present."
    )
    diabetes = next(
        result for result in results
        if "Diabetes" in result.concept
    )
    assert diabetes.status == "REVIEW SPECIFICITY"


def test_empty_note_returns_manual_review():
    results = analyze_note("")
    assert results == []


def test_unknown_note_does_not_claim_no_diagnosis():
    results = analyze_note("Patient seen for a routine visit.")
    assert results[0].status == "MANUAL REVIEW REQUIRED"
    assert "does not mean" in results[0].explanation
    
