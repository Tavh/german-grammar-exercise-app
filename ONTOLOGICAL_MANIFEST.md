# 📜 German A2.1 Declination Trainer — Ontological Manifest (FINAL)

**Status:** FROZEN  
**Level:** A2.1  
**Authority:** Teacher-aligned classroom drills  
**Goal:** Deterministic, explainable, testable exercises

---

## 1. Purpose of the App

This app trains **morphological production in German**.

The student must actively produce:

- **article forms**
- **adjective endings**
- **verb forms** (secondary but required)

The app is **not** for:

- vocabulary learning
- sentence creativity
- discourse/pragmatics decisions

---

## 2. Core Pedagogical Principle

**The exercise encodes the grammatical situation. The student produces the correct surface forms.**

The student:

- does **not** choose article type
- does **not** guess meaning
- does **not** invent words

The exercise author fixes:

- article type
- case
- verb lemma
- adjective presence

---

## 3. Global Rules (Apply to ALL Exercises)

### 3.1 Lexical visibility

**Always visible:**

- noun lemma
- adjective lemma (if used)
- verb lemma (infinitive)

**Never guessed.**

### 3.2 What is blanked

The student must fill in:

- article form
- adjective ending (if adjective present)
- conjugated verb form
- Partizip II (if relevant)
- reflexive pronoun (if relevant)

### 3.3 Article-type encoding (CRITICAL)

| Article type | Prompt shows | Student produces |
|-------------|--------------|------------------|
| **bestimmt** | `___` | der / die / das / den / dem / … |
| **unbestimmt** | `ein__` | ein / eine / einen / einem / … |
| **possessiv** | `mein__`, `dein__` | mein / meine / meinen / … |
| **kein** | `kein__` | kein / keine / keinen / … |
| **nullartikel** | (nothing) | adjective ending only |

❗ **The student never decides article type**  
❗ **Article type is always encoded by the prompt**

### 3.4 Adjective rules

**If adjective declination is trained:**

- adjective must be present
- shown as `stem + __` (e.g. `gut__`)

**If no adjective is intended:**

- none is implied
- none is hinted

**No adjective is ever guessed.**

### 3.5 Verb rules (global)

- Verb is shown as infinitive (metadata or hint)
- Verb form in sentence is blank
- Tense: Präsens or Perfekt only (A2.1)
- Verbs are carriers, not the learning goal.

---

## 4. Exercise Types (by checklist_item)

### 4.1 Kasus

**Purpose:**

Train:

- Akkusativ vs Dativ vs Nominativ
- article + adjective declination
- verb conjugation

**Mandatory structure:**

- at least one declinable noun phrase
- verb conjugated by student

**Example (valid):**

```
Ich ___ ein__ gut__ Film.
Verb: sehen (Präsens)
```

### 4.2 Trennbar

**Purpose:**

Train:

- declination
- verb conjugation
- separable verb placement

**Mandatory structure:**

- same as Kasus
- separable verb infinitive shown
- prefix position structurally required

**Example (valid):**

```
Ich ___ ein__ gut__ Film ___.
Verb: anschauen (Präsens)
```

### 4.3 Reflexiv

**Purpose:**

Train:

- declination
- verb conjugation
- reflexive pronoun selection

**Mandatory rules:**

- reflexive pronoun must be blanked
- pronoun must be required by verb

**Example (valid):**

```
Ich ___ ___ für ein__ interessant__ Film.
Verb: sich interessieren (Präsens)
```

**Student produces:**

```
Ich interessiere mich für einen interessanten Film.
```

### 4.4 Präposition

**Purpose:**

Train:

- preposition → case mapping
- declination under that case
- verb conjugation

**Mandatory rules:**

- preposition must be explicit
- case must be forced by preposition

**Example (valid):**

```
Ich ___ zu ein__ neu__ Haus.
Verb: kommen (Präsens)
```

### 4.5 Partizip II

**Purpose:**

Train simultaneously:

- declination
- auxiliary selection & conjugation
- Partizip II formation

**Mandatory rules (NON-NEGOTIABLE):**

The student must produce:

- auxiliary verb (haben or sein)
- Partizip II form
- all declinations

**Canonical structure:**

```
Ich ___ ein__ gut__ Film ___.
Verb: kaufen (Perfekt)
```

**Student produces:**

```
Ich habe einen guten Film gekauft.
```

**Another example (sein-verb):**

```
Wir ___ zu ein__ neu__ Haus ___.
Verb: gehen (Perfekt)
```

---

## 5. Structural Hints (Optional, Controlled)

Structural hints may include:

- Kasus
- Artikeltyp (bestimmt / unbestimmt / null)
- Rolle (Subjekt / Objekt)
- Präposition → case
- „trennbares Verb"
- „Perfekt"

Structural hints must **never**:

- give endings
- give full forms
- repeat visible text

Hints reset on every new exercise.

---

## 6. Translation

- Optional
- Natural English only
- Must not disambiguate article type or endings

---

## 7. Forbidden Exercises (Delete on Sight)

❌ **Predicate adjectives only**

```
Das Auto ist neu.
```

❌ No declination present  
❌ Verb already conjugated  
❌ Partizip II already written  
❌ Sentence creation from nothing  
❌ Vocabulary guessing  
❌ Multiple-choice grammar questions

---

## 8. Validation Rules (Mechanical)

An exercise is invalid if:

- article type is ambiguous
- article is not blanked correctly
- adjective declination is implied but hidden
- verb form is pre-filled
- reflexive pronoun is pre-filled (for reflexive verbs)
- Partizip II is pre-filled (for Perfekt exercises)

**Invalid exercises must be deleted, not fixed.**

---

## 9. Quantity Rule

**Quality > quantity.**

Small, correct corpus is expected

Reduction is success, not failure.

---

**END OF MANIFEST**
