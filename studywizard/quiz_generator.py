from ai_engine import ask_ai

def generate_quiz(text):
    prompt = f"""
Create 5 multiple-choice questions from the following content.

Rules:
- Each question must have exactly 4 options.
- Format exactly like this:

Q: Question here
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: A

Content:
{text}
"""
    return ask_ai(prompt)
