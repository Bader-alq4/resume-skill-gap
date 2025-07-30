# test_similarity.py

from backend.core.embedder import get_embeddings
import numpy as np

# Words to compare
skills = ["Unix", "Linux"]

# Get Sentence-BERT embeddings
a, b = get_embeddings(skills)

# Compute cosine similarity
similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Show result
print(f"Semantic similarity between '{skills[0]}' and '{skills[1]}': {similarity:.4f}")
