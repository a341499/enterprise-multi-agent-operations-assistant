# Import retrieval functions from retrieval_engine
# These functions load enterprise incidents and search similar incidents
from retrieval_engine import load_incidents_into_chroma, retrieve_similar_incidents


# Load enterprise incident records into ChromaDB
load_incidents_into_chroma()


# Create a test query
# This simulates a user describing an operational issue
query = "Database performance issue after release"


# Search for similar historical incidents
results = retrieve_similar_incidents(query)


# Print the search query
print("Search Query:")
print(query)


# Print the retrieval results
print("\nSimilar Incidents Found:")
print(results)