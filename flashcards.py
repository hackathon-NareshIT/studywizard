from ai_engine import ask_ai


def generate_flashcards(text):
    prompt = f"""
    Create 5 short flashcards from the following content.

    Format:
    Question: ...
    Answer: ...

    Content:
    {text}
    """

    return ask_ai(prompt)