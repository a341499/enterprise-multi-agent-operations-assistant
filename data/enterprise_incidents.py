# ---------------------------------------------------
# Enterprise Operational Incident Dataset
# ---------------------------------------------------

# This file contains sample enterprise operational incidents.
# Later these incidents will be:
#
# 1. converted into embeddings
# 2. stored inside ChromaDB
# 3. retrieved using semantic similarity search
#
# This becomes the operational knowledge base
# used by the Retrieval Agent.


# Create list of enterprise operational incidents
enterprise_incidents = [

    {
        "id": 1,

        # Short incident title
        "title": "Database slowdown after deployment",

        # Detailed operational description
        "description":
        "Application experienced severe SQL slowdown "
        "after production deployment due to execution "
        "plan regression and index selection changes."
    },

    {
        "id": 2,

        "title": "High CPU utilization in database cluster",

        "description":
        "Database nodes reported sustained high CPU "
        "usage caused by parallel query execution "
        "and excessive workload concurrency."
    },

    {
        "id": 3,

        "title": "Partition maintenance job failure",

        "description":
        "Nightly partition maintenance workflow failed "
        "during split partition operation because of "
        "metadata lock contention."
    },

    {
        "id": 4,

        "title": "Vector index retrieval inconsistency",

        "description":
        "Semantic retrieval results became unstable "
        "after vector index rebuild causing ranking "
        "differences across repeated executions."
    },

    {
        "id": 5,

        "title": "Application timeout during peak workload",

        "description":
        "Application services experienced intermittent "
        "timeouts during peak workload periods because "
        "of database connection pool exhaustion."
    }

]