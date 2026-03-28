from ai_engine import ask_ai

def summarize(text):
    prompt = f"""
    Summarize the following PDF content into short, easy-to-read bullet points:

    {text}
    """

    return ask_ai(prompt)
