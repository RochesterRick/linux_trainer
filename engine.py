def ask_question(q):
    print("\n" + q["question"])

    # Multiple choice
    if q["type"] == "mc":
        for i, option in enumerate(q["options"], 1):
            print(f"{i}. {option}")

        raw = input("Your answer (1-{}): ".format(len(q["options"]))).strip()

        # Basic input guard
        if not raw.isdigit() or not (1 <= int(raw) <= len(q["options"])):
            user_display = f"(invalid choice: {raw})"
            is_correct = False
        else:
            idx = int(raw) - 1
            user_display = q["options"][idx]
            is_correct = (int(raw) == q["answer"])

        if is_correct:
            print("✅ Correct!")
        else:
            print("❌ Incorrect")
            print(f"Correct answer: {q['answer_text']}")
            print(f"Why: {q['explanation']}")
            print(f"Why this matters: {q['why']}")

        return is_correct, user_display

    # Typing (future use)
    else:
        raw = input("Type your answer: ").strip()
        user_display = raw
        is_correct = (raw == q["answer"])

        if is_correct:
            print("✅ Correct!")
        else:
            print("❌ Incorrect")
            print(f"Correct answer: {q['answer_text']}")
            print(f"Why: {q['explanation']}")
            print(f"Why this matters: {q['why']}")

        return is_correct, user_display

