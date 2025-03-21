import pandas as pd
import numpy as np

# ---------------------------
# STEP 1: Read and prepare the data
# ---------------------------
# For this example, assume CSV files have these columns:
# startups.csv: startup_id, name, industry, business_model, functions (comma-separated)
# mentors.csv: mentor_id, name, industry_preferences (comma-separated), business_models (comma-separated),
#              areas_of_expertise (comma-separated), mentor_preferences (e.g., preferred startup stage, or other custom info)

startups_df = pd.read_csv("startups.csv")
mentors_df = pd.read_csv("mentors.csv")

# Convert comma-separated string fields into lists for easier comparison
def str_to_list(x):
    if pd.isna(x):
        return []
    return [item.strip().lower() for item in x.split(",")]

startups_df['functions'] = startups_df['functions'].apply(str_to_list)
startups_df['industry'] = startups_df['industry'].str.lower()
startups_df['business_model'] = startups_df['business_model'].str.lower()

mentors_df['industry_preferences'] = mentors_df['industry_preferences'].apply(str_to_list)
mentors_df['business_models'] = mentors_df['business_models'].apply(str_to_list)
mentors_df['areas_of_expertise'] = mentors_df['areas_of_expertise'].apply(str_to_list)
mentors_df['mentor_preferences'] = mentors_df['mentor_preferences'].apply(str_to_list)

# ---------------------------
# STEP 2: Define compatibility score calculation
# ---------------------------
def calculate_score(startup, mentor):
    """
    Calculate compatibility score between a startup and a mentor.

    Scoring logic (weights can be adjusted):
    - Industry match: +30 points if startup's industry is in mentor's industry preferences.
    - Business model match: +20 points if startup's business model is in mentor's business models.
    - Function/Expertise match: +10 points for each matching element between startup functions and mentor's areas of expertise.
    - Mentor preferences: +5 points for each matching preference (if available criteria match between startup and mentor preference).
      (For simplicity, here we assume that if startup's industry matches one of mentor's preferences, it gets an extra 5 points.)
    """
    score = 0

    # Industry match
    if startup['industry'] in mentor['industry_preferences']:
        score += 30

    # Business model match
    if startup['business_model'] in mentor['business_models']:
        score += 20

    # Function/Expertise match (count common elements)
    function_matches = set(startup['functions']).intersection(set(mentor['areas_of_expertise']))
    score += 10 * len(function_matches)

    # Mentor preference based match (example: if startup industry appears in mentor preferences)
    if startup['industry'] in mentor['mentor_preferences']:
        score += 5

    return score

# ---------------------------
# STEP 3: Calculate scores for all startup-mentor pairs
# ---------------------------
matches = []  # List to hold allocation results

# For each startup, compute score with every mentor
for idx, startup in startups_df.iterrows():
    scores = []
    for jdx, mentor in mentors_df.iterrows():
        score = calculate_score(startup, mentor)
        scores.append({
            "startup_id": startup['startup_id'],
            "startup_name": startup['name'],
            "mentor_id": mentor['mentor_id'],
            "mentor_name": mentor['name'],
            "score": score
        })
    # Convert scores to DataFrame and sort descending by score
    scores_df = pd.DataFrame(scores).sort_values(by='score', ascending=False)
    # Select top two mentors (or fewer if not available)
    top_mentors = scores_df.head(2)
    matches.append(top_mentors)

# Combine all match results into a single DataFrame
allocation_df = pd.concat(matches, ignore_index=True)

# ---------------------------
# STEP 4: Save the matching results to a CSV file
# ---------------------------
allocation_df.to_csv("mentor_allocation_results.csv", index=False)

print("Mentor matching and allocation completed. Results saved to 'mentor_allocation_results.csv'.")