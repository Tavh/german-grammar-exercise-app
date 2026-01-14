"""
CLI interface for German grammar exercise app.

Commands: list, practice, stats
"""
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from german_grammar_app.app.loader import load_all_exercises, get_exercises_by_filters
from german_grammar_app.app.validator import validate_all_exercises
from german_grammar_app.app.models import Level, ChecklistItem
from german_grammar_app.app.session import PracticeSession
from german_grammar_app.app.engine import get_exercise_display_info, check_answer

app = typer.Typer(help="German Grammar Exercise App - CLI")
console = Console()

# Default paths
DEFAULT_DATA_DIR = Path(__file__).parent.parent / "data"
DEFAULT_SCHEMA_PATH = DEFAULT_DATA_DIR / "schema" / "exercise.schema.json"


@app.command()
def list(
    level: Optional[str] = typer.Option(None, "--level", "-l", help="Filter by level (A2.1, A2.2, B1.1, B1.2)"),
    checklist: Optional[str] = typer.Option(None, "--checklist", "-c", help="Filter by checklist item (kasus, trennbar, praeposition, reflexiv, partizip_ii)"),
    include_previous: bool = typer.Option(False, "--include-previous", "-p", help="Include exercises from previous levels"),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Path to data directory"),
):
    """List available exercises with optional filters."""
    try:
        # Validate exercises first
        schema_path = data_dir / "schema" / "exercise.schema.json"
        is_valid, errors = validate_all_exercises(data_dir, schema_path)
        if not is_valid:
            console.print("[red]Validation errors:[/red]")
            for error in errors:
                console.print(f"  [red]•[/red] {error}")
            raise typer.Exit(1)
        
        # Load exercises
        all_exercises = load_all_exercises(data_dir)
        
        # Apply filters
        level_enum = None
        checklist_enum = None
        
        if level:
            try:
                level_enum = Level(level)
            except ValueError:
                console.print(f"[red]Invalid level: {level}[/red]")
                raise typer.Exit(1)
        
        if checklist:
            try:
                checklist_enum = ChecklistItem(checklist)
            except ValueError:
                console.print(f"[red]Invalid checklist item: {checklist}[/red]")
                raise typer.Exit(1)
        
        exercises = get_exercises_by_filters(all_exercises, level_enum, checklist_enum, include_previous_levels=include_previous)
        
        # Display results
        if not exercises:
            console.print("[yellow]No exercises found matching filters.[/yellow]")
            return
        
        # Create table
        table = Table(title=f"Exercises ({len(exercises)} found)")
        table.add_column("ID", style="cyan")
        table.add_column("Level", style="green")
        table.add_column("Verb", style="yellow")
        table.add_column("Checklist", style="magenta")
        table.add_column("Task Type", style="blue")
        
        for exercise in sorted(exercises, key=lambda e: (e.level.value, e.checklist_item.value, e.id)):
            table.add_row(
                exercise.id,
                exercise.level.value,
                exercise.verb,
                exercise.checklist_item.value,
                exercise.task_type.value
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def practice(
    level: Optional[str] = typer.Option(None, "--level", "-l", help="Filter by level"),
    checklist: Optional[str] = typer.Option(None, "--checklist", "-c", help="Filter by checklist item"),
    include_previous: bool = typer.Option(False, "--include-previous", "-p", help="Include exercises from previous levels"),
    timed: bool = typer.Option(False, "--timed", "-t", help="Run timed practice session"),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Path to data directory"),
):
    """Run a practice session with exercises."""
    try:
        # Validate and load exercises
        schema_path = data_dir / "schema" / "exercise.schema.json"
        is_valid, errors = validate_all_exercises(data_dir, schema_path)
        if not is_valid:
            console.print("[red]Validation errors:[/red]")
            for error in errors:
                console.print(f"  [red]•[/red] {error}")
            raise typer.Exit(1)
        
        all_exercises = load_all_exercises(data_dir)
        
        # Apply filters
        level_enum = None
        checklist_enum = None
        
        if level:
            try:
                level_enum = Level(level)
            except ValueError:
                console.print(f"[red]Invalid level: {level}[/red]")
                raise typer.Exit(1)
        
        if checklist:
            try:
                checklist_enum = ChecklistItem(checklist)
            except ValueError:
                console.print(f"[red]Invalid checklist item: {checklist}[/red]")
                raise typer.Exit(1)
        
        exercises = get_exercises_by_filters(all_exercises, level_enum, checklist_enum, include_previous_levels=include_previous)
        
        if not exercises:
            console.print("[yellow]No exercises found matching filters.[/yellow]")
            return
        
        # Create session
        session = PracticeSession(exercises)
        
        console.print(f"[green]Starting practice session with {len(exercises)} exercises[/green]\n")
        
        # Practice loop
        while not session.is_complete():
            exercise = session.get_current_exercise()
            if not exercise:
                break
            
            current, total = session.get_progress()
            info = get_exercise_display_info(exercise)
            
            console.print(f"\n[bold cyan]Exercise {current}/{total}[/bold cyan]")
            console.print(f"[yellow]Verb:[/yellow] {info['verb']}")
            console.print(f"[yellow]Checklist:[/yellow] {info['checklist_item']}")
            console.print(f"[yellow]Task:[/yellow] {info['task_type']}")
            console.print(f"\n[bold]{info['prompt']}[/bold]")
            
            if info['choices']:
                console.print("\n[dim]Choices:[/dim]")
                for i, choice in enumerate(info['choices'], 1):
                    console.print(f"  {i}. {choice}")
            
            # Get user input
            if exercise.task_type.value == "reorder":
                console.print("\n[dim]Enter words in correct order (space-separated):[/dim]")
                user_input = typer.prompt("Your answer")
                user_answer = user_input.split()
            elif exercise.task_type.value == "multiple_choice":
                console.print("\n[dim]Enter choice number or text:[/dim]")
                user_input = typer.prompt("Your answer")
                # Try to match by number first
                if user_input.isdigit():
                    idx = int(user_input) - 1
                    if 0 <= idx < len(info['choices']):
                        user_answer = info['choices'][idx]
                    else:
                        user_answer = user_input
                else:
                    user_answer = user_input
            else:  # fill_blank
                console.print("\n[dim]Fill in the blank:[/dim]")
                user_answer = typer.prompt("Your answer")
            
            # Check answer
            result = session.submit_answer(user_answer)
            
            if result.is_correct:
                console.print("[green]✓ Correct![/green]")
            else:
                console.print("[red]✗ Incorrect[/red]")
                if len(result.correct_answers) == 1:
                    console.print(f"[dim]Correct answer: {result.correct_answers[0]}[/dim]")
                else:
                    console.print(f"[dim]Correct answers: {', '.join(result.correct_answers)}[/dim]")
            
            # Show hint/english on request
            show_more = typer.confirm("\nShow hint/English?", default=False)
            if show_more:
                console.print(f"[dim]Hint: {info['hint']}[/dim]")
                console.print(f"[dim]English: {info['english']}[/dim]")
            
            # Move to next
            if not session.move_to_next():
                break
            
            continue_practice = typer.confirm("\nContinue?", default=True)
            if not continue_practice:
                break
        
        # Show stats
        stats = session.get_stats()
        console.print("\n[bold]Session Statistics:[/bold]")
        console.print(f"Total: {stats.total_exercises}")
        console.print(f"Correct: {stats.correct}")
        console.print(f"Incorrect: {stats.incorrect}")
        console.print(f"Accuracy: {stats.accuracy:.1f}%")
        
        if stats.by_checklist_item:
            console.print("\n[bold]By Checklist Item:[/bold]")
            for checklist, breakdown in stats.by_checklist_item.items():
                acc = (breakdown['correct'] / breakdown['total'] * 100) if breakdown['total'] > 0 else 0
                console.print(
                    f"  {checklist}: {breakdown['correct']}/{breakdown['total']} ({acc:.1f}%)"
                )
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Practice session interrupted.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def stats(
    level: Optional[str] = typer.Option(None, "--level", "-l", help="Filter by level"),
    checklist: Optional[str] = typer.Option(None, "--checklist", "-c", help="Filter by checklist item"),
    include_previous: bool = typer.Option(False, "--include-previous", "-p", help="Include exercises from previous levels"),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Path to data directory"),
):
    """Show basic statistics about available exercises."""
    try:
        # Load exercises
        all_exercises = load_all_exercises(data_dir)
        
        # Apply filters
        level_enum = None
        checklist_enum = None
        
        if level:
            try:
                level_enum = Level(level)
            except ValueError:
                console.print(f"[red]Invalid level: {level}[/red]")
                raise typer.Exit(1)
        
        if checklist:
            try:
                checklist_enum = ChecklistItem(checklist)
            except ValueError:
                console.print(f"[red]Invalid checklist item: {checklist}[/red]")
                raise typer.Exit(1)
        
        exercises = get_exercises_by_filters(all_exercises, level_enum, checklist_enum, include_previous_levels=include_previous)
        
        if not exercises:
            console.print("[yellow]No exercises found.[/yellow]")
            return
        
        # Calculate stats
        by_checklist: dict[str, int] = {}
        by_level: dict[str, int] = {}
        by_task_type: dict[str, int] = {}
        
        for exercise in exercises:
            checklist = exercise.checklist_item.value
            by_checklist[checklist] = by_checklist.get(checklist, 0) + 1
            
            level = exercise.level.value
            by_level[level] = by_level.get(level, 0) + 1
            
            task_type = exercise.task_type.value
            by_task_type[task_type] = by_task_type.get(task_type, 0) + 1
        
        # Display
        console.print(f"[bold]Total Exercises: {len(exercises)}[/bold]\n")
        
        table = Table(title="By Checklist Item")
        table.add_column("Checklist Item", style="cyan")
        table.add_column("Count", style="green")
        for checklist, count in sorted(by_checklist.items()):
            table.add_row(checklist, str(count))
        console.print(table)
        
        table = Table(title="By Level")
        table.add_column("Level", style="cyan")
        table.add_column("Count", style="green")
        for level, count in sorted(by_level.items()):
            table.add_row(level, str(count))
        console.print(table)
        
        table = Table(title="By Task Type")
        table.add_column("Task Type", style="cyan")
        table.add_column("Count", style="green")
        for task_type, count in sorted(by_task_type.items()):
            table.add_row(task_type, str(count))
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

