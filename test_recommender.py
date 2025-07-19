from backend.core.recommender import recommend_learning_path

missing = ["Docker", "Kubernetes", "CI/CD"]

result = recommend_learning_path(missing)

import json
print(json.dumps(result, indent=2))
