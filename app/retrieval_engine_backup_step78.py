# ---------------------------------------------------
# Retrieval Engine
# ---------------------------------------------------

# Import operating system and Python path utilities
# These help Python locate project folders correctly
import os
import sys

# Add project root folder to Python path
# This allows importing from the data folder
project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(project_root)

# ChromaDB vector database
import chromadb

# Enterprise incident knowledge base
from data.enterprise_incidents import enterprise_incidents

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="enterprise_incidents"
)


# ---------------------------------------------------
# Load Enterprise Incidents Into ChromaDB
# ---------------------------------------------------

# Function to load incidents into ChromaDB
def load_incidents_into_chroma():

    # Loop through each incident in the knowledge base
    for incident in enterprise_incidents:

        # Convert incident id into string
        # ChromaDB record ids must be strings
        incident_id = str(incident["id"])

        # Combine title and description into one searchable document
        document = (
            incident["title"]
            + " "
            + incident["description"]
        )

        # Check whether incident already exists
        existing = collection.get(
            ids=[incident_id]
        )

        # Only add if it does not already exist
        if len(existing["ids"]) == 0:

            # Add incident to ChromaDB collection
            collection.add(
                ids=[incident_id],
                documents=[document],
                metadatas=[
                    {
                        "title": incident["title"],
                        "description": incident["description"]
                    }
                ]
            )


# ---------------------------------------------------
# Semantic Retrieval
# ---------------------------------------------------

# Function to retrieve similar incidents
def retrieve_similar_incidents(query, top_k=2):

    # Search ChromaDB for incidents similar to user query
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # Return search results
    return results