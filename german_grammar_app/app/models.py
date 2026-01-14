"""
Data models for German grammar exercises.

All exercises are pre-built data. No generation, no inference, no logic.
"""
from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum


class Level(str, Enum):
    """CEFR levels supported by the app."""
    A2_1 = "A2.1"
    A2_2 = "A2.2"
    B1_1 = "B1.1"
    B1_2 = "B1.2"
    
    def get_previous_levels(self) -> List['Level']:
        """
        Get all previous levels for this level.
        
        Returns:
            List of previous levels in order (A2.1, A2.2, B1.1, B1.2)
        """
        level_order = [Level.A2_1, Level.A2_2, Level.B1_1, Level.B1_2]
        try:
            current_index = level_order.index(self)
            return level_order[:current_index]
        except ValueError:
            return []


class ChecklistItem(str, Enum):
    """Grammar dimensions tested by exercises."""
    KASUS = "kasus"
    TRENNBAR = "trennbar"
    PRAEPOSITION = "praeposition"
    REFLEXIV = "reflexiv"
    PARTIZIP_II = "partizip_ii"


class TaskType(str, Enum):
    """Types of exercise tasks."""
    FILL_BLANK = "fill_blank"
    MULTIPLE_CHOICE = "multiple_choice"
    REORDER = "reorder"
    SENTENCE_CONSTRUCTION = "sentence_construction"


@dataclass
class Exercise:
    """
    A single German grammar exercise.
    
    All exercises are pre-written data. The app shows prompts and example solutions.
    The prompt must NEVER reveal the solution.
    """
    id: str
    level: Level
    verb: str
    checklist_item: ChecklistItem
    task_type: TaskType
    prompt: str  # Task description - must NOT reveal the solution
    example_solutions: List[str]  # Example solutions (hidden by default)
    english: str
    hint: str
    choices: Optional[List[str]] = None
    construction_hints: Optional[List[str]] = None  # Scaffolding hints (subject, noun hints without cases, context)
    structural_hints: Optional[List[str]] = None  # Structural role hints (Subjekt, Objekt, Ort, Zeit, Kasus, Genus, etc.) - NEVER declined forms
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate exercise data after initialization."""
        # Ensure multiple_choice has choices
        if self.task_type == TaskType.MULTIPLE_CHOICE:
            if not self.choices:
                raise ValueError(
                    f"Exercise {self.id}: multiple_choice task must have choices"
                )
        
        # Ensure example_solutions is not empty
        if not self.example_solutions or len(self.example_solutions) == 0:
            raise ValueError(
                f"Exercise {self.id}: example_solutions must contain at least one example"
            )
        
        # Ensure prompt doesn't contain full solutions
        # Check if any example solution appears in the prompt (allowing blanks)
        for solution in self.example_solutions:
            # Normalize for comparison (case-insensitive, no punctuation, no blanks)
            solution_clean = solution.strip().lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(' ', '')
            prompt_clean = self.prompt.strip().lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace('___', '').replace(' ', '')
            
            # Check if full solution (without blanks) appears in prompt
            # Allow prompts with blanks (fill_blank tasks), but not complete solutions
            if solution_clean in prompt_clean and len(solution_clean) > 15 and '___' not in self.prompt:
                raise ValueError(
                    f"Exercise {self.id}: prompt must not contain the full solution. "
                    f"Prompt: '{self.prompt}' appears to contain solution: '{solution}'"
                )


# Note: ExerciseResult and SessionStats removed
# This app does not validate or grade - it only shows example solutions

