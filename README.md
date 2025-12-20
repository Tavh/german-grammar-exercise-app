# German Grammar Exercise App

A data-driven German grammar exercise application focused on verb-centric decision making. This app prioritizes **correctness, scalability, and pedagogy over cleverness**.

## 🎯 Project Goal

Train learners at A2.1 (scalable to B1.2) in five key grammar dimensions:

- **Kasus** (Akkusativ / Dativ)
- **Trennbar** (prefix position)
- **Präposition** (fixed verb–preposition pairs)
- **Reflexiv** (mandatory reflexive usage)
- **Partizip II** (memorized past participle forms)

## 🚫 Core Principles (Non-Negotiable)

### NO FREE LANGUAGE GENERATION

This app **does NOT**:
- Generate sentences
- Infer grammar rules
- Conjugate verbs programmatically
- Generalize or derive rules

### ALL EXERCISES ARE PRE-BUILT DATA

- Sentences are **written by humans** and stored as JSON data
- The app only **loads, displays, and checks answers**
- No grammar logic, no NLP, no LLMs

### DATA-DRIVEN, NOT LOGIC-DRIVEN

- **Scaling = adding more data files**
- **NOT adding new grammar code**
- Adding new levels (A2.2, B1.1, B1.2) requires only adding JSON files

## 🧠 Pedagogical Model

Each exercise:
- Focuses on **exactly one verb**
- Tests **exactly one checklist decision**
- Has **exactly one correct answer**
- Is **unambiguous** without world knowledge

This mirrors classroom practice: students memorize correct patterns through repetition, not by exploring language rules.

### Why This Approach?

1. **Correctness**: Pre-written exercises ensure grammatical accuracy
2. **Speed**: No generation overhead = fast practice flow
3. **Pedagogy**: Repetition of correct patterns builds habits
4. **Scalability**: Add exercises by adding data, not code

## 🛠 Tech Stack

- **Python 3.11+**
- **CLI**: Typer
- **UI**: Streamlit
- **Storage**: JSON files
- **Validation**: JSON Schema
- **No database, no LLM, no NLP libraries**

## 📁 Project Structure

```
german_grammar_app/
├── data/
│   ├── exercises/
│   │   ├── a2_1/
│   │   │   ├── kasus.json
│   │   │   ├── trennbar.json
│   │   │   ├── praeposition.json
│   │   │   ├── reflexiv.json
│   │   │   └── partizip_ii.json
│   │   ├── a2_2/
│   │   ├── b1_1/
│   │   └── b1_2/
│   └── schema/
│       └── exercise.schema.json
├── app/
│   ├── loader.py          # Load exercises from JSON
│   ├── validator.py       # Validate against schema
│   ├── engine.py          # Exercise display & checking
│   ├── session.py         # Practice session management
│   └── models.py          # Data models
├── cli/
│   └── main.py            # CLI commands
├── streamlit_app.py       # Web UI
├── README.md
└── pyproject.toml
```

## 📄 Exercise Data Model

Every exercise follows this strict schema:

```json
{
  "id": "unique-string",
  "level": "A2.1 | A2.2 | B1.1 | B1.2",
  "verb": "string",
  "checklist_item": "kasus | trennbar | praeposition | reflexiv | partizip_ii",
  "task_type": "fill_blank | multiple_choice | reorder",
  "sentence": "string (must contain ___ for fill_blank)",
  "solution": "string or array",
  "choices": ["string"] (required for multiple_choice),
  "english": "string",
  "hint": "string",
  "tags": ["string"] (optional)
}
```

### Hard Constraints

- **Exactly one correct solution** per exercise
- **No optional grammar** - unambiguous answers only
- **No dynamic evaluation** - answers are exact matches
- `fill_blank` tasks **MUST** contain `___` in sentence

## 🧪 Validation

On startup, the app validates:

1. **JSON Schema compliance** for all exercise files
2. **Duplicate IDs** across all files
3. **One-answer-only** constraint
4. **Checklist item matches folder name**

**Fails fast** on any error. **No auto-fixing** of data.

## 🖥 CLI Usage

### List Exercises

```bash
python -m german_grammar_app.cli.main list
python -m german_grammar_app.cli.main list --level A2.1
python -m german_grammar_app.cli.main list --checklist kasus
python -m german_grammar_app.cli.main list --level A2.1 --checklist trennbar
```

### Practice Session

```bash
python -m german_grammar_app.cli.main practice
python -m german_grammar_app.cli.main practice --level A2.1 --checklist kasus
python -m german_grammar_app.cli.main practice --timed
```

### Statistics

```bash
python -m german_grammar_app.cli.main stats
python -m german_grammar_app.cli.main stats --level A2.1
```

## 🌐 Streamlit UI

Run the web interface:

```bash
streamlit run streamlit_app.py
```

Features:
- One exercise at a time
- Show/hide English translation
- Show/hide hints
- Reveal correct answer
- Level and checklist filters
- Session statistics

**No animations, no gamification, minimal UI** - focused on speed and repetition.

## 📖 How to Add New Exercises

### Step 1: Create JSON File

Create or edit a file in `data/exercises/{level}/{checklist_item}.json`:

```json
[
  {
    "id": "a2_1_kasus_001",
    "level": "A2.1",
    "verb": "helfen",
    "checklist_item": "kasus",
    "task_type": "fill_blank",
    "sentence": "Ich helfe ___ Freund.",
    "solution": "dem",
    "english": "I help the friend.",
    "hint": "helfen takes Dativ",
    "tags": ["dativ", "helfen"]
  }
]
```

### Step 2: Validate

The app will automatically validate on startup. If there are errors, fix them before proceeding.

### Step 3: Test

Run the app and verify the exercise appears and works correctly.

### That's It!

No code changes needed. Just add data files.

## 🔒 Safety Rules

If you are tempted to:

- "generate" sentences
- "derive" grammar rules
- "infer" conjugations
- "optimize" grammar logic

**Stop. Do not do it.**

This project is about **training correct habits**, not exploring language. All exercises must be pre-written by humans.

## 🚀 Installation

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install the package and dependencies
pip install -e .

# Or install dependencies directly
pip install typer rich streamlit jsonschema
```

## 🏃 Quick Start

After installation, you can use the app via CLI or Streamlit UI.

### CLI Usage

```bash
# List all exercises
python -m german_grammar_app.cli.main list

# Practice with filters
python -m german_grammar_app.cli.main practice --level A2.1 --checklist kasus

# View statistics
python -m german_grammar_app.cli.main stats
```

### Streamlit UI

```bash
streamlit run streamlit_app.py
```

Then open your browser to the URL shown (typically http://localhost:8501).

## 📝 Example Exercise Files

See `data/exercises/a2_1/` for example exercise files in each checklist category.

## 🎓 For Educators

This app is designed to mirror classroom practice:

1. **Pre-written exercises** ensure consistency
2. **Repetition** builds correct habits
3. **No ambiguity** - one clear answer per exercise
4. **Scalable** - add more exercises as students progress

The app does not replace instruction; it provides **focused, repetitive practice** on specific grammar points.

## 📄 License

MIT

