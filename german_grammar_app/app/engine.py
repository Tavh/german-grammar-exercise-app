"""
Exercise engine module.

Handles exercise presentation. No validation, only example solutions.
This app is a drill surface, not an evaluator.
"""
from typing import List, Optional
from german_grammar_app.app.models import Exercise, TaskType


def get_exercise_display_info(exercise: Exercise) -> dict:
    """
    Get all information needed to display an exercise.
    
    Args:
        exercise: Exercise to display
        
    Returns:
        Dictionary with display information including prompt and example solutions
    """
    return {
        "id": exercise.id,
        "verb": exercise.verb,
        "checklist_item": exercise.checklist_item.value,
        "task_type": exercise.task_type.value,
        "prompt": exercise.prompt,  # Task description - never reveals solution
        "choices": exercise.choices,
        "construction_hints": exercise.construction_hints,  # Scaffolding hints for sentence construction
        "english": exercise.english,
        "hint": exercise.hint,
        "level": exercise.level.value,
        "example_solutions": exercise.example_solutions  # Hidden by default
    }
