# ---------------------------------------------------
# AI Recommendation Engine
# ---------------------------------------------------

# Import Ollama library
# Ollama allows local LLM inference
import ollama


# ---------------------------------------------------
# Generate AI Recommendations
# ---------------------------------------------------

# Define recommendation function
# Accepts:
# 1. user incident
# 2. retrieved historical incidents
def generate_recommendation(
    user_input,
    retrieved_incidents
):

    # Create prompt for LLM
    prompt = f"""
You are an experienced enterprise operations engineer.

Operational Issue:
{user_input}

Historical Incidents:
{retrieved_incidents}

Provide:

1. Likely root cause
2. Investigation steps
3. Recommended actions
4. Risk assessment

Keep the response concise and practical.
"""

    # Send prompt to Ollama
    response = ollama.chat(

        # Local LLM model
        model="llama3.2:1b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Return generated response text
    return response["message"]["content"]