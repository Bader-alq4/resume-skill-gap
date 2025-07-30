from backend.core.recommender import get_recommendations

'''
Generate learning recommendations based on missing skills.

'''

def test_get_recommendations_returns_expected_structure():
    # Define a sample list of missing skills
    missing_skills = ["Pandas", "SQL"]

    # Call the function
    recommendations = get_recommendations(missing_skills)

    # Basic type checks for CI
    assert isinstance(recommendations, dict), "Expected a dictionary of recommendations"
    
    # The dictionary should have these keys
    for key in ["courses", "projects", "certifications"]:
        assert key in recommendations, f"Missing expected key: {key}"
        assert isinstance(recommendations[key], list), f"{key} should be a list"

    # At least one recommendation should exist for CI sanity check
    total_recs = sum(len(v) for v in recommendations.values())
    assert total_recs > 0, "Expected at least one recommendation"