"""
Streamlit UI for German grammar exercise app.

Verb-centric drill app. Shows example solutions, no validation.
This app is a drill surface, not an evaluator.
"""
import streamlit as st
from pathlib import Path
from german_grammar_app.app.loader import load_all_exercises, get_exercises_by_filters, get_all_verbs
from german_grammar_app.app.validator import validate_all_exercises
from german_grammar_app.app.models import Level, ChecklistItem
from german_grammar_app.app.session import PracticeSession
from german_grammar_app.app.engine import get_exercise_display_info

# Page config
st.set_page_config(
    page_title="German Grammar Exercises",
    page_icon="🇩🇪",
    layout="centered"
)

# Default paths
DEFAULT_DATA_DIR = Path(__file__).parent / "german_grammar_app" / "data"
DEFAULT_SCHEMA_PATH = DEFAULT_DATA_DIR / "schema" / "exercise.schema.json"

# Default favourite verbs for A2.1
DEFAULT_FAVOURITES = [
    # Core actions
    "helfen", "sehen", "geben", "nehmen", "finden", "bringen",
    # Daily life / routines
    "wohnen", "arbeiten", "lernen", "fahren", "einkaufen",
    # Communication / intention
    "sagen", "fragen", "antworten",
    # Separable essentials
    "aufstehen", "anrufen", "mitkommen", "anfangen", "aufhören",
    # Reflexive essentials
    "sich treffen", "sich fühlen", "sich interessieren", "sich freuen",
    # Basic verbs
    "gehen", "machen", "essen", "trinken", "kommen"
]


def load_favourites() -> set:
    """Load favourites from session state."""
    if "favourites" not in st.session_state:
        st.session_state.favourites = set(DEFAULT_FAVOURITES)
    # Ensure it's a set (handle any type issues)
    if not isinstance(st.session_state.favourites, set):
        st.session_state.favourites = set(st.session_state.favourites)
    return st.session_state.favourites


def save_favourites(favourites: set):
    """Save favourites to session state."""
    st.session_state.favourites = favourites


def reset_exercise_state():
    """Reset all per-exercise UI state."""
    st.session_state.user_input = ""
    # Note: hint, translation, and examples are now in expanders (no state needed)


@st.cache_data
def load_and_validate_exercises(data_dir: Path):
    """Load and validate exercises (cached)."""
    schema_path = data_dir / "schema" / "exercise.schema.json"
    is_valid, errors = validate_all_exercises(data_dir, schema_path)
    if not is_valid:
        st.error("Validation errors found:")
        for error in errors:
            st.error(f"  • {error}")
        st.stop()
    
    return load_all_exercises(data_dir)


def main():
    """Main Streamlit app."""
    # Initialize session state
    if "session" not in st.session_state:
        st.session_state.session = None
    
    # Load favourites
    favourites = load_favourites()
    
    st.title("🇩🇪 German Grammar Exercises")
    st.markdown("**Verb-centric practice drill**")
    
    # Sidebar filters
    with st.sidebar:
        st.header("Settings")
        
        # Level filter
        all_levels = [level.value for level in Level]
        available_levels = ["A2.1"]
        
        level_display_options = []
        for level in all_levels:
            if level in available_levels:
                level_display_options.append(level)
            else:
                level_display_options.append(f"{level} (coming soon)")
        
        selected_display = st.selectbox(
            "Level",
            level_display_options,
            index=0
        )
        selected_level_str = selected_display.split(" (")[0]
        
        if selected_level_str not in available_levels:
            st.info("💡 A2.1 is currently the only available level.")
            level_filter = Level.A2_1
        else:
            level_filter = Level(selected_level_str)
        
        # Checklist filter
        checklist_options = ["All"] + [item.value for item in ChecklistItem]
        selected_checklist = st.selectbox("Checklist Item", checklist_options)
        checklist_filter = None if selected_checklist == "All" else ChecklistItem(selected_checklist)
        
        # Load exercises
        try:
            all_exercises = load_and_validate_exercises(DEFAULT_DATA_DIR)
            all_filtered = get_exercises_by_filters(all_exercises, level_filter, checklist_filter)
            
            if not all_filtered:
                st.warning("No exercises found matching filters.")
                st.stop()
            
            # Get all verbs
            all_verbs = get_all_verbs(all_filtered)
            
            # Practice options
            st.divider()
            st.subheader("Practice Options")
            
            # Simple favourites toggle
            use_favourites_only = st.checkbox("Practice favourites only", value=False)
            
            if use_favourites_only:
                # Filter to favourite verbs
                available_verbs = [v for v in all_verbs if v in favourites]
                if not available_verbs:
                    st.warning("No favourite verbs yet. Add verbs to favourites using ⭐ on exercises.")
                    selected_verbs = []
                else:
                    selected_verbs = available_verbs
            else:
                # All verbs by default
                selected_verbs = all_verbs
            
            # Favourite verbs list - collapsible and calm
            st.divider()
            
            # Collapsible favourites section (default collapsed)
            fav_count = len(favourites)
            if fav_count > 0:
                expander_label = f"Favourite verbs ({fav_count})"
            else:
                expander_label = "Favourite verbs"
            
            with st.expander(expander_label, expanded=False):
                # Brief explanation (only when expanded)
                st.caption("Favourite verbs appear more often in practice. New verbs are still mixed in automatically.")
                
                if favourites:
                    # Display as editable list - use container to ensure all items render
                    fav_list = sorted(favourites)
                    # Create a container to force rendering of all items
                    container = st.container()
                    with container:
                        for verb in fav_list:
                            col1, col2 = st.columns([5, 1])
                            with col1:
                                st.markdown(f"⭐ **{verb}**")
                            with col2:
                                # Subtle removal button
                                if st.button("×", key=f"remove_{verb}", use_container_width=True, help="Remove from favourites"):
                                    favourites.discard(verb)
                                    save_favourites(favourites)
                                    st.rerun()
                else:
                    st.caption("No favourites yet. Click ⭐ on exercises to add verbs.")
            
            # Apply verb filter
            if use_favourites_only:
                if not available_verbs:
                    exercises = []
                else:
                    exercises = get_exercises_by_filters(
                        all_exercises, level_filter, checklist_filter, available_verbs
                    )
            elif selected_verbs:
                exercises = get_exercises_by_filters(
                    all_exercises, level_filter, checklist_filter, selected_verbs
                )
            else:
                # No verb filter - show all
                exercises = all_filtered
            
            if not exercises:
                st.warning("No exercises found matching filters.")
                st.stop()
            
            st.info(f"**{len(exercises)} exercises** available")
            
        except Exception as e:
            st.error(f"Error loading exercises: {e}")
            st.stop()
    
    # Main content area
    if st.session_state.session is None:
        # Start new session
        st.header("Start Practice Session")
        st.write(f"Ready to practice with **{len(exercises)} exercises**")
        st.write("**Flow:** See exercise → Practice → Compare with examples → Next")
        
        if st.button("Start Session", type="primary"):
            # Use practice mix: 75% favourites, 25% new verbs
            st.session_state.session = PracticeSession(
                exercises,
                shuffle=True,
                favourite_verbs=favourites,
                use_practice_mix=True
            )
            reset_exercise_state()
            st.rerun()
    
    else:
        # Practice session active
        session = st.session_state.session
        
        if session.is_complete():
            # Session complete
            st.header("Session Complete!")
            st.success(f"Completed **{len(session.exercises)} exercises**")
            
            if st.button("New Session", type="primary"):
                st.session_state.session = None
                reset_exercise_state()
                st.rerun()
        
        else:
            # Active exercise
            exercise = session.get_current_exercise()
            if not exercise:
                st.error("No current exercise")
                st.stop()
            
            current, total = session.get_progress()
            info = get_exercise_display_info(exercise)
            
            # Progress
            progress = current / total
            st.progress(progress)
            st.caption(f"Exercise {current} of {total}")
            
            # Exercise display - show prompt (never the solution)
            st.markdown(f"### {info['prompt']}")
            
            # Verb info and controls
            verb = info['verb']
            st.caption(f"**Verb:** {verb} | {info['checklist_item']}")
            
            # Favourite button (only one that needs rerun)
            col1, col2 = st.columns([5, 1])
            with col1:
                pass  # Space for expanders below
            with col2:
                is_favourite = verb in favourites
                fav_label = "⭐" if is_favourite else "☆"
                fav_tooltip = "Remove from favourites" if is_favourite else "Add to favourites"
                if st.button(fav_label, key=f"fav_{exercise.id}", use_container_width=True, help=fav_tooltip):
                    if is_favourite:
                        favourites.discard(verb)
                    else:
                        favourites.add(verb)
                    save_favourites(favourites)
                    st.rerun()
            
            # Use expanders for hint, translation, and examples (no rerun needed - instant!)
            with st.expander("💡 Hint", expanded=False):
                st.info(info['hint'])
            
            with st.expander("🇬🇧 Translation", expanded=False):
                st.info(info['english'])
            
            # Show construction hints if available (for sentence_construction tasks)
            if info.get('construction_hints'):
                with st.expander("🔧 Construction Hints", expanded=False):
                    st.write("**Available hints:**")
                    for hint in info['construction_hints']:
                        st.write(f"• {hint}")
            
            st.divider()
            
            # Answer input area (free practice - no validation)
            st.markdown("**Practice your answer:**")
            if info['task_type'] == "sentence_construction":
                user_input = st.text_area(
                    "Write your sentence:",
                    key=f"input_{exercise.id}",
                    height=150,
                    placeholder="Type your complete sentence here..."
                )
            elif info['task_type'] == "reorder":
                user_input = st.text_area(
                    "Enter words in correct order (space-separated):",
                    key=f"input_{exercise.id}",
                    height=100,
                    placeholder="Type your answer here..."
                )
            elif info['task_type'] == "multiple_choice":
                user_input = st.radio(
                    "Choose an answer:",
                    options=info['choices'],
                    key=f"input_{exercise.id}",
                    index=None  # No default selection
                )
            else:  # fill_blank
                user_input = st.text_input(
                    "Fill in the blank:",
                    key=f"input_{exercise.id}",
                    placeholder="Type your answer here..."
                )
            
            # Example solutions in expander (no rerun needed - instant!)
            st.divider()
            with st.expander("✅ Example Solution(s)", expanded=False):
                st.caption("These are example solutions for comparison. Your answer may also be correct.")
                example_solutions = info['example_solutions']
                if len(example_solutions) == 1:
                    st.success(example_solutions[0])
                    st.caption("One example solution")
                else:
                    for i, sol in enumerate(example_solutions, 1):
                        st.success(sol)
                        if i < len(example_solutions):
                            st.caption("or")
                    st.caption(f"{len(example_solutions)} example solutions")
            
            # Navigation
            st.divider()
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("← Previous"):
                    if session.current_index > 0:
                        session.move_to_previous()
                        reset_exercise_state()
                        st.rerun()
            
            with col2:
                if st.button("Next Exercise →", type="primary"):
                    if session.move_to_next():
                        reset_exercise_state()
                        st.rerun()
                    else:
                        # Session complete
                        st.rerun()
            
            # Reset session button
            if st.button("Reset Session", use_container_width=True):
                st.session_state.session = None
                reset_exercise_state()
                st.rerun()


if __name__ == "__main__":
    main()
