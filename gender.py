from fuzzywuzzy import fuzz

def determine_gender(gender):
    gender = gender.lower()  # Convert gender to lowercase for case-insensitive checks

    # List of keywords and their corresponding gender labels
    gender_mapping = {
        "male": "Male",
        "female": "Female",
        "other": "Other"
    }

    best_match = None
    best_score = 0

    for keyword, gender_label in gender_mapping.items():
        score = fuzz.partial_ratio(gender, keyword.lower())
        if score > best_score:
            best_score = score
            best_match = gender_label

    if best_match is not None and best_score >= 80:  # Adjust the threshold as needed
        return best_match
    else:
        return "Other"  # Return "Other" when no match is found

# Example usage:
gender = data.get("Gender", "").lower()  # Get the gender field from your data and convert to lowercase
determined_gender = determine_gender(gender)
print(f"Determined Gender: {determined_gender}")
