from backend.core.recommender import get_recommendations

# Define a test list of missing skills
missing_skills = ["Pandas", "SQL"]

# Call the recommendation function
recommendations = get_recommendations(missing_skills)

# Print results
print("Missing Skills:", missing_skills)
print("\nRecommendations:")
print("Courses:", recommendations.get("courses", []))
print("Projects:", recommendations.get("projects", []))
print("Certifications:", recommendations.get("certifications", []))
