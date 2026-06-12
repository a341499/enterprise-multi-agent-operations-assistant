# ---------------------------------------------------
# Workflow State Definition
# ---------------------------------------------------

# This file defines the shared state object
# used by all agents in the workflow.
#
# Instead of passing many parameters between
# agents, we keep everything in one state object.
#
# This is similar to how LangGraph manages state.


# Create workflow state factory function
def create_workflow_state():

    # Return initial workflow state dictionary
    return {

        # Original user incident
        "user_input": "",

        # Incident classification
        "classification": "",

        # Incident analysis output
        "analysis": "",

        # Historical incidents found by retrieval
        "retrieved_incidents": "",

        # AI-generated recommendation
        "recommendation": "",

        # Escalation decision
        "escalation": "",

        # Incident severity
        "severity": "",

        # Notification action
        "notification": "",

        # Executive summary
        "summary": "",

        # Root cause analysis
        "root_cause": "",

        # Workflow execution trace
        "workflow_trace": []
    }