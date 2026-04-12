def generate_content(client, messages):
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model=model, contents=messages)
    if response.usage_metadata.prompt_token_count is None or response.usage_metadata.candidates_token_count is None:
        raise RuntimeError("invalid response")
    return response