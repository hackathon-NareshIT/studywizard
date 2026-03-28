import streamlit as st
from summarizer import summarize
from quiz_generator import generate_quiz
from flashcards import generate_flashcards
from pdf_reader import read_pdf
from auth import login, register
from database import create_table


st.set_page_config(page_title="StudyWizard", layout="centered")
create_table()

st.title("📚 StudyWizard")

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []


# Login/Register screen
if not st.session_state.logged_in:
    st.subheader("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", use_container_width=True):
            if username.strip() == "" or password.strip() == "":
                st.warning("Please enter username and password")
            elif login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        if st.button("Register", use_container_width=True):
            if username.strip() == "" or password.strip() == "":
                st.warning("Please enter username and password")
            else:
                success = register(username, password)

                if success:
                    st.success("Account created. Please login.")
                else:
                    st.error("Username already exists")


# Main app after login
else:
    st.subheader(f"Welcome, {st.session_state.username} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.summary = ""
        st.session_state.quiz = []
        st.session_state.flashcards = []
        st.rerun()

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        uploaded_file.seek(0)
        text = read_pdf(uploaded_file)

        if text.startswith("Error") or text.startswith("No readable"):
            st.error(text)

        else:
            st.success("PDF loaded successfully")

            col1, col2, col3 = st.columns(3)

            # Summary
            with col1:
                if st.button("📝 Summarize"):
                    with st.spinner("Generating summary..."):
                        st.session_state.summary = summarize(text)

            # Quiz
            with col2:
                if st.button("❓ Generate Quiz"):
                    with st.spinner("Generating quiz..."):
                        raw_quiz = generate_quiz(text)
                        parsed_quiz = []

                        try:
                            for block in raw_quiz.split("Q:")[1:]:
                                lines = [
                                    line.strip()
                                    for line in block.split("\n")
                                    if line.strip()
                                ]

                                if len(lines) < 6:
                                    continue

                                question = lines[0]

                                options = [
                                    line
                                    for line in lines
                                    if line.startswith(("A)", "B)", "C)", "D)"))
                                ]

                                answer = ""
                                for line in lines:
                                    if line.startswith("Answer:"):
                                        answer = line.replace("Answer:", "").strip()

                                if len(options) == 4 and answer:
                                    parsed_quiz.append(
                                        {
                                            "question": question,
                                            "options": options,
                                            "answer": answer,
                                        }
                                    )

                        except Exception as e:
                            st.error(f"Quiz parsing error: {e}")

                        st.session_state.quiz = parsed_quiz

                        if not parsed_quiz:
                            st.warning("Could not generate quiz correctly. Try another PDF.")

            # Flashcards
            with col3:
                if st.button("🧠 Flashcards"):
                    with st.spinner("Generating flashcards..."):
                        flashcards_text = generate_flashcards(text)

                        st.session_state.flashcards = [
                            card.strip()
                            for card in flashcards_text.split("\n\n")
                            if card.strip()
                        ]

            # Show summary
            if st.session_state.summary:
                st.markdown("---")
                st.subheader("📌 Summary")
                st.write(st.session_state.summary)

            # Show flashcards
            if st.session_state.flashcards:
                st.markdown("---")
                st.subheader("📚 Flashcards")

                for i, card in enumerate(st.session_state.flashcards, start=1):
                    with st.expander(f"Card {i}"):
                        st.write(card)

            # Show quiz
            if st.session_state.quiz:
                st.markdown("---")
                st.subheader("🧠 Quiz")

                answers = []

                for i, q in enumerate(st.session_state.quiz):
                    st.write(f"Q{i + 1}. {q['question']}")

                    selected = st.radio(
                        f"Choose answer for question {i + 1}",
                        q["options"],
                        key=f"quiz_{i}"
                    )

                    answers.append(selected)

                if st.button("Submit Quiz"):
                    score = 0

                    for i, q in enumerate(st.session_state.quiz):
                        if answers[i].startswith(q["answer"]):
                            score += 1

                    st.success(
                        f"Your Score: {score}/{len(st.session_state.quiz)}"
                    )
