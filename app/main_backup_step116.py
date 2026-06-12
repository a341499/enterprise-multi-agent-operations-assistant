# Import Streamlit library
# Streamlit is used to build browser-based UI
import streamlit as st

# Import datetime module
# Used for workflow timestamps
from datetime import datetime

# Import retrieval functions
# These allow the Retrieval Agent to use ChromaDB semantic search
from retrieval_engine import load_incidents_into_chroma, retrieve_similar_incidents

# Import AI recommendation engine
# Generates recommendations using Ollama + Llama 3.2
from recommendation_engine import generate_recommendation

# Import workflow state factory
# Creates shared workflow state object
from workflow_state import create_workflow_state


# ---------------------------------------------------
# Initialize ChromaDB
# ---------------------------------------------------

# Load enterprise incidents into ChromaDB
# retrieval_engine.py should handle duplicate checks safely
load_incidents_into_chroma()


# ---------------------------------------------------
# Utility Function
# ---------------------------------------------------

# Define helper function to get current time
def current_time():

    # Return formatted current time
    # Example: 19:30:45
    return datetime.now().strftime("%H:%M:%S")

# ---------------------------------------------------
# Incident Classification Agent
# ---------------------------------------------------

# Classifies operational incidents
def classification_agent(state):

    # Read user incident
    user_input = state["user_input"].lower()

    # Default classification
    classification = "General Operational Issue"

    # Simple rule-based classification

    if "performance" in user_input:
        classification = "Performance Issue"

    elif "cpu" in user_input:
        classification = "Performance Issue"

    elif "slow" in user_input:
        classification = "Performance Issue"

    elif "deployment" in user_input:
        classification = "Deployment Issue"

    elif "release" in user_input:
        classification = "Deployment Issue"

    elif "unavailable" in user_input:
        classification = "Availability Issue"

    elif "down" in user_input:
        classification = "Availability Issue"

    elif "security" in user_input:
        classification = "Security Issue"

    elif "authentication" in user_input:
        classification = "Security Issue"

    # Save classification into workflow state
    state["classification"] = classification

    # Add workflow trace
    state["workflow_trace"].append(
        f"[{current_time()}] Classification Agent completed"
    )

    return state

# ---------------------------------------------------
# Escalation Agent
# ---------------------------------------------------

# Determines escalation path
def escalation_agent(state):

    # Read classification from workflow state
    classification = state["classification"]

    # Default escalation decision
    escalation = "Monitor"

    # Escalation rules

    if classification == "Performance Issue":
        escalation = "Escalate to Team Lead"

    elif classification == "Availability Issue":
        escalation = "Escalate to Incident Commander"

    elif classification == "Security Issue":
        escalation = "Escalate to Incident Commander"

    # Store escalation decision
    state["escalation"] = escalation

    # Add workflow trace
    state["workflow_trace"].append(
        f"[{current_time()}] Escalation Agent completed"
    )

    return state

# ---------------------------------------------------
# Severity Agent
# ---------------------------------------------------

# Determines incident severity
def severity_agent(state):

    # Read incident classification
    classification = state["classification"]

    # Default severity
    severity = "Medium"

    # Severity rules

    if classification == "Performance Issue":
        severity = "High"

    elif classification == "Availability Issue":
        severity = "Critical"

    elif classification == "Security Issue":
        severity = "Critical"

    # Store severity in workflow state
    state["severity"] = severity

    # Add workflow trace entry
    state["workflow_trace"].append(
        f"[{current_time()}] Severity Agent completed"
    )

    # Return updated workflow state
    return state

# ---------------------------------------------------
# Notification Agent
# ---------------------------------------------------

# Determines notification action
def notification_agent(state):

    # Read severity from workflow state
    severity = state["severity"]

    # Default notification action
    notification = "Monitor Only"

    # Notification rules

    if severity == "Critical":
        notification = "Notify Incident Commander"

    elif severity == "High":
        notification = "Notify Team Lead"

    # Store notification action
    state["notification"] = notification

    # Add workflow trace entry
    state["workflow_trace"].append(
        f"[{current_time()}] Notification Agent completed"
    )

    # Return updated workflow state
    return state

# ---------------------------------------------------
# Summary Agent
# ---------------------------------------------------

# Creates executive summary
def summary_agent(state):

    # Read values from workflow state
    classification = state["classification"]
    severity = state["severity"]
    escalation = state["escalation"]
    notification = state["notification"]

    # Create executive summary
    summary = (
        f"{classification} detected. "
        f"Severity: {severity}. "
        f"Escalation: {escalation}. "
        f"Notification: {notification}."
    )

    # Store summary in workflow state
    state["summary"] = summary

    # Add workflow trace entry
    state["workflow_trace"].append(
        f"[{current_time()}] Summary Agent completed"
    )

    # Return updated workflow state
    return state

# ---------------------------------------------------
# RCA Agent
# ---------------------------------------------------

# Creates root cause analysis
def rca_agent(state):

    # Read values from workflow state
    classification = state["classification"]
    severity = state["severity"]

    # Default root cause
    root_cause = (
        "Likely Root Cause: Further investigation required."
    )

    # RCA rules

    if classification == "Performance Issue":
        root_cause = (
            "Likely Root Cause: Configuration change or "
            "query execution plan regression after release."
        )

    elif classification == "Availability Issue":
        root_cause = (
            "Likely Root Cause: Service outage or "
            "resource exhaustion."
        )

    elif classification == "Security Issue":
        root_cause = (
            "Likely Root Cause: Unauthorized access attempt "
            "or security policy violation."
        )

    # Store RCA in workflow state
    state["root_cause"] = root_cause

    # Add workflow trace entry
    state["workflow_trace"].append(
        f"[{current_time()}] RCA Agent completed"
    )

    # Return updated workflow state
    return state
# ---------------------------------------------------
# Incident Analysis Agent
# ---------------------------------------------------

# Define Incident Analysis Agent
# Accepts shared workflow state as input
def incident_analysis_agent(state):

    # Read original user incident from workflow state
    user_input = state["user_input"]

    # Read classification from workflow state
    classification = state["classification"]

    # Read severity from workflow state
    severity = state["severity"]

    # Read escalation decision from workflow state
    escalation = state["escalation"]

    # Read notification action from workflow state
    notification = state["notification"]

    # Read executive summary from workflow state
    summary = state["summary"]

    # Read RCA from workflow state
    root_cause = state["root_cause"]

    # Create workflow trace message
    trace = f"[{current_time()}] Incident Analysis Agent completed"

    # Create formatted operational analysis result
    result = f"""
### Incident Analysis Agent

**Detected operational issue:**
{user_input}

**Classification:**
{classification}

**Escalation:**
{escalation}

**Severity:**
{severity}

**Notification:**
{notification}

**Executive Summary:**
{summary}

**Root Cause Analysis:**
{root_cause}

**Initial assessment:**
Further investigation required.
"""

    # Store analysis result inside shared workflow state
    state["analysis"] = result

    # Add trace message into shared workflow state
    state["workflow_trace"].append(trace)

    # Return updated workflow state
    return state


# ---------------------------------------------------
# Retrieval Agent
# ---------------------------------------------------

# Define Retrieval Agent
# Uses shared workflow state
def retrieval_agent(state):

    # Read original user incident from workflow state
    user_input = state["user_input"]

    # Create workflow trace message
    trace = f"[{current_time()}] Retrieval Agent completed"

    # Search for similar incidents using ChromaDB
    results = retrieve_similar_incidents(user_input)

    # Extract retrieved incident titles
    retrieved_titles = []

    # Loop through returned metadata records
    for metadata in results["metadatas"][0]:

        # Get incident title
        retrieved_titles.append(metadata["title"])

    # Convert list of titles into formatted bullet text
    incident_text = "\n".join(
        [f"- {title}" for title in retrieved_titles]
    )

    # Create retrieval response
    result = f"""
### Retrieval Agent

**Search target:**  
{user_input}

**Similar historical incidents found:**

{incident_text}
"""

    # Store retrieval response in workflow state
    state["retrieved_incidents"] = result

    # Add trace message into workflow state
    state["workflow_trace"].append(trace)

    # Return updated workflow state
    return state


# ---------------------------------------------------
# Recommendation Agent
# ---------------------------------------------------

# Define Recommendation Agent
# Uses shared workflow state and Ollama LLM reasoning
def recommendation_agent(state):

    # Read original user incident from workflow state
    user_input = state["user_input"]

    # Read retrieved incidents from workflow state
    retrieved_incidents = state["retrieved_incidents"]

    # Create workflow trace message
    trace = f"[{current_time()}] Recommendation Agent completed"

    # Generate AI recommendation using Ollama
    ai_response = generate_recommendation(
        user_input,
        retrieved_incidents
    )

    # Create formatted recommendation response
    result = f"""
### Recommendation Agent

**AI Generated Recommendation:**

{ai_response}
"""

    # Store AI recommendation inside workflow state
    state["recommendation"] = result

    # Add trace message into workflow state
    state["workflow_trace"].append(trace)

    # Return updated workflow state
    return state


# ---------------------------------------------------
# Orchestrator Agent
# ---------------------------------------------------

# Define Orchestrator Agent
# This coordinates all other agents using shared workflow state
def orchestrator(user_input):

    # Create shared workflow state
    state = create_workflow_state()

    # Store original user incident inside workflow state
    state["user_input"] = user_input

    # Add orchestrator start message into workflow trace
    state["workflow_trace"].append(
        f"[{current_time()}] Orchestrator started"
    )

    # Execute Classification Agent
    # Agent determines incident category
    state = classification_agent(state)

    # Execute Escalation Agent
    # Agent determines escalation path
    state = escalation_agent(state)

    # Execute Severity Agent
    # Agent determines incident severity
    state = severity_agent(state)

    # Execute Notification Agent
    # Agent determines notification action
    state = notification_agent(state)

    # Execute RCA Agent
    # Agent determines likely root cause
    state = rca_agent(state)

    # Execute Summary Agent
    # Agent creates executive summary
    state = summary_agent(state)

    # Execute Incident Analysis Agent
    # Agent reads and updates shared workflow state
    state = incident_analysis_agent(state)

    # Execute Retrieval Agent
    # Agent reads and updates shared workflow state
    state = retrieval_agent(state)

    # Execute Recommendation Agent
    # Agent reads and updates shared workflow state
    state = recommendation_agent(state)

    # Add final orchestration completion message
    state["workflow_trace"].append(
        f"[{current_time()}] Orchestrator completed final synthesis"
    )

    # Combine all agent responses
    # Read results from shared workflow state
    final_response = (
        state["analysis"]
        + "\n\n---\n\n"
        + state["retrieved_incidents"]
        + "\n\n---\n\n"
        + state["recommendation"]
    )

    # Return workflow trace from shared workflow state
    # and the final combined response
    return state["workflow_trace"], final_response


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------

# Create browser page title
st.title("Enterprise Multi-Agent Operations Assistant")

# Add small descriptive caption
st.caption(
    "Multi-agent operational workflow with orchestration trace"
)

# Create text input area
# User enters operational incident here
user_input = st.text_area(
    "Enter operational incident or issue:"
)

# Create workflow execution button
if st.button("Run Multi-Agent Workflow"):

    # Validate empty input
    if not user_input.strip():

        # Display warning if input is empty
        st.warning(
            "Please enter an operational incident before running the workflow."
        )

    else:

        # Execute orchestrator workflow
        # Receives workflow trace and final response
        trace, response = orchestrator(user_input)

        # Display execution trace section
        st.subheader("Workflow Execution Trace")

        # Loop through workflow trace items
        for item in trace:

            # Display each workflow event
            st.info(item)

        # Display final coordinated response section
        st.subheader("Coordinated Multi-Agent Response")

        # Render formatted markdown response
        st.markdown(response)