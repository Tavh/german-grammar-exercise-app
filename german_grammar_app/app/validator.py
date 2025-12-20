"""
Exercise validation module.

Validates exercise data against JSON Schema and business rules.
Fails fast on any error - no auto-fixing.
"""
import json
from pathlib import Path
from typing import List, Tuple
import jsonschema
from german_grammar_app.app.loader import load_all_exercises
from german_grammar_app.app.models import Exercise


def validate_exercise_schema(file_path: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single exercise file against JSON Schema.
    
    Args:
        file_path: Path to exercise JSON file
        schema_path: Path to JSON Schema file
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Load schema
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except Exception as e:
        errors.append(f"Failed to load schema: {e}")
        return False, errors
    
    # Load exercise file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Failed to read file: {e}")
        return False, errors
    
    # Validate structure
    if not isinstance(data, list):
        errors.append("Exercise file must contain a JSON array")
        return False, errors
    
    # Validate each exercise
    for idx, exercise_data in enumerate(data):
        try:
            jsonschema.validate(instance=exercise_data, schema=schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Exercise at index {idx} (ID: {exercise_data.get('id', 'unknown')}): {e.message}")
        except Exception as e:
            errors.append(f"Exercise at index {idx}: Unexpected error: {e}")
    
    return len(errors) == 0, errors


def validate_all_exercises(data_dir: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate all exercise files on startup.
    
    Checks:
    - JSON Schema compliance
    - Duplicate IDs (via loader)
    - One-answer-only (via Exercise model)
    - Checklist item matches folder name (via loader)
    
    Args:
        data_dir: Path to data directory
        schema_path: Path to JSON Schema file
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    exercises_dir = data_dir / "exercises"
    
    if not exercises_dir.exists():
        errors.append(f"Exercises directory not found: {exercises_dir}")
        return False, errors
    
    # Validate each JSON file against schema
    for level_dir in sorted(exercises_dir.iterdir()):
        if not level_dir.is_dir():
            continue
        
        for json_file in sorted(level_dir.glob("*.json")):
            is_valid, file_errors = validate_exercise_schema(json_file, schema_path)
            if not is_valid:
                errors.extend([f"{json_file}: {e}" for e in file_errors])
    
    # Try to load all exercises (this catches duplicate IDs and other structural issues)
    try:
        load_all_exercises(data_dir)
    except Exception as e:
        errors.append(f"Failed to load exercises: {e}")
    
    return len(errors) == 0, errors


def validate_correct_answers(exercise: Exercise) -> bool:
    """
    Validate that exercise has correct_answers with at least one item.
    
    Args:
        exercise: Exercise to validate
        
    Returns:
        True if valid, raises ValueError if not
    """
    if not exercise.correct_answers:
        raise ValueError(
            f"Exercise {exercise.id}: correct_answers must be provided"
        )
    
    if len(exercise.correct_answers) == 0:
        raise ValueError(
            f"Exercise {exercise.id}: correct_answers must contain at least one answer"
        )
    
    # Check for empty strings
    if any(not str(ans).strip() for ans in exercise.correct_answers):
        raise ValueError(
            f"Exercise {exercise.id}: correct_answers cannot contain empty strings"
        )
    
    return True

