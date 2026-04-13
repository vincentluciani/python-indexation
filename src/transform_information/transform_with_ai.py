"""Helper utilities for interacting with a local Ollama instance."""

import ollama


def summarize_with_ai(model, list_to_summarize, system_msg, list_prefix):
    """Generate a merged summary from a list of suggestions."""
    client = ollama.Client(host="http://localhost:11434")
    formatted_input = "\n".join([f"- {s}" for s in list_to_summarize])

    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_msg,
            },
            {
                "role": "user",
                "content": f"{list_prefix}:\n{formatted_input}",
            },
        ],
        options={"temperature": 0},
    )
    answer = response.get("message", {}).get("content", "")
    return answer
