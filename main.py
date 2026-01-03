import random
from engine import ask_question
from progress import (
    load_level_progress, save_level_progress, record_answer,
    remaining_questions, reset_all_progress
)

from questions_level1 import level1_questions
from questions_level2 import level2_questions
from questions_level3 import level3_questions
from questions_level4 import level4_questions


def main_menu():
    while True:
        # Recompute every time so it updates after play/reset
        r1 = remaining_questions("level1", len(level1_questions))
        r2 = remaining_questions("level2", len(level2_questions))
        r3 = remaining_questions("level3", len(level3_questions))
        r4 = remaining_questions("level4", len(level4_questions))

        print(f"1. Level 1 – Linux Foundations ({r1} of {len(level1_questions)} remaining)")
        print(f"2. Level 2 – Daily Linux Use ({r2} of {len(level2_questions)} remaining)")
        print(f"3. Level 3 – Command Confidence - Typing ({r3} of {len(level3_questions)} remaining)")
        print(f"4. Level 4 – Troubleshooting & Thinking ({r4} of {len(level4_questions)} remaining)")
        print("5. Reset Progress")
        print("6. Exit")

        choice = input("Select a level: ").strip()

        if choice == "1":
            run_level("level1", level1_questions, count=10)
        elif choice == "2":
            run_level("level2", level2_questions, count=10)
        elif choice == "3":
            run_level("level3", level3_questions, count=10)
        elif choice == "4":
            run_level("level4", level4_questions, count=10)
        elif choice == "5":
            confirm = input("This will erase ALL progress. Type YES to confirm: ").strip()
            if confirm == "YES":
                reset_all_progress()
                print("✅ Progress reset.")
            else:
                print("Cancelled.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, 4, 5, or 6.")


def run_level(level_key, questions, count=10):
    prog = load_level_progress(level_key)

    all_indexes = set(range(len(questions)))
    unasked = all_indexes - prog["asked_seen"]
    wrong_pool = set(prog["asked_wrong"])

    # Only these are "remaining"
    remaining_pool = list(unasked | wrong_pool)

    if not remaining_pool:
        print("\n✅ Level mastered! Nothing remaining in this level.")
        input("\nPress Enter to return to the menu...")
        return

    ask_count = min(count, len(remaining_pool))

    # Priority: unasked first, then wrong (that have been seen)
    primary = list(unasked)
    secondary = list(wrong_pool - unasked)

    random.shuffle(primary)
    random.shuffle(secondary)

    chosen = []

    for idx in primary:
        chosen.append(idx)
        if len(chosen) >= ask_count:
            break

    if len(chosen) < ask_count:
        for idx in secondary:
            chosen.append(idx)
            if len(chosen) >= ask_count:
                break

    results = []
    for idx in chosen:
        q = questions[idx]
        is_correct, user_display = ask_question(q)
        record_answer(prog, idx, is_correct)
        results.append((q, user_display, is_correct))

    save_level_progress(level_key, prog)

    print("\n=== Level Summary ===")
    correct_count = 0

    for q, user_display, is_correct in results:
        icon = "✅" if is_correct else "❌"
        print(f"\n{icon} Q: {q['question']}")
        print(f"Your answer: {user_display}")

        if is_correct:
            correct_count += 1
        else:
            print(f"Correct answer: {q['answer_text']}")
            print(f"Why: {q['explanation']}")

    total = len(results)
    print(f"\nScore: {correct_count}/{total}")
    input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    main_menu()

