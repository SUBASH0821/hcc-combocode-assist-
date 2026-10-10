"""HCC ComboCode Assist — illustrative, non-production coding engine.

The rules below are teaching examples, not an official ICD-10-CM codebook.
Never use this demo engine to submit claims or determine payment.
"""

import re
from dataclasses import dataclass, asdict


@dataclass
class Candidate:
    concept: str
    evidence: list[str]
    missing_details: list[str]
    status: str
    explanation: str

    def to_dict(self):
        return asdict(self)


# Demonstration concept rules, NOT official coding rules.
# Each concept is intentionally broader than a billable code.
DEMO_RULES = [
    {
        "concept": "Diabetes with a documented complication",
        "terms": ["diabetes", "diabetic"],
        "complications": [
            "neuropathy",
            "nephropathy",
            "retinopathy",
            "chronic kidney disease",
            "ckd",
            "foot ulcer",
        ],
        "missing": [
            "Diabetes type and applicable code specificity",
            "Provider documentation linking the condition, when required",
            "Current official tabular instructions and code validity",
        ],
    },
    {
        "concept": "Hypertension with a possible related condition",
        "terms": ["hypertension", "high blood pressure"],
        "complications": [
            "heart failure",
            "chronic kidney disease",
            "ckd",
        ],
        "missing": [
            "Exact documented diagnoses and relationship",
            "Applicable ICD-10-CM classification instructions",
            "Specificity required by the candidate code",
        ],
    },
]


NEGATION_PATTERNS = [
    r"\bno\b",
    r"\bdenies\b",
    r"\bwithout\b",
    r"\bnegative for\b",
    r"\babsence of\b",
    r"\bruled out\b",
    r"\bnot present\b",
]


def normalize_note(note: str) -> str:
    """Normalize text without discarding clinically meaningful words."""
    return re.sub(r"\s+", " ", str(note).lower()).strip()


def is_negated(text: str, term: str) -> bool:
    """Conservatively detect negation close to a term.

    This is not a clinically validated NLP model. Long-distance scope,
    historical diagnoses, family history, and complex grammar need review.
    """
    for match in re.finditer(re.escape(term), text):
        prefix = text[max(0, match.start() - 55):match.start()]
        for pattern in NEGATION_PATTERNS:
            neg = re.search(pattern + r"(?:\s+\w+){0,5}\s*$", prefix)
            if neg:
                return True
    return False


def analyze_note(note: str) -> list[Candidate]:
    text = normalize_note(note)
    results = []

    if not text:
        return results

    for rule in DEMO_RULES:
        conditions = rule["terms"] + rule["complications"]

        found = [
            term for term in conditions
            if re.search(r"\b" + re.escape(term) + r"\b", text)
            and not is_negated(text, term)
        ]

        documented_main = [
            term for term in rule["terms"] if term in found
        ]
        documented_complications = [
            term for term in rule["complications"] if term in found
        ]

        if not documented_main:
            continue

        if documented_complications:
            status = "REVIEW COMBINATION CANDIDATE"
            evidence = documented_main + documented_complications
            explanation = (
                "The note contains a main condition and a possible "
                "complication concept. Verify the provider's documentation, "
                "causal relationship when required, code specificity, "
                "tabular instructions, and applicable fiscal-year rules."
            )
        else:
            status = "REVIEW SPECIFICITY"
            evidence = documented_main
            explanation = (
                "A main condition concept was found, but no supported "
                "complication concept was identified by these demo rules. "
                "Do not infer a complication from laboratory values or "
                "other clinical indicators."
            )

        results.append(
            Candidate(
                concept=rule["concept"],
                evidence=evidence,
                missing_details=rule["missing"],
                status=status,
                explanation=explanation,
            )
        )

    if not results:
        results.append(
            Candidate(
                concept="No supported demo concept found",
                evidence=[],
                missing_details=[
                    "Review the complete note",
                    "Check the official Alphabetic Index and Tabular List",
                    "Check applicable HCC mappings separately",
                ],
                status="MANUAL REVIEW REQUIRED",
                explanation=(
                    "The demo engine did not identify a supported concept. "
                    "This does not mean the record has no reportable diagnosis."
                ),
            )
        )

    return results


def analyze_batch(notes):
    """Return one result row per note and candidate."""
    rows = []

    for note_id, note in notes:
        for candidate in analyze_note(note):
            rows.append({
                "note_id": note_id,
                **candidate.to_dict(),
            })

    return rows

