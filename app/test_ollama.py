# ---------------------------------------------------
# Ollama Connectivity Test
# ---------------------------------------------------

# Import Ollama library
# This allows Python to talk to the local LLM
import ollama


# Display start message
print("Testing Ollama connection...")


# Send a simple prompt to Llama 3.2
response = ollama.chat(

    model="llama3.2:1b",

    messages=[
        {
            "role": "user",
            "content": "In one sentence, explain what a database index is."
        }
    ]
)

# Display AI response
print("\nLLM Response:\n")

print(response["message"]["content"])