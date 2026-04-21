"""Scaffold a new DSA problem file and matching pytest file.

Usage:
    python scripts/new_problem.py --pattern arrays --name three_sum
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new DSA problem scaffold.")
    parser.add_argument("--pattern", required=True, help="Pattern folder name, e.g. arrays")
    parser.add_argument("--name", required=True, help="Problem file name in snake_case, e.g. three_sum")
    return parser.parse_args()


def ensure_snake_case(value: str, field: str) -> None:
    if not value.replace("_", "").isalnum() or "-" in value or " " in value:
        raise ValueError(f"{field} must be snake_case-friendly: {value}")


def create_solution_file(pattern: str, name: str) -> Path:
    solution_path = ROOT / pattern / f"{name}.py"
    if solution_path.exists():
        raise FileExistsError(f"Solution file already exists: {solution_path}")

    solution_stub = f'''from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        """TODO: Replace with actual problem-specific signature and logic.

        Time Complexity: O(?)
        Space Complexity: O(?)
        """
        raise NotImplementedError("Implement solution")
'''

    solution_path.write_text(solution_stub, encoding="utf-8")
    return solution_path


def create_test_file(pattern: str, name: str) -> Path:
    test_dir = ROOT / "tests" / pattern
    test_dir.mkdir(parents=True, exist_ok=True)
    init_path = test_dir / "__init__.py"
    if not init_path.exists():
        init_path.write_text("", encoding="utf-8")

    test_path = test_dir / f"test_{name}.py"
    if test_path.exists():
        raise FileExistsError(f"Test file already exists: {test_path}")

    test_stub = f'''from {pattern}.{name} import Solution


def test_{name}() -> None:
    solver = Solution()

    # Replace with real assertions for your selected problem.
    # Example:
    # assert solver.solve([1, 2, 3]) == 6
    assert solver is not None
'''

    test_path.write_text(test_stub, encoding="utf-8")
    return test_path


def main() -> None:
    args = parse_args()
    pattern = args.pattern.strip()
    name = args.name.strip()

    ensure_snake_case(pattern, "pattern")
    ensure_snake_case(name, "name")

    pattern_dir = ROOT / pattern
    if not pattern_dir.exists() or not pattern_dir.is_dir():
        raise FileNotFoundError(f"Pattern directory not found: {pattern_dir}")

    solution_file = create_solution_file(pattern, name)
    test_file = create_test_file(pattern, name)

    print(f"Created: {solution_file}")
    print(f"Created: {test_file}")
    print("Run: python -m pytest")


if __name__ == "__main__":
    main()
