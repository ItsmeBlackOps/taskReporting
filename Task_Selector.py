from fuzzywuzzy import fuzz

def determine_task_type(subject):
    subject = subject.lower()  # Convert subject to lowercase for case-insensitive checks

    # List of keywords and their corresponding task types
    keyword_mapping = {
        "interview support": "Interview Support",
        "technical support": "Interview Support",
        "assessment": "Assessment Support",
        "mock": "Mock Interview",
        "Screening Interview": "Screening Interview"
    }

    best_match = None
    best_score = 0

    for keyword, task_type in keyword_mapping.items():
        score = fuzz.partial_ratio(subject, keyword.lower())
        if score > best_score:
            best_score = score
            best_match = task_type

    if best_match is not None and best_score >= 80:
        return best_match
    else:
        return "Other"
