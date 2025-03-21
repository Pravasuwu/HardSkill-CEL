import pandas as pd
import numpy as np

startups_df = pd.read_csv("startups.csv")
mentors_df = pd.read_csv("mentors.csv")

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

def calculate_score(startup, mentor):
    score = 0
    if startup['industry'] in mentor['industry_preferences']:
        score += 30
    if startup['business_model'] in mentor['business_models']:
        score += 20
    function_matches = set(startup['functions']).intersection(set(mentor['areas_of_expertise']))
    score += 10 * len(function_matches)
    if startup['industry'] in mentor['mentor_preferences']:
        score += 5
    return score

matches = []

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

    scores_df = pd.DataFrame(scores).sort_values(by='score', ascending=False)
    top_mentors = scores_df.head(2)
    matches.append(top_mentors)

allocation_df = pd.concat(matches, ignore_index=True)
allocation_df.to_csv("mentor_allocation_results.csv", index=False)

print("Mentor matching and allocation completed. Results saved to 'mentor_allocation_results.csv'.")
