import json
import os
from typing import Dict, Set, List, Any

PROGRESS_FILE = "progress.json"

def reset_all_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

def remaining_questions(level_key, total_questions):
    prog = load_level_progress(level_key)
    mastered = set(prog["asked_seen"]) - set(prog["asked_wrong"])
    return total_questions - len(mastered)


def _load_raw() -> Dict[str, Any]:
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_raw(data: Dict[str, Any]) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def load_level_progress(level_key: str) -> Dict[str, Set[int]]:
    """
    Returns sets of indexes: asked_correct, asked_wrong, asked_seen
    """
    data = _load_raw()
    lvl = data.get(level_key, {})
    asked_correct = set(lvl.get("asked_correct", []))
    asked_wrong = set(lvl.get("asked_wrong", []))
    asked_seen = set(lvl.get("asked_seen", []))
    return {
        "asked_correct": asked_correct,
        "asked_wrong": asked_wrong,
        "asked_seen": asked_seen,
    }


def save_level_progress(level_key: str, prog: Dict[str, Set[int]]) -> None:
    data = _load_raw()
    data[level_key] = {
        "asked_correct": sorted(list(prog["asked_correct"])),
        "asked_wrong": sorted(list(prog["asked_wrong"])),
        "asked_seen": sorted(list(prog["asked_seen"])),
    }
    _save_raw(data)


def record_answer(prog: Dict[str, Set[int]], q_index: int, is_correct: bool) -> None:
    prog["asked_seen"].add(q_index)

    if is_correct:
        prog["asked_correct"].add(q_index)
        # If it was previously wrong, remove it from wrong once you get it right.
        prog["asked_wrong"].discard(q_index)
    else:
        prog["asked_wrong"].add(q_index)
        # Do NOT remove from correct here; but if it was in correct already, keep it correct.

