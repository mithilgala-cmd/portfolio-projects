# DSA Python

A placement-focused Data Structures and Algorithms workspace in Python.

This folder is designed to show interview readiness through:

- Pattern-based problem solving
- Clean, tested implementations
- Consistent folder structure
- Progress tracking and roadmap discipline
- Room for DSA-related mini projects

## Current Coverage

Implemented and tested solutions:

- `arrays/two_sum.py`

Scaffolded pattern folders are ready for expansion.

## Structure

```text
dsa-python/
|-- arrays/
|-- backtracking/
|-- binary_search/
|-- bit_manipulation/
|-- dynamic_programming/
|-- graphs/
|-- greedy/
|-- hashing/
|-- heap/
|-- intervals/
|-- linked_list/
|-- math_geometry/
|-- sliding_window/
|-- stack/
|-- trees/
|-- trie/
|-- two_pointers/
|-- projects/           # DSA-related mini projects
|-- scripts/            # utility scripts (scaffolders, helpers)
|-- tests/
|-- template.py
|-- ROADMAP.md
|-- PROGRESS.md
|-- pytest.ini
`-- requirements.txt
```

## Quick Start

```bash
cd dsa-python
pip install -r requirements.txt
python -m pytest
```

## Workflow for Every New Problem

1. Pick a pattern folder.
2. Add solution file (snake_case), for example `three_sum.py`.
3. Add tests under matching path, for example `tests/arrays/test_three_sum.py`.
4. Run `python -m pytest`.
5. Update `PROGRESS.md`.

## Placement Outcome Goal

Build a high-quality and reviewable DSA repository that demonstrates:

- Correctness under tests
- Complexity awareness
- Pattern recognition
- Consistent coding style
- Long-term interview preparation discipline
