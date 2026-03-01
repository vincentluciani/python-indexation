import ollama

def summarize_with_ai(model, list_to_summarize,system_msg, list_prefix):
    """Helper to talk to your local Ollama instance."""

    formatted_input = "\n".join([f"- {s}" for s in list_to_summarize])

    # Construct the message structure
    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': (
                    f"{system_msg}"
                )
            },
            {
                'role': 'user',
                'content': f"{list_prefix}:\n{formatted_input}"
            }
        ],
        options={
            'temperature': 0  # We set this to 0 for consistent, logical grouping
        }
    )
    answer = response.get('message', {}).get('content', '')
    return answer

    