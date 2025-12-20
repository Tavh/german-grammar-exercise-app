"""
Practice session management.

Tracks exercises in a shuffled order. No validation, no grading.
This app is a drill surface, not an evaluator.
"""
from typing import List, Optional
from datetime import datetime
import random
from german_grammar_app.app.models import Exercise


def shuffle_exercises_with_mix(
    exercises: List[Exercise],
    favourite_verbs: set[str],
    favourite_ratio: float = 0.75
) -> List[Exercise]:
    """
    Shuffle exercises with 75/25 mix: ~75% favourites, ~25% new verbs.
    Avoids back-to-back same verb when possible.
    
    Args:
        exercises: List of exercises to shuffle
        favourite_verbs: Set of favourite verb strings
        favourite_ratio: Ratio of favourite exercises (default 0.75)
        
    Returns:
        Shuffled list of exercises with practice mix applied
    """
    if not exercises:
        return []
    
    # Separate into favourite and new verb exercises
    favourite_exercises = [ex for ex in exercises if ex.verb in favourite_verbs]
    new_exercises = [ex for ex in exercises if ex.verb not in favourite_verbs]
    
    # Calculate target counts
    total = len(exercises)
    target_favourite = int(total * favourite_ratio)
    target_new = total - target_favourite
    
    # Adjust if we don't have enough of one type
    if len(favourite_exercises) < target_favourite:
        target_favourite = len(favourite_exercises)
        target_new = total - target_favourite
    elif len(new_exercises) < target_new:
        target_new = len(new_exercises)
        target_favourite = total - target_new
    
    # Shuffle each group
    random.shuffle(favourite_exercises)
    random.shuffle(new_exercises)
    
    # Take target amounts
    selected_favourites = favourite_exercises[:target_favourite]
    selected_new = new_exercises[:target_new]
    
    # Combine and shuffle to mix them
    combined = selected_favourites + selected_new
    random.shuffle(combined)
    
    # Group by verb to avoid back-to-back same verb
    by_verb: dict[str, List[Exercise]] = {}
    for ex in combined:
        verb = ex.verb
        if verb not in by_verb:
            by_verb[verb] = []
        by_verb[verb].append(ex)
    
    # Shuffle within each verb group
    for verb in by_verb:
        random.shuffle(by_verb[verb])
    
    # Interleave verbs
    shuffled = []
    verb_keys = list(by_verb.keys())
    random.shuffle(verb_keys)
    
    max_count = max(len(by_verb[v]) for v in verb_keys) if verb_keys else 0
    
    for i in range(max_count):
        for verb in verb_keys:
            if i < len(by_verb[verb]):
                shuffled.append(by_verb[verb][i])
    
    # Add remaining exercises
    remaining = []
    for verb in verb_keys:
        for ex in by_verb[verb][max_count:]:
            remaining.append(ex)
    
    random.shuffle(remaining)
    shuffled.extend(remaining)
    
    # Final shuffle for randomness
    random.shuffle(shuffled)
    
    return shuffled


def shuffle_exercises(exercises: List[Exercise]) -> List[Exercise]:
    """
    Shuffle exercises, avoiding back-to-back same verb when possible.
    Legacy function - use shuffle_exercises_with_mix for practice mix.
    
    Args:
        exercises: List of exercises to shuffle
        
    Returns:
        Shuffled list of exercises
    """
    if not exercises:
        return []
    
    # Group by verb for better distribution
    by_verb: dict[str, List[Exercise]] = {}
    for ex in exercises:
        verb = ex.verb
        if verb not in by_verb:
            by_verb[verb] = []
        by_verb[verb].append(ex)
    
    # Shuffle within each verb group
    for verb in by_verb:
        random.shuffle(by_verb[verb])
    
    # Interleave verbs to avoid back-to-back repetition
    shuffled = []
    verb_keys = list(by_verb.keys())
    random.shuffle(verb_keys)
    
    max_count = max(len(by_verb[v]) for v in verb_keys) if verb_keys else 0
    
    for i in range(max_count):
        for verb in verb_keys:
            if i < len(by_verb[verb]):
                shuffled.append(by_verb[verb][i])
    
    # If we have leftover exercises, add them randomly
    remaining = []
    for verb in verb_keys:
        for ex in by_verb[verb][max_count:]:
            remaining.append(ex)
    
    random.shuffle(remaining)
    shuffled.extend(remaining)
    
    # Final shuffle to add more randomness while maintaining verb distribution
    random.shuffle(shuffled)
    
    return shuffled


class PracticeSession:
    """
    Manages a practice session with exercises.
    No validation, no grading - just practice.
    """
    
    def __init__(
        self,
        exercises: List[Exercise],
        shuffle: bool = True,
        favourite_verbs: Optional[set[str]] = None,
        use_practice_mix: bool = True
    ):
        """
        Initialize a practice session.
        
        Args:
            exercises: List of exercises for this session
            shuffle: Whether to shuffle exercises (default True)
            favourite_verbs: Set of favourite verbs for practice mix (default None)
            use_practice_mix: Whether to apply 75/25 practice mix (default True)
        """
        if shuffle:
            if use_practice_mix and favourite_verbs:
                self.exercises = shuffle_exercises_with_mix(exercises, favourite_verbs)
            else:
                self.exercises = shuffle_exercises(exercises)
        else:
            self.exercises = exercises
        self.current_index = 0
        self.start_time = datetime.now()
    
    def get_current_exercise(self) -> Optional[Exercise]:
        """Get the current exercise."""
        if self.current_index < len(self.exercises):
            return self.exercises[self.current_index]
        return None
    
    def move_to_next(self) -> bool:
        """
        Move to the next exercise.
        
        Returns:
            True if there is a next exercise, False if session is complete
        """
        self.current_index += 1
        return self.current_index < len(self.exercises)
    
    def move_to_previous(self) -> bool:
        """
        Move to the previous exercise.
        
        Returns:
            True if there is a previous exercise, False if at start
        """
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False
    
    def is_complete(self) -> bool:
        """Check if session is complete."""
        return self.current_index >= len(self.exercises)
    
    def get_progress(self) -> tuple[int, int]:
        """Get current progress as (current, total)."""
        return (self.current_index + 1, len(self.exercises))
    
    def get_verb_list(self) -> List[str]:
        """Get list of unique verbs in this session."""
        return sorted(set(ex.verb for ex in self.exercises))
