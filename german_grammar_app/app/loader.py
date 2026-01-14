"""
Exercise loader module.

Loads pre-built exercise data from JSON files. No generation, no inference.
"""
import json
from pathlib import Path
from typing import List, Dict
from german_grammar_app.app.models import Exercise, Level, ChecklistItem, TaskType


def load_exercises_from_file(file_path: Path) -> List[Exercise]:
    """
    Load exercises from a single JSON file.
    
    Args:
        file_path: Path to JSON file containing exercise array
        
    Returns:
        List of Exercise objects
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is invalid JSON
        ValueError: If exercise data is invalid
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Exercise file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        raise ValueError(f"Exercise file must contain a JSON array: {file_path}")
    
    exercises = []
    for item in data:
        # Handle prompt field (required)
        if 'prompt' in item:
            prompt = item['prompt']
        elif 'sentence' in item:
            # Legacy: use sentence as prompt (for fill_blank with ___)
            prompt = item['sentence']
        else:
            raise ValueError(f"Exercise {item.get('id', 'unknown')}: missing 'prompt' field")
        
        # Handle example_solutions field (required)
        if 'example_solutions' in item:
            example_solutions = item['example_solutions']
        elif 'correct_answers' in item:
            # Legacy: correct_answers becomes example_solutions
            example_solutions = item['correct_answers']
        elif 'solution' in item:
            # Legacy: single solution becomes list
            solution = item['solution']
            example_solutions = [solution] if isinstance(solution, str) else solution
        else:
            raise ValueError(f"Exercise {item.get('id', 'unknown')}: missing 'example_solutions' field")
        
        # Ensure example_solutions is a list
        if not isinstance(example_solutions, list):
            raise ValueError(f"Exercise {item.get('id', 'unknown')}: example_solutions must be a list")
        
        # Remove duplicates (preserve order)
        seen = set()
        unique_solutions = []
        for sol in example_solutions:
            normalized = str(sol).strip().lower()
            if normalized not in seen:
                seen.add(normalized)
                unique_solutions.append(str(sol))  # Keep original case for display
        
        exercise = Exercise(
            id=item['id'],
            level=Level(item['level']),
            verb=item['verb'],
            checklist_item=ChecklistItem(item['checklist_item']),
            task_type=TaskType(item['task_type']),
            prompt=prompt,
            example_solutions=unique_solutions,
            english=item['english'],
            hint=item['hint'],
            choices=item.get('choices'),
            construction_hints=item.get('construction_hints'),
            structural_hints=item.get('structural_hints'),
            tags=item.get('tags')
        )
        exercises.append(exercise)
    
    return exercises


def load_all_exercises(data_dir: Path) -> Dict[str, List[Exercise]]:
    """
    Load all exercises from the data directory structure.
    
    Expected structure:
        data/exercises/{level}/{checklist_item}.json
        
    Args:
        data_dir: Path to data directory
        
    Returns:
        Dictionary mapping "{level}/{checklist_item}" to list of exercises
        
    Raises:
        ValueError: If directory structure is invalid or exercises have errors
    """
    exercises_dir = data_dir / "exercises"
    if not exercises_dir.exists():
        raise ValueError(f"Exercises directory not found: {exercises_dir}")
    
    all_exercises: Dict[str, List[Exercise]] = {}
    exercise_ids: Dict[str, str] = {}  # id -> file path for duplicate detection
    
    # Map directory names to Level enum values
    # Directory names use underscores (a2_1), enum values use dots (A2.1)
    level_dir_to_enum = {
        "a2_1": "A2.1",
        "a2_2": "A2.2",
        "b1_1": "B1.1",
        "b1_2": "B1.2"
    }
    
    # Iterate through level directories
    for level_dir in sorted(exercises_dir.iterdir()):
        if not level_dir.is_dir():
            continue
        
        level_dir_name = level_dir.name
        # Convert directory name to Level enum value
        level = level_dir_to_enum.get(level_dir_name.lower())
        if not level:
            raise ValueError(
                f"Unknown level directory: {level_dir_name}. "
                f"Expected one of: {', '.join(level_dir_to_enum.keys())}"
            )
        
        # Iterate through checklist item files
        for json_file in sorted(level_dir.glob("*.json")):
            checklist_item = json_file.stem
            
            # Verify checklist item matches filename
            expected_checklist_items = {
                "kasus", "trennbar", "praeposition", "reflexiv", "partizip_ii"
            }
            if checklist_item not in expected_checklist_items:
                raise ValueError(
                    f"Unexpected checklist item file: {json_file.name}. "
                    f"Expected one of: {', '.join(expected_checklist_items)}"
                )
            
            # Load exercises
            exercises = load_exercises_from_file(json_file)
            
            # Check for duplicate IDs
            for exercise in exercises:
                if exercise.id in exercise_ids:
                    raise ValueError(
                        f"Duplicate exercise ID '{exercise.id}' found in:\n"
                        f"  - {exercise_ids[exercise.id]}\n"
                        f"  - {json_file}"
                    )
                exercise_ids[exercise.id] = str(json_file)
                
                # Verify checklist item matches folder name
                if exercise.checklist_item.value != checklist_item:
                    raise ValueError(
                        f"Exercise {exercise.id}: checklist_item '{exercise.checklist_item.value}' "
                        f"does not match filename '{checklist_item}'"
                    )
            
            key = f"{level}/{checklist_item}"
            all_exercises[key] = exercises
    
    return all_exercises


def get_exercises_by_filters(
    all_exercises: Dict[str, List[Exercise]],
    level: Level = None,
    checklist_item: ChecklistItem = None,
    verbs: List[str] = None,
    include_previous_levels: bool = False
) -> List[Exercise]:
    """
    Filter exercises by level, checklist item, and/or verbs.
    
    Args:
        all_exercises: Dictionary from load_all_exercises
        level: Optional level filter (Level enum)
        checklist_item: Optional checklist item filter (ChecklistItem enum)
        verbs: Optional list of verbs to filter by
        include_previous_levels: If True and level is specified, include exercises from previous levels
        
    Returns:
        Filtered list of exercises
    """
    filtered = []
    
    # Determine which levels to include
    levels_to_include = set()
    if level:
        levels_to_include.add(level.value)
        if include_previous_levels:
            previous_levels = level.get_previous_levels()
            levels_to_include.update(prev.value for prev in previous_levels)
    
    for key, exercises in all_exercises.items():
        level_part, checklist_part = key.split('/')
        
        # Apply level filter
        if level:
            if include_previous_levels:
                if level_part not in levels_to_include:
                    continue
            else:
                if level.value != level_part:
                    continue
        elif not level and include_previous_levels:
            # If include_previous_levels is True but no level specified, ignore it
            pass
        
        # Apply checklist item filter
        if checklist_item and checklist_item.value != checklist_part:
            continue
        
        # Filter by verb if specified
        if verbs:
            exercises = [ex for ex in exercises if ex.verb in verbs]
        
        filtered.extend(exercises)
    
    return filtered


def get_all_verbs(exercises: List[Exercise]) -> List[str]:
    """
    Get list of all unique verbs from exercises.
    
    Args:
        exercises: List of exercises
        
    Returns:
        Sorted list of unique verbs
    """
    return sorted(set(ex.verb for ex in exercises))

